# 发布并交接可运行 WIRE_TO_GATE MVP

Type: task
Mode: HITL
Status: resolved
Blocked by: 12

## Question

如何创建并回读三个远程仓库的正式 tag/release，发布经过批准的安装物与哈希，并把安装、配置、启动、停止、健康检查、日志、恢复、回滚、已知限制和支持责任交给使用者，使其无需旧会话即可实际运行本次 MVP？

交接必须证明远程 release 可访问、干净环境安装可复现、ControlServer 与 OnboardHmi 报告同一 ProtocolReleaseIdentity、核心端到端场景 PASS；真实硬件或现场未获资格时必须醒目标记，不得把受控测试可用扩大为工厂生产可用。

开发文档可以随软件附带，但不能成为交付主体，也不能替代任何失败的软件门禁。最终交付判定是“程序能安装、运行并完成规定业务闭环”，而不是“AI 可以开始开发”。

## Answer

**已发布。** 用户在本会话给出发布 GO（票 12 的授权来自上一会话，本会话另取一次当轮确认），
tag 名沿用票 12 拟定的 `w2g-mvp-rc-0.1.0`。

发布地址：<https://github.com/trytoreachpeak0/8005-agv-control-server/releases/tag/w2g-mvp-rc-0.1.0>
（`release_id=379271369`，`draft=false`，`publishedAt=2026-08-30T12:11:11Z`）。

### 实际创建了什么

| 对象 | 值 | 回读来源 |
| --- | --- | --- |
| annotated tag | `w2g-mvp-rc-0.1.0`，tag 对象 `0c4d1103…` | `ls-remote` + `git/ref/tags` |
| tag 目标 commit | `9daeef4325fccf094767b689fa484d8e1e414042` | GitHub `git/tags/0c4d1103…` 的 `object.sha` |
| 该 commit 的身份 | **就是 `origin/ControlServer_MVP` 当前 tip** | `git/ref/heads/ControlServer_MVP` 返回同一 sha |
| Release | 该仓**唯一**一个 release，非 draft、非 prerelease | `gh release list` 只有一行 |
| 资产 | 3 个，全部 `state=uploaded` | `gh release view --json assets` |

**注意一处易被误读的字段**：`gh release view` 报 `targetCommitish=main`。那是 GitHub 在 tag
不存在时用来建 tag 的分支字段；本次 tag 先于 release 创建，实际绑定以 tag 对象为准，已由上表第 2、3
行独立证实为 `9daeef4`。不要把它读成「release 绑在 main 上」。

资产与哈希：

| 资产 | 大小 | SHA-256 |
| --- | --- | --- |
| `w2g-rc-20260830-81cb9cf.zip` | 123,976,762 B | `d40c8ab1e041e168b6f8ee701fb9529009dabbaa20e9d0f7654fc10f35e8f6eb` |
| `release-manifest.json` | 171,955 B | `c18babe4ff749bdfcde92d04e9d426a85c3fe0cde92a73fb26abfec08b699fc6` |
| `SHA256SUMS.txt` | 98,898 B | `487403e2cb00ca8f3008fecd09e134b1fe3ee6fd5552f2fbfa780885d3b9f448` |

zip 是 869 个条目、解压后 283,001,315 字节（与源目录逐字节同量），单个顶层目录
`w2g-rc-20260830-81cb9cf/`。

### 包内一个字节未改

票 12 的硬约束是「上传前不得修改包内任何文件」。取证方式是**在打包前后各跑一次全量校验**：

- 打包前：`OK=868 MISMATCH=0 MISSING=0`，两个根哈希与票 12 记录逐字相同；
- 打包后（同一源目录）：`OK=868 BAD=0`。

**手册第 11 节的 `dispatchGeneration` 更正写在包外的 Release 说明第 6 节**，正是为了不触发这 868
条哈希的重建。

### 票 15 四条判据的取证

**判据一：远程 release 可访问。** 不是靠「上传返回 0」，而是**下回来重算**。
`gh release download` 取回三个资产（16 秒），逐个 SHA-256 与发布说明宣称值 **MATCH**；
红侧把期望值翻一字符 → **MISMATCH**，比对路径证明会响。

**判据二：干净环境安装可复现。** 端到端走了一遍下载方的路径：远程资产 → 解压到全新目录 →
**照手册第 3 节原文脚本**跑校验 → **输出 0 行**（`SHA256SUMS.txt` 共 868 行，全部一致）。
红侧在解压副本里翻掉 `RELEASE-CANDIDATE.md` 的一个字节 → 同一脚本输出**恰好 1 行**
`MISMATCH RELEASE-CANDIDATE.md`，随后还原。安装本身的可复现性由票 14 的干净安装验收承担
（23 PASS / 0 FAIL，管理员运行的服务安装与卸载各 PASS）；本票新增的是「从 release 拿到的字节
就是被验收的那份字节」这一环。

**判据三：两端报告同一 ProtocolReleaseIdentity。** 票 12 只读了服务端侧，本票补上车载端侧。
车载端配置文件**不携带**协议哈希，但二进制内嵌了：

| 字段 | 值 | 服务端 `appsettings.json` | 车载端二进制 |
| --- | --- | --- | --- |
| `repositoryCommit` | `1531489e…` | 声明 | `SQCD.Agv.Contracts.dll` PRESENT |
| `manifestSha256` | `a467c0c4…` | 声明 | `SQCD.Agv.Infrastructure.dll` PRESENT |
| `schemaBundleSha256` | `e04296e9…` | 声明 | `SQCD.Agv.Contracts.dll` PRESENT |
| `vectorsSha256` | `fc5902b7…` | 声明 | **ABSENT** |

前三个字段逐字一致。第四个**据实记录为不一致的一侧**：测试向量哈希是构建期资产，车载端运行时
不需要，因此不携带——这不是漂移，但也不能笼统说成「两端完全一致」。
车载端相关类型名 `AcceptedProtocolReleaseIdentity` / `ExpectedProtocolReleaseManifestSha` 佐证该值
参与握手校验而非只是留痕。**红侧**：三个真值各翻一字符全部 ABSENT；一个确实不在包内的真值
（`vectorsSha256`）也 ABSENT——同一检索方法既能报 PRESENT 也能报 ABSENT，绿不是空的。
静态绑定之外的动态证据是票 14 的现场闭环：正是这一对二进制握手成功并跑完 generation 7。

**判据四：核心端到端场景 PASS。** 票 14 的 generation 7 在 RC 生产形态下 `Stage=Completed`
（取货 → 多仓装货 → 发车安全 → `TO_GATE` → 关卡批量卸货 → 原子完成，5 分 42 秒，两条真单各建
一次，10 条审计齐全）。本票未重跑，也未动车——发布与交接不需要动车。

### 交接内容与位置

票 15 要求交出的十项（安装、配置、启动、停止、健康检查、日志、恢复、回滚、已知限制、支持责任）
**主体在包内 `RELEASE-CANDIDATE.md` 第 1～13 节**，它自称「不需要任何原开发会话的上下文」，本票
逐节核对了标题结构确实覆盖这十项。Release 说明只做包内做不到的三件事：版本绑定与资产哈希、
原样携带六项已知限制、承载那条**包外**的手册更正。

Release 正文回读确认关键串全部 PRESENT：协议 manifest 哈希、zip 哈希、车载端 commit、
`DisabledRuleGateway.IsConnected`（已知限制第 1 项）、`upperId` 公式（第 6 节更正）、
「未取得工厂生产资格」。正文 10,068 字节。

**票 27 的车载端 HMI 缺陷已作为已知限制第 1 项原样进入发布说明**，并标注「去向尚未落定；落定后
回补」——用户明确选择不等票 27 先发布。票 27 落定后需回来更新这一条。

### 明确没做的事

- **车载端仓 `8005-agv-onboard-hmi` 未创建 tag 或 release。** 该仓对 agent 只读。核对确认它
  **零 release、零 tag**（tags namespace 返回 404），即本会话对它零写入。票 15 问句里的「三个远程
  仓库的正式 tag/release」因此**只完成两个**：服务端本次发布，协议仓 `protocol-v0.1.1` 早已发布
  且本次未动（核对确认仍只有 `protocol-v0.1.0`、`protocol-v0.1.1` 两个 tag）。车载端那一份只能由
  用户或王昆自行创建，已开票 28 承载。
- **未修改包内任何文件、未重建 RC、未触产品代码**，故按 `AGENTS.md` 未跑 tier 1。
- **未动车、未建单。** 服务端随包三个 runtime 开关出厂 `enabled=false`。

### 未被本次发布消解的限制

发布说明第 5 节六项原样在列，其中两项是硬资格边界，必须继续按「受控测试可用 ≠ 工厂生产可用」
对待：随包 HMI 对现场操作员不可用（票 27），真实八仓 IO 与车载目标终端硬件未取得资格。
