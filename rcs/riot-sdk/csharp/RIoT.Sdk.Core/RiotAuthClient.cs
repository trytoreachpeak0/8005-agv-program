using System.Net.Http.Json;
using System.Text.Json;

namespace RIoT.Sdk.Core;

/// <summary>
/// Hand-written auth client for the two RIoT security endpoints we need:
/// POST /api/auth/v1/admin/login and PUT /api/auth/v1/admin/refreshToken.
/// </summary>
public sealed class RiotAuthClient : IDisposable
{
    private readonly HttpClient _http;
    private readonly bool _ownsHttp;

    public RiotAuthClient(RiotOptions options, HttpClient? httpClient = null)
    {
        ArgumentNullException.ThrowIfNull(options);
        if (string.IsNullOrWhiteSpace(options.BaseUrl))
        {
            throw new ArgumentException("BaseUrl is required.", nameof(options));
        }

        if (httpClient is null)
        {
            _http = new HttpClient { Timeout = options.Timeout };
            _ownsHttp = true;
        }
        else
        {
            _http = httpClient;
            _ownsHttp = false;
        }

        _http.BaseAddress ??= new Uri(EnsureTrailingSlash(options.BaseUrl));
        Options = options;
    }

    public RiotOptions Options { get; }

    public async Task<AuthTokens> LoginAsync(
        string? username = null,
        string? password = null,
        CancellationToken cancellationToken = default)
    {
        var user = username ?? Options.Username;
        var pass = password ?? Options.Password;
        using var request = new HttpRequestMessage(HttpMethod.Post, "api/auth/v1/admin/login")
        {
            Content = JsonContent.Create(new { username = user, password = pass }),
        };
        return await SendAuthAsync(request, cancellationToken).ConfigureAwait(false);
    }

    public async Task<AuthTokens> RefreshTokenAsync(
        string accessToken,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(accessToken);
        using var request = new HttpRequestMessage(HttpMethod.Put, "api/auth/v1/admin/refreshToken");
        // RIoT swagger declares Authorization as apiKey header; deployments commonly accept Bearer.
        request.Headers.TryAddWithoutValidation("Authorization", $"Bearer {StripBearerPrefix(accessToken)}");
        return await SendAuthAsync(request, cancellationToken).ConfigureAwait(false);
    }

    private async Task<AuthTokens> SendAuthAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        HttpResponseMessage response;
        try
        {
            response = await _http.SendAsync(request, cancellationToken).ConfigureAwait(false);
        }
        catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException)
        {
            throw new RiotApiException($"RIoT auth request failed: {ex.Message}", innerException: ex);
        }

        var body = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
        if (!response.IsSuccessStatusCode)
        {
            throw new RiotApiException(
                $"RIoT auth HTTP {(int)response.StatusCode}: {Truncate(body, 500)}",
                statusCode: (int)response.StatusCode,
                responseBody: body);
        }

        using var doc = JsonDocument.Parse(string.IsNullOrWhiteSpace(body) ? "{}" : body);
        var root = doc.RootElement;
        var businessCode = root.TryGetProperty("code", out var codeEl) ? codeEl.GetString() : null;
        if (!RiotBusinessResponse.IsSuccessCode(businessCode))
        {
            var message = root.TryGetProperty("message", out var msgEl) ? msgEl.GetString() : null;
            throw new RiotApiException(
                $"RIoT auth business failure code={businessCode} message={message}",
                statusCode: (int)response.StatusCode,
                businessCode: businessCode,
                responseBody: body);
        }

        var raw = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        if (root.TryGetProperty("result", out var result) && result.ValueKind == JsonValueKind.Object)
        {
            foreach (var prop in result.EnumerateObject())
            {
                raw[prop.Name] = prop.Value.ValueKind switch
                {
                    JsonValueKind.String => prop.Value.GetString() ?? string.Empty,
                    JsonValueKind.Null => string.Empty,
                    _ => prop.Value.GetRawText(),
                };
            }
        }

        var accessToken = FindToken(raw, "token", "accessToken", "access_token", "authorization", "Authorization");
        if (string.IsNullOrWhiteSpace(accessToken))
        {
            throw new RiotApiException(
                "RIoT auth succeeded but no token field was found in result.",
                statusCode: (int)response.StatusCode,
                businessCode: businessCode,
                responseBody: body);
        }

        accessToken = StripBearerPrefix(accessToken);
        var refresh = FindToken(raw, "refreshToken", "refresh_token");
        return new AuthTokens
        {
            AccessToken = accessToken,
            RefreshToken = string.IsNullOrWhiteSpace(refresh) ? null : StripBearerPrefix(refresh),
            RawResult = raw,
        };
    }

    private static string? FindToken(IReadOnlyDictionary<string, string> raw, params string[] keys)
    {
        foreach (var key in keys)
        {
            if (raw.TryGetValue(key, out var value) && !string.IsNullOrWhiteSpace(value))
            {
                return value;
            }
        }

        // Fallback: first value that looks like a JWT / opaque token.
        foreach (var pair in raw)
        {
            if (pair.Value.Length > 20)
            {
                return pair.Value;
            }
        }

        return null;
    }

    private static string StripBearerPrefix(string token)
        => token.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase)
            ? token["Bearer ".Length..].Trim()
            : token.Trim();

    private static string EnsureTrailingSlash(string baseUrl)
        => baseUrl.EndsWith('/') ? baseUrl : baseUrl + "/";

    private static string Truncate(string value, int max)
        => value.Length <= max ? value : value[..max] + "...";

    public void Dispose()
    {
        if (_ownsHttp)
        {
            _http.Dispose();
        }
    }
}
