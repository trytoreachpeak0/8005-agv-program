using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade Map enumeration (BC-MAP-001 / ADR-sdk-0005 / ADR-sdk-0006).
/// Expected values from Lab fixture C1-mapInfo-excludeMapJson.
/// </summary>
public class MapFacadeTests
{
    // Known-good envelope shaped like RIoT ResponseMsg; items from C1-mapInfo-excludeMapJson.
    private const string ExcludeMapJsonBody =
        """
        {"code":"0","message":"成功","result":[
          {"id":6,"name":"尊阳电镀线"},
          {"id":29,"name":"api测试"},
          {"id":26,"name":"新基测试1"}
        ]}
        """;

    [Fact]
    public async Task ListMaps_returns_domain_maps_from_excludeMapJson()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, ExcludeMapJsonBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var maps = await session.Maps.ListMapsAsync();

        Assert.Equal(3, maps.Count);
        Assert.Contains(maps, m => m.MapId == 29 && m.Name == "api测试");
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
