using RIoT.Sdk.Core;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin imap Map facade (BC-MAP-001 / ADR-0007).
/// </summary>
public sealed class MapClient
{
    private readonly RiotSession _session;

    internal MapClient(RiotSession session) => _session = session;

    /// <summary>
    /// GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson — list Maps without mapJson (BC-MAP-001).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-0006).
    /// </summary>
    public async Task<IReadOnlyList<Map>> ListMapsAsync(CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedImapClient();
        var response = await client.Api.Imap.V1.MapInfo.GetALLMapInfoExcludeMapJson
            .GetAsync(cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException("getALLMapInfoExcludeMapJson returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        var result = response.Result ?? [];
        return result
            .Where(m => m.Id is not null && !string.IsNullOrWhiteSpace(m.Name))
            .Select(m => new Map(m.Id!.Value, m.Name!))
            .ToList();
    }

    /// <summary>
    /// GET /api/imap/v1/mapInfo/stations/{mapId} — list Stations on a Map (BC-MAP-002).
    /// Throws <see cref="RiotApiException"/> on business failure (ADR-0006).
    /// Empty list on success is a valid domain result (e.g. invalid mapId=0).
    /// </summary>
    public async Task<IReadOnlyList<Station>> ListStationsAsync(
        int mapId,
        CancellationToken cancellationToken = default)
    {
        var client = _session.CreateGeneratedImapClient();
        var response = await client.Api.Imap.V1.MapInfo.Stations[mapId]
            .GetAsync(cancellationToken: cancellationToken)
            .ConfigureAwait(false);

        if (response is null)
        {
            throw new RiotApiException($"stations/{mapId} returned empty response.");
        }

        if (!IsSuccessCode(response.Code))
        {
            throw new RiotApiException(
                $"RIoT business failure code={response.Code} message={response.Message}",
                statusCode: 200,
                businessCode: response.Code);
        }

        var result = response.Result ?? [];
        return result
            .Where(s => s.Id is not null && !string.IsNullOrWhiteSpace(s.Name))
            .Select(s => new Station(mapId, s.Id!.Value, s.Name!))
            .ToList();
    }

    /// <summary>Underlying Kiota imap client for endpoints not yet wrapped.</summary>
    public RIoT.Sdk.Generated.Imap.ImapClient Raw => _session.CreateGeneratedImapClient();

    private static bool IsSuccessCode(string? code)
        => string.IsNullOrWhiteSpace(code)
           || code is "0" or "200" or "OK" or "ok" or "success" or "SUCCESS";
}
