using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade RouteCost via getRouteCostsBy (BC-ROUTE-001 / ADR-sdk-0005).
/// Expected costs from Lab fixture R15-map29-costs (map 29 / station 1).
/// </summary>
public class RouteCostFacadeTests
{
    private const string DeviceKey = "BROKERX-aee2f93d717546cf9510c98c854fe83e";

    // Known-good body from R15-map29-costs[0].body
    private const string ReachableBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":{"deviceCostsList":[{"costs":2210,"deviceKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","message":"ok"}],"mapId":29,"stationId":1},"tid":""}
        """;

    // Known-good body from Round15 R2 getRouteCostsBy (map28 / station 1, cross-map unreachable)
    private const string UnreachableBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":{"deviceCostsList":[{"costs":-1,"deviceKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","message":"vehicle route to station unreachable"}],"mapId":28,"stationId":1},"tid":""}
        """;

    [Fact]
    public async Task GetRouteCost_reachable_returns_non_negative_costs_mm()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, ReachableBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var cost = await session.Tasks.GetRouteCostAsync(
            mapId: 29,
            stationId: 1,
            deviceKey: DeviceKey);

        Assert.Equal(2210, cost.CostsMm);
        Assert.True(cost.IsReachable);
    }

    [Fact]
    public async Task GetRouteCost_unreachable_returns_minus_one_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, UnreachableBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var cost = await session.Tasks.GetRouteCostAsync(
            mapId: 28,
            stationId: 1,
            deviceKey: DeviceKey);

        Assert.Equal(-1, cost.CostsMm);
        Assert.False(cost.IsReachable);
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
