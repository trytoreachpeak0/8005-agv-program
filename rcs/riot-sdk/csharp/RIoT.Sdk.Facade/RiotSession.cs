using Microsoft.Kiota.Abstractions.Authentication;
using Microsoft.Kiota.Http.HttpClientLibrary;
using System.Net.Http.Headers;
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
    private readonly HttpClient _httpClient;
    private readonly bool _ownsHttpClient;
    private readonly HttpClientRequestAdapter _adapter;

    public RiotSession(RiotOptions options, HttpClient? httpClient = null)
        : this(
            options,
            httpClient ?? CreateNoRetryHttpClient(options),
            ownsHttpClient: httpClient is null)
    {
    }

    /// <summary>
    /// Creates an SDK-owned transport around a caller-supplied primary handler. The SDK
    /// adds no retry or redirect middleware; this overload is also the deterministic test seam.
    /// </summary>
    public RiotSession(RiotOptions options, HttpMessageHandler primaryHandler)
        : this(options, CreateNoRetryHttpClient(options, primaryHandler), ownsHttpClient: true)
    {
    }

    private RiotSession(RiotOptions options, HttpClient httpClient, bool ownsHttpClient)
    {
        ArgumentNullException.ThrowIfNull(options);
        ArgumentNullException.ThrowIfNull(httpClient);
        ValidateHttpClientOrigin(options, httpClient);
        Options = options;
        TokenProvider = new RiotTokenProvider();
        _httpClient = httpClient;
        _ownsHttpClient = ownsHttpClient;

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

    internal async Task<HttpResponseMessage> SendRawAsync(
        HttpMethod method,
        string path,
        CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(method);
        ArgumentException.ThrowIfNullOrWhiteSpace(path);

        string token = await TokenProvider.GetAccessTokenAsync(cancellationToken).ConfigureAwait(false);
        Uri optionsBaseUri = new(Options.BaseUrl.TrimEnd('/') + "/", UriKind.Absolute);
        Uri requestUri = new(optionsBaseUri, path.TrimStart('/'));
        using var request = new HttpRequestMessage(method, requestUri);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return await _httpClient.SendAsync(
            request,
            HttpCompletionOption.ResponseContentRead,
            cancellationToken).ConfigureAwait(false);
    }

    private static void ValidateHttpClientOrigin(RiotOptions options, HttpClient httpClient)
    {
        if (httpClient.BaseAddress is null)
        {
            return;
        }

        Uri configured = new(options.BaseUrl, UriKind.Absolute);
        Uri injected = httpClient.BaseAddress;
        if (!string.Equals(configured.Scheme, injected.Scheme, StringComparison.OrdinalIgnoreCase) ||
            !string.Equals(configured.IdnHost, injected.IdnHost, StringComparison.OrdinalIgnoreCase) ||
            configured.Port != injected.Port)
        {
            throw new ArgumentException(
                "Injected HttpClient.BaseAddress origin must match RiotOptions.BaseUrl.",
                nameof(httpClient));
        }
    }

    private static HttpClient CreateNoRetryHttpClient(
        RiotOptions options,
        HttpMessageHandler? primaryHandler = null)
    {
        ArgumentNullException.ThrowIfNull(options);
        HttpMessageHandler handler = primaryHandler ?? new HttpClientHandler
        {
            AllowAutoRedirect = false,
        };
        return new HttpClient(handler, disposeHandler: true)
        {
            Timeout = options.Timeout,
            BaseAddress = new Uri(options.BaseUrl.TrimEnd('/') + "/"),
        };
    }

    public void Dispose()
    {
        if (_ownsAuth)
        {
            _auth.Dispose();
        }

        _adapter.Dispose();
        if (_ownsHttpClient)
        {
            _httpClient.Dispose();
        }
    }

    public ValueTask DisposeAsync()
    {
        Dispose();
        return ValueTask.CompletedTask;
    }
}
