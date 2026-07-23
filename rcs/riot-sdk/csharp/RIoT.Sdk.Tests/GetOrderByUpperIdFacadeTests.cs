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
