namespace RIoT.Sdk.Core;

/// <summary>
/// Identifiers for an order created via byDefaultMissions (BC-ORDER-001 / BC-ORDER-005).
/// Id = numeric PK; OrderId = string order-...; UpperId = caller correlation id.
/// </summary>
public sealed record OrderRef(int Id, string OrderId, string UpperId, int OrderState);
