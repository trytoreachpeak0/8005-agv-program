# R10 仓位模拟器需求与决定调查

## 2026-08-03 范围更新

用户在本调查完成后明确“供应商手册可以忽略”。因此本报告对厂商 PDF 及其派生中文寄存器表的既有核验，只用于证明 R10 无损清单覆盖、文件哈希、Git 状态和来源关系；后文记录的手册协议语义不再作为本次当前基线候选、外部约束来源或后续项目适用性调查依据。该范围更新不修改或删除原始材料。

## 结论

R10 固定清单共 46 份材料。2026-08-03 对全部路径重新计算 SHA-256，46/46 与[无损材料清单](../material-inventory/material-inventory.tsv)一致；所有源文件当前均无工作区修改。

本批次的主体是尚未实现的开发辅助工具规划，不是多仓位 AGV 主系统需求基线：

- 15 份 `FR-*` 是模拟器自身功能需求，状态均为 `review`。
- 15 份 `DR-*` 是模拟器技术/范围决定，状态均为 `decided`。索引声称这些决定“与用户（邵正宇）确认”，但没有原始对话、会议记录或其它可核查批准证据，也没有把确认动作绑定到日期、适用范围与当前文件版本。
- 5 份设计材料、测试计划和实施计划仍是 `Draft`/`template`/`TODO`；根 README 第 28 行明确“代码尚未搭建，以上均为规划状态”，当前目录也没有源代码或测试实现。
- 2 份 `_templates` 只是指向仓库规范模板的占位文件，4 份 README 是索引或派生概览；它们不独立形成需求。
- 第三方硬件 PDF 是 C2000-A2-KDDA0A0-AD6 型号的厂商资料，能证明该型号手册所述 16DI/16DO、Modbus TCP、寄存器和功能码，但不能证明 8005 项目实际采购/安装的型号、固件和布线。中文寄存器表是对 PDF 第 21～24 页的可追溯摘录，不是独立来源。

没有一份 R10 材料具备当前基线治理规则要求的完整批准四要素，因此 0/46 可直接作为“已确认主系统需求”。19 份当前快照由含 Cursor 共同署名的后续提交修改，归为“AI 生成或修改但尚未确认”；25 份项目文档只有一次普通 Git 提交且缺少来源链，归为“来源未知”；其余 2 份分别是第三方厂商资料及其可追溯摘录。

R10 仍包含值得回到主系统来源核实的约束线索：硬件协议/寄存器、是否存在移动硬联锁、是否有独立门磁、锁 DO 与锁 DI 的机构语义、是否必须使用多个 IO 模块、以及业务超时/任务状态由主系统负责。这些线索不能因被模拟器文档复述就自动升级为主系统需求。

## 范围、勘误与判定方法

调查边界由[票 22](../../issues/22-investigate-slot-simulator-materials.md)和材料清单的 `batch_id=R10` 固定。分类遵守[票 01](../../issues/01-authority-and-classification-evidence-rules.md)的批准四要素、[票 04](../../issues/04-atomic-requirement-approval-granularity.md)的条目粒度和[票 06](../../issues/06-current-baseline-history-boundary.md)的按需历史回溯。

首先应用[票 26](../../issues/26-correct-initial-snapshot-git-status-classification.md)及其[追加勘误](../initial-snapshot/git-status-correction.md)：

- `slots-simulator/docs/reference/C2000-A2-KDDA0A0-AD6_寄存器表.md`
- `slots-simulator/docs/reference/C2000-A2-KDDA0A0-AD6-使用说明书2023-02-22].pdf`

原清单把二者误记为 `untracked`；勘误后均为 `tracked-clean`。两者在固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e` 的 blob 分别为 `802bc4025a453d11625c0067b515c6d1590579ac`、`b16ae45dd6fb1a232fc5b50e905347d919bd6c95`，与当前 HEAD blob 相同。本调查因此对二者正常执行 `git log --follow`，没有遗漏历史。

分类标签：

- `SIM-REQ`：模拟器工具自身需求。
- `SIM-DEC`：模拟器范围、技术或实现决定。
- `DESIGN`：设计规格或 API 草案。
- `TEST` / `PLAN`：测试计划 / 实施计划，不是通过证据。
- `MAIN-LEAD`：涉及主系统或现场约束的待核实线索，不表示已确认主系统需求。
- `VENDOR`：第三方厂商拥有的型号资料。
- `DERIVED`：能指向上游资料的摘录或概览。
- `INDEX` / `TEMPLATE`：索引、入口或占位模板。

## 来源、历史与批准证据

### Git 历史分组

| 历史码 | 数量 | 形成与修改历史 | 来源/批准结论 |
| --- | ---: | --- | --- |
| H-AI | 19 | `96eb203`（2026-07-13，Zhengyu Shao，“szy: 第一次提交”）创建；`493ac5a`（2026-07-31，Zhengyu Shao，`Co-authored-by: Cursor`）修改 | 最新版本有直接 AI 修改证据，且无授权人确认当前版本，归“AI 生成或修改但尚未确认” |
| H-U | 25 | 仅见 `96eb203` 一次提交，Git 作者为 Zhengyu Shao | Git 作者只证明提交者；没有原始需求输入、确认事件或版本绑定，归“来源未知” |
| H-V | 1 | PDF 仅见 `96eb203` 纳入仓库；PDF 封面标识深圳市中联创新自控系统有限公司、2019-12-13 更新，PDF 元数据修改时间为 2023-02-22 | 可作为该厂商/型号的第三方资料；仓库纳入时间和文件名不是项目适配批准 |
| H-D | 1 | 中文寄存器表仅见 `96eb203`；正文第 3 行明确来源为 PDF 第 5.1 节、第 21～24 页 | 来源链清楚的人工摘录，但加入了计算地址范围和“疑似原文笔误”判断，须保留与 PDF 的区分 |

`493ac5a` 对 R10 的修改主要把旧的“锁 DI 镜像 DO”模型改成“开锁脉冲、弹簧弹门、人工关门后才锁闭”，但并未改完所有派生设计与测试材料，见后文一致性问题。

### 批准四要素

| 要素 | 发现 | 结论 |
| --- | --- | --- |
| 具名授权人 | DR 索引第 3 行声称关键决定与“用户（邵正宇）确认”；多份 DR 写“用户确认/明确”。没有原始对话、会议或签署记录，也没有证据证明每条决定的授权范围 | 只有二手确认陈述，不足以证明批准 |
| 可核查批准日期 | FR/DR 有 `created`、`updated`，Git 有提交日期；这些都是文档日期，不是确认动作日期 | 不满足 |
| 批准范围 | 文档可辨认模拟器范围，但多项决定同时陈述主系统/现场事实；没有批准记录说明哪些只批准工具设计、哪些批准主系统约束 | 不满足 |
| 版本绑定 | 当前 SHA、Git commit 可恢复；没有确认记录绑定任一 SHA/commit/会议版 | 不满足 |

FR 的 `status: review` 明确表示尚在评审；DR 的 `status: decided` 只是一项无主体、日期和版本绑定的文档字段。厂商手册也只对其产品型号范围负责，不等于 8005 项目已批准采用该型号或这些模拟语义。

## 46 份逐件矩阵

SHA 列为清单完整 SHA-256 的前 12 个十六进制字符；本次比较使用完整值。适用性中的“当前”仅表示仓库现有规划没有显式废弃，不表示已批准或已实现。

| 材料 | SHA 前 12 | 历史 | 分类 | 范围、来源与当前适用性 |
| --- | --- | --- | --- | --- |
| [DR 模板占位](../../../../slots-simulator/docs/_templates/template-decision-record.md) | `cb28ac491a45` | H-U | TEMPLATE | 仅指向根模板；不含决定内容 |
| [FR 模板占位](../../../../slots-simulator/docs/_templates/template-functional-requirement.md) | `0a0521c5a559` | H-U | TEMPLATE | 仅指向根模板；不含需求内容 |
| [模拟器愿景](../../../../slots-simulator/docs/00-vision/vision-and-scope.md) | `36700686b64e` | H-AI | SIM-REQ + MAIN-LEAD | 当前工具范围总览；混入硬件/主系统事实，须逐条回源 |
| [FR-001](../../../../slots-simulator/docs/01-requirements/fr-001-configurable-slot-count-and-io-mapping.md) | `6c30831ae7bc` | H-U | SIM-REQ | `review`；工具配置/映射需求，无实现证据 |
| [FR-002](../../../../slots-simulator/docs/01-requirements/fr-002-slot-state-machine-normal-flow.md) | `da7627a47f12` | H-AI | SIM-REQ + MAIN-LEAD | `review`；工具状态机，包含门/锁/光幕现场假设 |
| [FR-003](../../../../slots-simulator/docs/01-requirements/fr-003-exception-scenario-simulation.md) | `4227ba265ac4` | H-AI | SIM-REQ + MAIN-LEAD | `review`；工具故障注入，复述主系统超时职责 |
| [FR-004](../../../../slots-simulator/docs/01-requirements/fr-004-mis-stored-product-retrieval.md) | `b7c1e6a1c284` | H-AI | SIM-REQ | `review`；模拟器取出/关门刺激，不实现主业务 |
| [FR-005](../../../../slots-simulator/docs/01-requirements/fr-005-modbus-tcp-slave-protocol.md) | `1a6dbbefa60a` | H-U | SIM-REQ + VENDOR | `review`；工具协议保真要求，硬件部分须回厂商手册/真机 |
| [FR-006](../../../../slots-simulator/docs/01-requirements/fr-006-automation-control-api.md) | `a89a8c69c81d` | H-AI | SIM-REQ | `review`；仅测试控制面 API，不是主系统 API |
| [FR-007](../../../../slots-simulator/docs/01-requirements/fr-007-wpf-visualization-panel.md) | `030d837ad802` | H-AI | SIM-REQ | `review`；内部开发工具 UI，不是车载 HMI 需求 |
| [FR-008](../../../../slots-simulator/docs/01-requirements/fr-008-single-instance-single-agv.md) | `824424294f17` | H-U | SIM-REQ | `review`；模拟器部署方式，不约束主系统部署 |
| [FR-009](../../../../slots-simulator/docs/01-requirements/fr-009-headless-host.md) | `54308a5ea4de` | H-U | SIM-REQ | `review`；未来 CI 可用性，不是当前 CI 承诺 |
| [FR-010](../../../../slots-simulator/docs/01-requirements/fr-010-automation-test-infrastructure.md) | `b40db5e14edf` | H-U | SIM-REQ | `review`；测试 reset/探针/日志，不是主系统行为 |
| [FR-011](../../../../slots-simulator/docs/01-requirements/fr-011-configurable-slot-layout.md) | `56c00339ed41` | H-U | SIM-REQ | `review`；模拟器 WPF 布局，不是实际 HMI 布局 |
| [FR-012](../../../../slots-simulator/docs/01-requirements/fr-012-do-pulse-level-control-mode.md) | `7151362a10b8` | H-AI | SIM-REQ + MAIN-LEAD | `review`；工具行为依赖锁机构/IO 模式现场事实 |
| [FR-013](../../../../slots-simulator/docs/01-requirements/fr-013-configurable-register-table-template.md) | `2924ae0dd721` | H-U | SIM-REQ + VENDOR | `review`；模板要求，厂商事实只限具体型号 |
| [FR-014](../../../../slots-simulator/docs/01-requirements/fr-014-multi-io-module-simulation.md) | `1712993bf188` | H-U | SIM-REQ + MAIN-LEAD | `review`；多模块模拟，实际车辆拓扑尚缺 IO 清单证据 |
| [FR-015](../../../../slots-simulator/docs/01-requirements/fr-015-destination-station-unload-support.md) | `6dbc003a157d` | H-AI | SIM-REQ | `review`；仅提供 UC-010 所需硬件刺激，不批准 UC 业务 |
| [FR 索引](../../../../slots-simulator/docs/01-requirements/README.md) | `3d19382933b9` | H-U | INDEX | 15 份 FR 导航；不独立形成需求 |
| [DR-001](../../../../slots-simulator/docs/02-decisions/dr-001-tech-stack.md) | `4deebb851230` | H-U | SIM-DEC | `decided`；.NET/WPF、编辑/热重载设计，无批准绑定 |
| [DR-002](../../../../slots-simulator/docs/02-decisions/dr-002-simulation-scope.md) | `28e03dc44998` | H-U | SIM-DEC + MAIN-LEAD | 工具范围决定；“无硬件移动联锁”为待核实现场约束 |
| [DR-003](../../../../slots-simulator/docs/02-decisions/dr-003-first-batch-scenarios.md) | `3d2c512d8b18` | H-AI | SIM-DEC | 工具覆盖范围，不批准所引用 UC 的业务语义 |
| [DR-004](../../../../slots-simulator/docs/02-decisions/dr-004-configurable-slot-count.md) | `cb4b22c0c406` | H-U | SIM-DEC | 工具可配置性设计；8 仓仅作背景引用 |
| [DR-005](../../../../slots-simulator/docs/02-decisions/dr-005-modbus-protocol-fidelity.md) | `ee1adde83de0` | H-U | SIM-DEC + VENDOR | 工具协议决定；厂商手册支持部分协议事实 |
| [DR-006](../../../../slots-simulator/docs/02-decisions/dr-006-users-and-automation-style.md) | `f72c8df92d25` | H-AI | SIM-DEC | 开发自测/API 范围，只适用于工具 |
| [DR-007](../../../../slots-simulator/docs/02-decisions/dr-007-multi-agv-support.md) | `f47c10de48bb` | H-U | SIM-DEC | 单进程单 AGV 是工具部署决定；正文承认旧理由被推翻 |
| [DR-008](../../../../slots-simulator/docs/02-decisions/dr-008-ci-readiness.md) | `965c223ef88f` | H-U | SIM-DEC + MAIN-LEAD | 工具 CI 预留；业务超时归主系统是职责线索 |
| [DR-009](../../../../slots-simulator/docs/02-decisions/dr-009-slot-layout-model.md) | `65faf11d947a` | H-U | SIM-DEC | 工具 UI 布局决定，不是实际车载 HMI |
| [DR-010](../../../../slots-simulator/docs/02-decisions/dr-010-do-control-mode.md) | `811b27ccd000` | H-AI | SIM-DEC + MAIN-LEAD | 工具模型；脉冲、弹簧、锁 DI 事实需现场/设备证据 |
| [DR-011](../../../../slots-simulator/docs/02-decisions/dr-011-full-register-table-fidelity.md) | `a4f124205d0c` | H-U | SIM-DEC + VENDOR | 模板化是设计；16DI/16DO 可由厂商手册支持 |
| [DR-012](../../../../slots-simulator/docs/02-decisions/dr-012-multi-io-module-support.md) | `07faa2420d7c` | H-U | SIM-DEC + MAIN-LEAD | 工具决定；“实际必需多模块”缺项目 IO/布线证据 |
| [DR-013](../../../../slots-simulator/docs/02-decisions/dr-013-door-state-not-independent-io-point.md) | `72566706ff4a` | H-AI | SIM-DEC + MAIN-LEAD | 无独立门磁/锁 DI 语义为主系统硬件线索，不能靠 DR 自证 |
| [DR-014](../../../../slots-simulator/docs/02-decisions/dr-014-fault-injection-mirror-exception.md) | `0f10f9682f20` | H-AI | SIM-DEC + MAIN-LEAD | 当前故障模型；还复述主系统“不盲目重试”规则，须回源 |
| [DR-015](../../../../slots-simulator/docs/02-decisions/dr-015-do-power-on-state-vs-reset.md) | `2d93e4febdb3` | H-U | SIM-DEC | 工具确定性与真机副作用间的有意偏差，不能用于真机验收 |
| [DR 索引](../../../../slots-simulator/docs/02-decisions/README.md) | `13928ef5f4a6` | H-U | INDEX | 决定导航及“与用户确认”二手陈述；不是确认记录 |
| [架构设计](../../../../slots-simulator/docs/03-design/architecture.md) | `2cac6908cb30` | H-AI | DESIGN | Draft 模板、维护者/日期/TODO 未补；不可作为实现证据 |
| [配置规格](../../../../slots-simulator/docs/03-design/configuration-spec.md) | `b62043bed1be` | H-U | DESIGN | Draft 模板，字段名和热重载迁移仍 TODO |
| [控制 API OpenAPI](../../../../slots-simulator/docs/03-design/control-api.openapi.yaml) | `2d5d55556490` | H-AI | DESIGN | `0.1.0-template`；故障枚举落后于 DR-014，非已实现契约 |
| [Modbus 实现规格](../../../../slots-simulator/docs/03-design/modbus-implementation-spec.md) | `e5dd40be4faf` | H-AI | DESIGN + VENDOR | Draft；地址换算、Unit ID 等关键项未定，且有锁 DI 镜像冲突 |
| [仓位状态机设计](../../../../slots-simulator/docs/03-design/slot-state-machine.md) | `704384b03fb1` | H-AI | DESIGN | Draft；当前较接近 DR-010/013/014，但仍有多项 TODO |
| [测试计划](../../../../slots-simulator/docs/04-testing/test-plan.md) | `c81bbf6f355a` | H-AI | TEST | Draft/Planned/TODO；没有测试实现或执行结果，不能当通过证据 |
| [实施计划](../../../../slots-simulator/docs/05-planning/implementation-plan.md) | `2251a8ec6105` | H-U | PLAN | Draft，负责人/日期未定，M0–M7 均 Not Started |
| [文档中心](../../../../slots-simulator/docs/README.md) | `f4ac3dbd5205` | H-U | INDEX + DERIVED | 导航和派生技术摘要；不独立批准 FR/DR |
| [中文寄存器表](../../../../slots-simulator/docs/reference/C2000-A2-KDDA0A0-AD6_寄存器表.md) | `593b0c96b8a7` | H-D | DERIVED + VENDOR | 可追溯 PDF 21–24 页；地址范围和原文笔误判断是派生加工 |
| [厂商使用说明书 PDF](../../../../slots-simulator/docs/reference/C2000-A2-KDDA0A0-AD6-使用说明书2023-02-22].pdf) | `0a2696eb9898` | H-V | VENDOR | 30 页第三方型号资料；未绑定项目采购、固件或实际布线 |
| [子项目 README](../../../../slots-simulator/README.md) | `699d2143794c` | H-AI | INDEX + DERIVED | 当前入口与派生摘要；明确代码未搭建、全部为规划状态 |

## 第三方硬件资料核验

PDF 共 30 页，封面为“C2000-A2-KDDA0A0-AD6 使用说明书”，标注 2019-12-13 更新和深圳市中联创新自控系统有限公司。文本提取后又视觉核对了完整封面、第 7、13、14、21～24 页：

- 第 7 页列 16 路 DI、16 路 DO、干接点 DI、A 型继电器 DO、电平/脉冲输出和标准 Modbus TCP。
- 第 13～14 页说明 DI 地址从 10200 开始、DO 地址从 100 开始，DO 支持 `0x01/0x05/0x0F`，并给出脉冲宽度 50～65535 ms。
- 第 21～24 页是寄存器表，列出模块/网络寄存器、DO/DI、工作模式、脉宽和适用功能码。中文摘录逐项来自这些页，整体可追溯。

但需要保留以下限制：

1. 手册页 13 把 DI 滤波范围写为 0～20，页 23 又写为 `0x1～0x14` 且写 0 失败；中文摘录采用后者。厂商资料自身存在不一致，不能由摘录静默裁决。
2. 页 22 的 DO 组标题、数量均为 DO1～DO16/16 个，却在说明中写“保存 DO1～DO4”；中文摘录明确标注疑似原文笔误。该判断合理但仍是派生判断。
3. 页 24 例子明确 Unit Identifier 为 `0xFF`、文档地址 10200 对应 PDU 地址 `0x00C8`。当前 Modbus 设计仍把 Unit ID 与地址换算标成 TODO（`modbus-implementation-spec.md:17,28-34,134`），所以“协议完全透明/保真”尚无可实施的完整规格。
4. 该 IO 模块手册不描述 AGV 柜门、弹簧锁、门磁、光幕安装位置、8005 实际仓位数或项目布线，因此不能支持 DR-002、DR-010、DR-012、DR-013 的现场断言。

## 与主系统基线的关系

### 可作为主系统约束证据的内容

只有厂商手册中属于该具体型号的声明具有独立外部来源价值：16DI/16DO、接口类型、Modbus TCP、寄存器表、功能码、工作模式和脉宽范围。即使如此，进入主系统基线前仍须补充采购/BOM/设备铭牌/固件或现场配置，证明 8005 实际使用的就是这份手册适用的型号与版本。

中文寄存器表可以作为便捷派生材料，但基线引用应同时保留 PDF 页码，特别是存在原文冲突或人工判断的条目。

### 仅为工具需求或设计实现的内容

以下内容只约束 `slots-simulator`，不得进入主系统功能基线：WPF 技术栈与布局、HTTP/JSON 测试 API、Headless Host、reset/健康探针/结构化日志、JSON Schema/热重载、单实例单 AGV、多模块端点的模拟器部署方式、故障注入接口、测试和里程碑计划。

FR/DR 对 UC-001、002、005、006、010、018 的链接只说明模拟器拟支持哪些硬件刺激。它们不能证明这些 UC 已批准，也不能由模拟器的验收条件反向改写主系统业务流程。

### 必须回主系统/现场来源核实的线索

1. **没有硬件移动联锁**：愿景第 21 行、DR-002 第 21 行声称用户确认。应绑定电气图、IO 清单或具名设备责任人确认；这不等于取消主系统软件的移动安全职责。
2. **没有独立门磁，锁 DI 代表闩合**：DR-013 第 18、25 行与根 UC-017 的“信号来源待供应商确认”有关。应以实际锁具/传感器资料和现场点检确认；厂商 IO 模块手册不能证明。
3. **脉冲解锁、弹簧自动弹门、DO 复位后仍未锁**：DR-010/014 与 FR-002/012 使用此模型。需要锁具规格、接线和现场动作记录。
4. **一台 AGV 必须多个 IO 模块**：DR-012/FR-014 从“单模块 16DI/16DO”和“实际仓位会超限”推导。前者有手册证据，后者没有项目仓位/每仓信号/IO 余量表；不能单靠厂商容量推出实际拓扑。
5. **业务超时、任务、站点和异常锁定归主系统**：这是合理的工具边界，但主系统具体阈值、状态和处置仍应来自主系统 FR/UC/ADR，而非 R10。
6. **结果未知不得盲目重试开锁**：DR-014 第 23 行是主系统安全策略陈述，应回主系统安全决定；模拟器只需能产生该故障刺激。

## 当前内部不一致与缺口

1. **锁 DI 镜像残留**：DR-010、DR-013、DR-014 和当前状态机都明确锁 DI 不镜像 DO；但 Modbus 规格第 97 行仍写 `lockStateDI = lockCommandDO`，测试计划第 144 行仍要求清除锁 DI 脱钩后“按当前 DO 重建”。这会产生不同实现，当前设计不能视为稳定。
2. **API 故障枚举落后**：OpenAPI 仍只有 `lock-di-detached`、`light-curtain-di-detached`、模块断连/不响应；DR-014 已区分开锁/弹门失败与闩锁失败。模板 API 尚未表达当前决定。
3. **协议关键项未定**：Modbus 规格仍有地址换算、Unit Identifier、Pulse 写 OFF、PDU 上限、多客户端/超时和库选型 TODO；无法据此证明真机协议保真。
4. **设计/测试/计划未完成**：架构维护者和日期为空，配置规格字段/迁移未定，测试矩阵仅 Planned，实施 M0–M7 未开始；仓库不存在模拟器实现。当前适用性只能是规划输入。
5. **“与用户确认”缺证据**：DR 索引的总括性陈述没有逐条确认内容、日期、范围和版本。尤其后来由 AI 修改的 7 份 FR、5 份 DR 与其它规划材料，原先可能存在的口头确认也不能自动覆盖当前文本。

## 后续证据动作

1. 找回生成 DR-001～DR-015 的原始对话/会议记录；由具名授权人逐条确认模拟器范围和工具需求，并绑定具体 hash。FR 仍为 `review`，应在完成原子评审后再改变状态。
2. 对 MAIN-LEAD 六类线索分别取得电气图、IO 点表、BOM/铭牌、锁具/传感器规格与现场验证；另行进入主系统基线调查，不能批量批准 R10。
3. 明确 8005 实际 IO 模块型号、硬件/固件版本和安装数量；若确为 C2000-A2-KDDA0A0-AD6，再把厂商手册页码和项目设备身份绑定。
4. 修正锁 DI 镜像残留与 OpenAPI 故障枚举；解决 Unit ID、地址换算等 TODO 后，由技术责任人批准具体设计版本。
5. 代码和测试落地后，单独保存构建、协议向量、真机对照和 FR→TC 执行证据。代码现状和测试通过可证明实现一致性，仍不能替代需求批准。

## 可复核性

- 从 TSV 精确筛选 `batch_id=R10`，得到 46 份、2,192,376 bytes；原始角色虽全部标 `candidate-requirement`，本报告按内容重新分组。
- 应用 2 条 Git 状态勘误，并验证固定 HEAD blob、当前 HEAD blob和路径跟踪状态一致。
- 对 46 路径逐个执行完整 SHA-256 比较，结果 46/46 相同；复核工作区状态均无修改。
- 对 46 路径逐个执行 `git -c core.quotepath=false log --follow`；全部由 `96eb203` 创建，19 份后来由含 Cursor 共同署名的 `493ac5a` 修改。
- 逐份阅读全部 Markdown/YAML；对 30 页 PDF 提取全部页文本，并视觉检查封面、技术参数、产品功能和完整寄存器表相关页。
- 本调查仅新增本报告，没有修改 issue、map、模拟器源材料或其它基线材料，也没有创建提交。
