using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Runtime.ExceptionServices;
using System.Text;
using FlaUI.Core;
using FlaUI.Core.AutomationElements;
using FlaUI.UIA3;
using MesIngest.Watch;
using FlaUIApplication = FlaUI.Core.Application;

namespace MesIngest.Watch.UiTests;

public sealed class WatchWindowJourneyTests
{
    private static readonly TimeSpan StepTimeout = TimeSpan.FromSeconds(12);

    [Theory]
    [InlineData("cold-start-overview")]
    [InlineData("visible-gone-paging-details")]
    [InlineData("alert-to-demand")]
    [InlineData("slow-request-cancel")]
    [InlineData("offline-reconnect")]
    [Trait("Category", "watch-ui-journeys")]
    [Trait("Category", "watch-window-visual")]
    public async Task Operator_completes_high_value_real_window_journey(string journeyName)
    {
        await RunJourneyAsync(journeyName);
    }

    [Fact]
    [Trait("Category", "watch-ticket11-previews")]
    public async Task Operator_can_review_all_four_production_pages_on_the_golden_desktop()
    {
        await RunJourneyAsync("ticket11-four-page-preview");
    }

    private static async Task RunJourneyAsync(string journeyName)
    {
        Assert.SkipUnless(
            string.Equals(
                Environment.GetEnvironmentVariable("MESINGEST_WATCH_RUN_REAL_WINDOWS"),
                "1",
                StringComparison.Ordinal),
            "Run through Invoke-WatchUiTests.ps1 so desktop checks and serial execution are enforced.");

        var cancellationToken = TestContext.Current.CancellationToken;
        var fixture = CreateFixture(journeyName);
        await using var host = await WatchWindowFakeHost.StartAsync(
            fixture.Scenario,
            ShouldUseDeterministicVisualInputs() ? "http://127.0.0.1:51542" : null,
            cancellationToken);
        var root = ResolveArtifactRoot();
        var testRoot = Path.Combine(root, "runtime", journeyName);
        var logDirectory = Path.Combine(testRoot, "logs");
        var localAppData = Path.Combine(testRoot, "local-app-data");
        Directory.CreateDirectory(logDirectory);
        Directory.CreateDirectory(localAppData);
        var evidence = new WatchJourneyEvidence(
            root,
            journeyName,
            fixture.SensitiveValues.Append("fake-window-secret"));
        // Match the launched Watch process before recording the auditable environment contract.
        // The child also receives MesIngestWatch__RenderingMode=SoftwareOnly below.
        System.Windows.Media.RenderOptions.ProcessRenderMode = System.Windows.Interop.RenderMode.SoftwareOnly;
        evidence.RecordEnvironment(FormatEnvironment(WatchVisualEnvironment.Capture()));

        var watchExecutable = ResolveWatchExecutable();
        var startInfo = new ProcessStartInfo
        {
            FileName = watchExecutable,
            WorkingDirectory = Path.GetDirectoryName(watchExecutable)!,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = false,
        };
        startInfo.Environment["LOCALAPPDATA"] = localAppData;
        startInfo.Environment["MesIngestWatch__BaseUrl"] = host.BaseUrl;
        startInfo.Environment["MesIngestWatch__SharedSecret"] = "fake-window-secret";
        startInfo.Environment["MesIngestWatch__RequestTimeoutSeconds"] = "30";
        startInfo.Environment["MesIngestWatch__RenderingMode"] = "SoftwareOnly";
        startInfo.Environment["MesIngestWatch__LogDirectory"] = logDirectory;
        if (ShouldUseDeterministicVisualInputs())
        {
            // Pixel journeys freeze display time and disable transient banner holds.
            // The separate UIA suite runs with the production clock and animations.
            startInfo.Environment["MESINGEST_WATCH_UI_TEST_MODE"] = "1";
            startInfo.Environment["MESINGEST_WATCH_UI_FIXED_UTC_NOW"] = "2026-08-08T01:30:00.0000000+00:00";
        }

        using var process = Process.Start(startInfo)
            ?? throw new Xunit.Sdk.XunitException("MesIngestWatch process did not start.");
        using var application = FlaUIApplication.Attach(process.Id);
        var stdout = process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderr = process.StandardError.ReadToEndAsync(cancellationToken);
        using var automation = new UIA3Automation();
        FlaUI.Core.AutomationElements.Window? window = null;
        Exception? failure = null;
        var failedStep = "launch";
        byte[]? finalCapture = null;

        try
        {
            window = application.GetMainWindow(automation, StepTimeout)
                ?? throw new Xunit.Sdk.XunitException("MesIngestWatch main window did not appear.");
            WatchWindowNative.SetClientSize(process.MainWindowHandle, 1440, 900);
            WaitUntil(
                () => FindById(window, "OverviewRefreshButton") is not null,
                "main window UIA tree",
                StepTimeout);
            RecordStep(evidence, window, "window-started");
            WaitUntil(
                () => FindById(window, "ErrorBannerText") is not { } error
                    || !DynamicText(error).Contains("Not ready", StringComparison.Ordinal),
                "initial projection to replace the startup placeholder",
                StepTimeout);

            failedStep = journeyName;
            switch (journeyName)
            {
                case "cold-start-overview":
                    RunColdStartOverview(window);
                    break;
                case "visible-gone-paging-details":
                    RunVisibleGonePaging(window);
                    break;
                case "alert-to-demand":
                    RunAlertToDemand(application, automation, window, fixture.PrimaryDemandId!);
                    break;
                case "slow-request-cancel":
                    RunSlowRequestCancel(window, fixture.PrimaryDemandId!);
                    break;
                case "offline-reconnect":
                    RunOfflineReconnect(window, host);
                    break;
                case "ticket11-four-page-preview":
                    RunTicket11FourPagePreview(
                        window,
                        evidence,
                        process.MainWindowHandle);
                    break;
                default:
                    throw new ArgumentOutOfRangeException(nameof(journeyName), journeyName, null);
            }

            NormalizeFinalVisualState(window);
            finalCapture = WatchWindowNative.CaptureClientArea(process.MainWindowHandle);
            evidence.RecordStep("final", finalCapture);
            evidence.RecordUiaTree(DumpUiaTree(window, automation));

            if (ShouldCompareWindowBaselines())
            {
                WatchWindowBaseline.Verify(journeyName, finalCapture, evidence);
            }
        }
        catch (Exception ex)
        {
            failure = ex;
            if (window is not null)
            {
                TryRecordFailureWindow(evidence, window, process.MainWindowHandle, automation);
            }
        }
        finally
        {
            if (!process.HasExited && window is not null)
            {
                try
                {
                    window.Close();
                }
                catch (Exception)
                {
                    // WaitForExitAsync below is the authoritative bounded cleanup.
                }
            }

            await WaitForExitAsync(process, cancellationToken);
            evidence.RecordProcessOutput(await stdout, await stderr);
            evidence.RecordFakeHostTimeline(host.Timeline, host.TimelineSummary);
            evidence.RecordWatchLogs(logDirectory);
        }

        if (failure is not null)
        {
            evidence.RecordFailure(failedStep, failure, StepTimeout);
            ExceptionDispatchInfo.Capture(failure).Throw();
        }
    }

    private static void RunColdStartOverview(FlaUI.Core.AutomationElements.Window window)
    {
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "OverviewConclusionText"))
                .Contains("健康", StringComparison.Ordinal),
            "healthy cold-start overview",
            StepTimeout);
        WaitUntil(
            () => FindById(window, "ErrorBannerText") is null,
            "cold-start error banner cleared",
            StepTimeout);
        Assert.Contains(
            "已连接",
            DynamicText(FindRequiredById(window, "OverviewHostText")),
            StringComparison.Ordinal);
        Assert.Contains(
            "SUCCESS",
            DynamicText(FindRequiredById(window, "OverviewPollHealthText")),
            StringComparison.Ordinal);
    }

    private static void RunTicket11FourPagePreview(
        FlaUI.Core.AutomationElements.Window window,
        WatchJourneyEvidence evidence,
        IntPtr handle)
    {
        RunColdStartOverview(window);
        evidence.RecordStep("preview-overview", WatchWindowNative.CaptureClientArea(handle));

        var navigation = FindRequiredById(window, "PrimaryNavigation").AsListBox();
        navigation.Select(1);
        var demandGrid = FindRequiredById(window, "DemandsGrid").AsGrid();
        WaitUntil(() => demandGrid.Rows.Length > 0, "Demand preview rows", StepTimeout);
        demandGrid.Select(0);
        evidence.RecordStep("preview-demand", WatchWindowNative.CaptureClientArea(handle));

        navigation.Select(2);
        var alertGrid = FindRequiredById(window, "AlertsGrid").AsGrid();
        WaitUntil(() => alertGrid.Rows.Length > 0, "Alert preview rows", StepTimeout);
        alertGrid.Select(0);
        evidence.RecordStep("preview-alert", WatchWindowNative.CaptureClientArea(handle));

        navigation.Select(3);
        WaitUntil(
            () => FindRequiredById(window, "ApplyHostButton").Properties.IsOffscreen.ValueOrDefault == false,
            "Settings preview",
            StepTimeout);
        evidence.RecordStep("preview-settings", WatchWindowNative.CaptureClientArea(handle));

        navigation.Select(0);
        RunColdStartOverview(window);
    }

    private static void RunVisibleGonePaging(FlaUI.Core.AutomationElements.Window window)
    {
        FindRequiredById(window, "PrimaryNavigation").AsListBox().Select(1);
        var grid = FindRequiredById(window, "DemandsGrid").AsGrid();
        WaitUntil(() => grid.Rows.Length == 1, "VISIBLE first page", StepTimeout);
        grid.Select(0);
        Assert.False(FindRequiredById(window, "DemandDetailsPanel").Properties.IsOffscreen.ValueOrDefault);

        var next = FindRequiredById(window, "DemandNextButton").AsButton();
        WaitUntil(() => next.IsEnabled, "VISIBLE next page enabled", StepTimeout);
        next.Invoke();
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "DemandPageText"))
                .Contains("第 2 页", StringComparison.Ordinal),
            "VISIBLE second page",
            StepTimeout);
        grid.Select(0);

        FindRequiredById(window, "DemandStatusTabs").AsTab().SelectTabItem(1);
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "DemandModeText"))
                .Contains("GONE", StringComparison.Ordinal),
            "GONE independent view",
            StepTimeout);
        WaitUntil(() => grid.Rows.Length == 1, "GONE page", StepTimeout);
        grid.Select(0);
        Assert.False(FindRequiredById(window, "DemandDetailsPanel").Properties.IsOffscreen.ValueOrDefault);
    }

    private static void RunAlertToDemand(
        FlaUIApplication application,
        UIA3Automation automation,
        FlaUI.Core.AutomationElements.Window mainWindow,
        string expectedDemandId)
    {
        FindRequiredById(mainWindow, "PrimaryNavigation").AsListBox().Select(2);
        var alertGrid = FindRequiredById(mainWindow, "AlertsGrid").AsGrid();
        WaitUntil(() => alertGrid.Rows.Length == 1, "active IngestAlert page", StepTimeout);
        alertGrid.Select(0);
        FindRequiredById(mainWindow, "AlertDetailsButton").AsButton().Invoke();

        AutomationElement? locateButton = null;
        WaitUntil(
            () =>
            {
                locateButton = automation.GetDesktop().FindFirstDescendant(
                    automation.ConditionFactory.ByAutomationId("LocateDemandButton"));
                return locateButton is not null;
            },
            "IngestAlert detail window",
            StepTimeout);
        var detailWindow = FindOwningWindow(locateButton!, automation);
        locateButton!.AsButton().Invoke();

        var demandGrid = FindRequiredById(mainWindow, "DemandsGrid").AsGrid();
        WaitUntil(
            () => demandGrid.Rows.Any(row =>
                string.Equals(row.Name, expectedDemandId, StringComparison.Ordinal)),
            "exact Alert to TransportDemand navigation",
            StepTimeout);
        detailWindow!.Close();
        WaitUntil(
            () => FindRequiredById(mainWindow, "DemandDetailsPanel")
                .Properties.IsOffscreen.ValueOrDefault == false,
            "located TransportDemand details",
            StepTimeout);
    }

    private static void RunSlowRequestCancel(
        FlaUI.Core.AutomationElements.Window window,
        string expectedDemandId)
    {
        FindRequiredById(window, "PrimaryNavigation").AsListBox().Select(1);
        var grid = FindRequiredById(window, "DemandsGrid").AsGrid();
        WaitUntil(
            () => grid.Rows.Any(row => string.Equals(row.Name, expectedDemandId, StringComparison.Ordinal)),
            "initial VISIBLE result",
            StepTimeout);
        FindRequiredById(window, "DemandRefreshButton").AsButton().Invoke();
        var cancel = FindRequiredById(window, "DemandCancelButton").AsButton();
        WaitUntil(() => cancel.IsEnabled, "slow refresh cancellation affordance", StepTimeout);
        cancel.Invoke();
        WaitUntil(() => !cancel.IsEnabled, "slow refresh canceled", StepTimeout);
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "DemandNoticeText"))
                .Contains("取消", StringComparison.Ordinal),
            "cancellation result notice",
            StepTimeout);
        WaitUntil(
            () => FindById(window, "ErrorBannerText") is null,
            "user cancellation not to become a Host error",
            StepTimeout);
        Assert.Contains(
            grid.Rows,
            row => string.Equals(row.Name, expectedDemandId, StringComparison.Ordinal));
    }

    private static void NormalizeFinalVisualState(
        FlaUI.Core.AutomationElements.Window window)
    {
        var focusTarget = new[]
            {
                "OverviewRefreshButton",
                "DemandRefreshButton",
                "AlertRefreshButton",
            }
            .Select(id => FindById(window, id))
            .FirstOrDefault(element => element is not null
                && element.Properties.IsEnabled.ValueOrDefault
                && !element.Properties.IsOffscreen.ValueOrDefault)
            ?? throw new Xunit.Sdk.XunitException(
                "The current Watch view has no visible refresh button for canonical screenshot focus.");

        focusTarget.Focus();
        WaitUntil(
            () => focusTarget.Properties.HasKeyboardFocus.ValueOrDefault,
            "canonical final screenshot focus",
            StepTimeout);
        WatchWindowNative.MovePointerOffWindow();
        Thread.Sleep(250);
    }

    private static void RunOfflineReconnect(
        FlaUI.Core.AutomationElements.Window window,
        WatchWindowFakeHost host)
    {
        RunColdStartOverview(window);
        host.SetOnline(false);
        FindRequiredById(window, "OverviewRefreshButton").AsButton().Invoke();
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "ErrorBannerText"))
                .Contains("503", StringComparison.Ordinal),
            "offline error banner",
            StepTimeout);

        host.SetOnline(true);
        var refresh = FindRequiredById(window, "OverviewRefreshButton").AsButton();
        WaitUntil(() => refresh.IsEnabled, "offline refresh completed", StepTimeout);
        refresh.Invoke();
        WaitUntil(
            () => DynamicText(FindRequiredById(window, "OverviewConclusionText"))
                .Contains("健康", StringComparison.Ordinal),
            "reconnected healthy overview",
            StepTimeout);
        WaitUntil(
            () => FindById(window, "ErrorBannerText") is null,
            "recovered connection banner cleared",
            StepTimeout);
    }

    private static WatchWindowJourneyFixture CreateFixture(string journeyName)
    {
        var first = WatchWindowScenarioData.VisibleDemand("dmd-7f91c2a8") with
        {
            TaskType = "DIE_TO_WIRE_STAGING",
            Sublot = "Q26063201-2",
            Area = "C6-12",
            Eqp = "3ZPS122",
        };
        var second = WatchWindowScenarioData.VisibleDemand("dmd-2a10bd44") with
        {
            TaskType = "DIE_TO_OVEN",
            Sublot = "Q26063224-8",
            Area = "C6-14",
            Eqp = "3ZPS136",
        };
        var third = WatchWindowScenarioData.VisibleDemand("dmd-7d3e4b91") with
        {
            TaskType = "WIRE_TO_GATE",
            Sublot = "Q26063189-5",
            Area = "B4-09",
            Eqp = "WB-031",
        };
        var fourth = WatchWindowScenarioData.VisibleDemand("dmd-a773ed12") with
        {
            TaskType = "WIRE_TO_OPTICAL",
            Sublot = "Q26063177-3",
            Area = "A3-18",
            Eqp = "WB-114",
        };
        var gone = WatchWindowScenarioData.GoneDemand("journey-gone-001");
        var alert = WatchWindowScenarioData.ActiveAlert("journey-alert-001", first.DemandId);
        var fieldDrift = alert with
        {
            AlertId = "alert-field-drift",
            TaskType = first.TaskType,
            Sublot = first.Sublot,
            Message = "冻结字段 EQP 与当前快照不一致。",
        };
        var duplicate = alert with
        {
            AlertId = "alert-duplicate-key",
            Code = "DUPLICATE_RECONCILE_KEY",
            TaskType = first.TaskType,
            Sublot = first.Sublot,
            DemandId = null,
            Message = "同一 TASK_TYPE + SUBLOT 在快照中重复。",
            Details = "{\"rows\":2}",
            OccurrenceCount = 4,
        };
        first = first with { Alerts = [fieldDrift, duplicate] };
        var reappear = alert with
        {
            AlertId = "alert-reappear",
            Code = "REAPPEAR_AFTER_GONE",
            Severity = "WARNING",
            TaskType = second.TaskType,
            Sublot = second.Sublot,
            DemandId = second.DemandId,
            Message = "同一业务键在 GONE 后再次出现，系统创建了新的 DemandId。",
            Details = $"{{\"previousDemandId\":\"dmd-old-116a\",\"newDemandId\":\"{second.DemandId}\"}}",
            OccurrenceCount = 1,
        };
        var paused = alert with
        {
            AlertId = "alert-paused-zero",
            Code = "PAUSED_ZERO_DROP",
            TaskType = "STAGING_TO_WIRE",
            Sublot = null,
            DemandId = null,
            Message = "该任务类型从健康非零基线骤降为零。",
        };
        var pollFailure = alert with
        {
            AlertId = "alert-poll-failure",
            Code = "POLL_FAILURE",
            TaskType = null,
            Sublot = null,
            DemandId = null,
            Message = "MES 快照读取失败。",
            OccurrenceCount = 3,
        };
        var visibleFirstPage = new WatchDemandPage([first, second, third, fourth], "journey-visible-cursor", true);
        var visibleSecondPage = new WatchDemandPage([second], null, false);
        var gonePage = new WatchDemandPage([gone], null, false);

        var scenario = journeyName switch
        {
            "visible-gone-paging-details" => WatchWindowScenario.Scripted(
                [
                    new WatchWindowHttpReply<WatchDemandPage>(visibleFirstPage),
                    new WatchWindowHttpReply<WatchDemandPage>(visibleFirstPage),
                    new WatchWindowHttpReply<WatchDemandPage>(visibleSecondPage),
                ],
                [new WatchWindowHttpReply<WatchDemandPage>(gonePage)],
                [new WatchWindowHttpReply<WatchAlertPage>(new WatchAlertPage([], null, false))]),
            "slow-request-cancel" => WatchWindowScenario.Scripted(
                [
                    new WatchWindowHttpReply<WatchDemandPage>(new WatchDemandPage([first], null, false)),
                    new WatchWindowHttpReply<WatchDemandPage>(new WatchDemandPage([first], null, false)),
                    new WatchWindowHttpReply<WatchDemandPage>(
                        new WatchDemandPage([second], null, false),
                        TimeSpan.FromSeconds(30)),
                ],
                [new WatchWindowHttpReply<WatchDemandPage>(gonePage)],
                [new WatchWindowHttpReply<WatchAlertPage>(new WatchAlertPage([], null, false))]),
            "alert-to-demand" => WatchWindowScenario.Healthy(
                visiblePages: [new WatchDemandPage([first], null, false)],
                gonePages: [gonePage],
                alerts: [alert]),
            "ticket11-four-page-preview" => WatchWindowScenario.Scripted(
                [new WatchWindowHttpReply<WatchDemandPage>(new WatchDemandPage([first, second, third, fourth], null, false))],
                [new WatchWindowHttpReply<WatchDemandPage>(gonePage)],
                [
                    new WatchWindowHttpReply<WatchAlertPage>(new WatchAlertPage([], null, false)),
                    new WatchWindowHttpReply<WatchAlertPage>(new WatchAlertPage([reappear, duplicate, paused, pollFailure], null, false)),
                    new WatchWindowHttpReply<WatchAlertPage>(new WatchAlertPage([], null, false)),
                ]),
            _ => WatchWindowScenario.Healthy(
                visiblePages: [new WatchDemandPage([first], null, false)],
                gonePages: [gonePage],
                alerts: []),
        };

        return new WatchWindowJourneyFixture(
            scenario,
            first.DemandId,
            [first.DemandId, second.DemandId, gone.DemandId, alert.AlertId!, "journey-visible-cursor"]);
    }

    private static AutomationElement FindRequiredById(
        FlaUI.Core.AutomationElements.Window window,
        string automationId) =>
        FindById(window, automationId)
        ?? throw new Xunit.Sdk.XunitException($"UIA element not found: {automationId}");

    private static AutomationElement? FindById(
        FlaUI.Core.AutomationElements.Window window,
        string automationId) =>
        window.FindFirstDescendant(window.ConditionFactory.ByAutomationId(automationId));

    private static string DynamicText(AutomationElement element) => string.Join(
        Environment.NewLine,
        element.Properties.HelpText.ValueOrDefault ?? string.Empty,
        element.Properties.ItemStatus.ValueOrDefault ?? string.Empty);

    private static void WaitUntil(Func<bool> condition, string description, TimeSpan timeout)
    {
        var stopwatch = Stopwatch.StartNew();
        Exception? lastException = null;
        while (stopwatch.Elapsed < timeout)
        {
            try
            {
                if (condition())
                {
                    return;
                }
            }
            catch (Exception ex)
            {
                lastException = ex;
            }

            Thread.Sleep(100);
        }

        throw new Xunit.Sdk.XunitException(
            lastException is null
                ? $"Timed out after {timeout.TotalSeconds:0.#}s waiting for {description}."
                : $"Timed out after {timeout.TotalSeconds:0.#}s waiting for {description}. Last error: {lastException.Message}");
    }

    private static void RecordStep(
        WatchJourneyEvidence evidence,
        FlaUI.Core.AutomationElements.Window window,
        string step)
    {
        var path = Path.Combine(evidence.DirectoryPath, $"{step}.capture.png");
        window.CaptureToFile(path);
        evidence.RecordStep(step, File.ReadAllBytes(path));
        File.Delete(path);
    }

    private static void TryRecordFailureWindow(
        WatchJourneyEvidence evidence,
        FlaUI.Core.AutomationElements.Window window,
        IntPtr handle,
        UIA3Automation automation)
    {
        try
        {
            evidence.RecordStep("failure", WatchWindowNative.CaptureClientArea(handle));
        }
        catch (Exception captureFailure)
        {
            evidence.RecordUiaTree($"Screenshot capture failed: {captureFailure.Message}");
        }

        try
        {
            evidence.RecordUiaTree(DumpUiaTree(window, automation));
        }
        catch (Exception treeFailure)
        {
            evidence.RecordUiaTree($"UIA tree capture failed: {treeFailure.Message}");
        }
    }

    private static string DumpUiaTree(
        AutomationElement root,
        UIA3Automation automation)
    {
        var output = new StringBuilder();
        var walker = automation.TreeWalkerFactory.GetControlViewWalker();
        var remaining = 5000;

        void Append(AutomationElement element, int depth)
        {
            if (remaining-- <= 0)
            {
                output.AppendLine("... UIA tree truncated at 5000 elements ...");
                return;
            }

            output.Append(' ', depth * 2)
                .Append(SafeProperty(() => element.ControlType.ToString()))
                .Append(" id=").Append(SafeProperty(() => element.Properties.AutomationId.ValueOrDefault))
                .Append(" name=").Append(SafeProperty(() => element.Properties.Name.ValueOrDefault))
                .Append(" help=").Append(SafeProperty(() => element.Properties.HelpText.ValueOrDefault))
                .Append(" itemStatus=").Append(SafeProperty(() => element.Properties.ItemStatus.ValueOrDefault))
                .Append(" enabled=").Append(SafeProperty(() => element.Properties.IsEnabled.ValueOrDefault.ToString()))
                .AppendLine();
            var child = walker.GetFirstChild(element);
            while (child is not null && remaining > 0)
            {
                Append(child, depth + 1);
                child = walker.GetNextSibling(child);
            }
        }

        Append(root, 0);
        return output.ToString();
    }

    private static FlaUI.Core.AutomationElements.Window FindOwningWindow(
        AutomationElement element,
        UIA3Automation automation)
    {
        var walker = automation.TreeWalkerFactory.GetControlViewWalker();
        AutomationElement? current = element;
        while (current is not null)
        {
            if (current.ControlType == FlaUI.Core.Definitions.ControlType.Window)
            {
                return current.AsWindow();
            }

            current = walker.GetParent(current);
        }

        throw new Xunit.Sdk.XunitException("LocateDemandButton has no UIA Window ancestor.");
    }

    private static string? SafeProperty(Func<string?> read)
    {
        try
        {
            return read();
        }
        catch (Exception ex)
        {
            return $"(unsupported:{ex.GetType().Name})";
        }
    }

    private static async Task WaitForExitAsync(Process process, CancellationToken cancellationToken)
    {
        if (!process.HasExited)
        {
            try
            {
                await process.WaitForExitAsync(cancellationToken).WaitAsync(TimeSpan.FromSeconds(5), cancellationToken);
            }
            catch (TimeoutException)
            {
                process.Kill(entireProcessTree: true);
                await process.WaitForExitAsync(cancellationToken);
            }
        }
    }

    private static bool ShouldCompareWindowBaselines() => string.Equals(
        Environment.GetEnvironmentVariable("MESINGEST_WATCH_COMPARE_WINDOW_BASELINES"),
        "1",
        StringComparison.Ordinal);

    private static bool ShouldUseDeterministicVisualInputs() =>
        ShouldCompareWindowBaselines()
        || string.Equals(
            Environment.GetEnvironmentVariable("MESINGEST_WATCH_CAPTURE_WINDOW_CANDIDATES"),
            "1",
            StringComparison.Ordinal);

    private static string ResolveArtifactRoot()
    {
        var configured = Environment.GetEnvironmentVariable("MESINGEST_WATCH_UI_ARTIFACTS");
        if (!string.IsNullOrWhiteSpace(configured))
        {
            Directory.CreateDirectory(configured);
            return Path.GetFullPath(configured);
        }

        var root = Path.Combine(Path.GetTempPath(), $"watch-window-ui-{Guid.NewGuid():N}");
        Directory.CreateDirectory(root);
        return root;
    }

    private static string ResolveWatchExecutable()
    {
        var configured = Environment.GetEnvironmentVariable("MESINGEST_WATCH_EXECUTABLE");
        if (!string.IsNullOrWhiteSpace(configured))
        {
            var explicitPath = Path.GetFullPath(configured);
            if (!File.Exists(explicitPath))
            {
                throw new FileNotFoundException("Configured Watch executable does not exist.", explicitPath);
            }

            return explicitPath;
        }

        var targetDirectory = new DirectoryInfo(AppContext.BaseDirectory);
        var configuration = targetDirectory.Parent?.Name
            ?? throw new InvalidOperationException("Cannot resolve UI test configuration directory.");
        var csharpDirectory = targetDirectory.Parent?.Parent?.Parent?.Parent
            ?? throw new InvalidOperationException("Cannot resolve MesIngest csharp directory.");
        var path = Path.Combine(
            csharpDirectory.FullName,
            "MesIngest.Watch",
            "bin",
            configuration,
            "net8.0-windows",
            "MesIngest.Watch.exe");
        if (!File.Exists(path))
        {
            throw new FileNotFoundException(
                "Build MesIngest.Watch before running real-window journeys.",
                path);
        }

        return path;
    }

    private static string FormatEnvironment(WatchVisualEnvironmentSnapshot snapshot) => string.Join(
        Environment.NewLine,
        $"interactive={snapshot.HasInteractiveInputDesktop}",
        $"desktop={snapshot.DesktopWidth}x{snapshot.DesktopHeight}",
        $"dpi={snapshot.Dpi}",
        $"scale={snapshot.Dpi / 96d:P0}",
        $"lightTheme={snapshot.AppsUseLightTheme}",
        $"culture={snapshot.CultureName}",
        $"uiCulture={snapshot.UiCultureName}",
        $"timezone={snapshot.TimeZoneId}",
        $"rendering={snapshot.RenderingMode}",
        $"framework={Environment.Version}",
        $"os={Environment.OSVersion}",
        $"processArchitecture={System.Runtime.InteropServices.RuntimeInformation.ProcessArchitecture}");

    private sealed record WatchWindowJourneyFixture(
        WatchWindowScenario Scenario,
        string? PrimaryDemandId,
        IReadOnlyList<string> SensitiveValues);
}
