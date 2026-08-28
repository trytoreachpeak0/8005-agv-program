# Round 10（2026-07-20）

## 1. 研究目标

1. **Q-004** 相同 `upperId` 重复提交的真实行为（终态 SUCCESS 后；可选 EXECUTING 中）。
2. **Q-006 续**：纯 move 上 `interrupt(pause=false)`；`CMD_ORDER_HELD` / `CONTINUE_FROM_HELD`；`order/v1/operate` 与 `task/.../command` 取消是否等价。含 `act` 的 interrupt：仅在能安全构造 act 子任务时测，否则记 BLOCKED。
3. **建单反例**：不存在 `appointVehicleKey`、非法 `mapId`、非法 `destination`；确认不误派其它车。OFF_LINE 建单：若无法安全切离线则记 SKIP。
4. **标识关联**：`upperId` ↔ 字符串 `orderId` ↔ 数值主键/`orderUuid`/`detailByOrderId` 交叉一致性。

## 2. 范围

- 仅测试车；map29；`byDefaultMissions`
- 不做：全局清理、批量、非测试车写操作、未知物理动作的深测

## 3. 授权

- 用户：批准测 1/2/3/4（幂等、Q-006 续、建单反例、标识关联）

## 4. 安全

- 写操作显式 `appointVehicleKey=测试车`
- 反例预期失败；若误派其它车 → 立即停测
- HELD/interrupt 后必须 cancel/continue 善后到 IDLE
- act：建单失败即停；若进入执行立即 cancel
