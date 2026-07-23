namespace RIoT.Sdk.Core;

/// <summary>
/// A vehicle that can be appointed for dispatch (task simpleInfo), not a generic device.
/// </summary>
public sealed record DispatchableVehicle(string DeviceKey, string DeviceName);
