using System.Text.Json;
using RIoT.Sdk.Core;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin order-module facade. Expose additional endpoints as needed.
/// </summary>
public sealed class OrderClient
{
    private readonly RiotSession _session;

    internal OrderClient(RiotSession session) => _session = session;

    /// <summary>
    /// POST /api/order/v1/add/byDefaultMissions — single-segment move order (BC-ORDER-001).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-sdk-0005).
    /// </summary>
    public async Task<OrderRef> CreateMoveOrderAsync(
        string upperId,
        string appointVehicleKey,
        int mapId,
        int destinationStationId,
        string? orderName = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(upperId);
        ArgumentException.ThrowIfNullOrWhiteSpace(appointVehicleKey);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(mapId);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(destinationStationId);

        var client = _session.CreateGeneratedOrderClient();
        var body = new RIoT.Sdk.Generated.Order.Models.OrderRecordDTOObject
        {
            AppointVehicleKey = appointVehicleKey,
            IsAppointEnable = 1,
            LockStatus = 0,
            OrderName = string.IsNullOrWhiteSpace(orderName) ? upperId : orderName,
            UpperId = upperId,
            Mission =
            [
                new RIoT.Sdk.Generated.Order.Models.MissionDTO
                {
                    Type = "move",
                    MapId = mapId,
                    Destination = destinationStationId,
                },
            ],
        };

        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Order.V1.Add.ByDefaultMissions
                .PostAsync(body, cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "byDefaultMissions");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        OrderRef created = ToOrderRef(response.Result, "byDefaultMissions");
        if (!string.Equals(created.UpperId, upperId, StringComparison.Ordinal))
        {
            throw new RiotApiException(
                "byDefaultMissions returned a mismatched upperId.",
                businessCode: "order-upper-id-mismatch");
        }
        return created;
    }

    /// <summary>
    /// GET /api/order/v1/orderRecord/detailByUpperId/{upperId} (BC-ORDER-005).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-sdk-0005).
    /// </summary>
    public async Task<OrderRef> GetOrderByUpperIdAsync(
        string upperId,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(upperId);

        var client = _session.CreateGeneratedOrderClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Order.V1.OrderRecord.DetailByUpperId[upperId]
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "detailByUpperId");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        return ToOrderRef(response.Result, "detailByUpperId");
    }

    /// <summary>
    /// Observes an order by upperId without conflating a successful empty response with
    /// authoritative not-found. Only HTTP 404 produces <see cref="OrderLookupStatus.NotFound"/>.
    /// </summary>
    public async Task<OrderLookupResult> FindOrderByUpperIdAsync(
        string upperId,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(upperId);

        HttpResponseMessage response;
        try
        {
            response = await _session.SendRawAsync(
                HttpMethod.Get,
                $"/api/order/v1/orderRecord/detailByUpperId/{Uri.EscapeDataString(upperId)}",
                cancellationToken).ConfigureAwait(false);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            throw;
        }
        catch (OperationCanceledException error)
        {
            throw new RiotApiException(
                "detailByUpperId timed out.",
                businessCode: "riot-read-timeout",
                innerException: error);
        }
        catch (HttpRequestException error)
        {
            throw new RiotApiException(
                $"detailByUpperId transport failure: {error.Message}",
                businessCode: "riot-read-failed",
                innerException: error);
        }

        using (response)
        {
            string body = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
            if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                return OrderLookupResult.NotFound(upperId);
            }
            if (!response.IsSuccessStatusCode)
            {
                throw new RiotApiException(
                    $"detailByUpperId HTTP {(int)response.StatusCode}.",
                    statusCode: (int)response.StatusCode,
                    responseBody: body);
            }

            JsonDocument document;
            try
            {
                document = JsonDocument.Parse(body);
            }
            catch (JsonException error)
            {
                throw new RiotApiException(
                    "detailByUpperId returned invalid JSON.",
                    statusCode: (int)response.StatusCode,
                    businessCode: "riot-response-invalid",
                    responseBody: body,
                    innerException: error);
            }

            using (document)
            {
                JsonElement root = document.RootElement;
                if (root.ValueKind != JsonValueKind.Object)
                {
                    throw new RiotApiException(
                        "detailByUpperId returned a non-object response.",
                        statusCode: (int)response.StatusCode,
                        businessCode: "riot-response-invalid",
                        responseBody: body);
                }

                string? code = root.TryGetProperty("code", out JsonElement codeElement)
                    ? codeElement.ValueKind == JsonValueKind.String
                        ? codeElement.GetString()
                        : codeElement.GetRawText()
                    : null;
                string? message = root.TryGetProperty("message", out JsonElement messageElement) &&
                    messageElement.ValueKind == JsonValueKind.String
                    ? messageElement.GetString()
                    : null;
                if (!RiotBusinessResponse.IsSuccessCode(code))
                {
                    throw new RiotApiException(
                        $"RIoT business failure code={code} message={message}",
                        statusCode: (int)response.StatusCode,
                        businessCode: code,
                        responseBody: body);
                }

                if (!root.TryGetProperty("result", out JsonElement resultElement) ||
                    resultElement.ValueKind is JsonValueKind.Null or JsonValueKind.Undefined)
                {
                    return OrderLookupResult.AbsentAtObservation(upperId);
                }
                if (resultElement.ValueKind != JsonValueKind.Object)
                {
                    return OrderLookupResult.Indeterminate(upperId);
                }

                OrderSnapshot? snapshot = ToOrderSnapshot(resultElement);
                if (snapshot is null ||
                    !string.Equals(snapshot.UpperId, upperId, StringComparison.Ordinal))
                {
                    return OrderLookupResult.Indeterminate(upperId);
                }

                return OrderLookupResult.Found(upperId, snapshot);
            }
        }
    }

    /// <summary>
    /// GET /api/order/v1/orderRecord/detailByOrderId/{orderId} (BC-ORDER-005).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-sdk-0005).
    /// </summary>
    public async Task<OrderRef> GetOrderByOrderIdAsync(
        string orderId,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedOrderClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Order.V1.OrderRecord.DetailByOrderId[orderId]
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "detailByOrderId");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        return ToOrderRef(response.Result, "detailByOrderId");
    }

    /// <summary>
    /// GET /api/order/v1/orderRecord with explicit state filters and page metadata.
    /// Callers must inspect <see cref="OrderStatePage.CoversAllRecords"/> before treating
    /// the returned rows as complete coverage.
    /// </summary>
    public async Task<OrderStatePage> ListOrdersByStatesAsync(
        IReadOnlyCollection<int> orderStates,
        int pageNum = 1,
        int pageSize = 100,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(orderStates);
        if (orderStates.Count == 0)
        {
            throw new ArgumentException("orderStates must not be empty.", nameof(orderStates));
        }
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(pageNum);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(pageSize);

        string filters = string.Join("&", orderStates.Select(state =>
            $"filterByState={Uri.EscapeDataString(state.ToString(System.Globalization.CultureInfo.InvariantCulture))}"));
        string rawUrl = $"{_session.Options.BaseUrl.TrimEnd('/')}/api/order/v1/orderRecord" +
            $"?pageNum={pageNum}&pageSize={pageSize}&{filters}";
        var client = _session.CreateGeneratedOrderClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Order.V1.OrderRecord.WithUrl(rawUrl)
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "orderRecord");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        if (response.Result?.Records is null)
        {
            throw new RiotApiException(
                "orderRecord returned missing page or records.",
                businessCode: "order-state-page-missing");
        }

        OrderStateRecord[] records = response.Result.Records.Select(record =>
            new OrderStateRecord(
                record.Id,
                record.OrderId,
                record.UpperId,
                record.OrderState,
                record.AppointVehicleKey,
                record.ExecuteVehicleKey)).ToArray();

        return new OrderStatePage(
            response.Result.Current,
            response.Result.Size,
            response.Result.Total,
            records);
    }

    /// <summary>
    /// POST /api/order/v1/orderRecordPriorityExec?orderTaskKey={orderId} (BC-ORDER-014).
    /// Promotes a QUEUEING order ahead of other QUEUEING orders on the same vehicle.
    /// Pass the string orderId (not numeric id / upperId).
    /// </summary>
    public async Task PriorityExecAsync(
        string orderId,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedOrderClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Order.V1.OrderRecordPriorityExec
                .PostAsync(config =>
                {
                    config.QueryParameters.OrderTaskKey = orderId;
                }, cancellationToken)
                .ConfigureAwait(false),
            "orderRecordPriorityExec");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
    }

    /// <summary>
    /// Access the underlying Kiota client for endpoints not yet wrapped.
    /// </summary>
    public RIoT.Sdk.Generated.Order.OrderClient Raw => _session.CreateGeneratedOrderClient();

    private static OrderRef ToOrderRef(
        RIoT.Sdk.Generated.Order.Models.OrderRecordObject? result,
        string source)
    {
        if (result?.Id is null
            || string.IsNullOrWhiteSpace(result.OrderId)
            || string.IsNullOrWhiteSpace(result.UpperId)
            || result.OrderState is null)
        {
            throw new RiotApiException(
                $"{source} returned incomplete order identifiers.",
                businessCode: "order-ref-missing");
        }

        return new OrderRef(
            result.Id.Value,
            result.OrderId,
            result.UpperId,
            result.OrderState.Value);
    }

    private static OrderSnapshot? ToOrderSnapshot(JsonElement result)
    {
        if (!result.TryGetProperty("id", out JsonElement idElement) ||
            !idElement.TryGetInt64(out long id) ||
            !TryGetRequiredString(result, "orderId", out string? orderId) ||
            !TryGetRequiredString(result, "upperId", out string? upperId) ||
            !result.TryGetProperty("orderState", out JsonElement stateElement) ||
            !stateElement.TryGetInt32(out int orderState))
        {
            return null;
        }

        List<OrderMissionSnapshot> missions = [];
        if (result.TryGetProperty("missions", out JsonElement missionsElement) &&
            missionsElement.ValueKind == JsonValueKind.Array)
        {
            foreach (JsonElement mission in missionsElement.EnumerateArray())
            {
                if (mission.ValueKind != JsonValueKind.Object)
                {
                    continue;
                }
                missions.Add(new OrderMissionSnapshot(
                    GetOptionalString(mission, "type"),
                    GetOptionalInt32(mission, "mapId"),
                    GetOptionalInt32(mission, "destination")));
            }
        }

        return new OrderSnapshot(
            id,
            orderId!,
            upperId!,
            orderState,
            GetOptionalString(result, "appointVehicleKey"),
            GetOptionalString(result, "executeVehicleKey"),
            GetOptionalInt32(result, "endStationNo"),
            missions);
    }

    private static bool TryGetRequiredString(
        JsonElement element,
        string propertyName,
        out string? value)
    {
        value = GetOptionalString(element, propertyName);
        return !string.IsNullOrWhiteSpace(value);
    }

    private static string? GetOptionalString(JsonElement element, string propertyName) =>
        element.TryGetProperty(propertyName, out JsonElement value) &&
        value.ValueKind == JsonValueKind.String
            ? value.GetString()
            : null;

    private static int? GetOptionalInt32(JsonElement element, string propertyName) =>
        element.TryGetProperty(propertyName, out JsonElement value) &&
        value.ValueKind == JsonValueKind.Number &&
        value.TryGetInt32(out int result)
            ? result
            : null;
}
