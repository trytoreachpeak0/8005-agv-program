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
    /// GET /api/device/v1/devices — list devices.
    /// </summary>
    public async Task<ResponseMsg_Of_Page_Of_DeviceObject?> ListDevicesAsync(
        int? pageNum = null,
        int? pageSize = null,
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedDeviceClient();
        return await client.Api.Device.V1.Devices.GetAsync(config =>
        {
            config.QueryParameters.PageNum = pageNum;
            config.QueryParameters.PageSize = pageSize;
        }, cancellationToken).ConfigureAwait(false);
    }

    /// <summary>
    /// GET /api/device/v1/devices/statistics/status
    /// </summary>
    public Task<ResponseMsg_Of_DeviceStatusStatisticsDto?> GetDeviceStatusStatisticsAsync(
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedDeviceClient();
        return client.Api.Device.V1.Devices.Statistics.Status.GetAsync(cancellationToken: cancellationToken);
    }

    /// <summary>
    /// POST /api/device/v1/command/sync/service/{deviceKey}/triggerEmergency (BC-VEH-005).
    /// Software emergency stop. HTTP/business success does not prove vehicle state;
    /// confirm via getVehicleInfo.emergencyState (expect CAN_RECOVER).
    /// Body must include messageId + mqCallback + thingsProperties (empty {} is NPE).
    /// </summary>
    public async Task TriggerEmergencyStopAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedDeviceClient();
        var body = new DeviceCommandDto
        {
            MessageId = Random.Shared.Next(100000, 999999).ToString(),
            MqCallback = new MqCallback { Tag = "string", Topic = "string" },
            ThingsProperties = new DeviceCommandDto_thingsProperties(),
        };

        var response = await client.Api.Device.V1.Command.Sync.Service[deviceKey]["triggerEmergency"]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("TriggerEmergencyStop returned empty response.");
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
    /// POST /api/device/v1/command/sync/service/{deviceKey}/cancelEmergency (BC-VEH-005).
    /// Clear software emergency stop. HTTP/business success does not prove vehicle state;
    /// confirm via getVehicleInfo.emergencyState (expect OK).
    /// Body must include messageId + mqCallback + thingsProperties (empty {} is NPE).
    /// </summary>
    public async Task CancelEmergencyStopAsync(
        string deviceKey,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceKey);

        var client = _session.CreateGeneratedDeviceClient();
        var body = new DeviceCommandDto
        {
            MessageId = Random.Shared.Next(100000, 999999).ToString(),
            MqCallback = new MqCallback { Tag = "string", Topic = "string" },
            ThingsProperties = new DeviceCommandDto_thingsProperties(),
        };

        var response = await client.Api.Device.V1.Command.Sync.Service[deviceKey]["cancelEmergency"]
            .PostAsync(body, cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("CancelEmergencyStop returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }
    }

    private static bool IsSuccessCode(string? code) =>
        string.IsNullOrEmpty(code) || code == "0";
}
