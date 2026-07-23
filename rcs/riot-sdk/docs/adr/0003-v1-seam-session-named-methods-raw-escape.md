# 第一版对外 seam：RiotSession 具名方法为主，Raw 为逃逸舱

调用方应以 `RiotSession` 上的具名 Facade 为稳定入口；Device/Tasks/Order 等上的 `.Raw` 仅作未封装接口的临时逃逸，不保证签名稳定，MES 生产路径不应依赖 Raw。在「Lab 共用 Facade、不为探针扩正式 API」与「Lab 仍需偶发摸未封装接口」之间取折中。

**Status**: accepted

**Considered Options**: 具名方法 + Raw 逃逸舱（采纳）；仅具名 Facade、不公开 Raw；允许业务直接依赖 Generated。
