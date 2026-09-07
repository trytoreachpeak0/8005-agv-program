# 当前需求基线

- Version: `v1.1.0`
- Baseline: [current-requirements-v1.1.0.md](baselines/current-requirements-v1.1.0.md)
- Release Record: 本版本经变更提案流程批准，见 [change-proposals/CP-0001.md](change-proposals/CP-0001.md)
- Baseline SHA-256: `5fe4b701a46b5d16818bcbfdd65748a8dcc774efab0583673daa53e08236fb53`
- Content Git Commit: `f2691893f7835a3d8035ba7dba6070e8dbc85b14`
- Annotated Git Tag: `requirements-baseline-v1.1.0`

本文件是唯一当前版本指针。候选版本在正式批准、提交并创建发布 tag 前不得替换此指针。

## 版本→哈希对照表

已归档的证据引用的是它当时那一版的哈希，**旧值一律不删**（变更执行流程第 4 步）。

| 版本 | 文件 | Baseline SHA-256 | Content Git Commit | Annotated Tag |
| --- | --- | --- | --- | --- |
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
| `v1.1.0` | 2026-09-07 | [`CP-0001`](change-proposals/CP-0001.md) | `REQ-0298` 重写（目录与路网分为两份各自具名的产品事实，`RouteGraphSnapshot` 持有有向站点图）；`REQ-0146` 增列五个 `imap` 只读端点 |
| `v1.0.0` | 2026-08-24 | none（首版恢复） | 首个批准需求基线，共 348 条 |
