# RIoT 目标环境与受控接口快照补证记录

## 目的与边界

本记录用于解决“补齐 RIoT 目标环境与受控接口快照证据”：把仓库现有 RIoT OpenAPI 静态文件绑定到可核查的环境、产品 build、捕获过程和 8005 项目适用范围。它只建立外部接口证据身份，不批准任何 API 的项目调用权限；API 白名单、鉴权和调用安全仍由后续独立票据决定。

本记录不得保存用户名、密码、token、CallApiKey、cookie、私钥或其它秘密。base URL 只使用环境标识；下列 IP 因已存在于受版本控制的项目说明、schema 和实验材料中，仅作为待映射的既有证据引用，不新增凭据。

## 仓库已能证明的事实

- `rcs/riot_swagger/` 中有 14 份 OpenAPI 3.0.3 JSON；全部缺少 `info.version`，并声明同一个 server `http://172.19.206.222:8888`。
- 这批文件的无损材料清单捕获时间约为 2026-07-06，最迟在 2026-07-13 首次进入 Git；仓库没有保留原始捕获命令、捕获人、源系统 build 或批准记录。
- 行为实验与 SDK 文档常用 `http://172.10.1.72:8888`；Round 1 把 RIoT 平台版本记为 `v2.2.0.30`，但明确标注为事后补记。用户于 2026-08-03 最终确认该测试环境地址为 `172.10.1.72`、build 为 `2.2.0.30`；其初次答复中的 `172.19.1.72` / `v2.2.014` 已由用户明确修正并保留在确认链中。
- 行为实验能证明其记录时点的有限观察，不能自行证明 14 份 schema 来自同一环境或适用于同一 build。
- `172.19.206.222` 与 `172.10.1.72` 之间的实例关系、用途、所有者和有效期在仓库中均未建立。不得根据地址、文件时间或调用成功自行推定。

## 项目方确认的环境映射与剩余歧义

用户的结构化确认见 [RIoT 环境与接口快照用户确认](riot-environment-and-snapshot-user-confirmation-2026-08-03.md)。若地址已失效，也要保留其历史用途和有效期，不删除该行。

| 环境标识 | 既有证据中的 base URL | 环境名称与用途 | 系统/环境所有者 | 有效期 | RIoT build | 与另一地址的关系 | 当前 8005 是否使用 | 确认者与日期 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RIOT-8005-RUNTIME` | `http://172.19.206.222:8888` | 8005 项目真实运行时 RIoT | 软件人员和实施人员（角色已确认，个人未具名） | 永久；仅现场网络可达 | `v2.2.0.14` | 与测试环境为不同现场、不同实例 | 是 | 用户本人，2026-08-03 |
| `RIOT-CROSS-PROJECT-TEST` | `http://172.10.1.72:8888` | 另一项目 RIoT；曾用作 8005 API 测试环境 | 软件人员和实施人员（角色已确认，个人未具名） | 永久；须通过对应网络、VPN 或 5G 模块访问 | `2.2.0.30` | 与 8005 环境为不同现场、不同实例 | 仅作 API 测试，不是 8005 真实运行时 | 用户本人，2026-08-03 |

“与另一地址的关系”必须明确选择并解释：同一实例换址、同一实例的不同网络入口、不同环境、不同实例/版本，或仍未知。不得只写“旧/新地址”而不说明实例和版本关系。

## 现存 OpenAPI 静态快照清单

下表固定当前 14 份原始字节。用户已确认这些文件由其本人于 2026 年 7 月初从 `RIOT-8005-RUNTIME` 手动导出，适用于 8005，源 build 为 `v2.2.0.14`；同一套 OpenAPI 客户端后来用于 `2.2.0.30` 环境的 riot-lab 行为测试，测试环境 build 不改变快照来源。精确导出日和逐项导出步骤未知，不得用 Git 作者或文件时间代填。

| 文件 | 字节数 | SHA-256 | schema server | source environment/build |
| --- | ---: | --- | --- | --- |
| `rcs/riot_swagger/configfile.json` | 2,242 | `eefea9b4fbe48df169eb04d251ae004e62caf3a927d14c18068d789b67cd1d1b` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/device.json` | 57,858 | `e35dad335c0d82663159ac5778337ff3aaae3f128bf5686318bf1fe75b8b9217` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/fcs.json` | 247,955 | `c00fc09b4c84d45578b1781926b61397f19dde392fe985928f2893d146fc645b` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/ifttt.json` | 33,016 | `eaa03c94c6509c3c3b5313ca002fde4b042e5dc0077ef3105a95366af8d25608` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/imap.json` | 45,355 | `253c5747586b9c7d9ca798c75a74193081e837a01167c6db7a20b78e8dd1a6d6` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/ithings.json` | 75,895 | `e812eea395ecc48af268d370fb00872e505eb616e6e361a0914affd5cd7d192f` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/logfile.json` | 2,599 | `0c74f952c9216a4d35c6aa1f4e320dd1587a6a876eb7220949a846388608b18d` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/metric.json` | 2,177 | `aba547573197d9f3891ff1d55019278580de86ca1c50107668caea5c9ef5c190` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/order.json` | 76,114 | `e364ffac680582f9cbdf3b3b7f4055486bd88bbcb20370bcf55889ca54efd038` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/secuirty.json` | 63,290 | `abb1eb572371e6eb44df0a6419c20de7db04a101bd5bc5dc9f1c138f2c491b74` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/system.json` | 3,457 | `a022916f06f330d5458430420a77f868f9b816964148de4d44a8ca3b811c4d50` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/task.json` | 126,915 | `050a612e21ebe01b95d6fa35ca54d592bd83e108b69f5eb0703d8b903274d6d1` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/tool.json` | 7,947 | `3323fb81a4d321b1eb8703140f113f947a0634f8d64b14337d3b46853d6ddaa4` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |
| `rcs/riot_swagger/version.json` | 4,097 | `acccc01ec233f13d7ba86bf052a35ffcbaa043eadc23887a6f3ae86ad0699aea` | `RIOT-8005-RUNTIME` 地址 | `RIOT-8005-RUNTIME` / `v2.2.0.14` |

Round 1 另记录了整目录摘要 `f77dda0c0b85dce7151b1f35ef5f5fb6f2a484ed60b157ee0c167b1b70433d0d`，但未保留足以独立复现其“按文件名排序后拼接”细节；逐文件 SHA-256 是本记录的规范身份。

## 受控快照 manifest 的最低字段

如果项目方确认现存 14 份文件就是适用快照，可直接在本记录中补齐以下字段并绑定上述逐文件哈希；如果不是，则须重新导出原始 schema，并为新快照建立同样字段。

| 字段 | 准入要求 |
| --- | --- |
| `snapshot_id` | 永久、不复用的标识，例如 `RIOT-OPENAPI-8005-YYYYMMDD-01` |
| `captured_by` / `captured_at` | 具名捕获人和带时区时间；未知不得推定 |
| `source_environment_id` | 指向上表已确认的稳定环境标识，不把 IP 当长期身份 |
| `source_base_url_fingerprint` | 可记录协议、端口和环境标识；若仓库需要脱敏，不记录可路由地址 |
| `riot_product_build` | 从目标实例界面、版本接口或受控发布记录取得；写明证据位置 |
| `capture_method` | 逐项导出路径、工具/脚本版本和是否经过代理；应可复现 |
| `schema_files` | 每个原始文件的相对路径、字节数、SHA-256、OpenAPI 版本和 `info.version` 原值 |
| `project_scope` | 至少说明项目 `8005`、适用站点/产线、运行环境和有效起止条件 |
| `confirmed_by` / `confirmed_at` | 有权确认环境与适用范围的具名人员和日期 |
| `supersedes` | 若替代旧快照，引用旧 `snapshot_id`；不覆盖旧原始字节 |

### 现存快照 manifest

| 字段 | 已绑定值 |
| --- | --- |
| `snapshot_id` | `RIOT-OPENAPI-8005-202607-EARLY-01` |
| `captured_by` | 用户本人 |
| `captured_at` | 2026 年 7 月初；精确日期/时间未知 |
| `source_environment_id` | `RIOT-8005-RUNTIME` |
| `source_base_url_fingerprint` | schema 内 server 为 `http://172.19.206.222:8888`；只可从现场网络访问 |
| `riot_product_build` | `v2.2.0.14`，由用户于 2026-08-03 最终澄清；`2.2.0.30` 是后来运行 riot-lab 行为测试的环境 build |
| `capture_method` | 手动逐项导出；精确 URL、步骤和工具版本未记录 |
| `schema_files` | 上表 14 份原始 JSON；逐文件路径、字节数和 SHA-256 为规范身份；OpenAPI 3.0.3，`info.version` 均缺失 |
| `project_scope` | 8005 项目真实运行时 RIoT；永久有效，现场网络可达条件适用 |
| `confirmed_by` / `confirmed_at` | 用户本人 / 2026-08-03 |
| `supersedes` | `none-known`；没有更早受控 snapshot ID |

## 不含秘密的捕获与保存规则

1. 从目标环境只导出 schema 或公开版本元数据；不得把请求头、cookie、token、CallApiKey 或登录响应保存进 manifest。
2. 若捕获工具必须鉴权，凭据只从本地秘密存储或临时环境变量注入；命令记录使用变量名，不记录变量值。
3. 原始响应先按字节保存，再计算 SHA-256；规范化、生成 SDK 或修改 `servers` 的副本另存为派生物，不能替代原始快照。
4. 保存捕获日志时只记录时间、目标环境标识、HTTP 状态、内容长度和哈希；对 URL、用户名、主机名或资产标识按项目安全规则脱敏。
5. 快照只证明该环境/build 暴露了哪些接口；它不自动授权 8005 调用这些接口，也不证明运行时副作用、权限或错误语义。

## 当前关闭缺口

| 缺口 | 状态 | 关闭所需事实 |
| --- | --- | --- |
| `RIOT-GAP-01` | `user-confirmed` | 两个环境的地址、用途、所有者角色、有效期、build 和相互关系均已确认；个人所有者未具名是显式证据边界，不再作为本票阻塞项 |
| `RIOT-GAP-02` | `user-confirmed-with-explicit-limits` | 已绑定捕获人、约略时间、手工方式、源环境/build 和 8005 范围；精确日时与逐项步骤明确记为未知，不再由其它证据推定 |
| `RIOT-GAP-03` | `user-confirmed` | 当前 8005 绑定 `RIOT-8005-RUNTIME` 和 `RIOT-OPENAPI-8005-202607-EARLY-01` |

三个补证缺口均已由用户直接确认关闭。14 份 schema 已绑定到 8005 环境/build 和当前项目范围，但这仍不能推导项目 API 白名单；任何接口调用授权必须由后续独立票据处理。
