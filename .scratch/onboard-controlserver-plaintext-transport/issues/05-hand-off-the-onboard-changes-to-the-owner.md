# 向车载端 owner 交付明文改造转交件

Type: task
Mode: HITL
Status: open
Blocked by: 01

## Question

车载端三处硬校验在 `8005-agv-onboard-hmi`，该仓对 agent **只读**，且用户 2026-08-25 已把车载端产品
代码划归王昆。用户 2026-08-31 选择路径 (a)：出精确转交件交王昆执行，不改变只读政策。本票产出该
转交件并完成交付，**对该仓零写入**。

转交件必须精确到可直接执行，至少包含：

- 三处改动点的当前代码与目标形态，按票 01 冻结的形态给出（行号以 owner 当前 tip
  `OnboardHmi_MVP@31263b1` 为准，已回读确认该 commit 上三处校验原封不动）：
  - `src/SQCD.Agv.Infrastructure/WireToGateSessionClient.cs:1850` —
    `if (!options.UseTls && !IsLoopback(options.Host))` 抛「非TLS WIRE_TO_GATE连接只允许loopback地址。」
  - `src/SQCD.Agv.Infrastructure/Configuration.cs:152` — endpoint scheme 必须等于 `Uri.UriSchemeHttps`
  - `src/SQCD.Agv.Infrastructure/ControlServerVehicleSafetySignalProvider.cs:95` — 同一 scheme 校验的运行时侧
- 配置面的对应改动：`appsettings.json` 与 `appsettings.Production.example.json`／`.template.json` 中
  `wireToGate.useTls`、`wireToGate.serverCertificateSha256`、`vehicleSafety.endpoint` 的终态，
  与服务端形态严格对齐；
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
