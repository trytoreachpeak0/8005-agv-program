namespace RIoT.Sdk.Core;

/// <summary>
/// Shared ADR-sdk-0005 helpers for Facade business envelopes (ResponseMsg code/message).
/// </summary>
public static class RiotBusinessResponse
{
    public static bool IsSuccessCode(string? code)
    {
        if (string.IsNullOrWhiteSpace(code))
        {
            return true;
        }

        var trimmed = code.Trim();
        return trimmed is "0" or "200" or "OK" or "ok" or "success" or "SUCCESS";
    }

    public static T RequireResponse<T>(T? response, string operation) where T : class
    {
        if (response is null)
        {
            throw new RiotApiException($"{operation} returned empty response.");
        }

        return response;
    }

    public static T RequireResult<T>(T? result, string operation, string businessCode)
        where T : struct
    {
        if (!result.HasValue)
        {
            throw new RiotApiException(
                $"{operation} returned null result.",
                businessCode: businessCode);
        }

        return result.Value;
    }

    public static void EnsureSuccess(string? code, string? message)
    {
        if (IsSuccessCode(code))
        {
            return;
        }

        throw new RiotApiException(
            $"RIoT business failure code={code} message={message}",
            statusCode: 200,
            businessCode: code);
    }
}
