# 17 — `FP-IS-00`～`07` 在 v2 下重证

**做什么：** 把八个批次 0 切片在协议 v2 下重新证一遍，三道门禁全 PASS：
`CONTROL_SERVER_G2`、`ONBOARD_HMI_G2`、`G3`。这是**批次 2 轨 A 的出口**。

八个切片与 `W2G-IS-00`～`07` 一一对应，关系是「**v2 下的重证**」而不是「可以沿用的通过
结论」——`ConformanceRunIdentity` 已规定任一绑定分量变化都必须建立新运行。

**而且根本没有通过结论可以沿用**：`RELEASE-CANDIDATE.md` 第 12 节末原文写着
`W2G-IS-00`～`07` 与 RC 目前仍为 `INCONCLUSIVE`，八类 G3 向量各有证据不等于八个切片通过。
**证据与说明里都不得暗示存在可沿用的通过结论。**

`ONBOARD_HMI_G2` 自 2026-09-04 起由我方跑、我方填那一列，不再等 Kun Wang。**但这不改变
谁签发布**——release attestation 仍要两名不同产品负责人。

**排期提示（不是硬依赖）**：G2 与 G3 证据绑定精确 commit。轨 B 的能力票会持续改服务端，
建议把这八个切片的重证放在一个**连续窗口**内跑完，窗口内轨 B 暂缓合并；或等轨 B 的票
09～13 合完再跑。两种都行，别边跑边合。

**前置：** ~~票 14（服务端 v2）~~✅、~~票 15（车载端 v2）~~✅、~~票 16（`vectorId` 绑定守卫）~~✅。
**三条前置全部解除，本票可开工。**

**票 16 于 2026-09-08 完成，这一条前置解除**（见 [16-answer.md](16-answer.md)）。守卫落在
控制端 `562544e`，CI 绿（run
[34227325616](https://github.com/trytoreachpeak0/8005-agv-control-server/actions/runs/34227325616)，
`569 passed / 0 failed / 0 skipped`）。

**票 14 于 2026-09-08 完成，这一条前置也解除**（见 [14-answer.md](14-answer.md)）。服务端已说
v2，三条 C_TO_O 快照的 payload 形状按 v2 schema 改对，186 处 trait 重打为 `FP-IS-NN`，
L1 `586 passed / 0 failed / 0 skipped`。
**票 15 于 2026-09-09 完成，最后一条前置解除**（见 [15-answer.md](15-answer.md)）。车载端
`w2g/fp-v2-impl` = `f0b4e0d`（已推送），`168 passed / 0 failed / 0 skipped`。

票 15 转交本票四件事，**其中前两件会挡住出证，开工先看**：

1. **`dotnet format --verify-no-changes` 在 `core.autocrlf=true` 的 checkout 上必然失败。**
   实测 `exit=2`、21494 条 `ENDOFLINE` ＋ 16 条 `WHITESPACE`，涉及 71 个 `.cs` 文件，**包括票 15
   一个字都没碰的 `App.xaml.cs` 与 `DomainModels.cs`**。原因是仓库存 LF、`.editorconfig` 要 LF、
   而 git 落盘成 CRLF。`run-w2g-g2.ps1` 把 format 的退出码计入 `hmiStatus`，所以**不先解决它，
   八份证据全是 FAIL**。两条路：跑门禁的机器设 `core.autocrlf=false`／`input`，或给该仓加
   `* text=auto eol=lf`（会重写全仓行尾，**属于对方仓库的决定**）。详见 15-answer.md 第十一节。
2. **`run-w2g-g2.ps1` 没有 `-Slice` 参数。** 它跑整个解决方案的测试、不按切片过滤，
   `summary.json` 里 `FP-IS-00` 与 `FP-IS-01` 共享同一个 `onboardHmiG2` 结论，其余六片根本不
   出现。**本票要按切片各出一份证据，这个脚本要先改造**——而按切片过滤需要车载端先有
   `IntegrationSlice` trait，那是票 20。已在脚本的 `knownLimitations` 里写明。
3. **车载端的门禁脚本身份已切到 v2 候选**，`$expected` 表十个值与
   `WireToGateProtocol.cs` 由 `ProtocolIdentityArchitectureTests` 逐字段钉住。tag 断言从「绑
   tag」改成「绑候选 commit」——`protocol-v1.0.0` 至今没打。`summary.json` 的 `protocol` 节多了
   `tagExists`／`candidateCommit`／`candidateIsAncestorOfHead`／`approvalStatus` 四个字段。
   `run-staged-g3-recovery-ack-drop.ps1` 的 `startedScope` 已改成 `FP-IS-00`／`FP-IS-06`。
4. **车载端的门禁跑在 `w2g/fp-v2-impl` 上，不是 `OnboardHmi_MVP`。**
   `OnboardHmi_MVP` 已钉到已发布的 `protocol-v0.3.0`（`ProtocolVersion 3`／`WIRE_TO_GATE_MVP`），
   与本线不是同一条协议。**证据里的 commit 绑定要写 `w2g/fp-v2-impl` 的 commit。**

票 14 转交本票三件事：

1. **`test-wire-to-gate.ps1` 的调用形态变了。** `-Slice` 只收 `FP-IS-NN`（正则
   `^FP-IS-(0[0-9]|1[0-5])$`）；身份不再硬编码在脚本里，改从
   `src/ControlServer.Host/appsettings.json` 的 `ProtocolCandidate` 读；切片的向量清单改从
   `vendor/8005-agv-protocol/integration-slices/index.json` 读，不再是脚本里那份手抄表。
   `gate-result.json` 的 `schemaVersion` 升到 `1.1.0`，新增 `protocolProfileId`、
   `protocolVersion`、`protocolApprovalStatus`、`integrationSliceIndexSha256`、
   `selectedTestCount` 五个字段。
2. **`FP-IS-08`～`15` 出不了 G2 证据，本票的出口只能是八片。** 票 14 实测发现
   `dotnet test --filter` 选不中任何测试时退出码是 0，脚本会把它写成 `"status": "PASS"`——
   一个零实现的切片拿到过一份绿的 G2 结果。已改成建目录前先数、选中 0 条即拒绝并报出该片向量。
3. **`ApprovalStatus` 是 `SUPERSEDING_CANDIDATE`，不是 `APPROVED_RELEASE`。**
   `New-WireToGateReleaseCandidate.ps1` 因此拒绝打 RC，这是规格 6.6 要的效果，不是要绕过的
   障碍。本票的出口是三道门禁全 PASS，**不含 RC**。

票 16 转交本票一件事：`CV-LOAD-CANCELLATION-ALL-EMPTY` 是它 20 条绑定里最薄的一条——服务端
取消面（`OnboardRecoveryCoordinator.AuthorizeLoadCancellationAsync`）只有
`FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 一条测试覆盖，
且走的是 `REJECTED` 分支，只证了 `AUTHORIZE_CANCELLATION_EXPLICITLY` 那一半；
`RECONCILE_EMPTY_FINAL_STATE` 那一半在实现里（同文件 `safeEmpty` 判据）但没有独立测试。
**`FP-IS-02` 重证时应当补上。**

**状态：** ready-for-agent

- [ ] 八个切片各跑一遍 `CONTROL_SERVER_G2`，八份 `gate-result.json` 全 PASS
- [ ] 八个切片各跑一遍 `ONBOARD_HMI_G2`，八份 `gate-result.json` 全 PASS
- [ ] 八个切片各跑一遍 `G3`，全 PASS
- [ ] 每份 `gate-result.json` 绑定精确的 `ProtocolReleaseIdentity`（v2 三元组）
- [ ] 证据落在 `evidence/g2/<日期>-<描述>/<FP-IS-NN>/` 与 `evidence/g3/<日期>-<描述>/`
- [ ] `-EvidenceRoot` 是不存在的目录；红的证据不被绿的重跑覆盖；失败时 stage root 不删
- [ ] 证据目录只增不改——若需纠正，写新目录并在 `SUMMARY.md` 里指向被纠正的那份
- [ ] 车载端侧的门禁跑在我方 `w2g/*` 分支上，commit 绑定如实记录
- [ ] 证据与说明中不出现「沿用已通过结论」这类表述
