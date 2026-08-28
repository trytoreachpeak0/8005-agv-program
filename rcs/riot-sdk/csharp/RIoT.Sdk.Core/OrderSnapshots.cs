namespace RIoT.Sdk.Core;

/// <summary>
/// Semantic result of observing one order by its caller-owned upperId.
/// </summary>
public enum OrderLookupStatus
{
    Found,
    NotFound,
    AbsentAtObservation,
    Indeterminate,
}

/// <summary>
/// Stable mission facts projected from a RIoT order response.
/// </summary>
public sealed record OrderMissionSnapshot(
    string? Type,
    int? MapId,
    int? Destination);

/// <summary>
/// Stable order facts exposed without leaking Kiota-generated types.
/// </summary>
public sealed record OrderSnapshot(
    long Id,
    string OrderId,
    string UpperId,
    int OrderState,
    string? AppointVehicleKey,
    string? ExecuteVehicleKey,
    int? EndStationNo,
    IReadOnlyList<OrderMissionSnapshot> Missions);

/// <summary>
/// Lookup result that keeps an observed absence distinct from authoritative not-found.
/// </summary>
public sealed record OrderLookupResult
{
    private OrderLookupResult(
        string requestedUpperId,
        OrderLookupStatus status,
        OrderSnapshot? order)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(requestedUpperId);
        RequestedUpperId = requestedUpperId;
        Status = status;
        Order = order;
    }

    public string RequestedUpperId { get; }
    public OrderLookupStatus Status { get; }
    public OrderSnapshot? Order { get; }

    public static OrderLookupResult Found(string requestedUpperId, OrderSnapshot order)
    {
        ArgumentNullException.ThrowIfNull(order);
        if (!string.Equals(requestedUpperId, order.UpperId, StringComparison.Ordinal))
        {
            throw new ArgumentException(
                "Found order upperId must match requestedUpperId.",
                nameof(order));
        }
        return new(requestedUpperId, OrderLookupStatus.Found, order);
    }

    public static OrderLookupResult NotFound(string requestedUpperId) =>
        new(requestedUpperId, OrderLookupStatus.NotFound, null);

    public static OrderLookupResult AbsentAtObservation(string requestedUpperId) =>
        new(requestedUpperId, OrderLookupStatus.AbsentAtObservation, null);

    public static OrderLookupResult Indeterminate(string requestedUpperId) =>
        new(requestedUpperId, OrderLookupStatus.Indeterminate, null);
}
