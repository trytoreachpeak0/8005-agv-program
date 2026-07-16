"""从规则 CSV 生成只读 Markdown 视图。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from mes.analysis.package_capacity import (  # type: ignore
        DEFAULT_RULES_PATH,
        RuleValidationError,
        load_rules,
    )
else:
    from .package_capacity import (
        DEFAULT_RULES_PATH,
        RuleValidationError,
        load_rules,
    )


DEFAULT_OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "reference"
    / "package-basket-capacity.md"
)


def _markdown_cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|")


def generate_markdown(rules_path: Path, output_path: Path) -> int:
    rule_set = load_rules(rules_path)
    lines = [
        "# PACKAGE / 花篮容量规则",
        "",
        "> **此文件由 CSV 自动生成，不可手工编辑。**",
        "> 规则源：`mes/reference/package-basket-capacity.csv`。",
        "",
        "| pattern | match_type | max_boxes_per_basket | source | status | note |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for rule in rule_set.rules:
        cells = (
            rule.pattern,
            rule.match_type,
            rule.max_boxes_per_basket,
            rule.source,
            rule.status,
            rule.note,
        )
        lines.append("| " + " | ".join(_markdown_cell(cell) for cell in cells) + " |")
    lines.extend(["", f"共 {len(rule_set.rules)} 条规则。", ""])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(rule_set.rules)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="从规则 CSV 生成 Markdown 视图")
    parser.add_argument(
        "--rules",
        type=Path,
        default=DEFAULT_RULES_PATH,
        help="规则 CSV 路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Markdown 输出路径",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        count = generate_markdown(args.rules, args.output)
    except (RuleValidationError, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    print(f"已生成 {args.output}（{count} 条规则）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
