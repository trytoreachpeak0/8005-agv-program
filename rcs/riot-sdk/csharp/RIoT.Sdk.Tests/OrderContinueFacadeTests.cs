using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade OrderContinue via task command CMD_ORDER_CONTINUE_FROM_HELD (BC-ORDER-006).
/// Known-good success body from Lab Round10 Q006-continue-call / Round36 P1-cont-call.
/// </summary>
public class OrderContinueFacadeTests
{
    private const string OrderId = "order-2079069601190248448";

    // Known-good body from Q006-continue-call.body
    private const string ContinueSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","tid":""}
        """;

    [Fact]
    public async Task OrderContinue_succeeds_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, ContinueSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        await session.Tasks.OrderContinueAsync(OrderId);
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
