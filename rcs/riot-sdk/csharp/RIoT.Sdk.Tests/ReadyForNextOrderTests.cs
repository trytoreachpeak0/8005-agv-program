using RIoT.Sdk.Core;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Core ReadyForNextOrder pure helper (BC-STATE-003 / ADR-0008).
/// Known-good SUCCESS=5 + IDLE from Lab Round8 state trajectory.
/// </summary>
public class ReadyForNextOrderTests
{
    [Fact]
    public void IsReady_success_and_idle_returns_true()
    {
        // Round8 E2: orderState=5 SUCCESS, procState=IDLE → 可再派
        var ready = ReadyForNextOrder.IsReady(
            orderState: 5,
            procState: "IDLE",
            processingOrder: false);

        Assert.True(ready);
    }

    [Fact]
    public void IsReady_awaiting_order_before_success_returns_false()
    {
        // BC-STATE-003: 物理到站时 proc=AWAITING_ORDER，order 仍可能为 EXECUTING(3)
        var ready = ReadyForNextOrder.IsReady(
            orderState: 3,
            procState: "AWAITING_ORDER",
            processingOrder: true);

        Assert.False(ready);
    }
}