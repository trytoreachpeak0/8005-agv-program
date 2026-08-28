namespace RIoT.Sdk.Core;

/// <summary>
/// Stable projection of the RIoT vehicle-card response.
/// </summary>
public sealed record VehicleCard(
    string DeviceKey,
    bool? Enable,
    int? Status,
    string? ProcState,
    string? CurrentMap,
    int? CurrentPosition,
    int? BatteryPercent,
    string? BatteryState,
    double? Speed,
    int? LockStatus,
    string? OrderTaskId);

/// <summary>
/// Stable projection of the diagnostic vehicle and vehicle-task response.
/// </summary>
public sealed record VehicleExecutionFacts(
    string DeviceKey,
    string? MovementState,
    string? ControlState,
    string? EmergencyState,
    string? BreakSwitchState,
    string? LocationState,
    double? Speed,
    string? ProcState,
    bool? ProcessingOrder,
    bool? Enable,
    string? IntegrationLevel);
