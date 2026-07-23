namespace RIoT.Sdk.Core;

/// <summary>
/// Exact deviceName → deviceKey resolution for dispatchable vehicles (BC-VEH-002).
/// </summary>
public static class DispatchableVehicleLookup
{
    public static string ResolveDeviceKey(
        IEnumerable<DispatchableVehicle> vehicles,
        string deviceName)
    {
        ArgumentNullException.ThrowIfNull(vehicles);
        ArgumentException.ThrowIfNullOrWhiteSpace(deviceName);

        var matches = vehicles.Where(v => string.Equals(v.DeviceName, deviceName, StringComparison.Ordinal)).ToList();
        if (matches.Count == 0)
        {
            throw new RiotApiException(
                $"No dispatchable vehicle with deviceName={deviceName}.",
                businessCode: "vehicle-name-not-found");
        }

        if (matches.Count > 1)
        {
            throw new RiotApiException(
                $"deviceName={deviceName} is not unique ({matches.Count} matches); refusing to pick arbitrarily.",
                businessCode: "vehicle-name-ambiguous");
        }

        return matches[0].DeviceKey;
    }
}
