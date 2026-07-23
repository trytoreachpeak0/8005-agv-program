using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade OrderHold via task command CMD_ORDER_HELD (BC-ORDER-006).
/// Known-good success body from Lab Round10 Q006-held-call / Round37 S3-probe.
/// </summary>
public class OrderHoldFacadeTests
{
    private const string OrderId = "order-2079797271662297088";

    // Known-good body from Q006-held-call.body / S3-probe-CMD_ORDER_HELD.call.body
    private const string HoldSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","tid":""}
        """;

    [Fact]
    public async Task OrderHold_succeeds_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, HoldSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        await session.Tasks.OrderHoldAsync(OrderId);
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
