using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade Station enumeration by mapId (BC-MAP-002 / ADR-sdk-0005).
/// Expected values from Lab fixture C2-stations-map-29.
/// </summary>
public class StationFacadeTests
{
    // Known-good envelope; items from C2-stations-map-29 (mapId=29, 站点1/站点2).
    private const string StationsMap29Body =
        """
        {"code":"0","message":"成功","result":[
          {"id":1,"name":"站点1"},
          {"id":2,"name":"站点2"}
        ]}
        """;

    [Fact]
    public async Task ListStations_for_map_29_returns_domain_stations()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, StationsMap29Body))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var stations = await session.Maps.ListStationsAsync(mapId: 29);

        Assert.Equal(2, stations.Count);
        Assert.Contains(stations, s => s.MapId == 29 && s.StationId == 1 && s.Name == "站点1");
        Assert.Contains(stations, s => s.MapId == 29 && s.StationId == 2 && s.Name == "站点2");
    }

    [Fact]
    public async Task ListStationsStrict_returns_all_valid_rows()
    {
        using var http = CreateHttp(StationsMap29Body);
        await using var session = CreateSession(http);

        IReadOnlyList<Station> stations = await session.Maps.ListStationsStrictAsync(29);

        Assert.Equal([1, 2], stations.Select(station => station.StationId));
    }

    [Fact]
    public async Task ListStationsStrict_rejects_malformed_row_instead_of_filtering()
    {
        using var http = CreateHttp(
            """{"code":"0","result":[{"id":1,"name":"站点1"},{"id":0,"name":""}]}""");
        await using var session = CreateSession(http);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Maps.ListStationsStrictAsync(29));

        Assert.Equal("station-catalog-entry-invalid", error.BusinessCode);
    }

    [Fact]
    public async Task ListStationsStrict_rejects_duplicate_station_id()
    {
        using var http = CreateHttp(
            """{"code":"0","result":[{"id":1,"name":"站点1"},{"id":1,"name":"重复站点"}]}""");
        await using var session = CreateSession(http);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Maps.ListStationsStrictAsync(29));

        Assert.Equal("station-catalog-duplicate", error.BusinessCode);
    }

    [Theory]
    [InlineData("{\"code\":\"0\",\"result\":null}", "station-catalog-missing")]
    [InlineData("{\"code\":\"0\",\"result\":[]}", "station-catalog-empty")]
    public async Task ListStationsStrict_rejects_null_or_empty_catalog(
        string body,
        string expectedBusinessCode)
    {
        using var http = CreateHttp(body);
        await using var session = CreateSession(http);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Maps.ListStationsStrictAsync(29));

        Assert.Equal(expectedBusinessCode, error.BusinessCode);
    }

    private static HttpClient CreateHttp(string body) => new(
        new FixedJsonHandler(HttpStatusCode.OK, body))
    {
        BaseAddress = new Uri("http://riot.test/"),
    };

    private static RiotSession CreateSession(HttpClient http) => new(
        new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        },
        http);

    private sealed class FixedJsonHandler : HttpMessageHandler
    {
        private readonly HttpStatusCode _status;
        private readonly string _body;

        public FixedJsonHandler(HttpStatusCode status, string body)
        {
            _status = status;
            _body = body;
        }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            var response = new HttpResponseMessage(_status)
            {
                Content = new StringContent(_body, Encoding.UTF8, "application/json"),
            };
            return Task.FromResult(response);
        }
    }
}
