namespace RIoT.Sdk.Core;

/// <summary>
/// Path cost (mm) from a vehicle to a station on a Map (BC-ROUTE-001).
/// CostsMm = -1 means unreachable; that is a domain result, not a business failure (ADR-sdk-0005).
/// </summary>
public sealed record RouteCost(long CostsMm)
{
    public bool IsReachable => CostsMm >= 0;
}
