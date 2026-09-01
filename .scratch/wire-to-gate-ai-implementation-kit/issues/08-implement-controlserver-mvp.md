# 实现并自测 ControlServer MVP

Type: task
Mode: AFK
Status: resolved
Blocked by: 07

## Question

如何在 `ControlServer_MVP` 分支按 W2G-IS-00～07 实现可运行 ControlServer：连接/session/readiness、五步恢复、可靠 inbox/outbox、需求受理与防重、单 Demand 选择、多仓装卸事务、RIoT 意图与未知结果对账、完成记录、持久化恢复、Fake Onboard、健康检查、配置与结构化日志？

每个切片必须先写或更新自动化测试，再实现最小生产代码，运行本端 G2 和 Fake Onboard 场景并保存绑定 commit/协议候选的证据。核心副作用不得由内存占位、手工按钮或测试专用路径代替。MesIngest 必须消费现有只读 V2 契约；RIoT 适配器单元测试可以隔离 HTTP/SDK 边界，但不得建设或声称通过 RIoT 模拟器，实际移动集成只能以真实 RIoT 环境证据通过。

## Answer

已在远程 `ControlServer_MVP` 完成并推送生产提交 `8fae66f65cde41d1b1c64a328661860ee16a481a`，精确绑定协议候选 `72ddde595165468520d9f3a46b25e4aa4eec0c3f` 与 manifest SHA-256 `e878d89e820535fe1eb64b85681b9c2994fb98646309e6ba768219c5c8735f2e`。实现包括 EF Core SQLite 持久状态核与初始迁移、五步 session/recovery/readiness、持久 inbox/outbox 与首响应重放、Demand/TransportDemandKey 原子受理、多仓装卸及原子完成、断联/强制恢复 generation 栅栏、只读 MesIngest V2 适配器、RIoT `upperId` 对账与默认 move 建单 allowlist、未知结果 fail-closed、Host 健康/版本端点、结构化日志及独立 Fake Onboard。

RIoT 建单冻结车辆、Map、目标站、AGV lifecycle generation 和 dispatch generation；只有 HTTP 404 被视为可靠不存在，超时、非成功业务码和畸形响应均保持 `UNKNOWN`。即使建单响应成功，也必须再按原 `upperId` 独立查询，查询确认后才把 movement intent 标记为 `CONFIRMED`。本票没有连接真实 RIoT、没有创建真实订单或触发车辆动作。

验证结果：锁定 SDK `8.0.424` / runtime `8.0.30` 的 Release 全解决方案构建为 0 warning、0 error；ControlServer 自动化测试 17/17 通过。全新 SQLite 文件成功应用 `20260825101420_InitialWireToGate`（EF product version `8.0.30`），真实 Host 与独立 FakeOnboard 进程完成八仓空恢复握手，`/health/ready` 返回 `ready`。提交后重新串行运行 W2G-IS-00～07，测试数分别为 2、3、1、7、1、1、3、1，八个 G2 全部 PASS；证据保存在产品仓库忽略目录 `artifacts/g2/issue08-8fae66f-final/`，每份 `gate-result.json` 都绑定上述实现 commit、协议 commit 和 manifest hash。

本票只关闭 ControlServer 候选实现与本地 G2。协议仍为 `CANDIDATE_UNAPPROVED`；真实 RIoT 环境移动集成、车辆/Map/站点资格、G3、OnboardHmi、安装和现场验收仍由后续票据负责，不能据此宣称整个双端 MVP 或真实移动闭环完成。
