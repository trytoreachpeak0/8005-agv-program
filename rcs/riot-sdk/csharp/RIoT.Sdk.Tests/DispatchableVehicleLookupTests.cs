using RIoT.Sdk.Core;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: dispatchable-vehicle name → deviceKey (BC-VEH-002).
/// Expected values from Lab fixture B1-name-to-deviceKey.
/// </summary>
public class DispatchableVehicleLookupTests
{
    private static readonly DispatchableVehicle[] SampleVehicles =
    [
        new("BROKERX-8ffb2294db594d7480125d379b39cfd6", "新基测试300c顶升2"),
        new("BROKERX-aee2f93d717546cf9510c98c854fe83e", "新基测试300c协作1"),
        new("BROKERX-757de62710d84cec9fe9907691672cbc", "尊阳-多仓位1"),
    ];

    [Fact]
    public void ResolveDeviceKey_exact_name_returns_unique_key()
    {
        var key = DispatchableVehicleLookup.ResolveDeviceKey(SampleVehicles, "新基测试300c协作1");

        Assert.Equal("BROKERX-aee2f93d717546cf9510c98c854fe83e", key);
    }

    [Fact]
    public void ResolveDeviceKey_unknown_name_throws_not_found()
    {
        // Fixture B1-name-to-deviceKey.unknownNameLookup
        var ex = Assert.Throws<RiotApiException>(() =>
            DispatchableVehicleLookup.ResolveDeviceKey(
                SampleVehicles,
                "不存在的车辆名-riot-behavior-lab"));

        Assert.Equal("vehicle-name-not-found", ex.BusinessCode);
    }

    [Fact]
    public void ResolveDeviceKey_duplicate_name_throws_ambiguous()
    {
        // BC-VEH-002: 重名必须失败而不是任选一台（现场本轮无重名，用合成样例）
        DispatchableVehicle[] duplicates =
        [
            new("BROKERX-key-a", "重名车"),
            new("BROKERX-key-b", "重名车"),
        ];

        var ex = Assert.Throws<RiotApiException>(() =>
            DispatchableVehicleLookup.ResolveDeviceKey(duplicates, "重名车"));

        Assert.Equal("vehicle-name-ambiguous", ex.BusinessCode);
    }
}
