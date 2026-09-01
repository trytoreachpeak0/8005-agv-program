# 进程崩溃重启 runner 归位并重绑

Type: task
Mode: AFK
Status: resolved
Blocked by: 19

## Question

「进程崩溃重启」向量由独立脚本 `run-staged-g3-no-movement.ps1` 负责，该脚本有两处问题：
绑定 `ControlServer cc6e2b9` + `OnboardHmi 0455147`，比当前双端落后两代；且位于规划仓
`.scratch/wire-to-gate-ai-implementation-kit/evidence/g3/`，而非归属仓。如何把它归位到
ControlServer 仓并重绑到 `3d8b00c` + `304e6ad`，取得当前 commit 下的重启向量证据？

### 与票据 18／19 的关系

本票只碰这一个独立脚本，不修改 `scripts/run-staged-g3.ps1`，与 18／19 无文件冲突。排在 19 之后
是为了保持单一前沿串行推进，不是技术依赖——若需调整顺序，直接改 `Blocked by` 即可。

### 位置决定（已定，2026-08-29 用户确认）

**搬到 ControlServer 仓 `scripts/` 下，保持独立脚本**，不并入主 runner：

- 主 runner 体量大（票据 18／19 交付后已达 2400 余行）；重启向量需要反复起停服务端进程，与其
  单进程 TLS 探针模型冲突，并入会让两种生命周期纠缠。
- 独立带来的绑定漂移问题（本票的成因），改为让两个脚本引用同一处 commit 常量来解决，而不是靠
  合并脚本。

执行时不需要再就此征询。若实施中发现共享常量确实不可行，可改走合并路线，但必须在本票记录
推翻该决定的具体理由。

### 票据 19 交付后可直接复用的事实

- 共享绑定来源的落点已明确：主 runner 的 commit 常量在 `param()` 块的默认值里
  （`$ControlServerCommit` 等四项），本票要建立的共享来源就是这四个默认值。
- 秒级回路仍然有效且已被证明能省下整轮 staged 运行：解析＋编译 harness、在本机发布的
  ControlServer 上直接跑探针、把 runner 的断言段原样抽出喂真实产物再做单点变异。票据 19 靠这三步
  在正式运行前抓完所有问题，正式运行一次通过。
- `-InstallTemporaryCurrentUserRoot` 每次运行都会弹 Windows 安全警告，需用户在场点确认；
  本票脚本为 plaintext loopback，不需要该授权，因此可以无人值守跑。

### 范围

- 脚本迁入 ControlServer 仓，从规划仓 `.scratch/` 移除。
- 重绑到 `3d8b00c` + `304e6ad` + `fb5f7c5` + `1531489e`，与主 runner 共享绑定来源。
- 重跑并断言：session generation 在「全新首连 → 车载重启复用 journal → 服务端重启复用数据库」
  三阶段稳定递增，每阶段后无意外 generation 变化，跨重启复用同一 Demand、车辆租约与消息身份。

### 完成判据

重启向量断言 PASS 且绑定 `3d8b00c` + `304e6ad`；脚本在 ControlServer 仓且规划仓不再保留副本；
证据归档于 ControlServer 仓 `evidence/g3/`，票据只留路由指针。

### 注意

不动车、不建单、不使用现场凭据。该脚本为 plaintext loopback，不需要临时根证书授权。

## Answer

脚本已归位为 ControlServer 仓 `scripts/run-staged-g3-restart.ps1`（保持独立，未并入主 runner，
位置决定未被推翻），规划仓 `.scratch/` 下的 `run-staged-g3-no-movement.ps1` 已删除。二十条断言
在 `3d8b00c` + `304e6ad` + `fb5f7c5` + `1531489e` 下全部 PASS。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server
Owner artifact: `evidence/g3/20260830-process-restart/SUMMARY.md`
Published branch/commit: `ControlServer_MVP@3c699d9`（已推送、回读一致）

### 共享绑定来源怎么落的

不是把四个 commit 抄一份，而是**解析主 runner 的 `param()` 块读回默认值**：
`Get-SharedCommitBinding` 用 `[Parser]::ParseFile` 取 `$ControlServerCommit`、`$OnboardCommit`、
`$SimulatorCommit`、`$ProtocolCommit` 四个 `StringConstantExpressionAst` 默认值，校验为 40 位小写
SHA-1，任一项缺失、非字面量、大小写或长度不符即抛错。来源文件路径与其 SHA-256 一并写入
`configuration.json`，绑定的出处可审计。本票脚本不接受 commit 参数覆盖——留了覆盖口就等于留了
漂移口。

顺带证出一条：PowerShell 的 `-match` / `-notmatch` **默认大小写不敏感**，`'^[0-9a-f]{40}$'` 会放过
大写 SHA。主 runner 自己那段 commit 校验也是这个写法，本票内未改（不属本票范围）。

### 断言分组（二十条）

| 组 | 断言 |
| --- | --- |
| 绑定 | 四 commit 取自主 runner 默认值；运行中的服务端在 `SessionAccepted` 自报 `serverBuildCommit = 3d8b00c`；运行中的车载在 `SessionHello` 自报 `onboardBuildCommit = 304e6ad` 与固定 instance id；`/version` 与 `SessionRecoveries.ProtocolCommit` 均为 `1531489e` |
| 代际 | 全新库起于 1；车载重启 +1；服务端重启 +1；每阶段十二次逐秒采样代际不变；无 peer 提前退出 |
| 重启真实性 | 阶段二只换车载进程、阶段三只换服务端进程，且被替换者已确认退出；连接身份每连接一个 |
| 持久身份 | 服务端库文件复用；车载 journal epoch 跨重启不变；两端存储的重启前行原样保留；三条 `RecoveryStateReport` 的 messageId 在两端是同一集合且全部已 ack；`SessionRecoveries` 每 AGV 单行 |
| 安全 | 十张副作用表全 0、`/health/ready` 503、readiness `RecoveryRequired`；secret scan |

### 三条本轮亲证的事实

**一、`serverInstanceId` 是每连接一个，不是每进程一个。** `OnboardMessageProcessor` 注册为
`Scoped`，`OnboardTcpServer` 每接受一条连接开一个 scope。三次会话必然三个 id，无论服务端有没有
重启，所以它**不能**用来证明进程重启。重启事实只能由 OS 进程身份承担（阶段间 PID 变化 + 被替换
进程已退出）。

**二、车载 journal 有一个持久 epoch，且它是消息身份的种子。**
`WireToGateJournalMetadata.JournalEpoch` 由 `INSERT OR IGNORE` 一次性生成，
`SafetyStateChanged` 的 dedup key 形如 `safety-state-changed:{epoch}:{version}:{observedAt}`。
journal 一旦被重建，epoch 变、派生 id 全变——这就是「跨重启复用 journal」最直接的可证伪判据，
比比对文件时间戳硬。

**三、Demand 与车辆租约在本形态下不可达。** `VehicleDispatchLeases` 以 `DemandId` 为主键，
不建单就没有租约行。票据范围里的「跨重启复用同一 Demand、车辆租约」因此无法在不动车不建单的
运行里取证，已具名记入 `configuration.json` 的 `vectorsNotReachableWithoutAnAcceptedDemand`，
与票据 18 的 `OperationResult`、`SlotOperationCommand` 归入同一类，随带 demand 的运行一并取证。

### 两次作废运行（均为 runner 缺陷，非产品 FAIL）

1. `Invoke-SqliteRows` 只匹配到一行时返回裸 `[ordered]`，`rows[0]` 变成按位取值 → 三条读
   `SessionRecoveries` 的断言在数据库其实正确时变红；同一次运行暴露了上面第一条事实。
2. 上一条的修复 `return ,$rows` 让函数以单个对象输出数组，外层残留的 `@()` 又套深一层，
   journal epoch 前后两次读取都成了 `null`。

两次都是断言抓到的。正式绿运行的 runner 身份为 `9def7f8`，起跑时工作区干净。

### 秒级回路（沿用票据 19 的方法，本轮再次奏效）

`Check-RestartRunner.ps1`（解析 + 抽出 `Get-SharedCommitBinding` 喂真实主 runner，四条绑定变异）
与 `Check-RestartAssertions.ps1`（按首行／停行从 runner 抽出真实的推导段与断言段再
`Invoke-Expression`，二十条基线 + 三十条单点变异全部检出）。第二次红之后补进的
`session rows arrived unwrapped` 变异精确复现了第一次那三条误红。踩到的坑：fixture 里
before/after 若共用同一批 `[ordered]` 引用，子集比较会恒真——必须深拷贝。

### 遗留的一处，不在本票范围

规划仓 `.scratch/wire-to-gate-ai-implementation-kit/evidence/g3/20260826-staged-no-movement-cc6e2b9-0455147/`
仍保留一份 `runner.ps1` 快照。它是那次已被本运行取代的旧运行的冻结证据，不是可执行脚本，
本票只删除了 live 脚本。若要按跨仓规则把历史证据一并迁走或删除，需另开一票。
