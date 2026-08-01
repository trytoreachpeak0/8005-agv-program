# 12 — Watch 本地日志故障不得阻塞刷新

**What to build:** Watch 的连接事件与延迟遥测在日志超限、文件被占用、目录只读或磁盘写入失败时，仍须在有界时间内返回，不得把已经成功的 Host 拉取变成卡死或失败；同时为本地日志自身的故障保留一个不依赖同一失败目录的可观察诊断通道。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 体积保留遇到无法删除的最旧文件时不会无限重试；单次清理有明确的无进展退出条件，并可继续处理其它可删除候选
- [x] 日志追加、目录枚举、文件属性读取和保留删除中的 IO/权限失败均不得阻塞或改变成功 HTTP refresh 的结果
- [x] 当主日志目录不可写或磁盘空间不足时，操作员仍能通过不依赖该目录的通道看到经过清理的 `TELEMETRY_IO` 诊断
- [x] 诊断不得包含 SharedSecret、Bearer token、密码或完整连接串
- [x] 自动化测试覆盖被占用的超限旧文件、只读/不可用目录、正常按天与按体积清理，并证明失败路径在有界时间内完成

## Comments

- 2026-08-01: Implemented a bounded single-reader background dispatcher for all Watch local log filesystem work, immediate in-memory connection-event visibility, and a 200-entry directory-independent `TELEMETRY_IO` fallback shown in Events. Retention now attempts each size candidate at most once and continues past locked files. Secret cleaning covers quoted SharedSecret/Bearer/password values and explicit or known-shape connection strings. Targeted tests (37) and the full suite (345) pass; the post-fix Spec review reported no remaining findings.
