# 初始快照 Git 状态追加勘误

## 结论

初始快照与无损材料清单中的 105 条 `untracked` 有 58 条是假阳性；它们都存在于固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e`，且捕获时 Git 视为 clean。原始资产保持不变，本目录新增 [git-status-corrections.tsv](git-status-corrections.tsv) 作为逐路径覆盖层，并由 [verify-git-status-corrections.ps1](verify-git-status-corrections.ps1) 验证。

有效统计应读取为：

| 状态 | 原始统计 | 勘误后 |
|---|---:|---:|
| `tracked-clean` | 1,704 | 1,762 |
| `untracked` | 105 | 47 |

## 根因

[capture.ps1](capture.ps1) 第 43～45 行直接读取默认 `git ls-files` 与 `git diff --name-only`，而候选路径来自第 80、109 行的 `rg --files`。Git 默认 `core.quotepath=true`，因此把非 ASCII 路径输出为带双引号的八进制转义文本；`rg` 返回真实 Unicode。第 134 行按字符串集合判断跟踪状态时，两种表示无法相等，58 条非 ASCII tracked 路径遂落入 `untracked`。

最小反例是 `file-naming-convention/文件命名规范.md`：

- 默认 `git ls-files` 输出 `"file-naming-convention/\346\226\207..."`；
- `git -c core.quotepath=false ls-files` 输出真实 Unicode 路径；
- 固定 HEAD 可精确定位该路径，原清单却记为 `untracked`。

105 条原始 `untracked` 中恰有 58 条非 ASCII；应用 `core.quotepath=false` 后，剩余 47 条均不在固定 HEAD，故是真正未跟踪材料。原始 [worktree-status.txt](worktree-status.txt) 未把这 58 条记录为修改；当前文件字节仍与捕获 SHA-256 全部相同，且对 58 条执行 `git hash-object --path` 后均与固定 HEAD blob 相同，所以修正状态统一为 `tracked-clean`。直接比较 Git blob 与工作树 SHA-256 曾出现 7 条差异，但那是换行/clean filter 的字节表现差异，不能据此标为 modified。

## 影响范围

逐路径批次分布为：

| 批次 | 条数 |
|---|---:|
| R01 | 12 |
| R03 | 1 |
| R10 | 2 |
| R11 | 1 |
| R13 | 3 |
| E02 | 29 |
| E03 | 9 |
| G01 | 1 |

R01 调查已经识别其中 12 条并保留了历史追溯；后续 R03、R10、R11、R13 调查必须先应用本勘误，再运行 `git log --follow`，不得因原 `untracked` 字段跳过历史。E02/E03/G01 仍只是现状或治理证据，勘误只恢复 Git 身份，不改变材料角色、内容哈希、批准状态或权威等级。

## 原始资产与未来采集

以下原始观察不改写：

- [candidate-documents.tsv](candidate-documents.tsv)
- [snapshot.md](snapshot.md) 中的原始状态统计
- [worktree-status.txt](worktree-status.txt)
- [capture.ps1](capture.ps1)
- [material-inventory.tsv](../material-inventory/material-inventory.tsv)

未来采集脚本应创建明确的新版本，并对所有返回路径的 Git 命令统一使用 `-c core.quotepath=false`，或改用 NUL 分隔输出并正确解码；至少覆盖 `ls-files`、两种 `diff --name-only`、`status` 和 `check-ignore`。不能直接改写本次 `capture.ps1` 后声称它仍是原始采集方法。

## 验证

运行：

```powershell
& '.scratch/current-requirements-baseline/evidence/initial-snapshot/verify-git-status-corrections.ps1'
```

验证器检查 58 条勘误路径唯一、原状态一致、固定 HEAD 路径与 blob 一致、覆盖后不再存在假 `untracked`，并断言修正统计为 1,762/47。

