using Microsoft.Kiota.Abstractions.Authentication;
using Microsoft.Kiota.Http.HttpClientLibrary;
using RIoT.Sdk.Core;
using GenDeviceClient = RIoT.Sdk.Generated.Device.DeviceClient;
using GenImapClient = RIoT.Sdk.Generated.Imap.ImapClient;
using GenOrderClient = RIoT.Sdk.Generated.Order.OrderClient;
using GenTaskClient = RIoT.Sdk.Generated.TaskApi.TaskClient;

namespace RIoT.Sdk.Facade;

/// <summary>
/// Shared session: default CallApiKey Bearer, or AdminLogin backup; reuse across facades.
/// </summary>
public sealed class RiotSession : IAsyncDisposable, IDisposable
{
    private readonly RiotAuthClient _auth;
    private readonly bool _ownsAuth;
    private readonly HttpClientRequestAdapter _adapter;

    public RiotSession(RiotOptions options, HttpClient? httpClient = null)
    {
        ArgumentNullException.ThrowIfNull(options);
        Options = options;
        TokenProvider = new RiotTokenProvider();

        // ADR-sdk-0001: CallApiKey is the default Bearer credential; AdminLogin is optional.
        if (!string.IsNullOrWhiteSpace(options.CallApiKey))
        {
            TokenProvider.SetAccessToken(options.CallApiKey);
        }

        _auth = new RiotAuthClient(options, httpClient);
        _ownsAuth = true;

        var authProvider = new BaseBearerTokenAuthenticationProvider(new KiotaAccessTokenProvider(TokenProvider));
        // Inject HttpClient when provided so Facade unit tests can mock at the HTTP boundary.
        _adapter = new HttpClientRequestAdapter(authProvider, httpClient: httpClient)
        {
            BaseUrl = options.BaseUrl.TrimEnd('/'),
        };

        Device = new DeviceClient(this);
        Tasks = new TaskClient(this);
        Order = new OrderClient(this);
        Maps = new MapClient(this);
    }

    public RiotOptions Options { get; }
    public RiotTokenProvider TokenProvider { get; }
    public DeviceClient Device { get; }
    /// <summary>Task-module facade (named Tasks to avoid clashing with System.Threading.Tasks.Task).</summary>
    public TaskClient Tasks { get; }
    public OrderClient Order { get; }
    public MapClient Maps { get; }

    internal HttpClientRequestAdapter Adapter => _adapter;

    public async Task<AuthTokens> LoginAsync(CancellationToken cancellationToken = default)
    {
        var tokens = await _auth.LoginAsync(cancellationToken: cancellationToken).ConfigureAwait(false);
        TokenProvider.SetAccessToken(tokens.AccessToken);
        return tokens;
    }

    public async Task<AuthTokens> RefreshTokenAsync(CancellationToken cancellationToken = default)
    {
        var current = await TokenProvider.GetAccessTokenAsync(cancellationToken).ConfigureAwait(false);
        var tokens = await _auth.RefreshTokenAsync(current, cancellationToken).ConfigureAwait(false);
        TokenProvider.SetAccessToken(tokens.AccessToken);
        return tokens;
    }

    internal GenDeviceClient CreateGeneratedDeviceClient() => new(_adapter);
    internal GenTaskClient CreateGeneratedTaskClient() => new(_adapter);
    internal GenOrderClient CreateGeneratedOrderClient() => new(_adapter);
    internal GenImapClient CreateGeneratedImapClient() => new(_adapter);

    public void Dispose()
    {
        if (_ownsAuth)
        {
            _auth.Dispose();
        }

        _adapter.Dispose();
    }

    public ValueTask DisposeAsync()
    {
        Dispose();
        return ValueTask.CompletedTask;
    }
}
