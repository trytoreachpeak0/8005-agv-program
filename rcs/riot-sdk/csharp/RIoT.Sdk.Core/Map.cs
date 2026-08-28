namespace RIoT.Sdk.Core;

/// <summary>
/// A dispatchable map identified by mapId (= RIoT mapInfo.id) and display name (BC-MAP-001).
/// </summary>
public sealed record Map(int MapId, string Name);
