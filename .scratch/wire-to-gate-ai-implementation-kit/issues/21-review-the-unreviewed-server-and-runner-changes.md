# 复核尚未经过审查的服务端现场修复与发布/runner 改动

Type: task
Mode: AFK
Status: resolved
Blocked by: 11

## Question

服务端自 `ea8dc98` 起的五处现场修复（至 `3d8b00c`）、票据 18／19／20／10 的五轮 runner 改动
（`938eb67`～`acc8a6d`），以及票据 11 的发布与安装脚本改动（`b9c7988`～`ee54988`），至今没有经过
一次 Standards + Spec 复核。在授权正式发布之前，这些改动是否符合本仓已记录的编码标准，并且是否
与各自票据的验收条件一致？

复核对象与判据：

- 范围是 ControlServer 仓 `ControlServer_MVP` 上 `ea8dc98..ee54988` 的全部改动，按「产品代码」
  与「脚本／证据」分别给结论；
- Standards 轴对照本仓 `CONTEXT.md`、accepted ADR 与既有代码惯例；
- Spec 轴对照票据 18／19／20／10／11 各自的 `## Answer` 与它们声称的验收条件；
- 任何被判为缺陷的项，必须给出「会在什么输入下出错」的具体失败场景，而不是风格意见；
- 复核本身不改产品代码；需要修的项若触及产品代码，按测试分层规则单独走 tier 1。

本票不覆盖车载端仓与协议仓：前者对 agent 只读，后者为审批门禁。

## Answer

两轴复核已完成，`ea8dc98..ee54988` 共 31 个 commit。**发现两个真产品代码缺陷**，均未被任何票
的验收条件覆盖，也未被 tier 1 保护；此外脚本／证据层有五项应记录的偏差。复核为只读，未改动
任何仓库文件。

判为缺陷的两条都给出了单点失败场景，并已由本会话独立核实（不采信子 agent 自报）。

### 真缺陷一：`worklistRevision` 从不持久化，第二趟 demand 必然复发 `3d8b00c` 刚修掉的故障

ADR-cross-0048 的原文是「worklistRevision 针对当前 AGV 与站点单调递增**并由服务端持久化**」。
实际实现不满足后半句：

| 事实 | 位置 |
| --- | --- |
| 唯一写入点，恒为 `1` | `WireToGateStore.cs:1811`（`ToRuntimeRow`） |
| 全仓无任何 `runtime.WorklistRevision = ` 写回 | `grep -rn "WorklistRevision" src/ tests/` |
| gate 的 `+ 1` 是读时算的，不落库 | `JourneyRuntimeEngine.cs:711` |
| runtime 行按 `DemandId` 查找／创建，新 demand 即新行 | `WireToGateStore.cs:235,288` |

`3d8b00c` 只修了**单趟内**pickup 与 gate 撞同一 revision 的问题。跨趟未修：车辆租约以
`VehicleKey` + `ReleasedAt == null` 排他，完整安全卸货后释放，**同一台车接第二趟 demand 是设计
内的正常路径**，而新 runtime 行把 revision 重置回 1。

失败场景：同一 AGV 完成 demand A（pickup rev=1、gate rev=2）后接 demand B，B 的 pickup 快照
再次以 rev=1 发出，内容却是新 demand 的 items。按 ADR-0048 的「相同 revision 幂等 ACK，更低
revision 丢弃」，两种 key 方式下 B 的清单都到不了车载端——按 (station, revision) 是幂等 ACK
（操作员在 pickup 站看到上一趟的清单），按 `3d8b00c` 注释所述的车载实际行为
（`the peer keys a snapshot's identity on its type and revision`）是 rev=1 < 已采用的 gate rev=2
被丢弃；而若车载按同注释「同 revision 内容变更即拒绝」处理，则**原样重演 `3d8b00c` 的连接被拆**。

现场未暴露，只因为 `20260829-closed-loop-gen3` 那次授权闭环只跑了一趟。

**一处诚实的未知**：车载端是否在会话间重置已采用 revision，决定这条是「第二趟必然复发」还是
「跨重连侥幸绕过」。车载端仓对 agent 只读，无法确证，需王昆确认或由一次双 demand 运行证伪。
修复方案的选择依赖该答案，因此不在本票内定方案。

### 真缺陷二：`f48e616` 的四处 settle 只有两处有回归保护

`f48e616` 在 `JourneyRuntimeEngine.cs` 加了四处 `SettleAnsweredCommandAsync`（行 395／409／
455／492）。唯一相关测试 `CommandsAnsweredByABusinessResultAreNotLeftPendingForReplay` 停在
`AwaitingDepartureSafety`，只断言前两处（`SublotEntryRequested`、load `SlotOperationCommand`），
并且**主动断言** `Assert.Contains("PreDepartureSafetyCheck", stillPending)`。

全仓 `ProtocolOutbox` 断言点已逐一排查（`grep -n "ProtocolOutbox" tests/ControlServer.Tests/*.cs`）：
没有任何测试断言行 455（`PreDepartureSafetyCheck`）或行 492（unload `SlotOperationCommand`）被
settle。走到那两处之后的测试
（`DepartureSafetyAnsweredPromptlyIsJudgedWhileItIsStillValid`、`RunToGateUnloadAsync` 的调用者）
只断言 stage、`BlockReasonCode`、intent status 与 worklist revision，不看 outbox。

失败场景：删除行 455 的 settle 调用，tier 1 全绿——而这恰恰是该 commit message 自述的现场故障
本体（`every reconnect was torn down by a safety check the journey had already obeyed and moved
past -- thirty-one generations in four minutes`）。该分支目前零回归保护。

### 三处现场 fix 合格

- `12eddf2` + `31569f5` 由 `DepartureSafetyAnsweredPromptlyIsJudgedWhileItIsStillValid` 同时锚住：
  `validUntil = answeredAt.AddSeconds(2)` 短于 poll interval，且 correlationId 用
  `preDepartureSafetyCheckId`，回退任一均变红——真锚在缺陷上，不是锚在实现细节上。
- `3d8b00c` 由 `EachStopPublishesItsWorklistUnderItsOwnRevision` 锚住：把 gate 改回
  `runtime.WorklistRevision` 即 `Distinct().Count()` 从 2 变 1 → 红。（它锚住的是单趟内那一半；
  跨趟那一半即真缺陷一。）
- `fa03e06` 纯证据文档，无代码改动。

### 脚本与证据层的五项偏差（均不需 tier 1）

1. **票 20 仍留一个等价漂移口。** 该票 Answer 自述「本票脚本不接受 commit 参数覆盖——留了覆盖口
   就等于留了漂移口」，但 `run-staged-g3-restart.ps1` 的 `param()` 保留
   `[string]$CommitBindingSource = (Join-Path $PSScriptRoot 'run-staged-g3.ps1')`，注释还写着
   `the two can never drift apart`。失败场景：`-CommitBindingSource <一份带旧 commit 的脚本副本>`
   即可让整轮证据宣称错误绑定而不报错。缓解项存在：`configuration.json` 记了源路径与其 SHA-256，
   事后可审计。`Get-SharedCommitBinding` 本身属实——确用 `[Parser]::ParseFile` 取四个
   `StringConstantExpressionAst` 默认值，且以 `-cnotmatch` 大小写敏感校验。
2. **票 11 的「二十六条断言」没有机器可读记录。** 它们只是 `SUMMARY.md` 里的 markdown 表格；
   `install-result.json` 只有 9 条 `checks` 字符串，第 1–6、19–26 条无任何机器可读落点。这与
   18／19／20 三票的 `assertions` 数组做法不一致，是本轮唯一一处证据格式回退。
3. **票 11 的证据目录缺关键产物。** Question 明确要求「必须执行秘密扫描、依赖／许可证清单和发布物
   哈希」，但 `evidence/rc/` 下没有归档 `release-manifest.json`、`SHA256SUMS.txt`、
   `inventory/dependencies-*.json`、`secret-scan.json`，只有两个根哈希写在 SUMMARY 正文。失败场景：
   要复核该票 findings #3（三个 RIoT 包无许可证元数据）或第 26 条扫描结论时，仓内无任何可查产物。
4. **`New-WireToGateReleaseCandidate.ps1` 的扫描结果不设闸。** `buildWarnings != 0` 硬失败，但
   `secretScan.totalFindingCount` 与 `unresolvedLicenseCount` 只写进 JSON。失败场景：源码含
   `"apiKey": "…"` 时脚本仍 PASS 出包。另 `Get-PackageLicense` 硬编码
   `$env:USERPROFILE\.nuget\packages`，设了 `NUGET_PACKAGES` 的机器上许可清单会全 UNRESOLVED 而
   照常出包。
5. **三个 runner 脚本逐字复制公共函数。** `Invoke-LoggedCommand`、`Get-Sha256Text`、
   `Wait-HttpJson`、`Stop-ProcessSafely`、`Invoke-SqliteRows` 在 `run-staged-g3.ps1` /
   `-restart.ps1` / `run-demand-bearing-g3-vectors.ps1` 间内容相同。而
   `run-demand-bearing-g3-vectors.ps1` 不抽公共模块，改用 AST 抓取另一脚本的函数体与 here-string。
   失败场景：重命名 `Get-SharedCommitBinding`、或把 harness here-string 从 `@'…'@` 改成 `@"…"@`
   （token 类型变 Expandable），该脚本启动即抛错。

### 三票的范围偏差，均为已披露而非隐瞒

- **票 18 无缺陷。** 12 条断言真实对应，四种动作在 `run-staged-g3.ps1:2157` 的 switch 中全部实现
  且各被真实触发，原七条基线不回归。其 `## 范围` 原写覆盖 `OperationResult`／
  `SlotOperationCommand`，Answer 改成另四种消息并把这两种写进 `businessProbe.coverageLimits`。
- **票 19 为已披露的部分完成。** 范围原文「在仓位操作进行中断开连接，断言服务端把操作与 Demand
  转入 `RecoveryRequired` 而非误报完成，物理事实不被提交，车辆租约不释放」这三条子断言一条未做，
  改由 `ForcedMechanicalRecoveryCommand` 的 drop-and-close 替代，已写入
  `recoveryProbe.coverageLimits.DisconnectDuringSlotOperation`。
- **票 20 的「规划仓不再保留副本」未严格达成**：
  `.scratch/…/20260826-staged-no-movement-cc6e2b9-0455147/runner.ps1` 仍是 284 行可执行、绑定
  `cc6e2b9`／`0455147` 的脚本。该票 Answer 已具名披露，仍需另开一票处理（与本轮无关）。
- **票 10 的四条 `riot*` 断言不是对被测构建的观测**：它们读的是恢复自
  `fullloop-20260829T131549Z` 库中**已存在**的 `RiotDispatchAuditEvents` 行，写这些行的构建早于
  `3d8b00c`，而本轮 `riotBaseUrl: http://127.0.0.1:1`、`riotCreateDispatchEnabled: false`。
  SUMMARY 与 `storeProvenance` 已写明，但该票 Answer 的「八类向量集齐」表未在那一行重复限定。
  「产品代码保持 `3d8b00c`」属实：`git diff 3d8b00c...ee54988 -- src/ tests/` 为空。

### 无违规的部分

- `evidence/`、`docs/` 已扫描：无明文密码、API key 或凭据落库，`credentialProof` 均为 `[REDACTED]`。
- 脚本未向两个只读仓写入；车载端仅一次性抛弃式 clone，符合 AGENTS.md 的保护仓规则。
- `Install-ControlServerLocal.ps1` 把 `-InstallCurrentUserRoot` 从强制改为可选、改用 `--cacert`
  钉住本次安装生成的根证书，回滚按 `$machineEnvironmentInjected` 收敛——无异议。
- 票 11「协议身份从产物读回而非重述」属实：`$protocol = $publishedSettings.ProtocolCandidate`
  源自 `$controlServerPackage/appsettings.json`，非 `APPROVED_RELEASE` 即 throw，
  `identitySource` 写入 manifest。
- `WireToGateStore.SettleAnsweredCommandAsync` 幂等、职责单一，符合本仓先落库再对外副作用的顺序。
  它不校验 `MessageType`／contentHash 且 `row is null` 时静默返回，是 judgement call 而非缺陷
  （传错 messageId 不报错，症状退化为线上重放）。
- `AwaitSafeDepartureResultAsync` 以尝试计数而非时钟设界，绕开注入的 `TimeProvider`；生产侧单次
  迭代因此最长阻塞 1.5 s，配合 `goto case` 跨阶段跳转有可读性代价。同为 judgement call。

### 路由

两个真缺陷都属 ControlServer 仓（可写），但修复触及产品代码，按本票判据「复核本身不改产品代码；
需要修的项若触及产品代码，按测试分层规则单独走 tier 1」不在本票内执行。已建
[票 22](22-close-the-worklist-revision-and-settle-coverage-defects.md) 承载，并挂在票 12
（授权发布）之前——本票 Question 的前提正是「在授权正式发布之前」。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server
Impact on this ticket: 已解决；复核结论为决策记录留在本票，缺陷的修复与证据归票 22 与归属仓。
本轮为只读复核，未改产品代码或测试项目，未跑 tier 1。
