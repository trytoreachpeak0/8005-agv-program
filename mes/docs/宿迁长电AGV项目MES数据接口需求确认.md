# 宿迁长电 AGV 项目 MES 数据接口需求确认

> 本文只记录业务问题、接口契约、已确认结论和待确认项，不保存正式 SQL 或生产查询样本。正式查询以 `mes/catalog` 登记项和 `mes/queries` 中的版本为准；现场回传数据必须进入 `mes/evidence`，可复用样本必须由导入流程晋升到 `mes/samples`。

## 0. 文档边界

- MES 数据库为 Oracle，当前阶段仅允许执行已登记的只读查询。
- 客户 IT 提供并批准查询对象、业务筛选条件和生产执行窗口；AGV 团队不从样本反推 MES 全部业务语义。
- 查询结果是当前状态快照，不是事件流，也不是数据全集。
- 文档中的字段和业务结论不能替代查询目录中的机器可执行版本。

相关入口：

- 查询目录：[`../catalog/queries.md`](../catalog/queries.md)
- 正式查询：[`../queries/`](../queries/)
- 样本治理：[`../samples/README.md`](../samples/README.md)
- 证据治理：[`../evidence/README.md`](../evidence/README.md)
- 实验定义：[`../experiments/README.md`](../experiments/README.md)
- 工厂连接配置：[`工厂环境配置说明.md`](工厂环境配置说明.md)

## 1. 业务与接口约定

### 1.1 术语

- `LOT`：客户订单对应的母批次号。
- `SUBLOT`：母批次拆分后的生产批次，现场扫描对象；MES 原字段仍可能名为 `lot`。
- `EQP`：MES 机台编号，业务上必须非空。
- `AREA`：机台区域号，允许为空；错误、缺失或无法映射时不得派车。
- `PACKAGE`：产品封装工艺，用于覆盖率分析和花篮容量换算。
- `QUERY_ID`：查询的稳定标识。业务文档引用 QUERY_ID，不复制 SQL。
- `run_id`：一次不可覆盖的执行证据标识。

### 1.2 五类运输任务

1. `DIE_TO_WIRE_STAGING`：装片完工机台到焊线/键合派工待送区。
2. `DIE_TO_OVEN`：装片完工机台到烘箱间。
3. `WIRE_TO_GATE`：焊线/键合完工机台到人工质检关卡区。
4. `WIRE_TO_OPTICAL`：焊线/键合完工机台到三光区。
5. `STAGING_TO_WIRE`：焊线/键合派工待送区到指定焊线/键合机台。

MES 的 `STEP`、`入库`、`入站`、`完工`仅用于客户 IT 批准的查询筛选。系统按 `TASK_TYPE` 解释物理运输含义，不根据 `STEP` 自行推导路线。

### 1.3 任务接入规则

1. 正式运输任务幂等键为 `TASK_TYPE + SUBLOT`。
2. 单次查询中同一 `TASK_TYPE + SUBLOT` 最多一行；出现多行（含完全相同行，或 EQP/AREA/STEP/DATES/PACKAGE 任一不同）一律硬失败：对该冲突键报警并阻断，不得归并，其余未冲突键继续处理。
3. 同一 EQP 对应不同 AREA，或同一 SUBLOT 在同一快照命中多个任务类型时，按阻断性异常处理。
4. `WIRE_TO_GATE` 与 `WIRE_TO_OPTICAL` 绝对互斥。
5. EQP 和 AREA 仅去除首尾空格，不补零、不改变大小写；例如 `D4-06` 与 `D04-06` 是不同位置。
6. AREA 不符合编码约定或无法映射到唯一 `station_name` 时，保留候选记录并进入位置异常，不得下发 AGV。
7. 任务首次创建后冻结 EQP、AREA、DATES、起终点与 `station_name`；后续观测变化只作审计。
8. 正式任务只能来自 MES；Mock 任务必须使用独立来源和独立 ID，不参与正式任务幂等与消失对账。
9. 允许在无开仓会话、无有效占用、未开始运送时人工取消本地任务：对 `TASK_TYPE + SUBLOT` 永久抑制，无解除入口；异类型仍正常接入（详见 1.4）。

### 1.4 快照、轮询和消失处理

- 五类任务必须通过一个 `UNION ALL` 查询取得 Oracle 语句级一致性快照。
- 每轮完整结束后等待 10 秒再启动下一轮，禁止重叠或堆积。
- 只有完整成功的查询才能创建任务或累计消失次数。
- 同一记录连续 2 个完整成功快照未出现，且同时满足：未点击「开始运送」、无开仓未关会话、有效装载占用为 0 时，取消本地任务并撤销取货路线；保护期内消失计数仍累加。
- 开仓未关或仍有占用时不得因 MES 消失取消；空关无明细不保护。点击「开始运送」后进入运送，忽略 MES 消失；进入运送后禁用装货阶段“再开仓关门清占用”。本趟占用为 0 时「开始运送」灰掉不可点。
- 人工取消（无开仓会话、无有效占用、未开始运送）：对幂等键 `TASK_TYPE + SUBLOT` 永久抑制，不自动恢复/重建，不提供解除入口；同一 SUBLOT 的其他 `TASK_TYPE` 仍正常接入。MES 仍可见该键时可报警但不建单。
- 因 MES 消失自动取消后同键再次出现时转人工确认，不自动恢复或重新创建。
- 某任务类型上一轮正常数量不小于 10、本轮突然为 0 时进入 `PAUSED_ZERO_DROP`；该类型暂停消失累计与取消，连续 2 轮恢复非 0 后自动解除。
- 消失计数、最后正常非 0 数量、连续恢复次数和保护状态必须持久化。
- 系统重启后第一次完整查询只建立恢复基线：可创建新任务、可重置重新出现任务的计数，但不得累计缺失或取消。
- 固定上线基线时间为 `2026-08-01 00:00:00`，由应用层过滤；不得用持续滚动的短窗口替代可靠对账。

### 1.5 多仓位与花篮

- 一个 SUBLOT 可对应一个或多个花篮；一个运输任务可包含多条花篮装载明细。
- AGV 可混装不同任务类型并多站取送，但每次取货必须校验任务起点。
- 仓位数量和规格按车型配置；当前车型暂定 8 仓，程序不得写死。
- 不追踪实体花篮条码，只记录 SUBLOT、花篮序号和仓位。
- 料盒数与封装容量换算失败时，回退到“重复扫描同一 SUBLOT、二次确认新增一篮”的现场流程。
- 扫码防抖、确认提示、仓门与仓内物体传感器（如光幕）校验缺一不可；有效装载以“选定 SUBLOT + 有物关门”为准，无独立“装载完成”按钮；以「开始运送」进入运送。

### 1.6 AREA 与站点

- RCS/RIOT 地图提供 `station_id ↔ station_name`；业务配置与数据库只保存 `station_name`。
- `station_name → area_code[]` 由站点命名规则派生，最多 3 个 AREA；命名不规范时使用可审计的显式覆盖。
- 数字 `station_id` 只在派车调用瞬间查询，不落盘。
- 同一 AREA 映射到多个站点时必须列明冲突项并阻断。
- 焊线/键合派工待送区、烘箱间、关卡区、三光区分别配置可动态修改的固定 `station_name`。

## 2. 查询契约索引

### 2.1 `MES_TASK_UNION`

- 目的：一次返回五类当前运输候选快照。
- 正式查询：[`../queries/mes-task-union/`](../queries/mes-task-union/)
- 目录登记：[`../catalog/queries.md`](../catalog/queries.md)
- 输出契约：`TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE`，共 7 字段。
- 关键约束：`TASK_TYPE` 只能是 1.2 节的五个值；EQP、DATES 必须非空；AREA 可空；DATES 按北京时间 UTC+8 解释。
- 历史证据：[`../evidence/legacy/2026-07-10-mes-task-union/`](../evidence/legacy/2026-07-10-mes-task-union/)
- 样本入口：[`../samples/mes-task-union/`](../samples/mes-task-union/)
- 验证计划：[`../experiments/definitions/mes-task-union-validation/plan.md`](../experiments/definitions/mes-task-union-validation/plan.md)

各任务类型的业务问题：

- `DIE_TO_WIRE_STAGING`：老厂前线“共晶”和“低温共晶”产品不需要机器人运输。客户建议结合 AREA、EQP 排除；具体白名单/排除清单仍须客户确认。
- `DIE_TO_OVEN`：AREA 可能为空或错误，不得因当前样本看似完整而放松位置校验。
- `WIRE_TO_GATE`：需持续验证与三光任务互斥。
- `WIRE_TO_OPTICAL`：历史状态可能停留较久，不能把 DATES 当成唯一有效性判断。
- `STAGING_TO_WIRE`：优先级最高；若同一 SUBLOT 的上游任务仍在送往待送区而 MES 已出下游（常见于现场未按流程提前推进），下游等待上游卸货并报警/记审计，不取消上游。

### 2.2 `SUBLOT_BOX_COUNT`

- 目的：按现场扫描的 SUBLOT 查询各工序料盒计数的最大值，供估算花篮数量。
- 正式查询：[`../queries/sublot-box-count/`](../queries/sublot-box-count/)
- 目录登记：[`../catalog/queries.md`](../catalog/queries.md)
- 输入契约：绑定参数 `sublot`，禁止字符串拼接。
- 输出契约：单值 `MAX_BOX_COUNT`；无结果、失败或超时不得取消运输任务。
- 容量参考：[`../reference/package-basket-capacity.md`](../reference/package-basket-capacity.md)
- 样本入口：[`../samples/sublot-box-count/`](../samples/sublot-box-count/)
- 端到端实验：[`../experiments/definitions/sublot-basket-end-to-end/plan.md`](../experiments/definitions/sublot-basket-end-to-end/plan.md)

### 2.3 `OP_OPERATOR_IDENTITY`

- 目的：按工号解析操作员姓名，用于身份核验、操作会话和审计。
- 正式查询：[`../queries/operator-identity/`](../queries/operator-identity/)
- 目录登记：[`../catalog/queries.md`](../catalog/queries.md)
- 输入契约：绑定参数 `user_id`。
- 输出契约：`operator_name`；无结果、失败或超时时不建立操作会话，且不向现场暴露账号是否存在。
- 本地审计同时保存工号和姓名；本查询不负责岗位授权。
- 样本入口：[`../samples/operator-identity/`](../samples/operator-identity/)

### 2.4 PACKAGE 全量发现研究

- 目的：在客户批准的对象和时间范围内发现 PACKAGE 候选集合，为容量对照治理提供证据。
- 状态：仅有实验定义，不预留正式 QUERY_ID；客户 IT 批准对象、范围和负载后，再登记到 [`../catalog/queries.md`](../catalog/queries.md) 和 `../queries/`。
- 重要限制：任何一次活跃任务样本都不是 PACKAGE 全集；查询对象、时间范围、预估行数、执行计划和数据库负载必须由客户 IT 书面批准。
- 实验定义：[`../experiments/definitions/package-universe-discovery/plan.md`](../experiments/definitions/package-universe-discovery/plan.md)

### 2.5 `MES_SCHEMA_INTROSPECTION`

- 目的：核验接口涉及字段的 Oracle 类型、长度和可空性。
- 正式查询：[`../queries/schema-introspection/`](../queries/schema-introspection/)
- 目录登记：[`../catalog/queries.md`](../catalog/queries.md)
- 历史参考结果：[`../evidence/legacy/schema-introspection-before-2026-07-16/`](../evidence/legacy/schema-introspection-before-2026-07-16/)
- 样本入口：[`../samples/schema-introspection/`](../samples/schema-introspection/)
- 字段长度以数据库声明为准，不得按当前样本最大值缩短应用模型。

## 3. 性能与安全结论

- 性能目标：正常不超过 5 秒；超过 10 秒产生慢查询警告；30 秒硬超时。
- 连续 3 轮失败产生高级报警。
- 2026-07-13 的后续实测记录曾报告：单次约 3.28 秒，连续 10 轮平均 3.13 秒、最大 4.37 秒，并与原五组查询行数一致。该结论必须由相应 run 的 manifest、日志和哈希支撑后才能作为可追溯验收证据。
- 2026-07-10 的旧结果只有 6 列，缺少 `PACKAGE`，只作为历史证据，不得标记为 latest 或用于证明当前 7 字段契约通过。
- 账号即使具有写权限，运行器也只能执行目录登记的 SELECT，并使用只读事务；禁止通用 SQL 入口、DDL、DML 和存储过程写操作。
- 日志、manifest、样本和文档不得包含数据库密码或可直接连接生产环境的完整凭据。

## 4. 已确认结论

1. 当前阶段不做 MES 回写，本地保存运输任务全生命周期。
2. 五类任务使用一个 `UNION ALL` 查询，输出 7 字段。
3. 正式任务只允许来自 MES，Mock 与正式任务隔离。
4. 花篮兜底采用重复扫码后二次确认，不增加独立“新增一篮”按钮。
5. 固定区域配置使用 `station_name`，不是 `station_id`。
6. AREA 映射默认采用地图同步加命名规则派生，显式覆盖只处理例外。
7. 解析失败、位置异常和冲突必须逐项列出站点、AREA 和原因，不能只报汇总数量。
8. PACKAGE 活跃样本只能说明当前观察覆盖，不能声明工厂 PACKAGE 全集。

## 5. 待确认事项

### 5.1 客户 IT / MES

1. “共晶、低温共晶”不使用 AGV 的最终 AREA/EQP 排除规则和变更治理方式。
2. PACKAGE 全量发现实验可访问的对象、历史时间范围、执行窗口、行数上限和数据库负载边界。
3. 当前 7 字段正式查询的最终版本、执行计划和客户批准记录。
4. 设备资料缺失或工序条件不匹配导致记录被内连接过滤时，采用何种异常检查。
5. 岗位权限是否需要独立 MES 接口；`OP_OPERATOR_IDENTITY` 当前只解析身份。

### 5.2 AGV / 现场

1. 除 `STAGING_TO_WIRE` 外各任务类型的相对优先级。
2. 无车辆响应升级阈值在 1～3 分钟范围内的默认值。
3. 顺路取货允许的最大配送延迟。
4. 各车型仓位数量、尺寸、载重和花篮兼容性。
5. 四个固定区域最终 `station_name`。
6. 命名不规范站点的显式 AREA 覆盖数据。
7. 封装容量对照的完整覆盖范围，以及 `TOLL-` 前缀匹配边界。

## 6. 证据提交要求

现场执行不得直接把结果覆盖到 samples。每次执行必须：

1. 先按实验 plan 获得所需客户批准。
2. 由 runner 创建唯一 `run_id` 和独立 evidence 目录。
3. 保存 manifest、执行日志、原始输出和每个文件的 SHA-256。
4. 工厂回传压缩包后先导入 evidence，校验来源、批准信息、哈希和脱敏状态。
5. 只有 `import-run` 可以从已验证 evidence 生成 samples/latest；latest 必须同时包含 `meta` 和 `sourceEvidence`。
