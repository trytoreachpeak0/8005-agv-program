# 协作工作流

8005 AGV 项目由两个人推进。本文是**跨仓库协作的权威文档**：人读这一份，agent 读各
仓库 `CLAUDE.md` 里内联的规则（两边内容必须一致，改了这里就要同步过去）。

## 谁做什么

| 仓库 | 负责人 | GitHub |
| --- | --- | --- |
| `8005-agv-onboard-hmi` | Kun Wang | `SocialKKKK` |
| `slots-simulator` | Kun Wang | `SocialKKKK` |
| `8005-agv-control-server` | Zhengyu Shao | `trytoreachpeak0` |
| `8005-agv-protocol` | **共同维护** | 双方 |

其余仓库（`8005---AGV`、`8005-workspace`）是 Zhengyu Shao 的项目治理与工程环境记录。

## 协作单位：integration slice

不要自己发明推进单位。`8005-agv-protocol/integration-slices/index.json` 已经定义了
`W2G-IS-00` 到 `W2G-IS-07` 八个切片，每个带 `sequence` 和 `prerequisites`。**切片是
有序的，所以"现在推进到哪"永远有唯一答案。**

每个切片的 `gates` 数组正好就是分工：

| Gate | 谁跑 | 内容 |
| --- | --- | --- |
| `G1` | 双方共用 | 协议内容清单与审批签名校验（`pnpm g1`） |
| `CONTROL_SERVER_G2` | Zhengyu Shao | 服务端单端 + Fake Onboard，绑定精确 manifest 哈希 |
| `ONBOARD_HMI_G2` | Kun Wang | 车载端单端，同样绑定 |
| `G3` | **两人一起** | 双端联调，绑定两端精确 commit |

两边的 G2 之间**没有依赖，可以完全并行**。这是并行度的唯一来源。

## 推进节奏

1. **看板**：`8005-agv-protocol` 仓的 GitHub Project 是唯一的进度真相来源。每个
   integration slice 一张卡，四道门禁做成自定义字段。
2. **按 `sequence` 顺序推**，`prerequisites` 未满足不开工。这个依赖关系已经在
   `index.json` 里，不需要口头协调。
3. **两边各自过 G2**，互不阻塞。
4. **两边 G2 都绿了才约 G3**。G3 需要两人同时在场，是最贵的资源；用 G2 的绿灯当准入
   条件，避免约了才发现对方没准备好。
5. **G3 发现的问题按下节分流。**

## 反馈通道：三类问题走三条路

| 问题 | 提到哪 | 必须附什么 |
| --- | --- | --- |
| 协议契约有歧义或错误 | `8005-agv-protocol` 的 issue | 触发它的 `vectorId`，以及双方各自的理解 |
| 对方实现不符合契约 | **对方仓库**的 issue | **先跑 G3 拿证据**，附上 evidence 目录路径 |
| 自己仓库的活 | 自己仓库的 issue | 不用惊动对方 |

第二类的格式不用新造，`8005-agv-control-server/docs/defects/` 已经在用：文件开头一行
`Found by:` 加一条指向 G3 证据 `SUMMARY.md` 的链接。

**核心纪律：跨仓库指控必须带可复现的门禁证据，不能只是"我这边跑不通"。**没有证据的
问题先自己排查，或者先在 protocol 仓开 issue 讨论契约理解。

## 改 protocol 的规则

`8005-agv-protocol` 是唯一双方共有的仓库，但**决定权归 Zhengyu Shao 一个人**
（2026-09-02 定，此前的双人事先批准门控已取消）。

代替事先批准的是**事后通知**——协议是 Kun Wang 那一端据以实现的契约，而发布会作废他的
门禁证据，所以他必须知道每一次改动：

- **每次推送后，在 `8005-agv-protocol` 开一个 issue @`SocialKKKK`**，写清三件事：
  1. 改了什么；
  2. 影响哪些 `W2G-IS-*` 切片；
  3. 他的 `ONBOARD_HMI_G2` 证据是否作废。
- **通知和推送要在同一次工作里完成**，不能拖到以后。
- **发布（打 tag）仍然需要双人签名**，走
  `attestations/release-approval.template.json` 那套机制：完成的 attestation 不进 git，
  作为 GitHub Release Asset 上传。详见 `docs/release-governance.md`。
  **AI 和 CI 不能批准。**这一条管的是打正式 `ProtocolRelease`，不是日常提交。
- `main` 分支开了保护：**禁止 force push、禁止删除分支**，但不要求 PR，可以直接推。

### 协议发布很贵，改动要攒批次

`docs/release-governance.md` 原文：补丁发布 *"invalidates affected G1/G2/G3 evidence"*。

**协议一发新版，两边的 G2 证据全部作废，都要重跑。**已经发生过一次：`W2G-IS-01` 在
`protocol-v0.1.1` 里被重新映射到 `CV-DEMAND-ACCEPT-TO-PICKUP`，旧 `v0.1.0` 的 G2 证据
不能继承。

所以**协议改动必须攒批次发**，不要零敲碎打——每一次小改都在让对方重跑整套门禁。

## 语言约定

写进 GitHub 的东西用中文：README、文档正文、issue 标题与正文、PR 标题与正文、
commit message 正文。

保持英文：

- commit 的 conventional 前缀（`feat:` `fix:` `docs:` `chore:`）
- 标识符、路径、命令、环境变量、错误码
- 门禁与切片名（`G1`、`CONTROL_SERVER_G2`、`W2G-IS-00`）
- 协议消息名、schema 字段、`vectorId` —— **它们是契约的一部分，改不得**
- 引用报错和测试输出时先贴英文原文，再用中文解释

不回溯改旧的。现有英文 commit 和 README 留在原地。

## agent 指令落在哪

Agent 只会自动加载**当前工作仓库根**的指令文件，不会跟着链接跨仓库读。所以每个仓库的
`CLAUDE.md` 里**内联**了它自己需要遵守的协作规则，本文是给人读的完整版。

| 仓库 | agent 指令文件 | 状态 |
| --- | --- | --- |
| `8005---AGV` | `CLAUDE.md` | 已有，含协作节 |
| `8005-agv-control-server` | `CLAUDE.md` | 已有，含协作节与门禁定义 |
| `8005-agv-protocol` | `CLAUDE.md` | 已有，含协作节与发布规则 |
| `8005-agv-onboard-hmi` | 由 Kun Wang 决定 | 建议放一份对应的 |
| `slots-simulator` | 由 Kun Wang 决定 | 建议放一份对应的 |

**改了本文就要同步各仓 `CLAUDE.md` 的协作节**，否则 agent 按旧规则行动。
