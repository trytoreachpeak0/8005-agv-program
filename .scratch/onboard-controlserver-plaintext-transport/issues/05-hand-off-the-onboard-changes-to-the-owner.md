# 向车载端 owner 交付明文改造转交件

Type: task
Mode: HITL
Status: claimed
Blocked by: 01

## Question

车载端硬校验在 `8005-agv-onboard-hmi`，该仓对 agent **只读**，且用户 2026-08-25 已把车载端产品
代码划归王昆。用户 2026-08-31 选择路径 (a)：出精确转交件交王昆执行，不改变只读政策。本票产出该
转交件并完成交付，**对该仓零写入**。

**票 01 更正：是四处，不是三处。** 第四处与 `UseTls` 无关，漏改会让前三处全部白改。

转交件必须精确到可直接执行，至少包含：

- 四处改动点的当前代码与目标形态，按票 01 冻结的形态给出（行号以 owner 当前 tip
  `OnboardHmi_MVP@31263b1` 为准，已回读确认这些校验原封不动）：
  - `src/SQCD.Agv.Infrastructure/WireToGateSessionClient.cs:1850` —
    `if (!options.UseTls && !IsLoopback(options.Host))` 抛「非TLS WIRE_TO_GATE连接只允许loopback地址。」
  - `src/SQCD.Agv.Infrastructure/Configuration.cs:152` — endpoint scheme 必须等于 `Uri.UriSchemeHttps`
  - `src/SQCD.Agv.Infrastructure/ControlServerVehicleSafetySignalProvider.cs:95` — 同一 scheme 校验的
    运行时侧。**漏改不崩溃**：fail-closed 到 `UnknownSignal("HTTPS_REQUIRED")`，现场症状是车辆安全
    信号恒为 UNKNOWN、永不放行，无异常无日志红。转交件必须写明这个静默症状
  - `src/SQCD.Agv.Infrastructure/Configuration.cs` 的 `WireToGateSettings.Validate(production: true)` —
    强制 `ServerCertificateSha256` 非空且非全零，**该检查不看 `UseTls`**；漏改则 production 启动抛
    「Production环境的ControlServer地址、构建commit或TLS指纹仍是本机/占位配置。」
- **明确「不要动」的清单**，与「要改」写得同样具体：`Configuration.cs` 内两处
  `IsForbiddenProductionHost`（production 禁 loopback／占位主机）保留——异机形态本来就满足它，它拦的是
  「生产配置忘了改样例值」，与本轮无关；
- 配置面的对应改动：`appsettings.json` 与 `appsettings.Production.example.json`／`.template.json` 中
  删除 `wireToGate.useTls` 与 `wireToGate.serverCertificateSha256` 两键、`vehicleSafety.endpoint` 改
  `http://`，与服务端形态严格对齐；
- 受影响的车载端测试：`tests/SQCD.Agv.UnitTests/ConfigurationTests.cs`、
  `tests/SQCD.Agv.UnitTests/ControlServerVehicleSafetySignalProviderTests.cs`、
  `tests/SQCD.Agv.WireToGateG2Tests/WireToGateG2Tests.cs` 中绑在 TLS/HTTPS 形态上的断言；
- **改动的理由与代价**，不做美化：动机是工厂内网部署复杂度，代价是 `credentialProof` 明文过网与
  安全闸门输入可篡改，二者由用户知情接受；
- 需要他回传的东西：改完后的 commit SHA 与分支，供票 06 只读回读核验。

交付形态沿用上一轮惯例：转交件写在**仓外**（如 `C:\Users\szy\Desktop\致王昆<日期><主题>.md`），
不进本规划仓，更不进车载端仓。

**这是本地图的已知阻塞点**。票 27 的经验是 owner 会响应但有延迟，且他可能不接受本改动、或提出
替代方案（例如坚持链路 B 保留 TLS）。本票的答案要据实记录他的实际回应，**不得代他决定**，也不得
在他未回应时把「已发出」表述为「已接受」。若他提出反对或替代，本地图的完成定义需与用户重新协商，
而不是由 agent 自行调整。

## 交付记录（2026-08-31）

**状态：转交件已产出，尚未转交，王昆零回应。本票据此保持 `claimed` 而非 `resolved`。**

- 转交件：`C:\Users\szy\Desktop\致王昆20260831明文传输改造.md`（仓外，未进任何 Git 仓）。
- 对 `8005-agv-onboard-hmi` 的写入：**零**。全程只做 `git fetch` 与
  `git show origin/OnboardHmi_MVP:<path>`，事后 `git status --porcelain` 为空。
- 基线复核：`origin/OnboardHmi_MVP` tip 仍是 `31263b1`，与开票时一致。四处硬校验的行号
  （`WireToGateSessionClient.cs:1850`、`Configuration.cs:152`、
  `ControlServerVehicleSafetySignalProvider.cs:95`、`Configuration.cs:284`）逐条回读确认原封不动。

### 本次回读对票据与票 01 的更正

1. **`.template.json` 不存在。** `git ls-tree` 确认全仓只有
   `src/SQCD.Agv.Wpf/appsettings.json` 与 `appsettings.Production.example.json` 两个配置文件。
   本票 Question 里「`.template.json`」一项作废。
2. **`appsettings.json`（Development）本来就没有 `serverCertificateSha256` 键**，只有
   `useTls: false`（第 21 行）。两键齐全的只有 Production example（第 21–22 行）。
3. **新增一处漏列的改动点：`scripts/run-staged-g3-recovery-ack-drop.ps1:292`** —
   `$settings.wireToGate.useTls = $false`。删键后这行会往 PSCustomObject 上新增回该属性并由
   `ConvertTo-Json` 写回配置文件；若车载端也加了「过时键拒绝」，G3 runner 直接起不来。已写入转交件 §5.4。
4. **明确划出「不要动」的证据文件**：`evidence/g3/20260826-recovery-ack-drop-cc6e2b9-0455147/runner.ps1:278`
   有同一行，但它是历史证据快照，不得修改。已写入转交件 §5.5。
5. **删字段的连带编译影响清单**（票 01 只冻结了形态，未展开）：`WireToGateSessionOptions` record 的
   两个位置参数、`CreateTransportStreamAsync` 的 `SslStream` 分支、`ValidateServerCertificate` 整个方法、
   失去调用点的 `IsLoopback`、两条 using。仓里 `TreatWarningsAsErrors=true` +
   `AnalysisLevel=latest-recommended`。已写入转交件 §3，并特别标注 `using System.Security.Cryptography;`
   不能删（第 1883 行内容哈希在用）。
6. **G2 里绝大多数 `Sha256` 与 TLS 无关**（`ContentSha256` / `ComputeContentSha256` /
   `appliedContentSha256`，共 13 处），只有第 929–930 行是 TLS。按关键字搜删会拆坏 G2。已写入转交件 §5.3。
7. **票 01 第 6 节「过时配置键启动期拒绝」只冻结了服务端**，未规定车载端是否对称。转交件 §4.3 如实
   标为「由王昆定」，未代他决定。这是票 01 的一个缺口，若他选择加，票 06 核验时要一并看。
8. **文档三处**（`README.md:157`、`docs/LOCAL_INTEGRATION_MATRIX.md:8`、
   `docs/ONBOARD_DEVELOPER_HANDOFF.md:86`）提到证书/HTTPS，已列进转交件 §7 供他判断，未替他定改法。

### 待办

转交动作（把该文件发给王昆）由用户执行，agent 不代发。王昆回应后在此追加 `## Answer`，据实记录
他的实际答复（接受／反对／替代方案），再决定本票能否 resolve 以及本地图完成定义是否需要重新协商。
