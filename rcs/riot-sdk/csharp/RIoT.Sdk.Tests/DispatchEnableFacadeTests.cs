using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade DispatchEnable via updateVehicleIntegrationLevel (BC-VEH-003).
/// Known-good success body from Lab fixture R12-enable-restore.
/// </summary>
public class DispatchEnableFacadeTests
{
    private const string DeviceKey = "BROKERX-aee2f93d717546cf9510c98c854fe83e";

    // Known-good body from R12-enable-restore.call.body
    private const string EnableSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","tid":""}
        """;

    [Fact]
    public async Task DispatchEnable_succeeds_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, EnableSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        await session.Tasks.DispatchEnableAsync(DeviceKey);
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
