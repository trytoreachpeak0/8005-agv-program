WIRE_TO_GATE MVP Release Candidate。**受控测试环境可用，未取得工厂生产资格**——两条硬件资格仍未通过，见第 6 节。

包内 `RELEASE-CANDIDATE.md` 是唯一操作入口：按它从零构建、校验、安装、启动、停止、重启、定位日志与证据、回滚，不需要任何开发会话的上下文。本说明只做三件包内文件做不到的事：给出版本绑定与资产哈希、原样携带已知限制、承载一条**包外**手册更正。

---

## 1. 版本绑定

| 组件 | 仓库 / 分支 | commit |
| --- | --- | --- |
| ControlServer | `8005-agv-control-server` / `ControlServer_MVP` | `81cb9cf60a7990a7a7fb1b235042df5d0a9afd99` |
| OnboardHmi | `8005-agv-onboard-hmi` / `OnboardHmi_MVP` | `304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6` |
| 协议 | `8005-agv-protocol` / tag `protocol-v0.1.1` | `1531489e42e328f28bfe0c51ed3f8c56e5ce0279` |

本 tag 指向 `9daeef4325fccf094767b689fa484d8e1e414042`。它与资产二进制的产品代码**同源**：`81cb9cf..9daeef4` 排除 `evidence/` 后 diff 为空，`src` 在该区间无提交，差异只有 `docs/RELEASE-CANDIDATE.md` 的 13 行与新增证据目录。

协议身份（`ProtocolReleaseIdentity`，`profileId=WIRE_TO_GATE_MVP`、`protocolVersion=1`、`approvalStatus=APPROVED_RELEASE`）：

| 字段 | 值 | 服务端 | 车载端 |
| --- | --- | --- | --- |
| `repositoryCommit` | `1531489e42e328f28bfe0c51ed3f8c56e5ce0279` | `controlserver/appsettings.json` | 内嵌于 `SQCD.Agv.Contracts.dll` |
| `manifestSha256` | `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f` | 同上 | 内嵌于 `SQCD.Agv.Infrastructure.dll` |
| `schemaBundleSha256` | `e04296e9bcf48c341bc91fef5731f6f465a5ecdbb9adedc17f3bac58e193d30c` | 同上 | 内嵌于 `SQCD.Agv.Contracts.dll` |
| `vectorsSha256` | `fc5902b71d1b276c674f8a21c738d27193ddcbaf9b352951deffbaf1488d356e` | 同上 | 不携带（测试向量哈希是构建期资产，运行时不需要） |

两端在前三个字段上逐字一致。同一 manifest 哈希也出现在八份 G2 `gate-result.json` 中。

---

## 2. 资产与校验

| 资产 | 大小 | SHA-256 |
| --- | --- | --- |
| `w2g-rc-20260830-81cb9cf.zip` | 123,976,762 B | `d40c8ab1e041e168b6f8ee701fb9529009dabbaa20e9d0f7654fc10f35e8f6eb` |
| `release-manifest.json` | 171,955 B | `c18babe4ff749bdfcde92d04e9d426a85c3fe0cde92a73fb26abfec08b699fc6` |
| `SHA256SUMS.txt` | 98,898 B | `487403e2cb00ca8f3008fecd09e134b1fe3ee6fd5552f2fbfa780885d3b9f448` |

后两个文件与 zip 内根目录下的同名文件是同一份，单独上传只为不下载 118 MB 也能读到清单。zip 解压出单个顶层目录 `w2g-rc-20260830-81cb9cf/`，869 个条目、解压后 283,001,315 字节。

解压后在包根目录执行（手册第 3 节）：

```powershell
Get-Content .\SHA256SUMS.txt | ForEach-Object {
    $parts = $_ -split '  ', 2
    if ($parts.Count -eq 2) {
        $actual = (Get-FileHash -LiteralPath $parts[1] -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $parts[0]) { "MISMATCH $($parts[1])" }
    }
}
```

无输出即 868 个文件全部一致。发布前在本机复验为 `OK=868 MISMATCH=0 MISSING=0`。

`scripts\Install-ControlServerLocal.ps1` 在安装前还会独立校验服务端包的 `deployment-manifest.json`，逐文件比对 SHA-256 并拒绝任何越出包目录的路径。

---

## 3. 从这里开始

全部步骤在包内 `RELEASE-CANDIDATE.md`：

| 需要做的事 | 章节 |
| --- | --- |
| 前置条件（目标机**不需要** .NET SDK 或运行时） | 1 |
| 从源码重建同一份候选 | 2 |
| 校验产物 | 3 |
| 外部秘密（四个环境变量，不在包内、不进 Git、不进日志） | 4.1 |
| 安装 ControlServer（需要管理员 PowerShell） | 4.2 |
| 隔离安装，不影响已有部署 | 4.3 |
| 启动、停止、重启、健康检查 | 5 |
| 数据库初始化与迁移（安装期自动执行） | 6 |
| 日志位置与格式 | 7 |
| 运行 OnboardHmi（交互式桌面会话，不是服务） | 8 |
| 回滚与卸载 | 9 |
| 依赖、许可证与秘密扫描清单 | 10 |
| 仍然阻断目标硬件与现场使用的外部条件 | 11 |
| 运行核心测试场景 | 12 |
| 证据在哪里 | 13 |

**上线前必做**：车载端 `appsettings.json` 出厂是开发默认值，含 7 个 `REPLACE_*` 现场占位符且 `environment=Development`；按手册第 8 节逐项改正后才能连上服务端。见已知限制第 4 项。

---

## 4. 已验证到什么程度

| 门禁 | 结果 | 绑定 |
| --- | --- | --- |
| 单元与集成测试 | 243 passed / 0 failed / **0 skipped** | `d243abf`（与本资产产品代码同源） |
| 协议一致性 G2，切片 W2G-IS-00～07 | **8/8 PASS** | manifest `a467c0c4…` |
| 干净安装验收 | **23 PASS / 0 FAIL / 5 INCONCLUSIVE** | 本资产 `81cb9cf` |
| 现场端到端闭环 | 取货 → 多仓装货 → 发车安全 → `TO_GATE` → 关卡批量卸货 → 原子完成，`Stage=Completed`，5 分 42 秒，两条真单各建一次，10 条审计齐全 | 本资产，RC 生产形态 |
| 服务安装 / 卸载 | 安装 PASS（9 项检查、NDJSON 落盘、迁移建库）；卸载 PASS | 本资产，管理员运行 |
| 发布扫描闸门 | 秘密 finding 0、密钥材料文件 0、UNRESOLVED 许可证 3 且逐个具名在允许清单内（三个自建 RIoT SDK 包） | `release-manifest.json:inventory.scanGate` |

验收的 5 条 INCONCLUSIVE 中，服务安装、持久日志、移动闭环三条已由后续运行补齐；**真正剩下两条硬件资格**，见下。

---

## 5. 已知限制（发布时原样携带，不得省略）

1. **车载端 HMI 在本 RC 的生产形态下不反映 WIRE_TO_GATE 业务，且 `RecoveryRequired` 无操作员出口。**
   业务闭环本身不受本项影响（上表 generation 7 已 `Completed`），受影响的是**随包 HMI 对现场操作员可用**这一条资格。该缺陷归车载端仓 `8005-agv-onboard-hmi`，两半的去向已落定，但**性质不同**：

   **1a 状态与操作记录不反映业务 —— 已在车载端仓修复，但不在本资产内。**
   本 RC 的车载端二进制建自 `OnboardHmi_MVP@304e6ad`，其中 `DisabledRuleGateway.IsConnected` 恒 `false`，把 HMI 状态机钉死在 `Connecting`，WIRE_TO_GATE 业务过程不进状态横幅与操作记录。该仓负责人已于 2026-08-30 在 `OnboardHmi_MVP@31263b1` 修复：横幅与「任务系统」状态改由正式上层会话驱动，不再依赖恒为离线的 `DisabledRuleGateway`；子批录入、仓位操作阶段、结果确认与恢复阻断均投影到操作记录；批量操作失败后保持「需要管理员恢复」而不退回「连接中」。
   **该修复不在本资产内**，本 RC 的行为仍如上所述；需要它必须重建候选。

   **1b `RecoveryRequired` 无操作员出口 —— 不是车载端可单独修复的缺陷，是跨端结果身份缺口，未决。**
   站点操作落进 `RecoveryRequired` 后，现场操作员在随包 HMI 上没有前进或撤销的手段。经两端核对，车载端对恢复命令保持 fail-closed 是当前唯一正确的行为：`SlotOperationResumeCommand` 复用原 `slotOperationAttemptId` 且没有独立的 resume 结果消息，而 ControlServer 以 `(slotOperationAttemptId, forcedRecoveryGeneration)` 唯一接受 `OperationResult`，`RESUME_AFTER_REPAIR` 又不推进 `forcedRecoveryGeneration`。因此修复物理状态后发送同 attempt 的新结果会被判为内容冲突，重放原结果会被按 replay 忽略，恢复 workflow 两条路都不收敛。
   收敛需要两端先选定一个结果身份方案（resume 命令携带新的 operation/result identity；或服务端在活动 `recoveryActionId` 下允许同 attempt 的授权替代结果；或协议新增独立的 resume result 并明确它如何关闭原 `OperationResult`），涉及协议仓变更与两名负责人批准，**判为本 RC 范围外**。在方案选定并通过带 demand 的联合回归之前，`RecoveryRequired` 的现场处置须走人工流程。

2. **真实八仓 IO 与车载目标终端硬件未取得资格。**
   本轮 IO 全程是模拟器 `127.0.0.1:1502`。这**不构成**真实 IO 模块、接线、锁或光幕的资格，也不构成车载目标终端（屏幕、触摸、扫码枪）的资格。上线这两项前，本候选只适用于受控测试环境。

3. **服务端正确性依赖一条协议未强制要求的对端行为。**
   服务端每个迭代重发未确认的会话快照；当前车载端对重复快照会再次 ACK，因此快照重发冲突不可达。一个沉默但仍然合规的对端（收到重复快照不再 ACK）会让该冲突可达且自维持。更换或修改对端行为的一方需要重新评估这一点。

4. **车载端随包配置是开发默认，上线前必须逐项改正。**
   `appsettings.json` 中 `environment=Development`、`wireToGate.enabled=false`、`agvId=AGV-8005-01`、`vehicleSafety.endpoint` 是 `.invalid` 占位符，另有 7 个现场占位符：`REPLACE_CONTROL_SERVER_HOST`、`REPLACE_CONTROL_SERVER_IP`、`REPLACE_IO_MODULE_IP`、`REPLACE_RULE_SERVER_IP`、`REPLACE_WITH_64_CHARACTER_SHA256`、`REPLACE_WITH_EXPECTED_VEHICLE_KEY`、`REPLACE_WITH_STABLE_UUID`。
   另外 `wireToGate.onboardBuildCommit` 声明为 `a6f05fb…`，而二进制实际构建自 `304e6ad…`（`declaredBuildCommitMatchesBuild=false`）。
   手册第 8 节写了这些，但它是**上线前必做**，不是提示。
   注意：`environment=Production` 会拒绝回环地址，配错的表现是弹「软件无法启动」且**不产生任何日志目录**。

5. **服务端随包 `appsettings.json` 携带现场真值。**
   `RIoT.baseUrl=http://172.19.206.222:8888`、`vehicleKey=BROKERX-0c20ff06…`、`mapId=25`、中文站点名，随发布物一起分发（本仓库为 PRIVATE，发布已知情授权）。
   三个 runtime 开关 `RiotCreateDispatch`、`JourneyRuntime`、`OnboardSafetyProjection` 出厂均 `enabled=false`，因此**装完不建单、不动车**；要跑业务须显式打开。

6. **手册第 11 节关于 `dispatchGeneration` 的说明不完整（更正见下节）。**

---

## 6. 手册更正（包外，不修改资产）

包内 `RELEASE-CANDIDATE.md` 第 11 节只泛说「正数 `dispatchGeneration` 必须核验」，未说清何时必须递增。精确规则是：

`JourneyRuntimeEngine.cs` 构造的上层订单键为

```
upperId = W2G-{demandId}-{PICKUP|GATE}-{dispatchGeneration}
```

`demandId` **在键里**，所以：

- **新的 demand 用 `dispatchGeneration=1` 不会撞已有订单**；
- **只有重跑同一个已派过的 demand** 才必须换更大的代次。现场 1～7 已经用掉，重跑同一 demand 须从 8 起。

本更正不写进包内——`RELEASE-CANDIDATE.md` 在 868 条哈希之内，改动它会使全部哈希与 `release-manifest.json` 失效并要求整体重建候选。

---

## 7. 范围与支持责任

- 本 release 只在 `8005-agv-control-server` 创建。**车载端 `8005-agv-onboard-hmi` 的对应 tag 不在本次发布范围内**，需由该仓负责人自行创建；协议仓 `protocol-v0.1.1` 已发布，本次不改动。
- 交付判定是「程序能安装、运行并完成规定业务闭环」，上表已就此给出证据。**这不等于工厂生产可用**：已知限制第 1、2 项分别阻断随包 HMI 的操作员可用性与两项硬件资格。
- 真实车辆动作、Golden WPF tier 2/3、工厂试运行仍需逐次单独授权并满足现场物理安全条件，不因本 release 存在而获得授权。
- 外部秘密（`CONTROL_SERVER_ONBOARD_CREDENTIAL`、`CONTROL_SERVER_RIOT_CALL_API_KEY`、`CONTROL_SERVER_MES_INGEST_SHARED_SECRET`、`CONTROL_SERVER_OPERATOR_ID`）只以环境变量名出现在包内脚本与手册中，值不在包内、不进 Git、不进日志。
