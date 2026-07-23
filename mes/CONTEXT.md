# MES 调度与任务编排

宿迁长电 AGV 项目中，MES/调度侧如何消费 RIoT、处理运输任务生命周期与异常滞留。

## Language

**QueueingStall**:
RIoT 订单已创建但长期停留在 QUEUEING、迟迟不进入 EXECUTING 的滞留；通常需业务侧清积压或人工处理，不会自动变为 FAILED。
_Avoid_: 挂起（泛称）、OrderHang、HELD

**OrderHang**:
RIoT 订单 `orderState=HANG`；与 QueueingStall、HELD、急停冻结（可仍为 EXECUTING）都不同。已知可恢复路径依赖 HangContinue，且接口成功码不等于订单已恢复。
_Avoid_: QueueingStall、挂起（泛称）、HELD、急停

**HangContinue**:
对 OrderHang 下发 `CMD_ORDER_CONTINUE_FROM_HANG` 以尝试拉回 EXECUTING；须在真 HANG 且车辆可继续时使用，并复核订单是否真正离开 HANG。
_Avoid_: OrderContinue（从 HELD 恢复）、resume（泛称）

**ChargeHangReassign**:
充电失败 OrderHang 后，由 MES 自动改派前往其它充电桩再充的策略；改派前须 CANCEL 旧 HANG；选桩在配置允许的充电站集合内做 NearStationQuery（排除失败站）。
_Avoid_: HangContinue、人工改充（若未采用）
