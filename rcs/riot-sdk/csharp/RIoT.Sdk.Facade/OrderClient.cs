namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin order-module facade. Expose additional endpoints as needed.
/// </summary>
public sealed class OrderClient
{
    private readonly RiotSession _session;

    internal OrderClient(RiotSession session) => _session = session;

    /// <summary>
    /// Access the underlying Kiota client for endpoints not yet wrapped.
    /// </summary>
    public RIoT.Sdk.Generated.Order.OrderClient Raw => _session.CreateGeneratedOrderClient();
}
