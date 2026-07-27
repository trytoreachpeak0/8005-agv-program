using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade NearStationQuery via queryNearEnd / queryNearestStart (ADR-sdk-0003).
/// Expected stationIds from Lab fixture R15-near-tight-map28.
/// </summary>
public class NearStationQueryFacadeTests
{
    // Known-good body shape matching ResponseMsg_Of_int; result from R15-near-tight-map28 nearEnd-1to234
    private const string NearEndBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":2,"tid":""}
        """;

    // result from R15-near-tight-map28 nearStart-4from123
    private const string NearStartBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":3,"tid":""}
        """;

    [Fact]
    public async Task QueryNearestEnd_returns_closest_end_station_id()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, NearEndBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var stationId = await session.Tasks.QueryNearestEndAsync(
            mapId: 28,
            startStationId: 1,
            endStationIds: [2, 3, 4]);

        Assert.Equal(2, stationId);
    }

    [Fact]
    public async Task QueryNearestStart_returns_closest_start_station_id()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, NearStartBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var stationId = await session.Tasks.QueryNearestStartAsync(
            mapId: 28,
            endStationId: 4,
            startStationIds: [1, 2, 3]);

        Assert.Equal(3, stationId);
    }

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
