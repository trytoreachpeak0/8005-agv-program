using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade PriorityExec via orderRecordPriorityExec (BC-ORDER-014).
/// Known-good success body from Lab Round16 S2-priority-calls (orderId-string).
/// </summary>
public class PriorityExecFacadeTests
{
    private const string OrderId = "order-2079101767542505472";

    // Known-good body from S2-priority-calls.attempts[0].body
    private const string PrioritySuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","tid":""}
        """;

    [Fact]
    public async Task PriorityExec_succeeds_without_throwing()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, PrioritySuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        await session.Order.PriorityExecAsync(OrderId);
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
