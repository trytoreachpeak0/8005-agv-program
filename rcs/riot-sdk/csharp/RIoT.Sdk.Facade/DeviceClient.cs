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
}
