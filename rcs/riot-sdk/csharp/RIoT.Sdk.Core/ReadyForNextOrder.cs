namespace RIoT.Sdk.Core;

/// <summary>
/// Pure ReadyForNextOrder check (BC-STATE-003 / ADR-0008).
/// Safe to dispatch next order only when previous order is SUCCESS and vehicle is IDLE.
/// Not ArrivalAtStation; AWAITING_ORDER alone is not sufficient.
/// </summary>
public static class ReadyForNextOrder
{
    /// <summary>RIoT orderState for SUCCESS.</summary>
    public const int SuccessOrderState = 5;

    /// <summary>RIoT vehicle procState for IDLE.</summary>
    public const string IdleProcState = "IDLE";

    public static bool IsReady(int orderState, string? procState, bool processingOrder = false)
        => orderState == SuccessOrderState
           && string.Equals(procState, IdleProcState, StringComparison.Ordinal)
           && !processingOrder;
}
