# 修正初始快照的 Git 状态分类

Type: task
Status: resolved
Blocked by: 10, 11

## Question

初始快照与材料清单把 58 条实际存在于固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e` 的路径标为 `untracked`；如何在不静默改写原始快照的前提下，查明采集脚本或路径处理的根因，建立逐路径、可复核的追加勘误，修正 `tracked-clean`/`untracked` 统计视图，并确保受影响的 R03、R10、R11、R13 调查不会遗漏 Git 历史？

## Answer

根因、逐路径证据和有效统计见 [初始快照 Git 状态追加勘误](../evidence/initial-snapshot/git-status-correction.md)；覆盖层为 [git-status-corrections.tsv](../evidence/initial-snapshot/git-status-corrections.tsv)，验证器为 [verify-git-status-corrections.ps1](../evidence/initial-snapshot/verify-git-status-corrections.ps1)。原采集脚本使用默认 `git ls-files`/`git diff --name-only` 的 C 风格引号和八进制转义输出，却与 `rg --files` 的真实 Unicode 路径直接比较，导致 58 条非 ASCII tracked 路径误判为 `untracked`。

原快照、清单与采集脚本保持不变，只追加明确勘误。58/58 经固定 HEAD 路径、blob、捕获哈希和 Git clean filter 复核后修正为 `tracked-clean`；有效统计由 `tracked-clean=1704, untracked=105` 修正为 `tracked-clean=1762, untracked=47`。验证器与原始反馈环均已通过：`corrections=58`、`false_untracked=0`。R03、R10、R11、R13 后续调查必须叠加勘误后再追溯 Git 历史；未来采集应新建版本并统一使用 `core.quotepath=false` 或正确的 NUL 分隔解析。
