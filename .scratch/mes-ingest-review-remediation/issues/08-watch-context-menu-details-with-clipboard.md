# 08 — 右键菜单同时保留「查看详情」与剪贴板动作

**What to build:** TransportDemands/Alerts 网格右键须同时提供广告过的「查看详情」与复制单元格/整行动作；剪贴板行为不得整表替换掉详情入口。

**Blocked by:** None — can start immediately

**Status:** done

## Parent / References

- Issues:
  - `.scratch/mes-ingest-watch-operations/issues/08-watch-grid-clipboard.md`
  - `.scratch/mes-ingest-watch-operations/issues/11-watch-alert-detail-and-unified-events.md`
- Handoff finding: context menu replaced wholesale by clipboard behavior

不重新定义复制 TSV 或详情窗口行为；本票恢复菜单组合。

## Repro

1. 在 Alerts（及 Demand，若曾提供详情）行上右键。
2. 确认是否仍有「查看详情」以及复制单元格/整行/含列名整行。
3. 点「查看详情」应打开既有非模态详情。

期望失败态（现状）：clipboard behavior 整表替换 ContextMenu，详情入口不可用。

## Regression tests

- [x] 菜单项同时包含详情与三类复制（或 Demand 侧对等的已承诺项）
- [x] 「查看详情」仍走双击/Enter 同一详情通路
- [x] 复制行为（null → `null`、Tab 分隔、本地时区文本）回归不被破坏
- [x] 未选中单元格时右键仍先聚焦再复制（ticket 08 既有验收）

## Acceptance criteria

- [x] 右键可打开详情且可复制，二者共存
- [x] 不回归 clipboard 与详情投影既有测试
- [x] 手工或 UI 自动化可演示菜单完整

## Comments

- 2026-08-01: Implemented in `97e75a4`. Alerts XAML keeps「查看详情」; `WatchGridClipboardBehavior.Attach` appends clipboard actions. Covered by `ComposeContextMenuHeaders` + `MainWindow_attaches_clipboard_copy_to_both_grids` + `Alert_view_details_menu_and_double_click_open_same_detail_window` (menu / double-click / Enter → same `AlertDetailWindow`). Right-click focus remains `PreviewMouseRightButtonDown` → `SelectUnderMouse` (visual hit-test not unit-automated; same as original watch-ops ticket 08). Full suite green (338).
