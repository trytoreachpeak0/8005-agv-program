namespace RIoT.Sdk.Facade;

/// <summary>
/// Thin task-module facade. Expose additional endpoints as needed.
/// </summary>
public sealed class TaskClient
{
    private readonly RiotSession _session;

    internal TaskClient(RiotSession session) => _session = session;

    /// <summary>
    /// Access the underlying Kiota client for endpoints not yet wrapped.
    /// Prefer adding explicit facade methods for commonly used calls.
    /// </summary>
    public RIoT.Sdk.Generated.TaskApi.TaskClient Raw => _session.CreateGeneratedTaskClient();
}
