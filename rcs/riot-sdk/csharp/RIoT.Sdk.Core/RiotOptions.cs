namespace RIoT.Sdk.Core;

/// <summary>
/// Connection options for a RIoT instance.
/// </summary>
public sealed class RiotOptions
{
    /// <summary>Base URL, e.g. http://172.19.206.222:8888</summary>
    public required string BaseUrl { get; init; }

    /// <summary>Login username.</summary>
    public required string Username { get; init; }

    /// <summary>Login password.</summary>
    public required string Password { get; init; }

    /// <summary>HTTP timeout. Default 30s.</summary>
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}
