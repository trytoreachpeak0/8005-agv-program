using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade discovery of DispatchableVehicle via getAllVehicleSimpleInfo (BC-VEH-002 / ADR-0006).
/// Body shape from Lab fixture B1-getAllVehicleSimpleInfo (trimmed to 3 known vehicles).
/// </summary>
public class DispatchableVehiclesFacadeTests
{
    // Known-good envelope + items from B1-getAllVehicleSimpleInfo / B1-name-to-deviceKey.
    private const string SimpleInfoBody =
        """
        {"code":"0","message":"成功","result":[
          {"deviceKey":"BROKERX-8ffb2294db594d7480125d379b39cfd6","deviceName":"新基测试300c顶升2"},
          {"deviceKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","deviceName":"新基测试300c协作1"},
          {"deviceKey":"BROKERX-757de62710d84cec9fe9907691672cbc","deviceName":"尊阳-多仓位1"}
        ]}
        """;

    [Fact]
    public async Task GetDispatchableVehicles_returns_domain_vehicles_from_simpleInfo()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, SimpleInfoBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var vehicles = await session.Tasks.GetDispatchableVehiclesAsync();

        Assert.Equal(3, vehicles.Count);
        Assert.Contains(
            vehicles,
            v => v.DeviceKey == "BROKERX-aee2f93d717546cf9510c98c854fe83e"
                 && v.DeviceName == "新基测试300c协作1");
    }

    [Fact]
    public async Task ResolveDeviceKey_exact_name_returns_unique_key()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, SimpleInfoBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var key = await session.Tasks.ResolveDeviceKeyAsync("新基测试300c协作1");

        Assert.Equal("BROKERX-aee2f93d717546cf9510c98c854fe83e", key);
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
