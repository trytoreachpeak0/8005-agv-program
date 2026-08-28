namespace RIoT.Sdk.Core;

/// <summary>
/// A station on a Map; always paired with MapId (BC-MAP-002). StationId = RIoT station.id.
/// </summary>
public sealed record Station(int MapId, int StationId, string Name);
