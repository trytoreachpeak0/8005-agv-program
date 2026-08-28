"""离线分析 MES_TASK_UNION CSV 的 PACKAGE 规则覆盖率。"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from mes.analysis.package_capacity import (  # type: ignore
        PackageResolution,
        RuleSet,
        load_rules,
    )
else:
    from .package_capacity import PackageResolution, RuleSet, load_rules


class CoverageAnalysisError(ValueError):
    """输入 CSV 不能完成覆盖分析。"""


@dataclass
class PackageAggregate:
    package: str
    resolution: Optional[PackageResolution]
    count: int = 0
    task_types: Counter = field(default_factory=Counter)
    sample_sublots: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CoverageResult:
    total_rows: int
    unique_packages: int
    empty_packages: int
    exact_rows: int
    prefix_rows: int
    unmatched_rows: int
    output_dir: Path


SUMMARY_NAME = "summary.md"
UNMATCHED_NAME = "unmatched_packages.csv"
PREFIX_NAME = "prefix_matches.csv"
MATCHED_NAME = "matched_packages.csv"
MANIFEST_NAME = "analysis-manifest.json"


def _normalized_cell(row: Dict[str, Optional[str]], column: str) -> str:
    value = row.get(column)
    return value.strip() if isinstance(value, str) else ""


def _task_type(row: Dict[str, Optional[str]], has_column: bool) -> str:
    if not has_column:
        return "(缺失列)"
    return _normalized_cell(row, "TASK_TYPE") or "(空值)"


def _distribution(counter: Counter) -> str:
    return "; ".join(
        f"{name}:{count}" for name, count in sorted(counter.items())
    )


def _add_sample(samples: List[str], value: str, sample_limit: int) -> None:
    if value and value not in samples and len(samples) < sample_limit:
        samples.append(value)


def _write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _aggregate_row(aggregate: PackageAggregate) -> dict:
    return {
        "PACKAGE": aggregate.package,
        "次数": aggregate.count,
        "TASK_TYPE分布": _distribution(aggregate.task_types),
        "样例SUBLOT": " | ".join(aggregate.sample_sublots),
    }


def analyze_mes_task_union(
    input_csv: Union[str, Path],
    output_dir: Union[str, Path],
    rules: Optional[Union[str, Path, RuleSet]] = None,
    *,
    encoding: str = "utf-8-sig",
    sample_limit: int = 3,
) -> CoverageResult:
    """分析 CSV 并写出固定的四个覆盖报告文件。"""

    if sample_limit < 0:
        raise ValueError("sample_limit 不能小于 0")
    input_path = Path(input_csv)
    destination = Path(output_dir)
    rule_set = rules if isinstance(rules, RuleSet) else load_rules(rules)

    try:
        handle = input_path.open("r", encoding=encoding, newline="")
    except OSError as exc:
        raise CoverageAnalysisError(f"无法读取输入 CSV {input_path}: {exc}") from exc

    aggregates: Dict[str, PackageAggregate] = {}
    task_summary = defaultdict(Counter)
    total_rows = 0
    empty_packages = 0
    exact_rows = 0
    prefix_rows = 0
    unmatched_rows = 0

    with handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if "PACKAGE" not in fieldnames:
            raise CoverageAnalysisError(
                "输入 CSV 缺少必需的 PACKAGE 列；旧版 6 列 "
                "MES_TASK_UNION CSV 不能用于容量覆盖分析"
            )
        if len(fieldnames) != len(set(fieldnames)):
            raise CoverageAnalysisError("输入 CSV 存在重复列名")

        has_task_type = "TASK_TYPE" in fieldnames
        has_sublot = "SUBLOT" in fieldnames
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise CoverageAnalysisError(
                    f"输入 CSV 第 {line_number} 行字段数多于表头"
                )
            total_rows += 1
            package = _normalized_cell(row, "PACKAGE")
            task_type = _task_type(row, has_task_type)
            task_summary[task_type]["total"] += 1

            if not package:
                empty_packages += 1
                task_summary[task_type]["empty"] += 1
                continue

            resolution = rule_set.resolve(package)
            if resolution is None:
                category = "unmatched"
                unmatched_rows += 1
            elif resolution.match_type == "exact":
                category = "exact"
                exact_rows += 1
            else:
                category = "prefix"
                prefix_rows += 1
            task_summary[task_type][category] += 1

            aggregate = aggregates.get(package)
            if aggregate is None:
                aggregate = PackageAggregate(package, resolution)
                aggregates[package] = aggregate
            aggregate.count += 1
            aggregate.task_types[task_type] += 1
            if has_sublot:
                _add_sample(
                    aggregate.sample_sublots,
                    _normalized_cell(row, "SUBLOT"),
                    sample_limit,
                )

    destination.mkdir(parents=True, exist_ok=True)
    ordered = sorted(aggregates.values(), key=lambda item: item.package)
    unmatched = [item for item in ordered if item.resolution is None]
    matched = [item for item in ordered if item.resolution is not None]
    prefix = [
        item
        for item in matched
        if item.resolution is not None
        and item.resolution.match_type == "prefix"
    ]

    _write_csv(
        destination / UNMATCHED_NAME,
        ("PACKAGE", "次数", "TASK_TYPE分布", "样例SUBLOT"),
        (_aggregate_row(item) for item in unmatched),
    )
    _write_csv(
        destination / PREFIX_NAME,
        (
            "PACKAGE",
            "matched_pattern",
            "max_boxes_per_basket",
            "次数",
            "TASK_TYPE分布",
            "样例SUBLOT",
        ),
        (
            {
                "PACKAGE": item.package,
                "matched_pattern": item.resolution.matched_pattern,
                "max_boxes_per_basket": item.resolution.max_boxes_per_basket,
                "次数": item.count,
                "TASK_TYPE分布": _distribution(item.task_types),
                "样例SUBLOT": " | ".join(item.sample_sublots),
            }
            for item in prefix
            if item.resolution is not None
        ),
    )
    _write_csv(
        destination / MATCHED_NAME,
        (
            "PACKAGE",
            "match_type",
            "matched_pattern",
            "max_boxes_per_basket",
            "次数",
            "TASK_TYPE分布",
            "样例SUBLOT",
        ),
        (
            {
                "PACKAGE": item.package,
                "match_type": item.resolution.match_type,
                "matched_pattern": item.resolution.matched_pattern,
                "max_boxes_per_basket": item.resolution.max_boxes_per_basket,
                "次数": item.count,
                "TASK_TYPE分布": _distribution(item.task_types),
                "样例SUBLOT": " | ".join(item.sample_sublots),
            }
            for item in matched
            if item.resolution is not None
        ),
    )

    result = CoverageResult(
        total_rows=total_rows,
        unique_packages=len(aggregates),
        empty_packages=empty_packages,
        exact_rows=exact_rows,
        prefix_rows=prefix_rows,
        unmatched_rows=unmatched_rows,
        output_dir=destination,
    )
    _write_summary(
        destination / SUMMARY_NAME,
        input_path,
        result,
        task_summary,
    )
    if isinstance(rules, RuleSet):
        rules_path = None
    elif isinstance(rules, (str, Path)):
        rules_path = Path(rules)
    else:
        rules_path = (
            Path(__file__).resolve().parents[1]
            / "reference"
            / "package-basket-capacity.csv"
        )
    output_names = (SUMMARY_NAME, UNMATCHED_NAME, PREFIX_NAME, MATCHED_NAME)
    (destination / MANIFEST_NAME).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "input": str(input_path),
                "input_sha256": _sha256(input_path),
                "rules": str(rules_path) if rules_path is not None else "in-memory",
                "rules_sha256": (
                    _sha256(rules_path) if rules_path is not None else None
                ),
                "outputs": {
                    name: _sha256(destination / name) for name in output_names
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def _write_summary(
    path: Path,
    input_path: Path,
    result: CoverageResult,
    task_summary: Dict[str, Counter],
) -> None:
    lines = [
        "# PACKAGE / 花篮容量规则离线覆盖分析",
        "",
        "> 本报告由 `mes.analysis.analyze_package_coverage` 生成。",
        "",
        f"- 输入：`{input_path}`",
        f"- 总行数：{result.total_rows}",
        f"- 去重 PACKAGE 数（不含空值）：{result.unique_packages}",
        f"- PACKAGE 空值行数：{result.empty_packages}",
        f"- exact 命中行数：{result.exact_rows}",
        f"- prefix 命中行数：{result.prefix_rows}",
        f"- unmatched 行数：{result.unmatched_rows}",
        "",
        "## 按 TASK_TYPE 汇总",
        "",
        "| TASK_TYPE | 总行数 | 空值 | exact | prefix | unmatched |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for task_type in sorted(task_summary):
        counts = task_summary[task_type]
        escaped = task_type.replace("|", "\\|")
        lines.append(
            f"| {escaped} | {counts['total']} | {counts['empty']} | "
            f"{counts['exact']} | {counts['prefix']} | {counts['unmatched']} |"
        )
    lines.extend(
        [
            "",
            "## 明细文件",
            "",
            f"- `{UNMATCHED_NAME}`：未匹配 PACKAGE 聚合。",
            f"- `{PREFIX_NAME}`：显式前缀命中 PACKAGE 聚合。",
            f"- `{MATCHED_NAME}`：全部 exact/prefix 命中 PACKAGE 聚合。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="分析 MES_TASK_UNION CSV 的 PACKAGE 容量规则覆盖率"
    )
    parser.add_argument("input_csv", help="含 PACKAGE 列的 MES_TASK_UNION CSV")
    parser.add_argument("output_dir", help="报告输出目录")
    parser.add_argument("--rules", help="规则 CSV；默认使用仓库标准规则")
    parser.add_argument("--encoding", default="utf-8-sig", help="输入 CSV 编码")
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=3,
        help="每个 PACKAGE 最多保留的 SUBLOT 样例数",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = analyze_mes_task_union(
            args.input_csv,
            args.output_dir,
            args.rules,
            encoding=args.encoding,
            sample_limit=args.sample_limit,
        )
    except (CoverageAnalysisError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    print(
        f"完成：{result.total_rows} 行，"
        f"exact={result.exact_rows}，prefix={result.prefix_rows}，"
        f"unmatched={result.unmatched_rows}；输出 {result.output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
