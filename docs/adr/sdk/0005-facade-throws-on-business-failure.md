# 具名 Facade 统一将业务失败转为 RiotApiException

具名 Facade 在 HTTP 失败或业务 `code` 非成功时抛出 `RiotApiException`；成功路径返回已解开的业务结果。RouteCost 的 `costs=-1`（不可达）视为领域结果，不抛异常。RawEscape 不受此约束。这样 Session 成为稳定 seam，避免 MES 每次手拆 ResponseMsg，同时与 AdminLogin 已有行为对齐。

**Status**: accepted

**Considered Options**: Facade 统一抛业务异常（采纳）；一律返回原始 ResponseMsg；读写混合策略。
