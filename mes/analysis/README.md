# PACKAGE / 花篮容量离线分析

本包只使用 Python 标准库。

## 覆盖分析

从仓库根目录运行模块：

```powershell
python -m mes.analysis.analyze_package_coverage `
  path/to/MES_TASK_UNION.csv `
  path/to/output
```

或直接运行脚本：

```powershell
python mes/analysis/analyze_package_coverage.py `
  path/to/MES_TASK_UNION.csv `
  path/to/output
```

输入必须包含 `PACKAGE` 列；旧版不含该列的 6 列 CSV 会明确失败。
`TASK_TYPE` 和 `SUBLOT` 是可选列：缺少 `TASK_TYPE` 时统一归入
`(缺失列)`，缺少 `SUBLOT` 时样例为空。

输出目录包含：

- `summary.md`
- `unmatched_packages.csv`
- `prefix_matches.csv`
- `matched_packages.csv`

## API

- `load_rules()`：加载并严格校验规则 CSV。
- `resolve_package(package, rules=None)`：按“strip 后精确优先、最长前缀次之”解析。
- `calculate_expected_baskets(max_box_count, max_boxes_per_basket)`：整数上取整。
- `analyze_mes_task_union(input_csv, output_dir, rules=None)`：生成覆盖报告。

## 生成规则 Markdown 视图

```powershell
python -m mes.analysis.generate_package_rules_markdown
```

也可以直接运行同名 `.py` 文件。生成的 Markdown 仅供审阅，不可手工编辑。
