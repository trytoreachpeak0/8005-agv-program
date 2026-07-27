using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Facade ListDevices / GetDeviceStatusStatistics (ADR-sdk-0005 unwrap + throw).
/// </summary>
public class ListDevicesFacadeTests
{
    private const string ListDevicesSuccessBody =
        """
        {"code":"0","message":"成功","result":{"current":1,"size":10,"total":1,"records":[{"deviceKey":"DEV-1","deviceName":"agv-1"}]}}
        """;

    private const string ListDevicesFailureBody =
        """
        {"code":"500","message":"内部错误","result":null}
        """;

    private const string StatisticsSuccessBody =
        """
        {"code":"0","message":"成功","result":{"allCount":2,"onlineCount":1,"offlineCount":1,"enable":1,"unEnable":1,"inactiveCount":0}}
        """;

    [Fact]
    public async Task ListDevices_unwraps_page_on_success()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, ListDevicesSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        await using var session = new RiotSession(
            new RiotOptions { BaseUrl = "http://riot.test", CallApiKey = "test-key" },
            http);

        var page = await session.Device.ListDevicesAsync(pageNum: 1, pageSize: 10);

        Assert.Equal(1, page.Total);
        Assert.NotNull(page.Records);
        Assert.Single(page.Records!);
        Assert.Equal("DEV-1", page.Records[0].DeviceKey);
    }

    [Fact]
    public async Task ListDevices_throws_RiotApiException_on_business_failure()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, ListDevicesFailureBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        await using var session = new RiotSession(
            new RiotOptions { BaseUrl = "http://riot.test", CallApiKey = "test-key" },
            http);

        var ex = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Device.ListDevicesAsync(pageNum: 1, pageSize: 10));

        Assert.Equal("500", ex.BusinessCode);
    }

    [Fact]
    public async Task GetDeviceStatusStatistics_unwraps_dto_on_success()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, StatisticsSuccessBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        await using var session = new RiotSession(
            new RiotOptions { BaseUrl = "http://riot.test", CallApiKey = "test-key" },
            http);

        var stats = await session.Device.GetDeviceStatusStatisticsAsync();

        Assert.Equal(2, stats.AllCount);
        Assert.Equal(1, stats.OnlineCount);
    }

    [Fact]
    public void IsSuccessCode_accepts_common_success_tokens()
    {
        Assert.True(RiotBusinessResponse.IsSuccessCode("0"));
        Assert.True(RiotBusinessResponse.IsSuccessCode("200"));
        Assert.True(RiotBusinessResponse.IsSuccessCode("OK"));
        Assert.True(RiotBusinessResponse.IsSuccessCode(null));
        Assert.True(RiotBusinessResponse.IsSuccessCode("   "));
        Assert.True(RiotBusinessResponse.IsSuccessCode(" 0 "));
        Assert.False(RiotBusinessResponse.IsSuccessCode("500"));
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
