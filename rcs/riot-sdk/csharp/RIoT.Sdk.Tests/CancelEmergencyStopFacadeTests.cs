using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade CancelEmergencyStop via device sync cancelEmergency (BC-VEH-005).
/// Known-good success shape from Lab Round19 S4-cancel-call (callApiKey).
/// </summary>
public class CancelEmergencyStopFacadeTests
{
    private const string DeviceKey = "BROKERX-aee2f93d717546cf9510c98c854fe83e";

    // Known-good outer envelope from S4-cancel-call.preview (business code=0)
    private const string CancelSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":{"client":{"deviceKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","productKey":"standard.oasis.300ul","productType":1,"thingModelVersion":"1"},"code":200,"data":{"reason":"RESPONSE_PROCESSING","code":"RESULT_CODE_NONE","responseState":"RESPONSE_OK","state":"1","responseCode":"0"},"fType":"SERVICE_CALL_REPLY","id":"461003","timestamp":1784534968901},"tid":""}
        """;

    [Fact]
    public async Task CancelEmergencyStop_succeeds_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, CancelSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        await session.Device.CancelEmergencyStopAsync(DeviceKey);
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
