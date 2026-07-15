namespace RIoT.Sdk.Core;

/// <summary>
/// Mutable bearer-token holder shared by Facade clients.
/// </summary>
public sealed class RiotTokenProvider
{
    private string? _accessToken;
    private readonly SemaphoreSlim _gate = new(1, 1);

    public string? AccessToken => _accessToken;

    public void SetAccessToken(string token)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(token);
        _accessToken = token.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase)
            ? token["Bearer ".Length..].Trim()
            : token.Trim();
    }

    public async Task<string> GetAccessTokenAsync(CancellationToken cancellationToken = default)
    {
        await _gate.WaitAsync(cancellationToken).ConfigureAwait(false);
        try
        {
            if (string.IsNullOrWhiteSpace(_accessToken))
            {
                throw new InvalidOperationException(
                    "No access token. Call RiotSession.LoginAsync() before invoking API clients.");
            }

            return _accessToken;
        }
        finally
        {
            _gate.Release();
        }
    }
}
