using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: Session + CallApiKey (ADR-sdk-0001). Default auth without AdminLogin.
/// </summary>
public class CallApiKeyAuthTests
{
    [Fact]
    public async Task Session_with_CallApiKey_can_authenticate_without_AdminLogin()
    {
        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            CallApiKey = "test-call-api-key",
        };

        await using var session = new RiotSession(options);

        // Never called LoginAsync — CallApiKey is the default Bearer credential.
        var bearer = await session.TokenProvider.GetAccessTokenAsync();

        Assert.Equal("test-call-api-key", bearer);
    }
}
