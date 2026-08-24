# R09 MES 与 SDK 架构决定调查

## 范围、证据口径与结论

本报告只调查无损清单 `batch_id=R09` 的 18 个文件：9 个 MES ADR、8 个 RIoT SDK ADR、1 个全库 ADR 索引。清单记录位于 `.scratch/current-requirements-baseline/evidence/material-inventory/material-inventory.tsv:174-191`。逐文件重算 SHA-256 后与固定清单 18/18 一致，调查时这些路径全部 `tracked-clean`；R09 内 74 个 Markdown 链接均解析到现存文件。

证据判断遵循当前基线治理规则：权威需求必须同时具备**具名授权人、可核查日期、适用范围、具体版本/哈希**，实现、文件位置、措辞和表面合理性均不能赋予权威性（`.scratch/current-requirements-baseline/issues/01-authority-and-classification-evidence-rules.md:13-22`）；文档内的独立条目还须分别记录来源链和确认状态（`.scratch/current-requirements-baseline/issues/04-atomic-requirement-approval-granularity.md:13-19`）。

结论：

- **当前需求基线可批准项：0/18。** 17 个 ADR 都写 `Status: accepted`，但没有记录谁作出/接受决定、接受日期、授权身份、适用项目/站点/软件版本、被接受的文件版本或哈希。唯一可具名的人是 Git 作者 Zhengyu Shao；这只证明提交主体，不证明其拥有业务、客户、外部接口或安全批准权限。索引也没有批准信息。
- **工程上仍是当前设计护栏。** 仓库代理规则要求开发前阅读相关 ADR、遇到冲突必须显式标记（`docs/agents/domain.md:5-11,33-37`），故这些 ADR 对当前仓库实现具有程序性的工程参考地位；这与“能否进入需求基线”是两个不同问题。
- **7 个明显含业务/外部约束，必须回到需求基线逐条核实：** ADR-mes-0001～0006、ADR-mes-0008。它们决定自动取消/不取消、人工介入、充电失败自动改派、选桩、重试上限、MES 幂等/GONE/抑制语义、客户 SQL/DDL 边界等可观察系统行为，不只是内部代码形状。
- **5 个混合决定，须拆开处理：** ADR-mes-0007、ADR-sdk-0001、ADR-sdk-0003、ADR-sdk-0007、ADR-sdk-0008。技术栈、Facade 形状和“不内置 Wait”可留在地图目的地之外；但其中的 Oracle/客户 SQL/凭证约束、生产鉴权默认、业务必需能力范围、可再派判定和产品非目标要回到需求/外部约束或安全批准核实。
- **5 个主要是地图目的地之外的本地设计选择：** ADR-mes-0009、ADR-sdk-0002、ADR-sdk-0004、ADR-sdk-0005、ADR-sdk-0006。它们分别选择内部同步协议、SDK seam、双语言交付、异常表现和 Kiota 生成方式；只要没有被承诺给外部消费者，不应作为客户需求直接收入基线。若接口已对外承诺，则其公开契约部分需单独送审。
- **1 个索引：** `docs/adr/README.md` 只提供分类与链接，不形成独立决定或需求。

以上分类不否认设计价值，也不提前批准或否决任何原子条目。

## 形成、迁移、替代与版本历史

### 2026-07-23：最初形成

提交 `e6dc9eadc62a7a2415268602ed88bb13f8caa6ee`（作者 Zhengyu Shao）首次加入：

- `mes/docs/adr/0001`～`0005`，即当前 ADR-mes-0001～0005；
- `rcs/riot-sdk/docs/adr/0001`、`0003`～`0009`，即当前 ADR-sdk-0001～0008（中央化后编号发生偏移）；
- 同一提交还大规模更新行为实验知识、SDK Facade、生成代码和两语言测试。

在该提交的父版本中搜索当前标题未找到持久化前身。ADR 与实现/测试同一提交形成，只能证明共同形成时间，不能证明先有独立批准再实现。

### 2026-07-27：中央化与新增

提交 `ffe1f49e70ade8a9e2e2ef74fc922e5ce7c8917c`（作者 Zhengyu Shao）把 ADR 统一迁入 `docs/adr/`：

- MES-0001～0005 为 100% rename；
- SDK-0001/0002/0004～0008 为 100% rename；SDK-0003 为 82% rename，实际差异仅把旧 ADR 编号和实现文档链接改为中央目录的新编号/路径，决定内容未改变；
- 新建 ADR-mes-0006、ADR-mes-0007 和中央 `docs/adr/README.md`。

旧 SDK 编号 `0002`、`0010` 同次迁为 `ADR-cross-0001/0002`，所以当前 SDK 编号不能脱离迁移史与旧链接机械比较。

### 2026-07-31：MES 语义扩展

提交 `493ac5a89cb89daf1f8c090ef6091b8d006180be`（作者 Zhengyu Shao）：

- **实质修改** ADR-mes-0006：明确 `TASK_TYPE+SUBLOT` 同时承担接入对账键和调度永久抑制键、GONE 后同键再现产生新 `demand_id` 但不表示新需求、MesIngest 不读取调度抑制；
- 新建 ADR-mes-0008、ADR-mes-0009；
- 更新中央索引。

同一提交还修改 `BR-012`，所以当前 ADR-mes-0006 与 BR-012 的一致性证明“共同编辑”，不能证明其中一方是经批准的权威上游。

### 当前实现与发布绑定

- SDK 当前代码和方法表确实实现这些设计：`rcs/riot-sdk/docs/facade-v1.md:1-18,29-78` 列出两语言入口、能力、异常与非目标；C# 默认 CallApiKey 见 `rcs/riot-sdk/csharp/RIoT.Sdk.Facade/RiotSession.cs:11-45`，可再派辅助见 `rcs/riot-sdk/csharp/RIoT.Sdk.Core/ReadyForNextOrder.cs:3-19`。但 Python 包版本仍为 `0.1.0`（`rcs/riot-sdk/python/pyproject.toml:5-8`），ADR 的“V1”没有绑定 release/tag/包哈希；C# 工程也未记录与这些 ADR 对应的显式产品版本。
- SDK OpenAPI 生成流程会在上游 spec 缺少版本时填入通用 `1.0.0`（`rcs/riot-sdk/scripts/preprocess_openapi.py:1-8,95-103`），因此生成物中的该值不能充当现场 RIoT 产品/API 版本证据。
- MesIngest 当前实现对应 ADR-mes-0006～0009：阶段一链路和只读 API 见 `mes/ingest/csharp/README.md:1-29`，恢复/单线程轮询见 `:48-63`，Oracle/Service/WPF 边界见 `:65-89`，工厂包明确“已就绪不等于工厂已签字通过”见 `:121-127`。ADR-mes-0009 的 48 小时/410/24 小时规则也存在于当前代码（`mes/ingest/csharp/MesIngest.Core/DemandChangeFeed.cs:56-87`、`mes/ingest/csharp/MesIngest.Core/DemandListQuery.cs:38`）。这些实现提交晚于 ADR，并发生过修复；只能证明当前代码适配，不能反向补批准。
- 未发现 ADR-mes-0001～0005 的 MES 调度编排实现；当前仓库只有相关 SDK 能力、行为实验、术语和 draft UC/BR。故这五条更接近目标策略，而非可由已运行代码证明的当前业务行为。

## 一手来源与范围限制

### RIoT 行为实验能证明什么

`rcs/riot-behavior-lab/knowledge/behavioral-contracts.md:1-3` 自限为只收录可指向证据的现场观察。与 R09 直接相关的来源包括：

- BC-AUTH-002：CallApiKey 在 2026-07-20 对 imap/device **只读**探针有效，写接口、权限范围和密钥轮换/过期仍开放（`rcs/riot-behavior-lab/knowledge/behavioral-contracts.md:18-33`）。它支持 SDK 可使用该鉴权方式，但不能独自批准生产写控制面默认使用同一密钥。
- BC-STATE-003：本测试车/map29 成功路径观察到“物理到站早于订单 SUCCESS”，可再派应等待 SUCCESS + IDLE；取消/失败路径未覆盖（同文件 `:158-169`）。它支持判定辅助的外部事实，不批准 SDK/MES 分层或阻塞策略。
- BC-ORDER-013：现场观察支持拉取本车积压、取消 QUEUEING/HELD、等待 IDLE 后再派（同文件 `:269-280`）。它不决定 Stall 超时应报警、人工处理还是自动取消。
- BC-ORDER-015/018：现场观察支持 HANG 原因、HangContinue 成功码不等于已离开 HANG、单机任务占用时须等待（同文件 `:320-354`）。它不批准充电失败应自动改派、重试次数或何时转人工。

这些实验记录有环境时间、测试车/地图/现场基址等局部范围，但没有绑定当前生产 RIoT 软件/固件/API 版本；所以应被视为限定环境的外部行为证据，不是永久接口保证。

### MES 来源能证明什么

- `mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:5-10` 声称客户 IT 提供/批准查询对象、筛选和执行窗口，但未附具名 IT 批准人、记录、范围或 SQL 哈希；其任务接入规则位于 `:44-68`。
- 查询目录明确 `MES_TASK_UNION` 的“最后证据尚未迁入”，并警告这不表示已验证或未验证（`mes/catalog/queries.md:1-12`）；查询元数据的 `requires_approval=false`（`mes/queries/mes-task-union/query.toml:1-7`）不是客户批准记录。
- 五类/第六类客户 SQL README 只称为客户原始快照，并自限为差异比较、需求研究和实验基线，不能作为运行时回退（`mes/sources/customer/2026-07-16/mes-task-original-queries/README.md:1-17`、`mes/sources/customer/2026-07-24/mes-task-original-queries/README.md:1-17`）。
- `BR-012` 仍为 draft（`requirement-documents/02-business-rules/br-012-mes-task-idempotency-and-reconciliation.md:1-10`），虽与 ADR-mes-0006/0008 对 GONE、抑制、全快照与只读约束一致（`:17-63`），没有更高批准级别。

因此 R09 能建立仓库内派生/一致性关系，不能建立客户或业务批准链。

## 逐文件调查台账

分类代码：`R` = 含必须返回需求基线核实的业务/外部约束；`M` = 混合本地设计与待核实约束；`L` = 主要为地图目的地之外的本地设计选择；`I` = 索引。所有条目批准四要素均缺失，决定批准范围均为空。

| 文件与固定身份 | 形成/来源/替代关系 | 决定主体、当前适用性与分类 |
| --- | --- | --- |
| `docs/adr/mes/0001-queueing-stall-handling.md:1-7`<br>SHA-256 `9b915792d3760cdaf7d400465325fb9a08458cc261cc1b885e327f3715037573` | 7/23 在旧 MES ADR 目录形成，7/27 100% 迁移。BC-ORDER-013 只支持清积压事实；预防、超时只报警、不自动 CANCEL 是新增策略。 | 决定人未知；未见调度实现。`R`：取消/人工介入是业务行为；还须与 draft UC-008 的“RIoT 队列 0/1”口径核对（`requirement-documents/03-use-cases/04-transport-task-dispatch/uc-008-dispatch-move-order-to-riot.md:93-105`）。 |
| `docs/adr/mes/0002-order-hang-handling.md:1-7`<br>SHA-256 `49947c628ab8857d80410034e3c4742d1ff40ba7cb7d1fddbe77882343d3bd8c` | 7/23 形成，7/27 100% 迁移。BC-ORDER-015/018 支持 HANG/HangContinue 观察；原因分支、自动尝试、失败不自动取消是策略。其“充电人工或改派”由 0003～0005进一步冻结，未正式标注 superseded。 | 决定人未知；当前术语文档沿用，调度未实现。`R`：异常恢复/自动化边界须逐原因批准。 |
| `docs/adr/mes/0003-charging-hang-auto-reassign.md:1-7`<br>SHA-256 `ad9d0bc14fe9238cbefac143633c3e519953936b48f47ca5c6e0ef5514b37467` | 7/23 形成，7/27 迁移。没有直接 Source；以旧单先 CANCEL、确认终态再新建为架构+业务策略。细节由 0004/0005补充。 | 决定人未知，未实现。`R`：它填补 UC-012 明列的“充电过程中途异常如何处理”TBD（`requirement-documents/03-use-cases/05-agv-charging/uc-012-manually-dispatch-agv-to-charge.md:116-124`），必须回基线确认。 |
| `docs/adr/mes/0004-charge-hang-station-selection.md:1-7`<br>SHA-256 `51fbf15af5f375f514193b0828940db23076e0e8bf2fb87b7fe344b51b74022a` | 7/23 形成，7/27 迁移。NearStationQuery 有实验/SDK 能力基础；“允许集合、排除失败站、按路径最近”未链接批准源。 | 决定人未知，未实现。`R`：须与 draft BR-007 的候选有效、占用/预占、电量优先规则共同裁决（`requirement-documents/02-business-rules/br-007-charging-pile-allocation-and-queueing.md:17-48`），不能只凭本 ADR省略可用性条件。 |
| `docs/adr/mes/0005-charge-hang-retry-limit.md:1-7`<br>SHA-256 `5ab612f7fb60728c16d1fe2861f292b5318cff01cb5798afb007f309e40ee8f2` | 7/23 形成，7/27 迁移；`N=2` 无引用来源或测量依据。 | 决定人未知，未实现。`R`：可观察的自动重试/转人工阈值，须由业务/运维确认；不要与 UC-012“下发失败重试次数 TBD”擅自合并，两者失败阶段可能不同。 |
| `docs/adr/mes/0006-mes-ingest-vs-dispatch.md:1-18`<br>SHA-256 `aa6fa0fa0a46068326fa8db94d9ea53c6605d30aa205a3d5bcd4c77b5bb18e04` | 7/27 新建；7/31 实质扩展同键再现、`demand_id`、永久抑制和反向依赖语义，与 BR-012 同次修改。 | 决定人未知；当前 MesIngest 已实现边界。`R`：模块拆分是本地设计，但幂等键、GONE、抑制、不得派车等是业务规则，须按当前 7/31 哈希逐条送审，不能由共同提交或实现批准。 |
| `docs/adr/mes/0007-mes-ingest-tech-stack.md:1-18`<br>SHA-256 `88db8ba2b0b50bb1016e7a9b310e558fa73d45455ec6d14e7eabd62c0bceb923` | 7/27 新建；“团队要求全 C#”无具名来源。Service/WPF/SQL Server/Thin+Thick/查询复制已在当前实现落地。 | 决定人未知。`M`：技术栈与部署形状留在基线地图之外；Oracle 11g、客户 SQL 唯一原稿、工厂探针、凭证不入库是外部/运维/安全约束，须分别取证。当前 README 明确工厂链路未因能力就绪而自动通过（`mes/ingest/csharp/README.md:65-85,121-127`）。 |
| `docs/adr/mes/0008-full-source-snapshot-incremental-local-projection.md:1-16`<br>SHA-256 `06379baf4f4ed06e8e372df95fc4e6a32cd74512bcae6768609437221627b1c5` | 7/31 新建。与 BR-012 全快照/GONE/只读方向一致；“客户批准 SQL”没有绑定批准记录或 SQL 哈希。 | 决定人未知；当前实现采用全源快照+本地差异/分页。`R`：全快照是可靠消失语义的业务数据约束；不改客户 SQL/DDL 是外部授权边界；本地索引/分页是设计选择。必须拆条。 |
| `docs/adr/mes/0009-demand-change-feed-and-authoritative-bootstrap.md:1-16`<br>SHA-256 `99b6d3d4ebf6ab5df5c47bde9f5a4dac7e1554957b7738b8b2836cfd7abde92c` | 7/31 新建；实现于同日晚些时候并后续修复。无外部消费者批准记录；ADR 自述当前无旧外部消费者。 | 决定人未知；当前代码实施 48h/410/24h。`L`：目前是内部同步/API 技术契约；若下游已把 API 当外部契约，保留期、Bootstrap replace、高水位和错误码需另行版本化批准。 |
| `docs/adr/README.md:1-3,65-90`<br>SHA-256 `49a805fc9be26bf4acc9bfc562774398e041b8714376a56c7aea0e2a73ae174b` | 7/27 新建中央索引，7/31 加 MES-0008/0009；还索引大量不在 R09 的 cross ADR。 | 无独立决定主体。`I`：当前导航入口，不形成需求或批准，不向所链接 ADR 传递权威性。 |
| `docs/adr/sdk/0001-default-auth-callapikey.md:1-7`<br>SHA-256 `d0efa10157d914e362b7e3a72a4f0504646ad980d5819f3cde848366f1d2a6c8` | 7/23 在 SDK 目录形成，7/27 100% 迁移。来源 BC-AUTH-002 只验证 imap/device 只读；ADR 扩展为调度/MES 长连接默认。 | 决定人未知；C#/Python 已实现。`M`：SDK 默认选择可留在设计层，但生产写控制面是否可用 CallApiKey、权限/轮换/过期/密钥托管必须由 RIoT 外部契约与安全负责人确认并绑定版本。 |
| `docs/adr/sdk/0002-v1-seam-session-named-methods-raw-escape.md:1-7`<br>SHA-256 `c676158d2d879db5cfeb783123a8b5cd78f782081b4d103f41c05b88be9784a8` | 7/23 旧编号 0003形成，7/27 100% 迁移并改为当前编号。无业务来源，权衡稳定 Facade 与实验逃逸。 | 决定人未知；当前两语言实现具名入口与 Raw。`L`：本地 SDK seam；Raw 稳定性警告是开发契约，不是客户需求。 |
| `docs/adr/sdk/0003-v1-facade-method-scope.md:1-9`<br>SHA-256 `f671068c455fdc0b7e124d8c431f3e4d85bce7a8565ddd404948066fc487e6a6` | 7/23 旧编号 0004形成并与大批 SDK 代码/测试同提交；7/27 82% rename 仅修正 ADR 编号/链接。来源分散于行为 BC、cross ADR 和 MES闭环设想。 | 决定人未知；当前方法表与实现基本一致。`M`：Facade 形状是设计；取消、急停、HangContinue、调度启停等为何属于第一版必需能力是产品/安全范围，应回基线核实。实现清单不是批准。 |
| `docs/adr/sdk/0004-v1-csharp-python-parity.md:1-7`<br>SHA-256 `1619fb27412eff51837e57e8911aa45f85cc710b84143797e0bce8555f534914` | 7/23 旧编号 0005形成，7/27 100% 迁移。无客户/交付合同来源，只称两端同步和共用 fixtures/BC。 | 决定人未知；两语言当前均存在。`L`：本地交付/维护策略；若 C# 与 Python 双端是外部承诺，应另找合同/发布批准，不由本 ADR证明。 |
| `docs/adr/sdk/0005-facade-throws-on-business-failure.md:1-7`<br>SHA-256 `a9b5792e94b61ac0cbdcd7078b8fc1a587fb592479ce7118722051c1be7e6206` | 7/23 旧编号 0006形成，7/27 迁移。外部事实来自业务 `code` 观察和 RouteCost `-1`；异常统一方式是 SDK 设计。 | 决定人未知；当前两语言实现并有测试。`L`：本地 API 错误模型；具体 RIoT 成功码/领域结果仍须按观察环境和版本限制使用。 |
| `docs/adr/sdk/0006-imap-via-kiota.md:1-7`<br>SHA-256 `2d9af13839cc3c2ac82821c6ba1e9893b617cdb08a7eb5f73f555d64863a3c22` | 7/23 旧编号 0007形成，7/27 迁移。imap spec 和生成代码同期开通；无上游 spec 版本或厂商批准记录。 | 决定人未知；当前 generate 管线包含 imap。`L`：Kiota 与不手写旁路是本地代码生成选择；外部 imap 契约必须用真实 spec 哈希/RIoT 版本绑定，不能用预处理补出的 `1.0.0`。 |
| `docs/adr/sdk/0007-ready-helpers-no-blocking-wait.md:1-9`<br>SHA-256 `ca82a0226601eec928492ab69342a0915f473c01a4069830afea13c617527fdd` | 7/23 旧编号 0008形成，7/27 迁移。BC-STATE-003 支持 SUCCESS+IDLE 的局部外部事实；“SDK 不阻塞、MES 编排超时”是分层选择。 | 决定人未知；辅助已实现。`M`：不内置 Wait 属本地设计；可再派条件和 MES 必须承担轮询/超时属于业务/外部接口候选，须按失败/取消路径补证和批准。 |
| `docs/adr/sdk/0008-v1-explicit-non-goals.md:1-5`<br>SHA-256 `b8c68b23afd8e33149f7bc0c720265eb3552dd209888baef112da08f81aa2034` | 7/23 旧编号 0009形成，7/27 迁移。无产品范围来源；列出 interrupt、建单路径、Wait、发现接口、DSL、密钥轮换等排除项。 | 决定人未知；当前方法表沿用。`M`：作为 SDK V1 内部 scope 可留在设计层；若任何排除项影响已批准业务/安全/运维能力，必须回需求基线，不可凭 ADR 单方缩减承诺。 |

## 需回基线核实的原子候选

后续不应整份批准 ADR，而应至少拆出：

1. QueueingStall 的建单前检查、清积压范围、超时阈值、报警/人工介入、禁止自动取消与 PriorityExec 的适用边界。
2. 普通 OrderHang 各原因的自动 HangContinue 条件、状态复核、失败后人工处理及禁止自动取消；充电 HANG 与普通 HANG 的分界。
3. 充电 HANG 是否自动改派、旧单终态确认、备用桩可用性/占用/预占核验、Near 选择、最多两次和用尽后的责任人。
4. `TASK_TYPE+SUBLOT`、`demand_id`、VISIBLE/GONE、同键再现、调度永久抑制、不得绕过抑制的业务含义和适用阶段。
5. MES 完整快照、只读事务、不得改客户 SQL/DDL、客户批准 SQL 的具体 QUERY_ID/哈希/执行窗口/Oracle 环境。
6. 生产 RIoT 鉴权方式、CallApiKey 的读写权限、轮换/过期、密钥保管和目标 RIoT 版本。
7. 第一版产品真正需要的 RIoT 能力（取消、急停、调度启停、Hold/Continue/HangContinue、Map/Station 等）、可再派判定与失败路径。
8. 若 MesIngest ChangeFeed 或 SDK 双语言/非目标已对外交付，另建公开接口/交付范围版本与批准记录；否则保持为本地设计，不进入需求基线。

## 后续证据请求

1. 提供每条 ADR 的决定记录：具名决策人及其授权身份、决定日期、适用 8005/站点/阶段/软件版本范围、绑定 ADR SHA-256 或 Git commit；若只批准技术实现，不得把范围扩大为业务批准。
2. 为 ADR-mes-0001～0005 提供业务/运维对异常恢复和充电改派的会议或书面确认，并与 UC-008、UC-012、BR-007 的 draft/TBD 逐项对账。
3. 为 ADR-mes-0006/0008 提供客户 IT 批准的 `MES_TASK_UNION` 不可变 SQL/QUERY_ID 哈希、Oracle 版本/权限、完整快照与禁止 DDL 的授权记录；不要用 `requires_approval=false` 或目录声明替代。
4. 为 SDK ADR 提供目标 RIoT 产品/固件/API 版本、OpenAPI 原始文件哈希和生产读写探针；安全负责人批准 CallApiKey 权限、轮换、存储和失效处置。
5. 给 ADR 增加可审计的 supersedes/superseded-by 关系，至少明确 MES-0002 的充电分支被 MES-0003～0005如何细化，以及 SDK 旧编号到中央编号的迁移表；不得仅凭新编号推断替代。
6. 将实现/测试证据保留为“当前代码与设计一致”的验证附件，与业务批准、客户外部约束批准和工厂验收分别记录。
