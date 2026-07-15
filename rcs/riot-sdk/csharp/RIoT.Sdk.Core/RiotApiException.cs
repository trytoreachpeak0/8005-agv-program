namespace RIoT.Sdk.Core;

/// <summary>
/// Raised when a RIoT HTTP call fails or returns a non-success business code.
/// </summary>
public sealed class RiotApiException : Exception
{
    public int? StatusCode { get; }
    public string? BusinessCode { get; }
    public string? ResponseBody { get; }

    public RiotApiException(
        string message,
        int? statusCode = null,
        string? businessCode = null,
        string? responseBody = null,
        Exception? innerException = null)
        : base(message, innerException)
    {
        StatusCode = statusCode;
        BusinessCode = businessCode;
        ResponseBody = responseBody;
    }
}
