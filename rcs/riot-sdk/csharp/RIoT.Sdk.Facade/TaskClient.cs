using RIoT.Sdk.Core;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin task-module facade. Expose additional endpoints as needed.
/// </summary>
public sealed class TaskClient
{
    private readonly RiotSession _session;

    internal TaskClient(RiotSession session) => _session = session;

    /// <summary>
    /// GET /api/task/vehicles/getAllVehicleSimpleInfo — list DispatchableVehicle rows (BC-VEH-002).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-0006).
    /// </summary>
    public async Task<IReadOnlyList<DispatchableVehicle>> GetDispatchableVehiclesAsync(
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedTaskClient();
        var response = await client.Api.Task.Vehicles.GetAllVehicleSimpleInfo
            .GetAsync(cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("getAllVehicleSimpleInfo returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        var result = response.Result ?? [];
        return result
            .Where(v => !string.IsNullOrWhiteSpace(v.DeviceKey) && !string.IsNullOrWhiteSpace(v.DeviceName))
            .Select(v => new DispatchableVehicle(v.DeviceKey!, v.DeviceName!))
            .ToList();
    }

    /// <summary>
    /// Exact deviceName → deviceKey via getAllVehicleSimpleInfo (BC-VEH-002).
    /// </summary>
    public async Task<string> ResolveDeviceKeyAsync(
        string deviceName,
        CancellationToken cancellationToken = default)
    {
        var vehicles = await GetDispatchableVehiclesAsync(cancellationToken).ConfigureAwait(false);
        return DispatchableVehicleLookup.ResolveDeviceKey(vehicles, deviceName);
    }

    /// <summary>
    /// POST /api/task/v1/route/getRouteCostsBy — RouteCost for one vehicle to a station (BC-ROUTE-001).
    /// <c>CostsMm = -1</c> means unreachable and is returned, not thrown (ADR-0006).
    /// </summary>
    public async Task<RouteCost> GetRouteCostAsync(
        int mapId,
        int stationId,
        string deviceKey,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.U7533u8bf7u8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7
        {
            MapId = mapId,
            StationId = stationId,
            DeviceKeys = [deviceKey],
        };

        var response = await client.Api.Task.V1.Route.GetRouteCostsBy
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("getRouteCostsBy returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        var entry = response.Result?.DeviceCostsList?
            .FirstOrDefault(c => string.Equals(c.DeviceKey, deviceKey, StringComparison.Ordinal));

        if (entry?.Costs is null)
        {
            throw new RiotApiException(
                $"getRouteCostsBy returned no costs for deviceKey={deviceKey}.",
                businessCode: "route-cost-missing");
        }

        return new RouteCost(entry.Costs.Value);
    }

    /// <summary>
    /// POST /api/task/v1/route/queryNearEnd — nearest end Station among candidates (NearStationQuery).
    /// Returns stationId only (not path geometry). Throws on business failure (ADR-0006).
    /// </summary>
    public async Task<int> QueryNearestEndAsync(
        int mapId,
        int startStationId,
        IReadOnlyList<int> endStationIds,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(endStationIds);
        if (endStationIds.Count == 0)
        {
            throw new ArgumentException("endStationIds must not be empty.", nameof(endStationIds));
        }

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.U627eu6700u8fd1u7684u7ec8u70b9u53c2u6570Object
        {
            MapId = mapId,
            StartStationId = startStationId,
            EndStationIds = endStationIds.Select(id => (int?)id).ToList(),
        };

        var response = await client.Api.Task.V1.Route.QueryNearEnd
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("queryNearEnd returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        if (response.Result is null)
        {
            throw new RiotApiException(
                "queryNearEnd returned null result.",
                businessCode: "near-end-missing");
        }

        return response.Result.Value;
    }

    /// <summary>
    /// POST /api/task/v1/route/queryNearestStart — nearest start Station among candidates (NearStationQuery).
    /// Returns stationId only (not path geometry). Throws on business failure (ADR-0006).
    /// </summary>
    public async Task<int> QueryNearestStartAsync(
        int mapId,
        int endStationId,
        IReadOnlyList<int> startStationIds,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(startStationIds);
        if (startStationIds.Count == 0)
        {
            throw new ArgumentException("startStationIds must not be empty.", nameof(startStationIds));
        }

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object
        {
            MapId = mapId,
            EndStationId = endStationId,
            StartStationIds = startStationIds.Select(id => (int?)id).ToList(),
        };

        var response = await client.Api.Task.V1.Route.QueryNearestStart
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("queryNearestStart returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        if (response.Result is null)
        {
            throw new RiotApiException(
                "queryNearestStart returned null result.",
                businessCode: "near-start-missing");
        }

        return response.Result.Value;
    }

    /// <summary>
    /// POST /api/task/v1/order/command/{orderId} with CMD_ORDER_CANCEL (BC-ORDER-003).
    /// Uses string orderId; does not disable the vehicle. Throws on business failure (ADR-0006).
    /// </summary>
    public async Task CancelOrderAsync(
        string orderId,
        string? reason = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject
        {
            CommandType = RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject_commandType.CMD_ORDER_CANCEL,
            DisableVehicle = false,
            Reason = reason,
        };

        var response = await client.Api.Task.V1.Order.Command[orderId]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("CMD_ORDER_CANCEL returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// POST /api/task/v1/order/command/{orderId} with CMD_ORDER_HELD (BC-ORDER-006).
    /// Pauses an executing move order (orderState → HELD). Pair with OrderContinue.
    /// </summary>
    public async Task OrderHoldAsync(
        string orderId,
        string? reason = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject
        {
            CommandType = RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject_commandType.CMD_ORDER_HELD,
            DisableVehicle = false,
            Reason = reason,
        };

        var response = await client.Api.Task.V1.Order.Command[orderId]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("CMD_ORDER_HELD returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// POST /api/task/v1/order/command/{orderId} with CMD_ORDER_CONTINUE_FROM_HELD (BC-ORDER-006).
    /// Resumes a HELD move order. Do not use for OrderHang (use HangContinue).
    /// </summary>
    public async Task OrderContinueAsync(
        string orderId,
        string? reason = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject
        {
            CommandType = RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject_commandType.CMD_ORDER_CONTINUE_FROM_HELD,
            DisableVehicle = false,
            Reason = reason,
        };

        var response = await client.Api.Task.V1.Order.Command[orderId]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("CMD_ORDER_CONTINUE_FROM_HELD returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// POST /api/task/v1/order/command/{orderId} with CMD_ORDER_CONTINUE_FROM_HANG (BC-ORDER-015).
    /// Attempts to pull an OrderHang back to EXECUTING. Do not use for HELD (use OrderContinue).
    /// HTTP/business success does not prove the order left HANG — confirm via orderState.
    /// </summary>
    public async Task HangContinueAsync(
        string orderId,
        string? reason = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(orderId);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject
        {
            CommandType = RIoT.Sdk.Generated.TaskApi.Models.OrderCommandDTOObject_commandType.CMD_ORDER_CONTINUE_FROM_HANG,
            DisableVehicle = false,
            Reason = reason,
        };

        var response = await client.Api.Task.V1.Order.Command[orderId]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("CMD_ORDER_CONTINUE_FROM_HANG returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// POST /api/task/vehicles/updateVehicleIntegrationLevel with serviceId=enable (BC-VEH-003).
    /// Brings the vehicle into dispatch (ON_LINE). Never pass ON_LINE as serviceId.
    /// </summary>
    public async Task DispatchEnableAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.BatchVehicleOperation
        {
            DeviceKeys = [deviceKey],
            ServiceId = "enable",
        };

        var response = await client.Api.Task.Vehicles.UpdateVehicleIntegrationLevel
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("DispatchEnable returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// POST /api/task/vehicles/updateVehicleIntegrationLevel with serviceId=disable (BC-VEH-003).
    /// Removes the vehicle from dispatch (OFF_LINE). Does not cancel an executing order.
    /// </summary>
    public async Task DispatchDisableAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedTaskClient();
        var body = new RIoT.Sdk.Generated.TaskApi.Models.BatchVehicleOperation
        {
            DeviceKeys = [deviceKey],
            ServiceId = "disable",
        };

        var response = await client.Api.Task.Vehicles.UpdateVehicleIntegrationLevel
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("DispatchDisable returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    /// <summary>
    /// Access the underlying Kiota client for endpoints not yet wrapped.
    /// Prefer adding explicit facade methods for commonly used calls.
    /// </summary>
    public RIoT.Sdk.Generated.TaskApi.TaskClient Raw => _session.CreateGeneratedTaskClient();

    private static bool IsSuccessCode(string? code)
        => string.IsNullOrWhiteSpace(code)
           || code is "0" or "200" or "OK" or "ok" or "success" or "SUCCESS";
}
