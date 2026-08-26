# 决定双仓库一致性门禁、模拟对端与联调切片

Type: grilling
Status: resolved
Blocked by: 07, 09

## Question

ControlServer 仓库的 Fake Onboard、OnboardHmi 仓库的 Fake ControlServer 与共享协议仓库的一致性测试如何共用同一批 Schema、消息向量、虚拟时间和预期状态轨迹，并以稳定 IntegrationSliceId 分段证明会话恢复、Demand 受理、机台装货、RIoT 移动、关卡卸货、结果未知与重启对账？

决策必须固定每个切片的输入、输出、两端 commit、protocol release、Fake 版本、失败证据和合并门禁，以及哪些结果保存在各实现仓库、共享协议仓库或当前服务端产品验收记录中。

## Answer

### 决策依据与选择记录

本票依据用户对本 Wayfinder 后续各票采用推荐值的明确授权，在重新核对根 `CONTEXT.md`、`docs/adr/cross/`、地图 Notes、已解决的[决定 ControlServer—OnboardHmi 职责边界与 MVP 消息面](07-decide-controlserver-onboard-responsibilities-and-mvp-message-surface.md)及[决定共享协议仓库的发布内容与变更治理](09-decide-shared-protocol-repository-release-and-change-governance.md)后，采用本次列出的全部推荐值。该授权替代逐题等待，不表示用户曾逐项作答，也不表示车载端开发同事、ControlServer 开发者或任何第三方已经批准真实协议 release 或联合构建。

采用的候选为：语言无关共同向量与 runner contract；带完整复合身份且不模拟真实硬件能力的双 Fake；纯虚拟时间和脚本化故障；Schema、轨迹、持久事实、禁止副作用与终态的共同判定；八个稳定 IntegrationSliceId；机器可读切片 manifest；G0～G3 分层门禁；不可改写运行身份；FAIL／INCONCLUSIVE 永久证据；契约、各端和服务端验收索引三层存放；只有双 Fake 与真实对真实联合运行全部通过才完成切片。

拒绝两端复制契约、特定语言共享 Fake SDK、墙钟与随机网络、只验 Schema 或 happy path、按团队切片、自由 README、每次 PR 跨仓库互锁、只记分支/tag、覆盖失败、临时 CI 页面以及以 Fake 或现场单次成功替代联合门禁。理由分别是契约漂移、技术栈耦合、不可复现、遗漏安全状态、无法定位、不可机读、合并死锁、证据不可重现、红色证据丢失和错误的批准替代。

### 1. 共同一致性包与 runner contract

1. `8005-agv-protocol` 的每个不可变 ProtocolRelease 是测试语义的唯一权威。它发布上一票冻结的 Schema、manifest、错误码、合法／非法 envelope、状态轨迹向量和以下语言无关 runner contract；两个实现仓库不得抄写或改写这些资产。
2. runner contract 至少定义：规范化 JSON 输入输出、向量步骤顺序、虚拟单调时间、初始持久事实、故障注入动作、预期消息、预期持久化检查点、明确禁止的副作用、最终状态、唯一稳定错误码以及结果文件 Schema。实现仓库可以使用不同测试框架，但必须输出同一结果 Schema。
3. 所有共同运行先验证完整 `ProtocolReleaseIdentity` 和向量集合哈希，再执行用例。缺失、不同或无法重算任一身份分量直接 FAIL，不允许自动下载 `main`、猜测兼容或用本地副本补洞。
4. 共同向量以显式虚拟单调时钟运行。脚本动作只允许确定性的 `advance`、`drop`、`delay`、`duplicate`、`disconnect`、`reconnect`、`crash`、`restart` 和外部适配器预置结果；固定 seed 只用于稳定生成非语义测试数据。墙钟、真实 sleep、线程调度和无记录随机数不得决定 PASS。
5. 比较前只规范化 runner contract 明确允许忽略的非语义字段；MessageId、业务幂等键、revision、hash、顺序、错误码、持久化检查点和时间推进不可被归一化掉。额外发出权威命令、额外业务入账或把 UNKNOWN 猜成成功均为 FAIL。

### 2. 双 Fake 的位置、身份与边界

1. Fake Onboard 由 ControlServer 实现仓库维护，用来驱动 ControlServer-under-test；Fake ControlServer 由 OnboardHmi 实现仓库维护，用来驱动 OnboardHmi-under-test。它们都消费锁定的共同向量，不在共享协议仓库形成第三套业务实现。
2. 每个 Fake 形成 `FakePeerIdentity = {repository, commit, artifactSha256, protocolReleaseIdentity, harnessContractVersion, supportedIntegrationSliceIds}`。显示名称、分支名或包版本不能替代该身份；任一分量变化产生新身份。
3. Fake 必须能够：严格校验协议外壳与 release 身份；按向量重放、重复、乱序禁止项、断线与重启；保存 runner contract 要求的最小模拟持久事实；导出规范化观察轨迹。Fake 不得宣称验证真实车载 IO、锁/光幕、RIoT SDK、MesIngest 数据库、生产事务或真实性能。
4. 同一个向量在本端被测实现与本端 Fake 互换角色时，协议可观察输出、稳定错误码和允许的最终事实必须一致；实现内部事件、线程和表结构不要求一致。

### 3. 一致性判定与运行身份

每次运行必须生成不可改写的 `ConformanceRunIdentity`，至少包含：`runId`、`integrationSliceId`、run kind、ControlServer 完整 commit 与 build digest、OnboardHmi 完整 commit 与 build digest、`ProtocolReleaseIdentity`、适用的双方 `FakePeerIdentity`、runner/harness 版本、向量 ID 集及集合哈希、虚拟时间脚本哈希、非秘密环境／配置摘要、开始和结束时间、`PASS|FAIL|INCONCLUSIVE` 结果。

每个向量逐步同时判定：

- ProtocolEnvelope、payload Schema、方向、correlation 和稳定错误码；
- MessageDeliveryClass、原 MessageId 重试、业务二次键、revision 和 DurableAcceptance；
- 预期输出消息及其顺序、允许不输出的遥测和必须不存在的消息；
- 指令发送前、ACK 前、不可逆动作前和结果补报前的持久化检查点；
- 不可发生的 RIoT 建单、业务提交、开锁范围扩大、READY 授予或重复副作用；
- 最终 VehicleBusinessReadiness、Demand、移动段、仓位业务状态和车载可证明物理状态。

### 4. 稳定 IntegrationSliceId 与精确边界

切片 ID 一经在交接包发布不得改义或复用；内容变化只能增加向量、形成新 protocol release 或新增后缀切片。每个切片 manifest 固定前置切片、适用共同向量、初始持久事实、外部适配器脚本、虚拟时间／故障脚本、允许输入、逐步输出、最终事实、禁止副作用、两端所需能力及证据清单。

| IntegrationSliceId | 能力边界与固定输入 | 必须观察的输出／终态 | 最小共同向量映射 |
| --- | --- | --- | --- |
| `W2G-IS-00` | 精确 release identity、VehicleCredential、空能力/安全/恢复事实；首次连接、重连和恢复途中再断线 | 五步 RecoveryHandshake、积压结果原 MessageId 补报、身份错配拒绝、最终 READY 或具名 RECOVERY_REQUIRED | `CV-SESSION-RECOVERY-HAPPY`、`CV-SESSION-RECONNECT-DURING-RECOVERY`、快照替换/冲突及 envelope 非法向量 |
| `W2G-IS-01` | MesIngest 候选轮次、DemandRevision、单车空闲事实、Fake RIoT 去机台结果 | 唯一 AcceptedDemandSnapshot/DemandId、一次 TO_PICKUP 意图与到站、无重复受理或建单 | Demand/会话消息样例、可靠重试与请求结果重放向量；服务端专属 MesIngest/RIoT 断言作为切片附加输入 |
| `W2G-IS-02` | 机台到站、最新 worklist、扫码 Sublot、ExpectedBasketCount、目标完整仓位集 | `SublotSubmitted` 校验、单一 SlotOperationCommand、全部 OCCUPIED 安全闭环、整批提交；错码/放错不产生额外成功 | `CV-PICKUP-SUBLOT-LOAD`、`CV-LOAD-CORRECTION`、`CV-LOAD-CANCELLATION-ALL-EMPTY` |
| `W2G-IS-03` | 已提交 LoadBatch、有效/过期/不安全发车事实、Fake RIoT 去关卡结果 | 新鲜 PreDepartureSafetyCheck、只在 SAFE 有效期内建立一次 TO_GATE、关卡到站；UNSAFE/UNKNOWN/过期不得移动 | `CV-PREDEPARTURE-SAFETY-EXPIRES`；RIoT 结果未知对账为服务端切片附加断言 |
| `W2G-IS-04` | 关卡到站、车上完整业务状态、无需再次 Sublot/工号/PDA 输入 | 单一完整 UNLOAD、全部 EMPTY/锁闭/输出复位、本地 StopClosureCommit 与 TransportDemandCompletion；不等待或回写 PDA/MES | `CV-GATE-UNLOAD-ALL-EMPTY` |
| `W2G-IS-05` | 在 PREPARED、部分 ActiveUnlockSet、SAFE_FINISH 各检查点断线 | 不扩大开锁集合，安全收尾后暂停，新会话重新握手并按唯一检查点继续或 RECOVERY_REQUIRED | `CV-CONNECTION-LOSS-SAFE-FINISH`、`CV-SESSION-RECONNECT-DURING-RECOVERY` |
| `W2G-IS-06` | ACK、请求响应、RIoT 建单或 OperationResult 的丢失/延迟/重复/异内容脚本 | 同内容原 ID 幂等重放，异内容稳定冲突，未知不猜成功，最终只产生一次副作用 | `CV-RELIABLE-RETRY-SAME-CONTENT`、`CV-RELIABLE-RETRY-DIFFERENT-CONTENT`、`CV-REQUEST-FIRST-RESULT-REPLAY`、`CV-OPERATION-RESULT-UNKNOWN-RECONCILE` |
| `W2G-IS-07` | 在每个 durable-before-send/ack 和车载 ProvenRecoveryCheckpoint 后分别 crash/restart 两端 | 从已证明检查点恢复，业务 ID 与待补报 MessageId 不变，无重复建单/开锁/提交；歧义进入恢复 | `CV-OPERATION-RESULT-UNKNOWN-RECONCILE`、`CV-EXCEPTION-RESUME`、`CV-EXCEPTION-COMPENSATE`、`CV-FAULT-CARGO-HANDOFF`、`CV-FORCED-MECHANICAL-RECOVERY`、`CV-MANUAL-CHARGING-RETURN` |

每个切片除表列轨迹外还必须运行其中所有相关消息的合法/非法向量。纠错、取消、异常恢复、强制机械恢复和人工充电是受影响切片的必跑负向/恢复轨迹，不另造一个可被误解为主旅程的并行业务切片。

### 5. G0～G3 合并与联调门禁

| 门禁 | 必须证明 | 何时阻断 |
| --- | --- | --- |
| G0 契约锁定 | 依赖的是一个内容完整、不可变、批准记录真实且身份精确匹配的 ProtocolRelease | release 缺件、哈希不符、revoked、身份不同或缺少治理要求的真实人员确认时，阻断实现合并和部署 |
| G1 契约自检 | 共享仓库 Schema、样例、错误码、manifest、向量和 runner contract 全部自洽 | 任一共同资产或期望结果失败时，不得发布候选 release |
| G2 本仓组件门禁 | 被测真实本端 + 本仓 Fake 对端跑完受影响切片；另以 Fake-under-test 验证其自身遵循共同向量 | 新实现/修复未覆盖受影响切片、身份不全或存在未解决 FAIL/INCONCLUSIVE 时，阻断本仓合并 |
| G3 跨仓联合门禁 | 精确 ControlServer 候选构建与精确 OnboardHmi 候选构建真实对真实跑同一切片，共享同一 run 证据 | 声明该切片共同完成、进入受控试运行候选或发布任一绑定构建前必须 PASS |

普通、未改变跨端行为的实现 PR 不等待对方移动分支，只需 G0～G2，从而避免跨仓库合并死锁。任何 Schema、字段、错误码、交付、持久承诺、恢复或向量语义变化必须先创建 `ProtocolChangeProposal`，经[决定共享协议仓库的发布内容与变更治理](09-decide-shared-protocol-repository-release-and-change-governance.md)规定的两名开发者本人确认后形成新 release，再重跑受影响门禁；AI、CI 绿灯和原型票豁免均不能代替该确认。

### 6. 完成、失效和失败证据

1. 一个 IntegrationSlice 只有在 G1、双方各自 G2 与绑定同一两端候选的 G3 全部 PASS，身份字段齐全，并且该证据集没有未关闭的 FAIL/INCONCLUSIVE 时，才可标记 complete。
2. 任一端 commit/build digest、ProtocolReleaseIdentity、FakePeerIdentity、runner/harness、向量集合或影响判定的环境配置变化，都使旧完成证据对新候选失效；必须使用新 runId 重跑受影响切片。旧证据仍永久保留。
3. 运行结果只允许 PASS、FAIL、INCONCLUSIVE。环境中断、证据缺失或 runner 自身异常为 INCONCLUSIVE，不得算成功。
4. FAIL/INCONCLUSIVE 必须永久保留：首个分歧步骤、规范化 expected/actual diff、稳定错误码、进程日志与 OnboardTechnicalLog 指针、服务端 BusinessAuditRecord 指针、持久事实快照哈希、禁止副作用检查及后续修复 runId。重跑不得覆盖、删除或改写红色证据。
5. 身份、安全、持久化、恢复顺序、UNKNOWN 对账和禁止副作用失败无手工豁免。确属向量错误时只能按协议治理发布新 release；确属环境失败时修复环境并以新 runId 重跑。
6. G2 对 Fake 通过不能替代 G3，G3 不能替代受控工厂试运行；现场偶然成功也不能倒推切片或协议门禁通过。

### 7. 证据归属与保留

- **共享协议仓库**：保存并随 release 冻结 Schema、manifest、样例、错误码、向量、runner contract、切片到向量的机器索引、G1 结果和真实批准记录；不保存两端生产实现或伪造的批准。
- **ControlServer 实现仓库**：保存 Fake Onboard 源码、ControlServer harness/适配器、锁定 ProtocolReleaseIdentity、G2 结果，以及 MesIngest/RIoT 服务端专属断言与可复现脚本。
- **OnboardHmi 实现仓库**：保存 Fake ControlServer 源码、OnboardHmi harness/适配器、锁定 ProtocolReleaseIdentity、G2 结果和车载技术证据；高频原始 IO/Modbus 日志仍留车载侧并由哈希指针引用。
- **当前 ControlServer 产品验收记录**：作为跨仓库单一索引保存每个 IntegrationSlice 的 G3 `ConformanceRunIdentity`、完整候选构建身份、结果摘要、expected/actual diff、服务端业务审计摘要、双方原始证据 URI/相对路径与 SHA-256、失效/重跑链。实施交接建议规范路径为 `requirements/acceptance/wire-to-gate/integration-slices/<IntegrationSliceId>/<runId>/`；本票只决定结构，不创建实施或假证据。

所有证据只存无秘密配置摘要；VehicleCredential、RIoT 密钥、个人认证证明和原始秘密不得进入向量、日志、diff 或验收索引。

### 8. 本票边界

本票没有开发 ControlServer、OnboardHmi、Fake、runner 或共享协议仓库，没有创建远程仓库，没有运行真实联合测试，也没有宣称首个 ProtocolRelease 或任何两端 commit 已获得真实人员批准。后续实施必须先取得治理规定的真实批准再满足 G0；后续[决定受控工厂试运行配置、执行顺序与验收证据](11-decide-controlled-factory-pilot-configuration-and-acceptance-evidence.md)负责把完成的切片证据作为现场前置门禁，而不能反向放宽本票规则。
