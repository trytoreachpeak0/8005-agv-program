using System.Net;
using System.Text;
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

namespace RIoT.Sdk.Tests;

/// <summary>
/// Seam: AdminLogin BusinessFailure (BC-AUTH-001 / ADR-sdk-0005).
/// Expected shape from Lab fixture A1-login-invalid-password (HTTP 200 + code 2009).
/// </summary>
public class AdminLoginAuthTests
{
    // Known-good body from BC-AUTH-001 / A1 invalid-password fixture (not inventing codes).
    private const string InvalidPasswordBody =
        """{"code":"2009","message":"密码不正确","result":null}""";

    [Fact]
    public async Task AdminLogin_with_invalid_password_throws_BusinessFailure()
    {
        using var http = new HttpClient(new FixedJsonHandler(HttpStatusCode.OK, InvalidPasswordBody))
        {
            BaseAddress = new Uri("http://riot.test/"),
        };

        var options = new RiotOptions
        {
            BaseUrl = "http://riot.test",
            Username = "admin",
            Password = "wrong-password",
        };

        await using var session = new RiotSession(options, http);

        var ex = await Assert.ThrowsAsync<RiotApiException>(() => session.LoginAsync());

        Assert.Equal("2009", ex.BusinessCode);
        Assert.Equal(200, ex.StatusCode);
    }

    [Fact]
    public async Task AdminLogin_propagates_caller_cancellation()
    {
        using var cts = new CancellationTokenSource();
        cts.Cancel();
        using var http = new HttpClient(new CancellationHandler())
        {
            BaseAddress = new Uri("http://riot.test/"),
        };
        await using var session = new RiotSession(
            new RiotOptions
            {
                BaseUrl = "http://riot.test",
                Username = "admin",
                Password = "password",
            },
            http);

        await Assert.ThrowsAnyAsync<OperationCanceledException>(
            () => session.LoginAsync(cts.Token));
    }

    [Fact]
    public async Task AdminLogin_wraps_transport_timeout()
    {
        using var http = new HttpClient(new TimeoutHandler())
        {
            BaseAddress = new Uri("http://riot.test/"),
        };
        await using var session = new RiotSession(
            new RiotOptions
            {
                BaseUrl = "http://riot.test",
                Username = "admin",
                Password = "password",
            },
            http);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => session.LoginAsync());

        Assert.Contains("timed out", error.Message, StringComparison.Ordinal);
        Assert.IsAssignableFrom<OperationCanceledException>(error.InnerException);
    }

    [Theory]
    [InlineData(HttpStatusCode.TemporaryRedirect)]
    [InlineData(HttpStatusCode.PermanentRedirect)]
    public async Task StandaloneAuth_does_not_follow_redirect_or_replay_login(
        HttpStatusCode redirectStatus)
    {
        using var handler = new RedirectThenSuccessHandler(redirectStatus);
        using var auth = new RiotAuthClient(
            new RiotOptions
            {
                BaseUrl = "http://riot.test",
                Username = "admin",
                Password = "password",
            },
            (HttpMessageHandler)handler);

        RiotApiException error = await Assert.ThrowsAsync<RiotApiException>(
            () => auth.LoginAsync());

        Assert.Equal((int)redirectStatus, error.StatusCode);
        Assert.Equal(1, handler.CallCount);
    }

    private sealed class CancellationHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken) =>
            Task.FromCanceled<HttpResponseMessage>(cancellationToken);
    }

    private sealed class TimeoutHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken) =>
            Task.FromException<HttpResponseMessage>(new TaskCanceledException("simulated timeout"));
    }

    private sealed class RedirectThenSuccessHandler(
        HttpStatusCode redirectStatus) : HttpMessageHandler
    {
        public int CallCount { get; private set; }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            CallCount++;
            if (CallCount > 1)
            {
                return Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
                {
                    Content = new StringContent(
                        """{"code":"0","result":{"token":"abcdefghijklmnopqrstuvwxyz"}}""",
                        Encoding.UTF8,
                        "application/json"),
                });
            }

            var response = new HttpResponseMessage(redirectStatus)
            {
                Content = new StringContent("{}", Encoding.UTF8, "application/json"),
            };
            response.Headers.Location = new Uri("/must-not-follow", UriKind.Relative);
            return Task.FromResult(response);
        }
    }

    private sealed class FixedJsonHandler : HttpMessageHandler
    {
        private readonly HttpStatusCode _status;
        private readonly string _body;

        public FixedJsonHandler(HttpStatusCode status, string body)
        {
            _status = status;
            _body = body;
        }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            var response = new HttpResponseMessage(_status)
            {
                Content = new StringContent(_body, Encoding.UTF8, "application/json"),
            };
            return Task.FromResult(response);
        }
    }
}
