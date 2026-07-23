# 第一版必须封装的 Facade 能力范围

第一版具名 Facade 覆盖 DispatchLoop 全量控制面：CallApiKey 鉴权、可调度车发现与解析、Map/Station 枚举、RouteCost 与 NearStationQuery、byDefaultMissions 建单与查单、CMD_ORDER_CANCEL、DispatchEnable/Disable、EmergencyStop 触发与解除、PriorityExec、OrderHold/OrderContinue、**HangContinue**。明确排除：interrupt、task/v1/order 建单主路径、几何 path；不以「单一 Continue 自动按状态选命令」代替 HELD/HANG 配对。imap 经 Kiota 纳入生成（见 ADR-0007）。

**Status**: accepted

**Implementation**: C# / Python 具名方法已交付；对照表见 [`docs/facade-v1.md`](../facade-v1.md)。可再派纯判定辅助见 ADR-0008（已交付）。

**Considered Options**: 瘦身闭环；闭环+路径/控制面；上表 + HangContinue 具名（采纳）；HangContinue 仅 RawEscape；HELD/HANG 合并为一个 Continue。
