using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade get order by upperId (BC-ORDER-005).
/// Expected ids from Lab fixture E1-order-success-detail-station2.
/// </summary>
public class GetOrderByUpperIdFacadeTests
{
    private const string UpperId = "riot-lab-I-20260720-120949";

    // Known-good body from E1-order-success-detail-station2.body
    private const string DetailSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":{"appointMapId":0,"appointStationId":0,"appointVehicleGroupId":0,"appointVehicleGroupName":"0","appointVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","changeVehicle":0,"changeVehicleReason":"","changeVehicleRecord":"","createTime":"2026-07-20 12:11:32","createdBy":"api-test","distance":0,"doneTime":"2026-07-20 12:11:40","endStationName":"站点2","endStationNo":2,"eta":0,"executeTime":"2026-07-20 12:11:36","executeVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","executeVehicleName":"新基测试300c协作1","executingIndex":-1,"failReason":"","finalState":true,"id":488003,"isAppointEnable":1,"isDeleted":0,"lockStatus":0,"missions":[{"actionId":0,"actionName":"","actionParam1":0,"actionParam2":0,"actionParamStr":"","createTime":"2026-07-20 12:11:35","createType":0,"destination":2,"destinationName":"站点2","executeTime":"2026-07-20 12:11:36","executingIndex":0,"failStrategy":"FAIL_STRATEGY_VOID","failValue":"0","finishTime":"2026-07-20 12:11:40","functionKey":"","id":7416323,"isDeleted":0,"length":0,"mapId":29,"mapName":"api测试","missionState":2,"orderId":488003,"orderUuid":"be8cb2d2-c50c-4b36-b04b-fb034a2ca3fb","resultCode":900,"resultStr":"订单完成","speed":0.0,"successStrategy":"SUCCESS_STRATEGY_VOID","type":"move","updateTime":"2026-07-20 12:11:40","width":0}],"modifiedBy":"internal","orderId":"order-2079056586101358592","orderName":"riot-lab-I-20260720-120949","orderState":5,"orderType":1,"priority":0,"priorityQueue":0,"progress":100,"source":"FMS","startEndStationNameDetail":"api测试 站点2 > api测试 站点2","startStationName":"站点2","startStationNo":2,"taskState":"1","totalCosts":0,"updateTime":"2026-07-20 12:11:40","upperId":"riot-lab-I-20260720-120949","userId":0},"tid":""}
        """;

    [Fact]
    public async Task GetOrderByUpperId_returns_order_identifiers()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, DetailSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var order = await session.Order.GetOrderByUpperIdAsync(UpperId);

        Assert.Equal(488003, order.Id);
        Assert.Equal("order-2079056586101358592", order.OrderId);
        Assert.Equal(UpperId, order.UpperId);
        Assert.Equal(5, order.OrderState);
    }

    [Fact]
    public async Task FindOrderByUpperId_returns_found_for_matching_complete_result()
    {
        const string body =
            """{"code":"0","result":{"id":7,"orderId":"ORDER-7","upperId":"UPPER-7","orderState":3,"appointVehicleKey":"VEHICLE-1","executeVehicleKey":"VEHICLE-1","endStationNo":12,"missions":[{"type":"move","mapId":25,"destination":12}]}}""";
        using var handler = new RecordingJsonHandler(HttpStatusCode.OK, body);
        await using var session = CreateSession(handler);

        OrderLookupResult result = await session.Order.FindOrderByUpperIdAsync("UPPER-7");

        Assert.Equal(OrderLookupStatus.Found, result.Status);
        Assert.Equal("UPPER-7", result.RequestedUpperId);
        Assert.NotNull(result.Order);
        Assert.Equal("ORDER-7", result.Order.OrderId);
        Assert.Equal("VEHICLE-1", result.Order.ExecuteVehicleKey);
        Assert.Equal(25, Assert.Single(result.Order.Missions).MapId);
        Assert.Equal("/api/order/v1/orderRecord/detailByUpperId/UPPER-7", handler.RequestPath);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_returns_not_found_only_for_http_404()
    {
        using var handler = new RecordingJsonHandler(HttpStatusCode.NotFound, "{}");
        await using var session = CreateSession(handler);

        OrderLookupResult result = await session.Order.FindOrderByUpperIdAsync("UPPER-404");

        Assert.Equal(OrderLookupStatus.NotFound, result.Status);
        Assert.Null(result.Order);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_returns_absent_at_observation_for_success_without_result()
    {
        using var handler = new RecordingJsonHandler(
            HttpStatusCode.OK,
            """{"code":"0","message":"成功","msgDetail":"","tid":""}""");
        await using var session = CreateSession(handler);

        OrderLookupResult result = await session.Order.FindOrderByUpperIdAsync("UPPER-ABSENT");

        Assert.Equal(OrderLookupStatus.AbsentAtObservation, result.Status);
        Assert.NotEqual(OrderLookupStatus.NotFound, result.Status);
        Assert.Null(result.Order);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_returns_indeterminate_for_incomplete_result()
    {
        using var handler = new RecordingJsonHandler(
            HttpStatusCode.OK,
            """{"code":"0","result":{"upperId":"UPPER-INCOMPLETE","orderState":1}}""");
        await using var session = CreateSession(handler);

        OrderLookupResult result = await session.Order.FindOrderByUpperIdAsync("UPPER-INCOMPLETE");

        Assert.Equal(OrderLookupStatus.Indeterminate, result.Status);
        Assert.Null(result.Order);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_returns_indeterminate_for_mismatched_upper_id()
    {
        using var handler = new RecordingJsonHandler(
            HttpStatusCode.OK,
            """{"code":"0","result":{"id":8,"orderId":"ORDER-8","upperId":"OTHER-UPPER","orderState":1}}""");
        await using var session = CreateSession(handler);

        OrderLookupResult result = await session.Order.FindOrderByUpperIdAsync("EXPECTED-UPPER");

        Assert.Equal(OrderLookupStatus.Indeterminate, result.Status);
        Assert.Null(result.Order);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_propagates_caller_cancellation()
    {
        using var cts = new CancellationTokenSource();
        using var handler = new CancellationHandler();
        await using var session = CreateSession(handler);

        Task<OrderLookupResult> read = session.Order.FindOrderByUpperIdAsync(
            "UPPER-CANCEL",
            cts.Token);
        await handler.Started;
        cts.Cancel();

        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => read);
    }

    [Fact]
    public async Task FindOrderByUpperId_wraps_http_500_as_RiotApiException()
    {
        const string body = "{\"error\":\"upstream unavailable\"}";
        using var handler = new RecordingJsonHandler(HttpStatusCode.InternalServerError, body);
        await using var session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.FindOrderByUpperIdAsync("UPPER-500"));

        Assert.Equal(500, error.StatusCode);
        Assert.Equal(body, error.ResponseBody);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_wraps_invalid_json_as_RiotApiException()
    {
        const string body = "not-json";
        using var handler = new RecordingJsonHandler(HttpStatusCode.OK, body);
        await using var session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.FindOrderByUpperIdAsync("UPPER-JSON"));

        Assert.Equal(200, error.StatusCode);
        Assert.Equal("riot-response-invalid", error.BusinessCode);
        Assert.Equal(body, error.ResponseBody);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_preserves_business_failure_evidence()
    {
        const string body = "{\"code\":\"500\",\"message\":\"业务失败\",\"result\":null}";
        using var handler = new RecordingJsonHandler(HttpStatusCode.OK, body);
        await using var session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.FindOrderByUpperIdAsync("UPPER-BUSINESS"));

        Assert.Equal(200, error.StatusCode);
        Assert.Equal("500", error.BusinessCode);
        Assert.Equal(body, error.ResponseBody);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task FindOrderByUpperId_wraps_transport_failure_as_RiotApiException()
    {
        using var handler = new TransportFailureHandler();
        await using var session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.FindOrderByUpperIdAsync("UPPER-TRANSPORT"));

        Assert.Equal("riot-read-failed", error.BusinessCode);
        Assert.IsType<HttpRequestException>(error.InnerException);
    }

    [Fact]
    public async Task FindOrderByUpperId_wraps_body_read_timeout_as_RiotApiException()
    {
        using var handler = new HangingContentHandler();
        using var http = new HttpClient(handler)
        {
            BaseAddress = new Uri("http://riot.test/"),
            Timeout = TimeSpan.FromMilliseconds(100),
        };
        await using var session = new RiotSession(
            new RiotOptions
            {
                BaseUrl = "http://riot.test",
                CallApiKey = "test-call-api-key",
                Timeout = TimeSpan.FromMilliseconds(100),
            },
            http);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Order.FindOrderByUpperIdAsync("UPPER-TIMEOUT"));

        Assert.Equal("riot-read-timeout", error.BusinessCode);
    }

    private static RiotSession CreateSession(HttpMessageHandler handler)
    {
        var http = new HttpClient(handler)
        {
            BaseAddress = new Uri("http://riot.test/"),
        };
        return new RiotSession(
            new RiotOptions
            {
                BaseUrl = "http://riot.test",
                CallApiKey = "test-call-api-key",
            },
            http);
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

    private sealed class RecordingJsonHandler(
        HttpStatusCode status,
        string body) : HttpMessageHandler
    {
        public int CallCount { get; private set; }
        public string? RequestPath { get; private set; }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            CallCount++;
            RequestPath = request.RequestUri?.AbsolutePath;
            return Task.FromResult(new HttpResponseMessage(status)
            {
                Content = new StringContent(body, Encoding.UTF8, "application/json"),
            });
        }
    }

    private sealed class CancellationHandler : HttpMessageHandler
    {
        private readonly TaskCompletionSource _started = new(
            TaskCreationOptions.RunContinuationsAsynchronously);

        public Task Started => _started.Task;

        protected override async Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            _started.TrySetResult();
            await Task.Delay(Timeout.InfiniteTimeSpan, cancellationToken);
            throw new InvalidOperationException("Unreachable after cancellation.");
        }
    }

    private sealed class TransportFailureHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken) =>
            Task.FromException<HttpResponseMessage>(new HttpRequestException("simulated failure"));
    }

    private sealed class HangingContentHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken) =>
            Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new HangingContent(),
            });
    }

    private sealed class HangingContent : HttpContent
    {
        protected override Task SerializeToStreamAsync(
            Stream stream,
            TransportContext? context) =>
            Task.Delay(Timeout.InfiniteTimeSpan);

        protected override Task SerializeToStreamAsync(
            Stream stream,
            TransportContext? context,
            CancellationToken cancellationToken) =>
            Task.Delay(Timeout.InfiniteTimeSpan, cancellationToken);

        protected override bool TryComputeLength(out long length)
        {
            length = 0;
            return false;
        }
    }
}
