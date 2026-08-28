using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade create move order via byDefaultMissions (BC-ORDER-001 / BC-ORDER-005).
/// Expected ids from Lab fixture E1-byDefaultMissions-create-2to1.
/// </summary>
public class CreateMoveOrderFacadeTests
{
    private const string DeviceKey = "BROKERX-aee2f93d717546cf9510c98c854fe83e";
    private const string UpperId = "riot-behavior-lab-E1b-2to1-20260720-121102";

    // Known-good body from E1-byDefaultMissions-create-2to1.responseBody
    private const string CreateSuccessBody =
        """
        {"code":"0","message":"成功","msgDetail":"","result":{"appointVehicleGroupId":0,"appointVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","createTime":"2026-07-20 12:12:44","createdBy":"api-test","endStationName":"站点1","endStationNo":1,"finalState":false,"id":488004,"isAppointEnable":1,"lockStatus":0,"missions":[{"actionId":0,"actionName":"","actionParam1":0,"actionParam2":0,"actionParamStr":"","createTime":"2026-07-20 12:12:44","createType":0,"destination":1,"destinationName":"","executingIndex":0,"failStrategy":"","failValue":"","functionKey":"","id":7416324,"isDeleted":0,"length":0,"mapId":29,"mapName":"","missionState":0,"orderId":488004,"orderUuid":"72461016-4273-4d35-b6f1-ad9f0e726643","resultCode":0,"resultStr":"","speed":0.0,"successStrategy":"SUCCESS_STRATEGY_VOID","type":"move","updateTime":"2026-07-20 12:12:44","width":0}],"modifiedBy":"api-test","orderId":"order-2079056892281356288","orderName":"riot-behavior-lab-E1b-2to1-20260720-121102","orderState":1,"orderType":1,"priority":0,"source":"FMS","startEndStationNameDetail":"null null > null null","startStationName":"站点1","startStationNo":1,"updateTime":"2026-07-20 12:12:44","upperId":"riot-behavior-lab-E1b-2to1-20260720-121102","userId":0},"tid":""}
        """;

    [Fact]
    public async Task CreateMoveOrder_returns_order_identifiers()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, CreateSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options, http);

        var order = await session.Order.CreateMoveOrderAsync(
            upperId: UpperId,
            appointVehicleKey: DeviceKey,
            mapId: 29,
            destinationStationId: 1);

        Assert.Equal(488004, order.Id);
        Assert.Equal("order-2079056892281356288", order.OrderId);
        Assert.Equal(UpperId, order.UpperId);
        Assert.Equal(1, order.OrderState);
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
