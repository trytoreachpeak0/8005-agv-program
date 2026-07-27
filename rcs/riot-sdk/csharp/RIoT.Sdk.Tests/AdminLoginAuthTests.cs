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
