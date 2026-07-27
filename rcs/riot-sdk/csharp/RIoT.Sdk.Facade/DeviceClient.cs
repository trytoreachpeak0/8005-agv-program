using RIoT.Sdk.Core;
using RIoT.Sdk.Generated.Device.Models;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin device-module facade. Method names stay stable for callers;
/// internals may change when swagger / Kiota output changes.
/// </summary>
public sealed class DeviceClient
{
    private readonly RiotSession _session;

    internal DeviceClient(RiotSession session) => _session = session;

    /// <summary>
    /// GET /api/device/v1/devices — list devices (not DispatchableVehicle discovery).
    /// Throws <see cref="RiotApiException"/> on business failure; returns unwrapped page (ADR-sdk-0005).
    /// </summary>
    public async Task<Page_Of_DeviceObject> ListDevicesAsync(
        int? pageNum = null,
        int? pageSize = null,
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedDeviceClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Device.V1.Devices.GetAsync(config =>
            {
                config.QueryParameters.PageNum = pageNum;
                config.QueryParameters.PageSize = pageSize;
            }, cancellationToken).ConfigureAwait(false),
            "ListDevices");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        return response.Result ?? new Page_Of_DeviceObject();
    }

    /// <summary>
    /// GET /api/device/v1/devices/statistics/status
    /// Throws <see cref="RiotApiException"/> on business failure; returns unwrapped DTO (ADR-sdk-0005).
    /// </summary>
    public async Task<DeviceStatusStatisticsDto> GetDeviceStatusStatisticsAsync(
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedDeviceClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Device.V1.Devices.Statistics.Status
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "GetDeviceStatusStatistics");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        return response.Result ?? new DeviceStatusStatisticsDto();
    }

    /// <summary>
    /// POST /api/device/v1/command/sync/service/{deviceKey}/triggerEmergency (BC-VEH-005).
    /// Software emergency stop. HTTP/business success does not prove vehicle state;
    /// confirm via getVehicleInfo.emergencyState (expect CAN_RECOVER).
    /// Body must include messageId + mqCallback + thingsProperties (empty {} is NPE).
    /// </summary>
    public Task TriggerEmergencyStopAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
        => PostEmergencyServiceAsync(deviceKey, "triggerEmergency", cancellationToken);

    /// <summary>
    /// POST /api/device/v1/command/sync/service/{deviceKey}/cancelEmergency (BC-VEH-005).
    /// Clear software emergency stop. HTTP/business success does not prove vehicle state;
    /// confirm via getVehicleInfo.emergencyState (expect OK).
    /// Body must include messageId + mqCallback + thingsProperties (empty {} is NPE).
    /// </summary>
    public Task CancelEmergencyStopAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
        => PostEmergencyServiceAsync(deviceKey, "cancelEmergency", cancellationToken);

    private async Task PostEmergencyServiceAsync(
        string deviceKey,
        string serviceId,
        CancellationToken cancellationToken)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedDeviceClient();
        var body = new DeviceCommandDto
        {
            MessageId = Random.Shared.Next(100000, 999999).ToString(),
            MqCallback = new MqCallback { Tag = "string", Topic = "string" },
            ThingsProperties = new DeviceCommandDto_thingsProperties(),
        };

        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Device.V1.Command.Sync.Service[deviceKey][serviceId]
                .PostAsync(body, cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            serviceId);

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
    }
}
