using Microsoft.Kiota.Abstractions.Authentication;
using RIoT.Sdk.Core;

namespace RIoT.Sdk.Facade;

internal sealed class KiotaAccessTokenProvider : IAccessTokenProvider
{
    private readonly RiotTokenProvider _tokens;

    public KiotaAccessTokenProvider(RiotTokenProvider tokens)
    {
        _tokens = tokens;
        AllowedHostsValidator = new AllowedHostsValidator();
    }

    public AllowedHostsValidator AllowedHostsValidator { get; }

    public Task<string> GetAuthorizationTokenAsync(
        Uri uri,
        Dictionary<string, object>? additionalAuthenticationContext = null,
        CancellationToken cancellationToken = default)
        => _tokens.GetAccessTokenAsync(cancellationToken);
}
