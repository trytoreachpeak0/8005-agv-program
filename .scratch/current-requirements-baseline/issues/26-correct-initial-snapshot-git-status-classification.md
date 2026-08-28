# 修正初始快照的 Git 状态分类

Type: task
Status: open
Blocked by: 10, 11

## Question

初始快照与材料清单把 58 条实际存在于固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e` 的路径标为 `untracked`；如何在不静默改写原始快照的前提下，查明采集脚本或路径处理的根因，建立逐路径、可复核的追加勘误，修正 `tracked-clean`/`untracked` 统计视图，并确保受影响的 R03、R10、R11、R13 调查不会遗漏 Git 历史？
