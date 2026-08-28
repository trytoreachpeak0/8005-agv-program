using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

public sealed class OrderStatePageFacadeTests
{
    [Fact]
    public async Task ListOrdersByStates_returns_records_and_complete_page_metadata()
    {
        RecordingHandler handler = new(_ => JsonResponse("""
            {"code":"0","result":{"current":1,"size":100,"total":2,"records":[
              {"id":1,"orderId":"ORDER-1","upperId":"UPPER-1","orderState":1,
               "appointVehicleKey":"VEHICLE-1","executeVehicleKey":null},
              {"id":2,"orderId":"ORDER-2","upperId":"UPPER-2","orderState":3,
               "appointVehicleKey":"VEHICLE-1","executeVehicleKey":"VEHICLE-1"}
            ]}}
            """));
        await using RiotSession session = CreateSession(handler);

        OrderStatePage page = await session.Order.ListOrdersByStatesAsync([1, 3, 7, 9]);

        Assert.Equal(1, page.Current);
        Assert.Equal(100, page.Size);
        Assert.Equal(2, page.Total);
        Assert.Equal(2, page.Records.Count);
        Assert.Equal("UPPER-2", page.Records[1].UpperId);
        Assert.True(page.CoversAllRecords);

        OrderStateRecord[] fullFirstPage = Enumerable.Range(1, 100)
            .Select(id => new OrderStateRecord(id, $"ORDER-{id}", $"UPPER-{id}", 1, null, null))
            .ToArray();
        Assert.False(new OrderStatePage(1, 100, 101, fullFirstPage).CoversAllRecords);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task ListOrdersByStates_sends_each_non_final_state_filter()
    {
        RecordingHandler handler = new(request =>
        {
            Assert.Equal("/api/order/v1/orderRecord", request.RequestUri?.AbsolutePath);
            string[] pairs = request.RequestUri!.Query.TrimStart('?').Split('&');
            Assert.Contains("pageNum=1", pairs);
            Assert.Contains("pageSize=100", pairs);
            Assert.Equal(1, pairs.Count(pair => pair == "filterByState=1"));
            Assert.Equal(1, pairs.Count(pair => pair == "filterByState=3"));
            Assert.Equal(1, pairs.Count(pair => pair == "filterByState=7"));
            Assert.Equal(1, pairs.Count(pair => pair == "filterByState=9"));
            return JsonResponse("""{"code":"0","result":{"current":1,"size":100,"total":0,"records":[]}}""");
        });
        await using RiotSession session = CreateSession(handler);

        OrderStatePage page = await session.Order.ListOrdersByStatesAsync([1, 3, 7, 9]);

        Assert.Empty(page.Records);
        Assert.True(page.CoversAllRecords);
        Assert.Equal(1, handler.CallCount);
    }

    [Theory]
    [InlineData("{\"code\":\"0\"}")]
    [InlineData("{\"code\":\"0\",\"result\":{\"current\":1,\"size\":100,\"total\":0}}")]
    public async Task ListOrdersByStates_rejects_missing_page_or_records(string body)
    {
        RecordingHandler handler = new(_ => JsonResponse(body));
        await using RiotSession session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.ListOrdersByStatesAsync([1, 3, 7, 9]));

        Assert.Equal("order-state-page-missing", error.BusinessCode);
        Assert.Equal(1, handler.CallCount);
    }

    private static RiotSession CreateSession(HttpMessageHandler handler) => new(
        new RiotOptions { BaseUrl = "http://riot.test", CallApiKey = "test-key" },
        new HttpClient(handler) { BaseAddress = new Uri("http://riot.test/") });

    private static HttpResponseMessage JsonResponse(string body) => new(HttpStatusCode.OK)
    {
        Content = new StringContent(body, Encoding.UTF8, "application/json"),
    };

    private sealed class RecordingHandler(
        Func<HttpRequestMessage, HttpResponseMessage> responseFactory) : HttpMessageHandler
    {
        public int CallCount { get; private set; }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            CallCount++;
            return Task.FromResult(responseFactory(request));
        }
    }
}
