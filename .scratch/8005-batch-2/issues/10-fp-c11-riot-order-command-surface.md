# 10 — `FP-C11` RIoT 订单命令面接入与对账

**做什么：** 让服务端能对 RIoT 侧的订单发出命令，并对每次命令做对账。做完之后，8005 的
阻断不再只是「停止建新单」——它能按住已发出的订单，也能让车真的停下来。

六个命令：`CANCEL`／`OrderHold`／`OrderContinue`／`HangContinue`／`triggerEmergency`／
`cancelEmergency`。**SDK 侧六个具名 Facade 已经存在并有测试**，本票是服务端接入，不是
写 SDK。

**继承 `RIoTRetryReconciliation` 对账语义**——命令不是发出去就算数，要确认终态。两条
需求对这件事有具体要求：

- `REQ-0248`：急停状态未确认前按受控退避持续重试 `triggerEmergency`，并保留现场兜底。
- `REQ-0249`：「停车宽、恢复严」——满足条件时自动触发不需人工授权；恢复走严格路径。

**一个同名不同物的陷阱，不要踩**：服务端现有 5 处 `DispatchDisable` 全是
`CreateDispatchDisabled`（8005 自己的建单开关），与 `REQ-0167` 说的 RIoT 侧车辆
`DispatchDisable` 是两回事。

`REQ-0167`（可证明的暂时阻断应自动恢复）落在本票：由 8005 自己造成、原因已消除且安全
事实可独立证明的临时阻断，自动恢复。

**安全类能力不允许带病投运**（规格 8.7 第 4 条）——三条自动急停属于这一类。

**冲突边界：** 命令面与对账实现为独立文件；表由票 06 提供；本票不改派车主循环，也不写
migration。

**前置：** 票 06（对账审计表与端口）、票 03（假 RIoT 的命令端点，否则无法在 L2 取证）。

**状态：** resolved（2026-09-08，见 `10-answer.md`）

- [x] 六个命令经具名 Facade 发出，`src/` 下 `.Raw` 仍零命中
- [x] 每次命令有对账：确认终态之前不认为命令成功
- [x] `triggerEmergency` 在状态未确认前按受控退避重试，退避参数可配置
- [x] 现场兜底路径保留并有文档说明（`REQ-0248`）
- [x] 自动触发急停不需人工授权；恢复路径走严格判据（`REQ-0249`）
- [~] `REQ-0167` 的自动恢复：原因消除且安全事实可独立证明时解除临时阻断，否则不解除
      —— 急停那一半完整落地；**`DispatchDisable` 那一半在本批次没有对象**（8005 从不向 RIoT
      发出车辆级 `DispatchDisable`，已由票 08 的 IL 扫描证实），见 `10-answer.md` 缺口一
- [x] 代码与测试里不把 `CreateDispatchDisabled` 与 RIoT 侧 `DispatchDisable` 混为一谈
- [x] L1 新增覆盖：每个命令的成功、失败、重试与对账各有测试
- [x] 无新增 migration
