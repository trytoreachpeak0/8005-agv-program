namespace RIoT.Sdk.Core;

/// <summary>
/// Tokens returned by RIoT login / refreshToken.
/// </summary>
public sealed class AuthTokens
{
    public required string AccessToken { get; init; }

    /// <summary>Optional refresh token when the server returns one.</summary>
    public string? RefreshToken { get; init; }

    /// <summary>Raw result map from ResponseMsg.result for diagnostics.</summary>
    public IReadOnlyDictionary<string, string> RawResult { get; init; }
        = new Dictionary<string, string>();
}
