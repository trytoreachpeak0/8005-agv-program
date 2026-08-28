using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

public sealed class VehicleFactsFacadeTests
{
    [Fact]
    public async Task GetVehicleCard_returns_exact_facts_for_matching_device_key()
    {
        RecordingHandler handler = new(request =>
        {
            Assert.Equal(HttpMethod.Get, request.Method);
            Assert.Equal("/api/task/vehicles/getVehicleInfoByDeviceKey", request.RequestUri?.AbsolutePath);
            Assert.Equal("?key=VEHICLE-1", request.RequestUri?.Query);
            return JsonResponse("""
                {"code":"0","result":{"deviceKey":"VEHICLE-1","enable":true,"status":1,
                "procState":"IDLE","currentMap":"MAP-25","currentPosition":12,"battery":80,
                "batteryState":"NO_CHARGE","speed":0,"lockStatus":0,"orderTaskId":null}}
                """);
        });
        await using RiotSession session = CreateSession(handler);

        VehicleCard card = await session.Tasks.GetVehicleCardAsync("VEHICLE-1");

        Assert.Equal("VEHICLE-1", card.DeviceKey);
        Assert.Equal(true, card.Enable);
        Assert.Equal(1, card.Status);
        Assert.Equal("IDLE", card.ProcState);
        Assert.Equal("MAP-25", card.CurrentMap);
        Assert.Equal(12, card.CurrentPosition);
        Assert.Equal(80, card.BatteryPercent);
        Assert.Equal("NO_CHARGE", card.BatteryState);
        Assert.Equal(0d, card.Speed);
        Assert.Equal(0, card.LockStatus);
        Assert.Null(card.OrderTaskId);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task GetVehicleCard_rejects_mismatched_device_key()
    {
        RecordingHandler handler = new(_ => JsonResponse(
            """{"code":"0","result":{"deviceKey":"OTHER","enable":true,"status":1}}"""));
        await using RiotSession session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Tasks.GetVehicleCardAsync("VEHICLE-1"));

        Assert.Equal("vehicle-key-mismatch", error.BusinessCode);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task GetVehicleCard_rejects_missing_result()
    {
        RecordingHandler handler = new(_ => JsonResponse("""{"code":"0","result":null}"""));
        await using RiotSession session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Tasks.GetVehicleCardAsync("VEHICLE-1"));

        Assert.Equal("vehicle-card-missing", error.BusinessCode);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task GetVehicleExecutionFacts_returns_vehicle_and_task_facts()
    {
        RecordingHandler handler = new(request =>
        {
            Assert.Equal("/api/task/v1/task/getVehicleInfo/VEHICLE-1", request.RequestUri?.AbsolutePath);
            return JsonResponse("""
                {
                  "vehicle":{"movementState":"MT_FINISHED","controlState":"CONTROL_STATE_OK",
                    "emergencyState":"OK","breakSwitchState":"MOVABLE",
                    "locationState":"LOCATION_STATE_RUNNING","speed":0},
                  "vehicleTaskInfo":{"key":"VEHICLE-1","procState":"IDLE",
                    "processingOrder":false,"enable":true,"integrationLevel":"ON_LINE"}
                }
                """);
        });
        await using RiotSession session = CreateSession(handler);

        VehicleExecutionFacts facts = await session.Tasks.GetVehicleExecutionFactsAsync("VEHICLE-1");

        Assert.Equal("VEHICLE-1", facts.DeviceKey);
        Assert.Equal("MT_FINISHED", facts.MovementState);
        Assert.Equal("CONTROL_STATE_OK", facts.ControlState);
        Assert.Equal("OK", facts.EmergencyState);
        Assert.Equal("MOVABLE", facts.BreakSwitchState);
        Assert.Equal("LOCATION_STATE_RUNNING", facts.LocationState);
        Assert.Equal(0d, facts.Speed);
        Assert.Equal("IDLE", facts.ProcState);
        Assert.Equal(false, facts.ProcessingOrder);
        Assert.Equal(true, facts.Enable);
        Assert.Equal("ON_LINE", facts.IntegrationLevel);
        Assert.Equal(1, handler.CallCount);
    }

    [Theory]
    [InlineData("{\"vehicleTaskInfo\":{\"key\":\"VEHICLE-1\"}}")]
    [InlineData("{\"vehicle\":{\"movementState\":\"MT_FINISHED\"}}")]
    public async Task GetVehicleExecutionFacts_rejects_missing_vehicle_or_task_half(string body)
    {
        RecordingHandler handler = new(_ => JsonResponse(body));
        await using RiotSession session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Tasks.GetVehicleExecutionFactsAsync("VEHICLE-1"));

        Assert.Equal("vehicle-execution-facts-missing", error.BusinessCode);
        Assert.Equal(1, handler.CallCount);
    }

    [Fact]
    public async Task GetVehicleExecutionFacts_rejects_mismatched_task_key()
    {
        RecordingHandler handler = new(_ => JsonResponse("""
            {"vehicle":{"movementState":"MT_FINISHED"},
             "vehicleTaskInfo":{"key":"OTHER","procState":"IDLE"}}
            """));
        await using RiotSession session = CreateSession(handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.Tasks.GetVehicleExecutionFactsAsync("VEHICLE-1"));

        Assert.Equal("vehicle-key-mismatch", error.BusinessCode);
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
