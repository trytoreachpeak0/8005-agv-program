using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

public sealed class PublicFacadeContractTests
{
    [Fact]
    public void PublicFacadeContract_matches_declared_cross_language_manifest()
    {
        Assert.Equal(
            ["Found", "NotFound", "AbsentAtObservation", "Indeterminate"],
            Enum.GetNames<OrderLookupStatus>());

        Assert.NotNull(typeof(OrderClient).GetMethod(nameof(OrderClient.FindOrderByUpperIdAsync)));
        Assert.NotNull(typeof(OrderClient).GetMethod(nameof(OrderClient.ListOrdersByStatesAsync)));
        Assert.NotNull(typeof(TaskClient).GetMethod(nameof(TaskClient.GetVehicleCardAsync)));
        Assert.NotNull(typeof(TaskClient).GetMethod(nameof(TaskClient.GetVehicleExecutionFactsAsync)));
        Assert.NotNull(typeof(MapClient).GetMethod(nameof(MapClient.ListStationsStrictAsync)));
    }

    [Fact]
    public void OrderLookupResultFactories_enforce_status_payload_invariants()
    {
        OrderSnapshot order = new(
            1,
            "ORDER-1",
            "UPPER-1",
            1,
            null,
            null,
            null,
            []);

        OrderLookupResult found = OrderLookupResult.Found("UPPER-1", order);
        Assert.Same(order, found.Order);
        Assert.Throws<ArgumentException>(() => OrderLookupResult.Found("OTHER", order));

        Assert.Null(OrderLookupResult.NotFound("UPPER-1").Order);
        Assert.Null(OrderLookupResult.AbsentAtObservation("UPPER-1").Order);
        Assert.Null(OrderLookupResult.Indeterminate("UPPER-1").Order);
    }
}
