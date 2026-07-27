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
        return ToOrderRef(response.Result, "byDefaultMissions");
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
}
