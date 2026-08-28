# Map/Station 经 imap OpenAPI 纳入 Kiota 生成

第一版将 `riot_swagger/imap.json` 纳入 `riot-sdk` 的 specs 与 generate 管线，再在 Session 下提供 Map/Station 具名 Facade，与 Device/Order/Task 一致。不采用长期手写 imap HTTP 旁路，以免双端与契约测试分叉。

**Status**: accepted

**Considered Options**: Kiota 生成 imap（采纳）；手写 Map/Station 客户端；Map/Station 不进主链。
