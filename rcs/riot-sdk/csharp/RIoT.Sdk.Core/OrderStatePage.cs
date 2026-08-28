namespace RIoT.Sdk.Core;

/// <summary>
/// Stable order identity and assignment facts from the order-state page.
/// </summary>
public sealed record OrderStateRecord(
    long? Id,
    string? OrderId,
    string? UpperId,
    int? OrderState,
    string? AppointVehicleKey,
    string? ExecuteVehicleKey);

/// <summary>
/// Paged order facts with enough metadata for a caller to prove complete coverage.
/// </summary>
public sealed record OrderStatePage(
    long? Current,
    long? Size,
    long? Total,
    IReadOnlyList<OrderStateRecord> Records)
{
    public bool CoversAllRecords =>
        Current == 1 &&
        Total.HasValue &&
        Total.Value >= 0 &&
        Total.Value == Records.Count &&
        (!Size.HasValue || Total.Value <= Size.Value);
}
