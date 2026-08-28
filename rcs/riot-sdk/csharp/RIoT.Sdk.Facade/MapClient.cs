using RIoT.Sdk.Core;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin imap Map facade (BC-MAP-001 / ADR-sdk-0006).
/// </summary>
public sealed class MapClient
{
    private readonly RiotSession _session;

    internal MapClient(RiotSession session) => _session = session;

    /// <summary>
    /// GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson — list Maps without mapJson (BC-MAP-001).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-sdk-0005).
    /// </summary>
    public async Task<IReadOnlyList<Map>> ListMapsAsync(CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedImapClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Imap.V1.MapInfo.GetALLMapInfoExcludeMapJson
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            "getALLMapInfoExcludeMapJson");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);

        var result = response.Result ?? [];
        return result
            .Where(m => m.Id is not null && !string.IsNullOrWhiteSpace(m.Name))
            .Select(m => new Map(m.Id!.Value, m.Name!))
            .ToList();
    }

    /// <summary>
    /// GET /api/imap/v1/mapInfo/stations/{mapId} — list Stations on a Map (BC-MAP-002).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-sdk-0005).
    /// Empty list on success is a valid domain result (e.g. invalid mapId=0).
    /// </summary>
    public async Task<IReadOnlyList<Station>> ListStationsAsync(
        int mapId,
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedImapClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Imap.V1.MapInfo.Stations[mapId]
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            $"stations/{mapId}");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);

        var result = response.Result ?? [];
        return result
            .Where(s => s.Id is not null && !string.IsNullOrWhiteSpace(s.Name))
            .Select(s => new Station(mapId, s.Id!.Value, s.Name!))
            .ToList();
    }

    /// <summary>
    /// Strict station-catalog read for safety-sensitive consumers. Unlike
    /// <see cref="ListStationsAsync"/>, malformed and duplicate rows are rejected rather
    /// than silently filtered.
    /// </summary>
    public async Task<IReadOnlyList<Station>> ListStationsStrictAsync(
        int mapId,
        CancellationToken cancellationToken = default)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(mapId);

        var client = _session.CreateGeneratedImapClient();
        var response = RiotBusinessResponse.RequireResponse(
            await client.Api.Imap.V1.MapInfo.Stations[mapId]
                .GetAsync(cancellationToken: cancellationToken)
                .ConfigureAwait(false),
            $"stations/{mapId}");

        RiotBusinessResponse.EnsureSuccess(response.Code, response.Message);
        if (response.Result is null)
        {
            throw new RiotApiException(
                $"stations/{mapId} returned null result.",
                businessCode: "station-catalog-missing");
        }
        if (response.Result.Count == 0)
        {
            throw new RiotApiException(
                $"stations/{mapId} returned an empty station catalog.",
                businessCode: "station-catalog-empty");
        }

        List<Station> stations = new(response.Result.Count);
        HashSet<int> stationIds = [];
        foreach (var row in response.Result)
        {
            if (row.Id is null or <= 0 || string.IsNullOrWhiteSpace(row.Name))
            {
                throw new RiotApiException(
                    $"stations/{mapId} returned a malformed station row.",
                    businessCode: "station-catalog-entry-invalid");
            }
            if (!stationIds.Add(row.Id.Value))
            {
                throw new RiotApiException(
                    $"stations/{mapId} returned duplicate station id {row.Id.Value}.",
                    businessCode: "station-catalog-duplicate");
            }

            stations.Add(new Station(mapId, row.Id.Value, row.Name));
        }

        return stations;
    }

    /// <summary>Underlying Kiota imap client for endpoints not yet wrapped.</summary>
    public RIoT.Sdk.Generated.Imap.ImapClient Raw => _session.CreateGeneratedImapClient();
}
