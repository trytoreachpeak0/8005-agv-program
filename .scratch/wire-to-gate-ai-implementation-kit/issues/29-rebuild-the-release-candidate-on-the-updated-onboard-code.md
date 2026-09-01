# 把发布候选更新到车载端 owner 的新代码

Type: task
Mode: HITL
Status: resolved
Blocked by:

## Question

车载端仓 owner 把 `OnboardHmi_MVP` 从 `304e6ad` 推进到 `31263b1`（2026-08-30 20:06，
`Fix production W2G HMI status and recovery visibility`）。票 27 已核实该修复**不在**
`w2g-mvp-rc-0.1.0` 的资产内，并把「需要它必须重建候选」写进了线上发布说明的已知限制第 1a 项。

如何把 RC 更新到该 commit，证明修复确实进了出厂字节而不只是"重新构建了一次"，并给出足以支撑
一次正式发布的验证？

约束：车载端仓对 agent 只读（脚本从一次性克隆构建，本仓对该仓零写入）；不改产品代码；协议仓不动；
0.1.0 的资产在新候选验证通过前不得删除或覆盖；真车动作需要用户逐次授权与现场物理安全 GO。

## Answer

**已发布 `w2g-mvp-rc-0.1.1`**，绑 `ControlServer_MVP@e5ee065`，资产建自
`9daeef4`（服务端，与 0.1.0 同一 commit）+ `31263b1`（车载端，本轮唯一变化）+ `protocol-v0.1.1`。
证据在服务端仓 `evidence/rc/20260831-rc011-onboard-31263b1/`。

### 身份与差异（从产物读回）

| 项 | 值 |
| --- | --- |
| 资产 | `w2g-rc-20260831-31263b1.zip`，123,983,741 B，`727b3fbb…`，868 个文件 |
| `release-manifest.json` | `12a7ce56…`（171,956 B） |
| `SHA256SUMS.txt` | `e607a9d9…`（98,898 B） |
| 协议四字段 | 与 0.1.0 **逐字相同**（只有车载端动了） |

逐文件差异：`controlserver/` 相同 373 / 变更 10、`onboard-hmi/` 相同 465 / 变更 12，无增删。
服务端那 10 项是同一 commit 的重建噪声（票 25 已立「托管构建每次新 MVID」这一事实），
车载端第 12 项是 `appsettings.Production.template.json`——构建脚本已把 `onboardBuildCommit`
填成 `31263b1`。

### 判据一：修复在出厂字节里（元数据级）

`31263b1` 新增的四个符号写进程序集元数据字符串堆，另取两个既有符号作检测器对照：

| 符号 | 0.1.0 产物 | 本候选 |
| --- | --- | --- |
| `ApplyWireToGatePresentationCore`／`ApplyWireToGateOperatorEvent`／`MatchesPersistedResumeState`／`WireToGateHmiBanner` | ABSENT | **PRESENT** |
| `HandleBlockedResumeAsync`／`SubmitSublotAsync`（既有） | PRESENT | PRESENT |

**红侧不空**：同一检索器在旧产物里对既有符号返回 PRESENT，故那四个 ABSENT 是真阴性而非坏读取；
四个符号在 `304e6ad` 源码里 `git grep` 命中 0 文件，故是新增而非改名。

### 判据二：界面对照，同一服务端状态下

隔离实例上先后跑两份车载端，配置逐字相同（只差各自声明的 commit 与 journal 路径），
服务端两次都判 `readiness=RecoveryRequired`：横幅从「连接中—正在等待仓门控制设备和任务系统连接…」
变为「需要恢复—上层会话要求恢复：`DEPARTURE_SAFETY_NOT_READY`」，顶栏「任务系统」从离线变在线。
**会话状态相同、二进制不同，差异只能来自修复。**

### 判据三：现场端到端闭环，generation 8（用户给 GO 后补跑）

原本判据一、二只能证到横幅与状态源，**操作记录投影那一半证不到**（对照里没有业务）。用户选择先补
闭环再发。用户现场安全 GO、操作员 `S0020310`、`dispatchGeneration=8`，把票 14 的脚本
`-ReleaseRoot` 指向本候选：

**`Stage=Completed`、`BlockReasonCode` 空、`SessionGeneration` 全程 1**，`08:43:15Z→08:52:54Z`。
Demand `18b7d18f…`，取货 `N2-4_N3-4`(20) → 关卡(210)，一筐。两条真单各建一次、五步审计各自齐全
（共 10 条），`Load`／`Unload` 均 `Committed`（子批 `Q26085155-5`），`hostStderrEmpty=true`、
端口全回收、`trustRemaining=0`。

四张截图逐节点证明 HMI 在跟随业务：到站→`收到子批录入请求：Q26085155-5。`；装货→`1号仓操作完成`
→`结果已被服务端确认`→**`收到重复仓位命令，已保持原结果重放，未再次执行仓门IO。`**；完成→卸货同样
投影。最后一条把「可靠重放」也证进了界面。顶栏「到站」与「发车安全」全程跟随安全闸门。

### 其余闸门

两端构建 0 warning；扫描闸门 PASS（秘密 0、密钥材料 0、UNRESOLVED 仅三个具名 RIoT SDK 包）；
868 条哈希 `OK=868 MISMATCH=0 MISSING=0`，**证明会红**（对副本追加一字节即 GREEN→RED，产物未被改）；
隔离安装 PASS（9 项检查）、卸载 PASS（服务与目录移除、根证书移除 1 张、端口零残留），
生产服务 `8005 AGV ControlServer` 全程 Running 未受影响。

### 新发现（外观级，归车载端只读仓，未在任何仓写入缺陷记录）

操作记录面板混用两个时区：「系统」启动行是本地时间（`16:43:12`），`31263b1` 新增的
「操作」／「成功」行是 UTC（`08:45:21` 等），业务条目看起来比其上方的启动条目早八小时。
四张截图里都可见。不阻断，仅在服务端仓的 SUMMARY 里具名留档。

### 边界（本票不成立的部分）

- **真实八仓 IO 与车载目标终端硬件仍未取得资格**：闭环里 IO 是模拟器 `127.0.0.1:1502`，
  车载端跑在开发工作站上。这两条与 0.1.0 时相同。
- **0.1.0 已知限制第 3 项（服务端正确性依赖对端对重复快照再次 ACK）未在 `31263b1` 上重新核对。**
- **`RecoveryRequired` 无操作员出口（票 27 的 1b）仍未决**，是跨端结果身份缺口，仍在 Out of scope。
- 车载端默认 `appsettings.json` 的 `onboardBuildCommit` 仍是 `a6f05fb…`
  （`declaredBuildCommitMatchesBuild=false`），归只读仓；随包 Production 模板已是正确的 `31263b1`。
- **车载端仓对应 `31263b1` 的 tag 不在本轮范围内**，需该仓 owner 自行创建；该仓已有的
  `w2g-mvp-rc-0.1.0` 指向 `304e6ad`，不可复用。
- 本仓对车载端只读仓**全程零写入**（仅 fetch 与只读阅读），协议仓未动。
- 0.1.0 的 release、tag 与三个资产**一字未改**，两份候选并存于桌面。
- 未触产品代码，故未跑 tier 1。
