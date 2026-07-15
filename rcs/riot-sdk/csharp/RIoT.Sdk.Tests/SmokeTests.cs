using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

public class SmokeTests
{
    private static RiotOptions? TryLoadOptions()
    {
        var baseUrl = Environment.GetEnvironmentVariable("RIOT_BASE_URL")
                      ?? "http://172.19.206.222:8888";
        var username = Environment.GetEnvironmentVariable("RIOT_USERNAME") ?? "admin";
        var password = Environment.GetEnvironmentVariable("RIOT_PASSWORD") ?? "admin";

        // Opt-in: set RIOT_SMOKE=1 to run against a live instance.
        var enabled = Environment.GetEnvironmentVariable("RIOT_SMOKE");
        if (!string.Equals(enabled, "1", StringComparison.Ordinal)
            && !string.Equals(enabled, "true", StringComparison.OrdinalIgnoreCase))
        {
            return null;
        }

        return new RiotOptions
        {
            BaseUrl = baseUrl,
            Username = username,
            Password = password,
        };
    }

    [Fact]
    public async Task Login_And_ListDevices_Smoke()
    {
        var options = TryLoadOptions();
        if (options is null)
        {
            // Keep CI / offline builds green; run with RIOT_SMOKE=1 when the host is reachable.
            return;
        }

        await using var session = new RiotSession(options);
        var tokens = await session.LoginAsync();
        Assert.False(string.IsNullOrWhiteSpace(tokens.AccessToken));

        var devices = await session.Device.ListDevicesAsync(pageNum: 1, pageSize: 10);
        Assert.NotNull(devices);
        Console.WriteLine($"devices.code={devices!.Code} message={devices.Message}");
    }
}
