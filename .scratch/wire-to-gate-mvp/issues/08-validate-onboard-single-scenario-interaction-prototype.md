# 验证 OnboardHmi 单场景操作原型

Type: prototype
Status: resolved
Blocked by: 07

## Question

什么样的低成本 OnboardHmi 交互原型，能让用户与车载端开发同事共同验证连接/业务就绪、当前唯一 Demand、机台到站、Sublot 扫码、多仓批量装货、安全等待发车、关卡到站、批量卸货、任务完成、断联/重启恢复和异常人工处置的状态、文案与可用操作？

原型只用于确认交互与责任边界，不作为任一实现仓库的生产依赖；车载端开发同事必须本人参与评审。

## Comments

### 2026-08-25 — 评审原型已就绪，等待车载端开发同事本人评审

已完成当前工作树、全部 Git 引用与历史、登记 worktree 和保存证据的原型源检索；未找到本票对应的既有 OnboardHmi 原型。仓库内已有的原型都属于 MesIngest.Watch，不能作为车载端设计权威。本票因此使用 UI prototype 分支建立新的 throwaway 单文件评审资产，未修改 ControlServer、OnboardHmi、共享协议实现或需求基线：

- [OnboardHmi 单场景操作原型 README](../prototype/onboard-single-scenario/README.md)
- [OnboardHmi 单场景操作原型 HTML](../prototype/onboard-single-scenario/onboard-single-scenario-prototype.html)

#### 需要裁决的候选与推荐值

1. **载体**：生产 WPF 分支／静态截图／`.scratch` 下零依赖单文件 HTML；推荐单文件 HTML，因为本仓库没有 OnboardHmi 页面或实现仓库，且该形态不会成为生产依赖。
2. **承载形态**：嵌入现有页面／新的 throwaway 单路由；推荐新的 throwaway 单路由，因为不存在可安全嵌入的 OnboardHmi 页面。
3. **方案数量**：2／3／4～5；推荐 3 个结构差异明显的方案。
4. **布局候选**：A“旅程导引台”、B“安全优先双栏”、C“站点作业板”；推荐 A 作为领先候选，以单一主任务、逐阶段下一步和固定八仓降低单 Demand 现场分支。B、C 继续作为安全信息优先级与触控密度对照，不被删除或冒充已拒绝方案。
5. **状态范围**：只做正常旅程／正常加异常／完整票据状态；推荐覆盖连接、五步恢复握手、业务就绪、TO_PICKUP、机台到站、Sublot 输入、批量装货、安全等待发车、TO_GATE、关卡到站、批量卸货、本地完成、断联收敛、重启恢复和 ExceptionRecoverySession。
6. **车辆概览**：单一在线灯／四维并列；推荐分离运行、通信与业务就绪、当前作业、安全与联锁，禁止用连接在线冒充 READY 或用业务完成冒充 DepartureSafe。
7. **正常操作边界**：车载选任务、改篮数或换仓／只提交 Sublot 并执行服务端冻结的完整仓位集；推荐后者。扫码和键盘共用 SublotSubmitted，ExpectedBasketCount 与目标仓位集只读。
8. **仓位表现**：简单列表／固定 1～8 号平面图／只显示目标仓；推荐固定八仓图，并分开显示业务绑定、`OCCUPIED|EMPTY|UNKNOWN`、锁闭反馈、开锁输出复位、本次目标和 ActiveUnlockSet。
9. **断联与恢复**：连接恢复即继续／本地取消／只收尾 ActiveUnlockSet 后执行五步对账；推荐第三项。离线投影只读，SessionReadiness=READY 前不恢复扫码、开仓或移动。
10. **异常处置**：普通操作员覆盖／管理员自由操作／固定事件、车辆、Demand 和仓位范围的 ExceptionRecoverySession；推荐第三项，只显示 `RESUME_AFTER_REPAIR`、`COMPENSATE_LOAD_ALL_EMPTY`、`FAULT_CARGO_HANDOFF`、`FORCED_MECHANICAL_RECOVERY` 四条已批准路径，且身份、记录和货物交接都不能覆盖物理 UNKNOWN 或现场资质。
11. **完成边界**：卸空即发车／等待 PDA/MES／本地完成与发车安全分离；推荐第三项。本地成功可已提交，但仍须新的 PreDepartureSafetyCheck；不等待、读取或回写 PDA/MES。
12. **定案方式**：代理宣布 A 获选／用户授权替代双方视觉确认／用户与车载端开发同事实测三案并记录选择；唯一安全推荐是第三项。

上述 1～11 项已依据前置决议、ADR、`CONTEXT.md` 和地图 Notes 完成事实核对，并**依据用户对本 Wayfinder 后续各票采用推荐值的明确授权**制作进原型；这里如实记录授权依据，不把它改写为新的逐项用户发言。

#### 窄验证

- 单一内嵌脚本语法检查通过；原型没有 HTTP(S) 外部脚本或样式依赖。
- A、B、C 三案均可在 `SUBLOT_ENTRY` 状态静态执行渲染；每案恰有 8 个仓位卡、当前方案标签、完整状态证据和统一 Sublot 输入。
- in-app Browser 的安全策略禁止直接访问本地 `file://` 资产，因此没有把浏览器或本地截图冒充视觉验收；也未运行 Golden WPF tier 2/3。

#### 尚未满足的解决门禁

本票 Question 明确要求车载端开发同事本人参与评审。当前没有该同事对真实目标分辨率、缩放、触控／扫码设备接入、状态与动作可实现性、现场可读性及 A/B/C 取舍的本人反馈。用户的推荐值授权可以推进原型内容，但不能诚实替代这名外部开发者的本人确认，也不能把代理的静态检查冒充共同视觉评审。

因此本票保持 `claimed`，不写 `## Answer`、不设 `resolved`，地图 `Decisions so far` 暂不追加。下一步应由用户与车载端开发同事运行 README 中的一条命令，按其中七个评审问题留下可追溯反馈；收到本人反馈后，才能记录获选方案／组合、必要改动与可实现性结论并解决本票。

## Answer

用户于 2026-08-25 追加明确决定：“不需要车载端评审，直接进入下一步。”用户是本 MVP 产品范围与最终发布的唯一批准人，因此本决定**仅豁免当前《验证 OnboardHmi 单场景操作原型》票中“车载端开发同事必须本人参与原型评审”的门禁**，并采用此前已完整展示的全部推荐值。该决定不声称车载端开发同事看过、接受或批准原型，也不豁免地图中共同协议 release、跨端契约变更或其它明确要求真实第三方批准的后续门禁。

### 获选原型与设计权威

1. **选定 A“旅程导引台”。** 后续生产 OnboardHmi 的单场景页面以 [A“旅程导引台”原型源](../prototype/onboard-single-scenario/onboard-single-scenario-prototype.html?variant=A) 为布局与交互权威：左侧固定单场景旅程，中央只呈现当前一步、权威任务事实与单一主动作，右侧固定展示 1～8 号仓位及完整状态证据。不得把 B 或 C 作为另一套可并行上线的信息架构，也不得只按文字规格重新设计一个结构不同但“功能齐全”的替代界面。
2. **B、C 只保留为设计证据。** B“安全优先双栏”与 C“站点作业板”用于说明安全优先级和大尺寸触控区的备选取舍，不是生产方向。若实施需要吸收其局部元素，必须保持 A 的窗口层级、旅程层级、主工作区与固定八仓关系，并在实施变更中明确映射和理由。
3. **原型仍是 throwaway。** 单文件 HTML、假 Demand、假站点、假仓位状态、原型切换栏和评审状态选择器不得进入 ControlServer、OnboardHmi 或共享协议生产仓库。实施团队须用生产框架、真实投影、正式术语、错误码、输入设备适配、可访问性和错误处理重写，但不能因此忽略获选 A 的结构。

### 采用的完整交互边界

1. **使用 `.scratch` 下零依赖单文件 HTML 和新的 throwaway 单路由。** 当前仓库没有可嵌入的 OnboardHmi 页面或实现仓库，不创建生产 WPF 分支，也不以静态截图代替可交互状态评审。
2. **保留三案原型，A 获选。** A 以单 Demand 旅程为主，B/C 留作对照；默认查询参数与后续实现映射均指向 A。
3. **覆盖完整状态面。** A 必须呈现连接、五步 RecoveryHandshake、VehicleBusinessReadiness、TO_PICKUP、可信机台到站、Sublot 输入、批量装货、装货后等待新 PreDepartureSafetyCheck、TO_GATE、可信关卡到站、批量卸货、8005 本地完成、ConnectionLossSlotContainment、重启恢复和 ExceptionRecoverySession。
4. **四维车辆概览不得压成单一状态。** 运行、通信与业务就绪、当前作业、安全与联锁必须并列；TCP/TLS/Heartbeat 在线不得冒充 READY，本地运输完成不得冒充 DepartureSafe 或发车命令。
5. **车载端不选任务、不改业务事实。** 当前界面只展示 ControlServer 已承诺的唯一 Demand 和权威投影。机台端扫码与键盘输入共用 SublotSubmitted；ExpectedBasketCount、完整目标仓位集、Demand、站点和停靠计划只读，车载端不得选择、增删、换绑或按 STEP/EQP 重判。
6. **固定八仓同时展示业务与物理事实。** 1～8 号仓位必须分别显示是否属于本次目标、业务绑定、`OCCUPIED|EMPTY|UNKNOWN`、锁闭反馈、开锁输出复位和 ActiveUnlockSet；任一维度未知不得被另一个维度或人员按钮覆盖。
7. **正常装卸只暴露当前合法动作。** 装货按服务端冻结的完整集合批量开锁，花篮可任意顺序放入；卸货在关卡按当前任务与在车状态自动批量开始，不再次扫描 Sublot、不输入工号或接收确认。每仓必须闭环到目标占用态、锁闭和输出复位；明确相反占用态自动重开纠正，UNKNOWN 进入恢复。
8. **断联与重启 fail-closed。** 断联后离线投影只读，只允许 `SafelyFinishActiveUnlockSet`，不扩大集合、不本地取消、不设置自动超时；重连或重启后沿原 MessageId／SlotOperationAttemptId 完成五步对账，只有 SessionReadiness=READY 才恢复扫码、新仓位操作或移动。
9. **异常处置只有四条已批准路径。** 固定事件、人员、车辆、Demand 与仓位范围的 ExceptionRecoverySession 只展示 `RESUME_AFTER_REPAIR`、`COMPENSATE_LOAD_ALL_EMPTY`、`FAULT_CARGO_HANDOFF`、`FORCED_MECHANICAL_RECOVERY`。管理员身份、HardwareRecoveryRecord、实物交接或自由文本都不能覆盖停稳、锁闭、占用 UNKNOWN、输出复位、恢复对账或现场作业资质。
10. **本地完成与后续发车、PDA/MES 分离。** 全部卸货证据形成 `UnloadBatch + StopClosureCommit + Demand 成功终态 + TransportDemandCompletion` 原子提交后，界面可显示“8005 本地运输已完成”，但仍等待新的 PreDepartureSafetyCheck 和服务端调度；不等待、读取或回写外部 PDA/MES，也不因其未操作产生 8005 待办。
11. **急停是独立安全入口。** 当前合法业务动作保持单一主按钮；本车急停始终醒目可请求，但急停不取消 Demand、订单、货物或仓位绑定，解除后也不自动继续。

### 已接受但转移到实施／验收的风险

本票没有取得车载端开发同事对实际屏幕、输入设备或实现框架的反馈，且原型采用 `min-width: 1120px` 的桌面评审画布。因此以下事实仍未被证明，但按用户明确豁免不再阻塞本票：真实车载分辨率与缩放下是否无裁切、关键状态是否无需危险滚动、按钮与仓位是否满足触控尺寸及误触隔离、扫码枪焦点和键盘备用输入是否可靠、安全／断联／UNKNOWN 文案在现场距离和光照下是否可读，以及 A 的状态组合能否由车载端实际框架稳定实现。

这些风险已写入[决定受控工厂试运行配置、执行顺序与验收证据](11-decide-controlled-factory-pilot-configuration-and-acceptance-evidence.md)的后续验收范围。实施必须先建立 A 到生产窗口层级、网格、尺寸、间距、控件、状态和交互的具体映射，再在目标车载硬件或等效校准环境验证；发现不满足时应作为实施缺陷或需要用户重新裁决的设计偏差处理，不能反过来声称本票已获得车载端开发同事批准。

### 资产与验证

- [OnboardHmi 单场景操作原型 README](../prototype/onboard-single-scenario/README.md)
- [OnboardHmi 单场景操作原型 HTML](../prototype/onboard-single-scenario/onboard-single-scenario-prototype.html)
- 单一内嵌脚本语法与隔离 DOM 静态执行检查通过；A/B/C 均能渲染，每案恰有 8 个仓位、方案标签、完整状态证据和统一 Sublot 输入，且没有 HTTP(S) 外部脚本或样式依赖。
- 未运行 Golden WPF tier 2/3；本 Answer 是用户对原型方向与评审门禁的产品决定，不是正式车载视觉验收或生产实现验收。
