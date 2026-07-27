# 16 — Watch 环境变量配置绑定修正

**What to build:** 修正 `MesIngest.Watch` 配置：`AddEnvironmentVariables(prefix: "MesIngestWatch__")` 当前写不进 `Watch` 节；实际生效的是手写 `GetEnvironmentVariable`。二选一修好或删掉死路径，并停止对 `RefreshSeconds` 的双重校验/覆盖。

**Blocked by:** None — can start immediately（09 已完成；本票为 review Standards near-hard 跟进）

**Status:** done

- [x] 环境变量能可靠覆盖 `Watch:BaseUrl` / `RefreshSeconds` / `SharedSecret`（与 README / INSTALL 文档声明一致）
- [x] 删除无效的 `AddEnvironmentVariables` 死路径，或改为能绑进 `Watch` 节的正确前缀/扁平键；不保留「看似配置了其实无效」的双轨
- [x] `RefreshSeconds` 只在一处规范化（最小值），避免 env 手写与 Bind 后再夹一道互相踩
- [x] 轻量测试或启动路径验证：仅设 `MesIngestWatch__BaseUrl`（及文档中的等价键）即可生效

## Comments

- 2026-07-27: From `/code-review ffe1f49` Standards (near-hard). Evidence: `App.xaml.cs` binds `config.GetSection("Watch")` after `AddEnvironmentVariables(prefix: "MesIngestWatch__")` — keys like `MesIngestWatch__BaseUrl` do not land under `Watch:*`; hand-written `Environment.GetEnvironmentVariable("MesIngestWatch__BaseUrl")` etc. are what work. Ticket 09 comment claimed env override via `MesIngestWatch__*`.
- 2026-07-27: Fixed via `WatchOptionsLoader`: bind `Watch` section, then overlay flat root keys from `MesIngestWatch__*` (prefix strip). Removed hand-written `GetEnvironmentVariable` dual path; `RefreshSeconds` min clamp only in the loader (also dropped `MainWindow` `Math.Max` clamp). Tests in `WatchOptionsLoaderTests`.
