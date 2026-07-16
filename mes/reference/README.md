# PACKAGE / 花篮容量规则

`package-basket-capacity.csv` 是 PACKAGE 与一花篮最多料盒数的唯一可执行规则源。
当前 28 条规则来自客户对照表的 2026-07-16 迁移快照：27 条精确规则和 1 条
显式前缀规则。旧 Markdown 已退出维护，审阅视图由 CSV 自动生成。

## 字段

- `pattern`：去除首尾空白后用于匹配的字面值。
- `match_type`：仅允许 `exact` 或 `prefix`。
- `max_boxes_per_basket`：正整数，表示一花篮最多料盒数。
- `source`：规则来源。
- `status`：当前仅允许 `active`。
- `note`：规则说明。

## 匹配规则

1. 输入 PACKAGE 先执行 `strip()`；空值不匹配。
2. 在所有 `exact` 规则中进行区分大小写的完整字符串匹配。
3. 没有精确命中时，再匹配字面 `prefix`；多个前缀同时命中时取最长前缀。
4. `TOLL-` 是显式前缀且容量为 3，只匹配以 `TOLL-`（含连字符）开头的值。
   因此 `TOLL-8L` 命中，而 `TOLL`、`TOLLX` 均不命中。
5. 禁止模糊匹配、相似匹配、通配符和从相近封装形式继承容量。
   未命中值必须保留为未匹配，不能推断容量。

精确匹配始终优先于前缀匹配，即使前缀更长或在 CSV 中排在更前。

## 校验与生成视图

从仓库根目录运行：

```powershell
python -m mes.analysis.generate_package_rules_markdown
```

也可以直接运行：

```powershell
python mes/analysis/generate_package_rules_markdown.py
```

命令会严格校验 CSV，并重建
`mes/reference/package-basket-capacity.md`。该 Markdown 仅供审阅，不是规则源。
