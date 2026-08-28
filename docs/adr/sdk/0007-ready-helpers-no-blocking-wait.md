# 第一版提供可再派判定辅助，不内置阻塞 Wait

具名 Facade 保持单次读写；另提供基于 BC-STATE-003 的纯判定辅助（例如是否可再派：订单 SUCCESS 且车 IDLE）。不在 SDK 内置阻塞轮询 Wait*，编排与超时策略留给 MES。避免把调度状态机塞进客户端，同时减少 MES 写错到站/可再派条件。

**Status**: accepted

**Implementation**: `ReadyForNextOrder.IsReady` / `is_ready_for_next_order` 已交付（SUCCESS=5 + `procState=IDLE` + 非 `processingOrder`）。

**Considered Options**: 仅薄读写；薄读写 + 纯判定辅助（采纳）；内置 Wait* 阻塞跟单。
