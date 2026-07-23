namespace RIoT.Sdk.Core;

/// <summary>
/// Connection options for a RIoT instance.
/// Default auth is <see cref="CallApiKey"/> (ADR-0001); AdminLogin username/password are optional backup.
/// </summary>
public sealed class RiotOptions
{
    /// <summary>Base URL, e.g. http://172.19.206.222:8888</summary>
    public required string BaseUrl { get; init; }

    /// <summary>Long-lived CallApiKey used as default Bearer credential.</summary>
    public string? CallApiKey { get; init; }

    /// <summary>AdminLogin username (backup auth path).</summary>
    public string? Username { get; init; }

    /// <summary>AdminLogin password (backup auth path).</summary>
    public string? Password { get; init; }

    /// <summary>HTTP timeout. Default 30s.</summary>
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}
