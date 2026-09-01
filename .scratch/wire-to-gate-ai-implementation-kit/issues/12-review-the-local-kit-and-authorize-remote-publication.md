# 审阅可运行 MVP 候选并授权正式发布

Type: task
Mode: HITL
Status: resolved
Blocked by: 14, 17, 21, 22

## Question

用户是否接受可运行 MVP Release Candidate 的三仓 commit、协议身份、安装物、端到端证据、恢复/重启证据、目标环境资格和已知限制，并授权创建正式远程 tag/release？若核心 WIRE_TO_GATE 路径、干净安装或版本绑定未通过，必须保持阻断，不得以文档、录屏或 Fake 单元测试替代。

本票必须先展示精确三仓 commit、候选协议 manifest/hash、安装物哈希、测试摘要、未通过项和拟创建 tag/release，并取得当轮批准。不得强推、覆盖历史、泄露凭据或在两名协议负责人确认前把候选称为正式 ProtocolRelease。

## Answer

**用户已批准发布。** 本票只做审阅与授权，未创建任何 tag、release 或远程写入；执行属票 15。

### 授权的三条决定

| 决定 | 用户选择 |
| --- | --- |
| 是否发布 | **授权发布**，第 4 节六项已知限制原样进发布说明 |
| tag 绑定 | **`9daeef4`**（当前 HEAD，含票 14 全部验收证据） |
| Release 资产 | **完整 RC 上传**（272 MB／868 文件，含服务端现场真值配置；仓库为 PRIVATE） |

拟用 tag 名 `w2g-mvp-rc-0.1.0`（与协议仓 `protocol-v0.1.1` 同风格；票 15 可在发布前另定）。

### 审阅所依据的事实（本会话从产物与仓库回读，非从票据转述）

三仓身份，读自 `w2g-rc-20260830-81cb9cf/release-manifest.json`：

| 组件 | 仓 / 分支 | commit | agent 写权限 | 仓可见性 |
| --- | --- | --- | --- | --- |
| ControlServer | `8005-agv-control-server` / `ControlServer_MVP` | `81cb9cf60a7990a7a7fb1b235042df5d0a9afd99` | 可写 | PRIVATE |
| OnboardHmi | `8005-agv-onboard-hmi` / `OnboardHmi_MVP` | `304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6` | **只读** | PRIVATE |
| 协议 | `8005-agv-protocol` / tag `protocol-v0.1.1` | `1531489e42e328f28bfe0c51ed3f8c56e5ce0279` | 审批门禁 | PUBLIC |

两条独立核对，都成立：

- 车载端 `304e6ad` **就是 `origin/OnboardHmi_MVP` 当前 tip**——本地 `bbfbc52` 经
  `git merge-base --is-ancestor` 证实是它的祖先，`rev-list --left-right --count` 为 `0 1`，即本地落后
  一个而非领先。RC 绑的不是陈旧 commit，且该仓无 agent 写入。
- `81cb9cf..9daeef4` 的 `git diff --name-only` 在排除 `evidence/` 后**为空**，`git log -- src` 在
  `d243abf..HEAD` 区间**无提交**。故 tag 目标 `9daeef4` 与 RC 二进制的产品代码完全同源，
  唯一非证据差异是 `264615a` 给 `docs/RELEASE-CANDIDATE.md` 加的 13 行。

协议身份从服务端包的 `appsettings.json:ProtocolCandidate` **读回**：
`manifestSha256=a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`、
`schemaBundleSha256=e04296e9bcf48c341bc91fef5731f6f465a5ecdbb9adedc17f3bac58e193d30c`、
`vectorsSha256=fc5902b71d1b276c674f8a21c738d27193ddcbaf9b352951deffbaf1488d356e`、
`approvalStatus=APPROVED_RELEASE`。同一组哈希在八份 G2 `gate-result.json` 中逐份一致。

安装物哈希，本会话对 RC 本体逐文件重算：**`OK=868 MISMATCH=0 MISSING=0`**。两个根哈希
`release-manifest.json = c18babe4ff749bdfcde92d04e9d426a85c3fe0cde92a73fb26abfec08b699fc6`
（171,955 B）、`SHA256SUMS.txt = 487403e2cb00ca8f3008fecd09e134b1fe3ee6fd5552f2fbfa780885d3b9f448`
（98,898 B）。**红侧**：同一比对路径下把首条期望哈希翻一个字符即 `MISMATCH`，真期望即 `OK`——
这个绿会变红。

门禁摘要：

| 门禁 | 结果 | 绑定 | 来源 |
| --- | --- | --- | --- |
| tier 1 | 243 passed / 0 failed / **0 skipped** | `d243abf`（与 RC 产品代码同源） | 票 23 `tier1-run.log`；本会话未触产品代码，按 `AGENTS.md` 未重跑 |
| G2 W2G-IS-00～07 | **8/8 PASS** | `264615a` + manifest `a467c0c4…` | `evidence/g2/20260830-issue26-264615a/*/gate-result.json` 逐份读回 |
| 干净安装验收 | **23 PASS / 0 FAIL / 5 INCONCLUSIVE** | RC `81cb9cf` | `assertions.json` 的 `counts` 与 28 条 `verdict` 一致 |
| 现场端到端闭环 | generation 7 `Stage=Completed`，5 分 42 秒，两条真单各建一次、10 条审计齐全 | 同上，RC 生产形态 | `20260830-issue14-field-closed-loop/SUMMARY.md` |
| 服务安装／卸载 | 安装 `PASS`（9 检查、NDJSON 落盘、迁移建库、首启 `RECOVERY_HANDSHAKE_REQUIRED` 为预期）；卸载 `PASS` | `81cb9cf` | 用户以管理员运行的 `result.json` / `uninstall.json` |
| 发布扫描闸门 | finding 0、密钥材料文件 0、UNRESOLVED 许可证 3 且**逐个具名在允许清单**（三个自建 RIoT SDK 包）、`unexpectedUnresolvedLicenses` 为空 | — | manifest `inventory.scanGate` |

验收的 5 条 INCONCLUSIVE 中，`INSTALL-AS-SERVICE` 与 `PERSISTENT-LOGS` 已由用户那次管理员安装补齐，
`MOVEMENT-CLOSED-LOOP` 已由 generation 7 补齐。**真正剩下两条**：`HW-ONBOARD-TARGET`、`HW-REAL-IO`。

### 发布说明必须原样携带的六项已知限制

1. **车载端 HMI 生产形态缺陷**（票 27，**仍未决**）：`DisabledRuleGateway.IsConnected` 恒 false 把
   HMI 状态机钉死在 `Connecting`，WIRE_TO_GATE 业务不进状态横幅与操作记录，`RecoveryRequired` 无
   操作员出口。归只读的车载端仓，本仓不存正文。用户选择不等票 27 而先授权发布，故**票 15 必须把
   这一条写进发布说明的已知限制，并在票 27 落定后回补去向**。
2. **真实八仓 IO 与车载目标终端硬件未取得资格**（上表两条 INCONCLUSIVE）。本轮 IO 全程是模拟器
   `127.0.0.1:1502`；不构成真实 IO 模块、接线、锁或光幕的资格。
3. **票 23 的具名残留风险**：服务端正确性依赖一条协议未要求的对端行为（重复快照必须再 ACK）。
   沉默但合规的对端会让快照重发冲突可达且自维持。
4. **车载端随包配置是开发默认**：`declaredBuildCommitMatchesBuild=False`（声明 `a6f05fb`，实际
   `304e6ad`），另有 7 个 `REPLACE_*` 现场占位符（`REPLACE_CONTROL_SERVER_HOST`／`_IP`、
   `REPLACE_IO_MODULE_IP`、`REPLACE_RULE_SERVER_IP`、`REPLACE_WITH_64_CHARACTER_SHA256`、
   `REPLACE_WITH_EXPECTED_VEHICLE_KEY`、`REPLACE_WITH_STABLE_UUID`）。手册第 8 节已写明，但它是
   **上线前必做**而非提示。
5. **服务端随包 `appsettings.json` 是现场真值**：`RIoT.baseUrl=http://172.19.206.222:8888`、
   `vehicleKey=BROKERX-0c20ff06…`、`mapId=25`、中文站点名。三个 runtime 开关
   （`RiotCreateDispatch`／`JourneyRuntime`／`OnboardSafetyProjection`）出厂均 `enabled=false`，
   所以装完不建单不动车；但这些值随发布物一起分发。用户已知情并选择完整上传（PRIVATE 仓）。
6. **手册的 `dispatchGeneration` 说明不完整**（本次复核新发现）：
   `JourneyRuntimeEngine.cs:1102/1104` 构造 `upperId = W2G-{demandId}-{PICKUP|GATE}-{generation}`，
   **demandId 在键里**，所以新 demand 用 `dispatchGeneration=1` 不会撞已有订单；但**重跑同一个已派过
   的 demand** 必须换更大代次，现场 1～7 已用掉。手册第 11 节只泛说「正数 dispatchGeneration 必须
   核验」，未说这一条。**不改包**——`RELEASE-CANDIDATE.md` 在 868 条哈希内，改它要重建 RC；这一条
   由票 15 写进包外的 Release 说明。

### 交给票 15 的执行约束

- tag 与 GitHub Release **只在 `8005-agv-control-server` 创建**，绑 `9daeef4`，资产为完整 RC
  `w2g-rc-20260830-81cb9cf` 及其 `release-manifest.json`、`SHA256SUMS.txt`。该仓当前**零 release**。
- **`8005-agv-onboard-hmi` 对 agent 只读，agent 不得在该仓创建 tag 或 release。** 票 15 问句里的
  「三个远程仓库的正式 tag/release」，车载端那一份只能由用户或王昆自行完成；票 15 不得为凑齐三仓而
  写入该仓。
- **`8005-agv-protocol` 的 `protocol-v0.1.1` 已发布**，无需也不应再动；协议侧任何变更仍需两名负责人
  对同一具体变更明确批准。
- 上传前不得修改包内任何文件——一旦修改，868 条哈希与 `release-manifest.json` 即失效，须整体重建
  RC 而非改文件。第 6 项的更正写在包外的 Release 说明里。
- 发布说明不得把受控测试可用扩大为工厂生产可用：第 2 项两条硬件资格必须醒目标记。
