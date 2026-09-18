# 当前需求基线

- Version: `v1.4.0`
- Baseline: [current-requirements-v1.4.0.md](baselines/current-requirements-v1.4.0.md)
- Release Record: 本版本经变更提案流程批准，见 [change-proposals/CP-0004.md](change-proposals/CP-0004.md) 与 [change-proposals/CP-0005.md](change-proposals/CP-0005.md)（合并批准）
- Baseline SHA-256: `ea3e3b11d131c01a5d4dfee6c7cc3c31eb6fa8205bacf3c505300277f3928d74`
- Content Git Commit: `3154c41fd0bef974290bc0f81ee05695f818921b`
- Annotated Git Tag: `requirements-baseline-v1.4.0`

本文件是唯一当前版本指针。候选版本在正式批准、提交并创建发布 tag 前不得替换此指针。

## 版本→哈希对照表

已归档的证据引用的是它当时那一版的哈希，**旧值一律不删**（变更执行流程第 4 步）。

| 版本 | 文件 | Baseline SHA-256 | Content Git Commit | Annotated Tag |
| --- | --- | --- | --- | --- |
| `v1.4.0` | [current-requirements-v1.4.0.md](baselines/current-requirements-v1.4.0.md) | `ea3e3b11d131c01a5d4dfee6c7cc3c31eb6fa8205bacf3c505300277f3928d74` | `3154c41fd0bef974290bc0f81ee05695f818921b` | `requirements-baseline-v1.4.0` |
| `v1.3.0` | [current-requirements-v1.3.0.md](baselines/current-requirements-v1.3.0.md) | `ac74c78e6e51778898041500c6d7a897909536707c5fed96b44349aacf8fbec7` | `e78cd24fa047b6599e896be6b55cd295f94cadce` | `requirements-baseline-v1.3.0` |
| `v1.2.0` | [current-requirements-v1.2.0.md](baselines/current-requirements-v1.2.0.md) | `08051d5eaa2be88d4388d95fd0467c31217a9ada10dad1ab8bc813cf8ac7c782` | `8f37b73fc205104ec5ba090317d3d125016d35d8` | `requirements-baseline-v1.2.0` |
| `v1.1.0` | [current-requirements-v1.1.0.md](baselines/current-requirements-v1.1.0.md) | `5fe4b701a46b5d16818bcbfdd65748a8dcc774efab0583673daa53e08236fb53` | `f2691893f7835a3d8035ba7dba6070e8dbc85b14` | `requirements-baseline-v1.1.0` |
| `v1.0.0` | [current-requirements-v1.0.0.md](baselines/current-requirements-v1.0.0.md) | `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba` | `b9f321228b534a3b316d3ac1abede05176ed6a70` | `requirements-baseline-v1.0.0` |

**哈希的计算口径是 git blob 的内容（LF 行尾），不是工作树文件。**该仓 `core.autocrlf=true`
而基线文件在 `.gitattributes` 里没有 `-text` 保护，checkout 后工作树是 CRLF，直接对工作树
文件跑 `sha256sum` 得到的值与本表对不上，那不是文件被改过。复核用：

```bash
git cat-file blob <tag>:requirements/baselines/current-requirements-<版本>.md | sha256sum
```

## 变更历史

| 版本 | 日期 | 变更提案 | 内容 |
| --- | --- | --- | --- |
| `v1.4.0` | 2026-09-18 | [`CP-0004`](change-proposals/CP-0004.md)、[`CP-0005`](change-proposals/CP-0005.md) | 一次只开一个仓门与仓位卡住时的出口，两份提案合并批准：`CP-0004` 新增 `REQ-0357`（业务仓位操作一次只开一扇仓门，先 FRONT 后 REAR、组内按仓位号，前一仓 `UNKNOWN` 时停下转人工，维护开门模式例外），修订 `REQ-0223`（操作员手工重开同样一次一扇）、`REQ-0353`（两组仓门同样一次一扇）、`REQ-0226`（维护开门只在整车没有未收敛的业务仓位操作时进入）；`CP-0005` 新增 `REQ-0358`（当前仓位等待操作员过久时上报服务端）、`REQ-0359`（持异常处置权限的管理员在服务端人工判故障，把该仓判为 `UNKNOWN` 进入恢复）。共 359 条 |
| `v1.3.0` | 2026-09-15 | [`CP-0003`](change-proposals/CP-0003.md) | 急停锁住即视为停稳、人员确认后由服务端解除：新增 `REQ-0356`（服务端已登录人员确认原因已消除、车上无货、仓门已关闭并记下身份后由服务端解除，解除前订单须已终结，不重触发）；修订 `REQ-0247`（急停状态回查确认为 `CAN_RECOVER`／`CAN_NOT_RECOVER` 即视为已停稳）、`REQ-0248`（锁住后监控急停状态，人工确认后的解除不属于意外恢复）。共 356 条 |
| `v1.2.0` | 2026-09-15 | [`CP-0002`](change-proposals/CP-0002.md) | 前后仓位分侧：新增 `REQ-0349`～`REQ-0355` 七条；修订十五条——`REQ-0191`／`0208`／`0210` 改为开门侧随分区归属指派、容量按所需仓位分组计，`REQ-0204`、`0324`、`0334`、`0335`、`0338`、`0340`、`0342`、`0343` 固定站点改按 `mapId + TASK_TYPE` 绑定，`REQ-0304`、`0336`、`0337`、`0348` 的「公共站点功能」措辞改为按任务类型、文义不变。共 355 条 |
| `v1.1.0` | 2026-09-07 | [`CP-0001`](change-proposals/CP-0001.md) | `REQ-0298` 重写（目录与路网分为两份各自具名的产品事实，`RouteGraphSnapshot` 持有有向站点图）；`REQ-0146` 增列五个 `imap` 只读端点 |
| `v1.0.0` | 2026-08-24 | none（首版恢复） | 首个批准需求基线，共 348 条 |
