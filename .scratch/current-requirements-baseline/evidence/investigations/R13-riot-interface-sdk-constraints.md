# R13 — RIoT 外部接口与 SDK 约束调查

## 结论

本调查逐项覆盖 R13 无损清单的 **26/26** 份材料。按用户 **2026-08-03** 的范围指示，两份供应商 PDF 在本次当前需求基线中均为 **OUT-OF-SCOPE / ignored source**：只保留清单身份、SHA-256、Git 勘误和已完成的 PDF 核验记录，不从中提取或晋升任何项目契约。剩余 24 份材料也没有一份同时具备“明确来源、适用厂商/环境版本、捕获时间、项目适用范围、批准证据”；因此本批次可直接进入当前需求基线的外部接口约束为 **0 条**。

剩余材料能支持的仅是分层事实：项目接入说明是未经批准的项目说明；物模型问题清单是本地分析与阶段性 SDK/应用决策；14 份 Swagger JSON 是某次静态接口快照；4 份 SDK specs 是其中 4 份快照的逐字节副本；1 份 normalized spec 是生成输入；3 份 SDK 文档是 SDK 产品设计/测试说明。E03 行为实验只能支持其记录环境内的观察，E04 生成物和转储只能支持实现/生成现状。**不得由任一实现、生成物、实验现象或既有 SDK 设计反推项目需求。**

## 调查边界与方法

- 票据：[25-investigate-riot-interface-sdk-constraints.md](../../issues/25-investigate-riot-interface-sdk-constraints.md)。R13 清单批次为 26 份、5,532,722 bytes，初始角色为 `candidate-external-constraint=12; current-state-evidence=14`（[batches.md](../material-inventory/batches.md)，第 49 行）。这些是待调查角色，不是调查结论。
- 固定快照以无损清单的路径、SHA-256、大小和捕获时间为准；本次重新计算 26 份现存文件 SHA-256，结果 **26/26 一致**。
- Git 身份先叠加 [git-status-corrections.tsv](../initial-snapshot/git-status-corrections.tsv)；勘误只修复 Git 身份，不提高材料权威性或批准状态（[git-status-correction.md](../initial-snapshot/git-status-correction.md)，第 24、35–41 行）。
- 分层标签：`IGN` 用户明确忽略；`PN` 项目说明；`LA` 本地分析/决策；`SS` 静态 schema 快照；`SD` schema 副本；`ND` 生成用派生物；`DS` SDK 设计/测试。分层计数为 `IGN=2, PN=1, LA=1, SS=14, SD=4, ND=1, DS=3`，合计 26。
- “批准”专指当前项目需求/约束的具名批准。Git 作者、实验执行授权、厂商署名、代码存在和测试通过均不等于项目需求批准。

## Git 状态与形成史

原始快照把两个 PDF 和物模型问题清单误记为 `untracked`；R13 correction overlay 的 **3 条**记录把它们修正为 `tracked-clean`。固定 HEAD 中对应 blob 分别为 `0317b78c…`、`7ab426b4…`、`547e8a01…`。其余 R13 路径沿用原始状态；`rcs/riot-sdk/specs/.normalized/imap.json` 的有效快照状态仍是 `untracked`，当前又被 `.gitignore` 忽略，不能因当前工作树看起来 clean 而改写捕获时身份。

`git log --follow` 表明：项目接入说明、原始 Swagger、两个 PDF 和物模型问题清单最迟在 2026-07-13 的初始提交中出现；接入说明 2026-07-16 又修改。SDK README/smoke/facade 与四份 specs 在 2026-07-15 至 2026-07-27 间继续形成；normalized imap 没有 Git 形成史。提交作者均为 Zhengyu Shao，但提交记录没有说明需求批准人、批准范围或目标环境，故只证明仓库形成史。

## PDF 排除记录

两份 PDF 已按 PDF 技能完成全量文本提取与相关页渲染/视觉核验，随后遵从用户范围决定，不再把手册语义用于基线判断：

- [文档_RIoT_V2.0.7_软件接口手册_CN_V1.0_20230510 (3).pdf](../../../../rcs/riot_documents/%E6%96%87%E6%A1%A3_RIoT_V2.0.7_%E8%BD%AF%E4%BB%B6%E6%8E%A5%E5%8F%A3%E6%89%8B%E5%86%8C_CN_V1.0_20230510%20%20%283%29.pdf)：123/123 页文本提取；视觉核验页 1、3、5、13、16–17、63–66、72–74、85、92–93、108、110、114–115。
- [Riot对外接口文档.pdf](../../../../rcs/riot_documents/Riot%E5%AF%B9%E5%A4%96%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.pdf)：38/38 页文本提取；视觉核验页 1–3、5、13–14、16、26、29、32、34–35、38。

这些动作只证明文件可读且完成了视觉 QA；**不构成内容采纳、版本适用或项目批准**。临时提取和渲染目录在终检后删除。

## 24 份在范围材料的证据判断

### 项目接入说明与物模型清单

[01-rcs-intro.md](../../../../rcs/01-rcs-intro.md) 第 8–25 行描述网页端/API 用法、`172.19.206.222:8888`、`admin/admin`、登录 token 与 Swagger 地址。这是项目内接入说明，但没有作者身份、批准人、适用设备/站点/发布版本或捕获方式。它不能把示例地址、共享管理员凭据或全部 Swagger 能力变成项目需求；明文默认凭据还应由后续安全/配置决策处理。

[物模型枚举问题清单](../../../../rcs/riot_ithing_model/standard.oasis.300ul/standard.oasis.300ul-%E7%89%A9%E6%A8%A1%E5%9E%8B%E6%9E%9A%E4%B8%BE%E9%97%AE%E9%A2%98%E6%B8%85%E5%8D%95.md) 第 3、30–65 行记录来源 TSL、缺号、不一致和无取值说明字段；第 67–72 行是建议；第 74–80 行是“当前阶段决策”。这些是本地分析/设计边界，不是厂商契约或项目批准需求。尤其“未知值原样透传/记录”“禁止业务依赖未说明 code”可作为保守 SDK 设计候选，但仍需由适当责任人确认；黑盒观察也只能形成有环境范围的观察证据，不能反推出权威枚举含义。

### OpenAPI 与 SDK specs

14 份 `rcs/riot_swagger/*.json` 均声明 OpenAPI 3.0.3、同一 server `http://172.19.206.222:8888` 和 `Authorization` header apiKey，但全部缺失 `info.version`。清单捕获时间约为 2026-07-06，首次 Git 提交为 2026-07-13；没有捕获脚本/manifest 把这批 schema 绑定到一个已核实的 RIoT 产品 build、厂商发布物或项目环境。因此它们只能证明“仓库保存了这批静态接口声明”，不能证明目标现场行为、权限、错误语义或项目获准使用范围。

四份 `riot-sdk/specs/{device,imap,order,task}.json` 与对应 raw Swagger **逐字节同哈希**，不是四份独立来源。`.normalized/imap.json` 与 raw imap 的 34 个 paths / 41 个 operations 数量相同，但属于本地预处理生成物；其中 `info.version=1.0.0` 是预处理缺省值，不得解释为 RIoT 产品/API 版本。接口存在也不代表应用获准调用，尤其不能把管理、写操作和危险操作自动纳入项目范围。

### SDK 设计与测试说明

[facade-v1.md](../../../../rcs/riot-sdk/docs/facade-v1.md) 第 1–17、76–80 行定义 V1 facade、默认 CallApiKey 和明确非目标；[SDK README](../../../../rcs/riot-sdk/README.md) 第 21–25、50–105 行定义生成/封装范围和示例基址 `172.10.1.72:8888`；[smoke-test.md](../../../../rcs/riot-sdk/docs/smoke-test.md) 第 24–32、100–118 行定义 smoke 环境和离线处理。它们属于 SDK 设计/测试说明。特别是 C# 未配置现场环境时可直接返回并计为通过，Python 可跳过，故“smoke 通过”本身不证明现场 API 可用。

接入说明/Swagger 的 `172.19.206.222` 与 SDK/行为实验常用的 `172.10.1.72` 没有环境映射证据。这不是可自行裁决的地址冲突，而是缺失环境、用途、有效期和维护人信息；基线只能要求外部化配置与环境映射，不应固化任一地址。

## E03 / E04 交叉证据边界

- E03 自身规定 Swagger/TSL 是 `SCHEMA`，不能证明现场版本、状态转移、幂等、错误码和副作用；单次观察不能推广到所有版本/环境（[sources/README.md](../../../../rcs/riot-behavior-lab/sources/README.md)，第 7–33 行）。其总 README 还明确区分 evidence、knowledge、fixtures 与业务需求（[README.md](../../../../rcs/riot-behavior-lab/README.md)，第 16–26、55–62 行）。
- round 1 计划把目标平台记为 `v2.2.0.30`，且标注为“事后补记”；同时明确 OpenAPI `info.version` 缺失（[round-plan.md](../../../../rcs/riot-behavior-lab/evidence/rounds/2026-07-15-round-1/round-plan.md)，第 5–13 行）。第 15–25 行的批准只授权那一轮实验写操作，不批准需求、SDK facade 或生产调用范围。
- E03 的 [behavioral-contracts.md](../../../../rcs/riot-behavior-lab/knowledge/behavioral-contracts.md) 记录了有范围的登录、CallApiKey、车辆/地图、建单、到达、取消、在线/离线、优先级和急停观察，并保留未验证项。它可用于提出待确认契约或设计防御，但不能替代厂商/项目权威决定；尤其 CallApiKey 的权限、轮换、失效与跨 API 适用性没有被普遍证明。
- E04 的 endpoint dump、Kiota lock、生成代码和包元数据只证明当时的 schema 处理/生成现状；`_imap_dump.txt` 甚至只保留了一次语法错误。生成模型仍属 `SCHEMA`，手写逻辑不自动成为现场事实，更不能从 SDK 当前方法集反推项目必须支持的方法集。

## 26/26 覆盖与哈希终检

| # | 材料 | SHA-256 | 有效状态 | 分类 | 结论 |
|---:|---|---|---|---|---|
| 1 | [rcs/01-rcs-intro.md](../../../../rcs/01-rcs-intro.md) | `b40f96da995b13b85f48e9e8cef6d2f03328b1357ce0f3fc583b7a8848025d9f` | tracked-clean | PN | 未批准项目说明 |
| 2 | [软件接口手册 PDF](../../../../rcs/riot_documents/%E6%96%87%E6%A1%A3_RIoT_V2.0.7_%E8%BD%AF%E4%BB%B6%E6%8E%A5%E5%8F%A3%E6%89%8B%E5%86%8C_CN_V1.0_20230510%20%20%283%29.pdf) | `5567b423be0dde5d5646396c416d15b97afcce5ecd362070b9dc835c0950635e` | tracked-clean（勘误） | IGN | 用户指示忽略 |
| 3 | [Riot 对外接口 PDF](../../../../rcs/riot_documents/Riot%E5%AF%B9%E5%A4%96%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.pdf) | `a051ad61b4442e52d7516929bab284cff17b33f81a0370af37a41f8050d1e68b` | tracked-clean（勘误） | IGN | 用户指示忽略 |
| 4 | [物模型枚举问题清单](../../../../rcs/riot_ithing_model/standard.oasis.300ul/standard.oasis.300ul-%E7%89%A9%E6%A8%A1%E5%9E%8B%E6%9E%9A%E4%B8%BE%E9%97%AE%E9%A2%98%E6%B8%85%E5%8D%95.md) | `bd0dd90f974288fa8f6246543ff78ddff2dd86d3f33a5872512fcfbee677415b` | tracked-clean（勘误） | LA | 本地分析/阶段决策 |
| 5 | [configfile.json](../../../../rcs/riot_swagger/configfile.json) | `eefea9b4fbe48df169eb04d251ae004e62caf3a927d14c18068d789b67cd1d1b` | tracked-clean | SS | 静态 schema |
| 6 | [device.json](../../../../rcs/riot_swagger/device.json) | `e35dad335c0d82663159ac5778337ff3aaae3f128bf5686318bf1fe75b8b9217` | tracked-clean | SS | 静态 schema |
| 7 | [fcs.json](../../../../rcs/riot_swagger/fcs.json) | `c00fc09b4c84d45578b1781926b61397f19dde392fe985928f2893d146fc645b` | tracked-clean | SS | 静态 schema |
| 8 | [ifttt.json](../../../../rcs/riot_swagger/ifttt.json) | `eaa03c94c6509c3c3b5313ca002fde4b042e5dc0077ef3105a95366af8d25608` | tracked-clean | SS | 静态 schema |
| 9 | [imap.json](../../../../rcs/riot_swagger/imap.json) | `253c5747586b9c7d9ca798c75a74193081e837a01167c6db7a20b78e8dd1a6d6` | tracked-clean | SS | 静态 schema |
| 10 | [ithings.json](../../../../rcs/riot_swagger/ithings.json) | `e812eea395ecc48af268d370fb00872e505eb616e6e361a0914affd5cd7d192f` | tracked-clean | SS | 静态 schema |
| 11 | [logfile.json](../../../../rcs/riot_swagger/logfile.json) | `0c74f952c9216a4d35c6aa1f4e320dd1587a6a876eb7220949a846388608b18d` | tracked-clean | SS | 静态 schema |
| 12 | [metric.json](../../../../rcs/riot_swagger/metric.json) | `aba547573197d9f3891ff1d55019278580de86ca1c50107668caea5c9ef5c190` | tracked-clean | SS | 静态 schema |
| 13 | [order.json](../../../../rcs/riot_swagger/order.json) | `e364ffac680582f9cbdf3b3b7f4055486bd88bbcb20370bcf55889ca54efd038` | tracked-clean | SS | 静态 schema |
| 14 | [secuirty.json](../../../../rcs/riot_swagger/secuirty.json) | `abb1eb572371e6eb44df0a6419c20de7db04a101bd5bc5dc9f1c138f2c491b74` | tracked-clean | SS | 静态 schema；保留原拼写 |
| 15 | [system.json](../../../../rcs/riot_swagger/system.json) | `a022916f06f330d5458430420a77f868f9b816964148de4d44a8ca3b811c4d50` | tracked-clean | SS | 静态 schema |
| 16 | [task.json](../../../../rcs/riot_swagger/task.json) | `050a612e21ebe01b95d6fa35ca54d592bd83e108b69f5eb0703d8b903274d6d1` | tracked-clean | SS | 静态 schema |
| 17 | [tool.json](../../../../rcs/riot_swagger/tool.json) | `3323fb81a4d321b1eb8703140f113f947a0634f8d64b14337d3b46853d6ddaa4` | tracked-clean | SS | 静态 schema |
| 18 | [version.json](../../../../rcs/riot_swagger/version.json) | `acccc01ec233f13d7ba86bf052a35ffcbaa043eadc23887a6f3ae86ad0699aea` | tracked-clean | SS | 静态 schema |
| 19 | [facade-v1.md](../../../../rcs/riot-sdk/docs/facade-v1.md) | `defd2a49141a43ed55a664f81d445f54bfebca7f367e59ff951e6bb734650dcb` | tracked-clean | DS | SDK 设计 |
| 20 | [smoke-test.md](../../../../rcs/riot-sdk/docs/smoke-test.md) | `4746824a85634ff24831556c28762b7c3a154bddab5602de9594f96c8a07bf0c` | tracked-clean | DS | 测试说明；非现场通过证据 |
| 21 | [riot-sdk/README.md](../../../../rcs/riot-sdk/README.md) | `fca234946c9bc0b082e2bda58a378faa9b2178547db1566f4d8d42c71725b8d2` | tracked-clean | DS | SDK 范围/用法设计 |
| 22 | [.normalized/imap.json](../../../../rcs/riot-sdk/specs/.normalized/imap.json) | `7a23019d348489ae73da4048eddc8e19526285a37683b8e9871458b0ae8e3340` | untracked（现 ignored） | ND | 本地生成输入 |
| 23 | [specs/device.json](../../../../rcs/riot-sdk/specs/device.json) | `e35dad335c0d82663159ac5778337ff3aaae3f128bf5686318bf1fe75b8b9217` | tracked-clean | SD | raw device 的字节副本 |
| 24 | [specs/imap.json](../../../../rcs/riot-sdk/specs/imap.json) | `253c5747586b9c7d9ca798c75a74193081e837a01167c6db7a20b78e8dd1a6d6` | tracked-clean | SD | raw imap 的字节副本 |
| 25 | [specs/order.json](../../../../rcs/riot-sdk/specs/order.json) | `e364ffac680582f9cbdf3b3b7f4055486bd88bbcb20370bcf55889ca54efd038` | tracked-clean | SD | raw order 的字节副本 |
| 26 | [specs/task.json](../../../../rcs/riot-sdk/specs/task.json) | `050a612e21ebe01b95d6fa35ca54d592bd83e108b69f5eb0703d8b903274d6d1` | tracked-clean | SD | raw task 的字节副本 |

## 待补证据与基线建议

1. 为真实目标环境补一份受控接口快照 manifest：捕获人/时间、RIoT build、环境用途、base URL 标识（不写秘密）、各 schema 哈希和厂商/项目适用性确认。
2. 由项目责任人审批 API 白名单、读写权限、鉴权/轮换/失效、错误处理、重试/幂等和安全边界；Swagger 中存在的 API 默认不授权。
3. 为 productKey `standard.oasis.300ul` 取得有版本的原始 TSL 与枚举/错误码权威说明；在此之前维持“未知值透传、不得据无文档 code 做业务判断”的防御性设计，但不要把它冒充外部契约。
4. 建立环境映射，解释 `172.19.206.222` 与 `172.10.1.72` 的用途、所有者和有效期，并把地址/凭据外部化。不得继续把 `admin/admin` 当作可批准的生产配置。
5. 需求地图中把“项目必须做什么”与“SDK 当前做什么”“现场某轮观察到什么”分别建边；只有经具名批准、版本和范围齐备的项目/外部约束才能进入当前基线。

## 终检

- R13 清单覆盖：**26/26**；现存文件 SHA-256 与无损清单一致：**26/26**。
- Git correction overlay：**3/3** 条已应用；未把 normalized imap 的真实 `untracked` 身份误改。
- 分类计数：`2+1+1+14+4+1+3=26`；批准进入当前基线的外部约束：**0**。
- R13 五份 Markdown 源中的链接扫描：本地链接 **20/20** 可解析，另有 2 个外部 URL；本调查未联网验证示例服务地址。
- 本报告所列 26 个材料链接均逐项对应清单路径；两份 PDF 保留覆盖但不参与内容判断。
