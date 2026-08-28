"""MES_TASK_UNION 工厂结果的离线质量与性能报告。"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .hashing import sha256_file


TASK_TYPES = (
    "DIE_TO_WIRE_STAGING",
    "DIE_TO_OVEN",
    "WIRE_TO_GATE",
    "WIRE_TO_OPTICAL",
    "STAGING_TO_WIRE",
    "WIRE_TO_NITROGEN",
)
EXPECTED_COLUMNS = (
    "TASK_TYPE",
    "SUBLOT",
    "AREA",
    "EQP",
    "STEP",
    "DATES",
    "PACKAGE",
)
DECLARED_MAX_BYTES = {"SUBLOT": 40, "AREA": 30, "EQP": 50, "STEP": 255}
GO_LIVE = datetime(2026, 8, 1, 0, 0, 0)
SOURCE_TASK_TYPES = {
    "CUSTOMER_BASELINE_DIE_TO_WIRE_STAGING": "DIE_TO_WIRE_STAGING",
    "CUSTOMER_BASELINE_DIE_TO_OVEN": "DIE_TO_OVEN",
    "CUSTOMER_BASELINE_WIRE_TO_GATE": "WIRE_TO_GATE",
    "CUSTOMER_BASELINE_WIRE_TO_OPTICAL": "WIRE_TO_OPTICAL",
    "CUSTOMER_BASELINE_STAGING_TO_WIRE": "STAGING_TO_WIRE",
    "CUSTOMER_BASELINE_WIRE_TO_NITROGEN": "WIRE_TO_NITROGEN",
}


class QualityError(ValueError):
    """MES_TASK_UNION 结果不满足可分析前提。"""


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
            raise QualityError(
                f"{path.name} 列不匹配：期望 {EXPECTED_COLUMNS}，"
                f"实际 {tuple(reader.fieldnames or ())}"
            )
        return [
            {column: (row.get(column) or "").strip() for column in EXPECTED_COLUMNS}
            for row in reader
        ]


def _date(value: str) -> datetime | None:
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def analyze_task_union(path: str | Path) -> dict[str, Any]:
    """返回可序列化的质量报告。"""

    source = Path(path)
    rows = _read_rows(source)
    counts = Counter(row["TASK_TYPE"] for row in rows)
    unknown = sorted(set(counts) - set(TASK_TYPES))
    nulls = {
        column: sum(not row[column] for row in rows)
        for column in EXPECTED_COLUMNS
    }

    by_task_sublot: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    by_sublot: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_eqp: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_task_sublot[(row["TASK_TYPE"], row["SUBLOT"])].append(row)
        by_sublot[row["SUBLOT"]].append(row)
        by_eqp[row["EQP"]].append(row)

    # 同一 TASK_TYPE + SUBLOT 多行一律硬失败（含完全相同行，或其它列不同）。
    task_sublot_duplicates = []
    for (task_type, sublot), items in by_task_sublot.items():
        if len(items) <= 1:
            continue
        distinct_fingerprints = sorted(
            {
                tuple(item[column] for column in EXPECTED_COLUMNS)
                for item in items
            }
        )
        task_sublot_duplicates.append(
            {
                "task_type": task_type,
                "sublot": sublot,
                "row_count": len(items),
                "distinct_row_count": len(distinct_fingerprints),
                "eqp_area_pairs": sorted(
                    {(item["EQP"], item["AREA"]) for item in items}
                ),
            }
        )
    task_sublot_duplicates.sort(key=lambda item: (item["task_type"], item["sublot"]))

    cross_type_conflicts = []
    gate_optical_conflicts = []
    for sublot, items in by_sublot.items():
        types = sorted({item["TASK_TYPE"] for item in items})
        if len(types) > 1:
            cross_type_conflicts.append({"sublot": sublot, "types": types})
        if {"WIRE_TO_GATE", "WIRE_TO_OPTICAL"}.issubset(types):
            gate_optical_conflicts.append(sublot)

    eqp_multi_area = []
    for eqp, items in by_eqp.items():
        areas = sorted({item["AREA"] for item in items if item["AREA"]})
        if eqp and len(areas) > 1:
            eqp_multi_area.append({"eqp": eqp, "areas": areas})

    hard_failures: list[str] = []
    if task_sublot_duplicates:
        hard_failures.append("TASK_TYPE_SUBLOT_DUPLICATE")

    dates = [_date(row["DATES"]) for row in rows if row["DATES"]]
    valid_dates = [value for value in dates if value is not None]
    invalid_dates = sum(value is None for value in dates)
    max_bytes = {
        column: max(
            (len(row[column].encode("utf-8")) for row in rows),
            default=0,
        )
        for column in DECLARED_MAX_BYTES
    }
    return {
        "input": source.name,
        "row_count": len(rows),
        "counts": {task_type: counts.get(task_type, 0) for task_type in TASK_TYPES},
        "unknown_task_types": unknown,
        "nulls": nulls,
        "hard_failures": hard_failures,
        "hard_failure": bool(hard_failures),
        "task_sublot_duplicate_count": len(task_sublot_duplicates),
        "task_sublot_duplicate_extra_rows": sum(
            item["row_count"] - 1 for item in task_sublot_duplicates
        ),
        "task_sublot_duplicate_samples": task_sublot_duplicates[:20],
        "cross_type_conflict_count": len(cross_type_conflicts),
        "cross_type_conflict_samples": cross_type_conflicts[:20],
        "gate_optical_conflict_count": len(gate_optical_conflicts),
        "gate_optical_conflict_samples": gate_optical_conflicts[:20],
        "eqp_multi_area_count": len(eqp_multi_area),
        "eqp_multi_area_samples": eqp_multi_area[:20],
        "invalid_date_count": invalid_dates,
        "date_min": min(valid_dates).isoformat(sep=" ") if valid_dates else None,
        "date_max": max(valid_dates).isoformat(sep=" ") if valid_dates else None,
        "before_go_live_count": sum(value < GO_LIVE for value in valid_dates),
        "suspicious_short_areas": sorted(
            {row["AREA"] for row in rows if row["AREA"] and len(row["AREA"]) <= 2}
        ),
        "max_utf8_bytes": max_bytes,
        "over_declared_bytes": {
            column: value
            for column, value in max_bytes.items()
            if value > DECLARED_MAX_BYTES[column]
        },
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_quality_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# MES_TASK_UNION 质量报告",
        "",
        f"- 行数：{report['row_count']}",
        f"- 未知 TASK_TYPE：{report['unknown_task_types'] or '无'}",
        f"- EQP 空值：{report['nulls']['EQP']}",
        f"- DATES 空值：{report['nulls']['DATES']}",
        f"- PACKAGE 空值：{report['nulls']['PACKAGE']}",
        f"- AREA 空值：{report['nulls']['AREA']}",
        f"- 硬失败：{'是' if report['hard_failure'] else '否'}",
        f"- 硬失败项：{', '.join(report['hard_failures']) if report['hard_failures'] else '无'}",
        f"- TASK_TYPE+SUBLOT 重复键（硬失败）：{report['task_sublot_duplicate_count']}",
        f"- TASK_TYPE+SUBLOT 重复多余行：{report['task_sublot_duplicate_extra_rows']}",
        f"- 跨任务冲突：{report['cross_type_conflict_count']}",
        f"- 关卡/三光互斥冲突：{report['gate_optical_conflict_count']}",
        f"- 同一 EQP 多 AREA：{report['eqp_multi_area_count']}",
        f"- 无法解析日期：{report['invalid_date_count']}",
        f"- 早于上线基线 2026-08-01：{report['before_go_live_count']}",
        f"- 可疑短 AREA：{report['suspicious_short_areas'] or '无'}",
        f"- 超过声明字节长度：{report['over_declared_bytes'] or '无'}",
        "",
        "## 各任务类型行数",
        "",
    ]
    lines.extend(
        f"- `{task_type}`：{report['counts'][task_type]}" for task_type in TASK_TYPES
    )
    if report["task_sublot_duplicate_samples"]:
        lines.extend(["", "## TASK_TYPE+SUBLOT 重复键样例", ""])
        for sample in report["task_sublot_duplicate_samples"]:
            lines.append(
                f"- `{sample['task_type']}` + `{sample['sublot']}`："
                f"{sample['row_count']} 行，"
                f"其中互异行 {sample['distinct_row_count']}，"
                f"EQP/AREA={sample['eqp_area_pairs']}"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_factory_reports(
    run_dir: Path, executions: list[dict[str, Any]]
) -> list[dict[str, str]]:
    """依据已完成执行生成质量、性能和客户基线行数对比报告。"""

    canonical = [
        item for item in executions if item["query_id"] == "MES_TASK_UNION"
    ]
    if not canonical:
        return []

    reports_dir = run_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    quality = analyze_task_union(run_dir / canonical[0]["output"])
    quality_json = reports_dir / "mes-task-union-quality.json"
    quality_md = reports_dir / "mes-task-union-quality.md"
    _write_json(quality_json, quality)
    _write_quality_markdown(quality_md, quality)

    durations = [float(item["duration_seconds"]) for item in canonical]
    performance = {
        "rounds": len(canonical),
        "average_seconds": sum(durations) / len(durations),
        "max_seconds": max(durations),
        "target_average_le_5_seconds": sum(durations) / len(durations) <= 5,
        "target_max_le_10_seconds": max(durations) <= 10,
    }
    performance_json = reports_dir / "mes-task-union-performance.json"
    _write_json(performance_json, performance)

    comparison_path = reports_dir / "customer-baseline-counts.csv"
    source_executions = [
        item for item in executions if item["query_id"] in SOURCE_TASK_TYPES
    ]
    if source_executions:
        with comparison_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=(
                    "task_type",
                    "source_query_id",
                    "merged_count",
                    "source_count",
                    "difference",
                    "merged_started_at",
                    "source_started_at",
                ),
            )
            writer.writeheader()
            for item in source_executions:
                task_type = SOURCE_TASK_TYPES[item["query_id"]]
                source_count = int(item["row_count"])
                merged_count = int(quality["counts"][task_type])
                writer.writerow(
                    {
                        "task_type": task_type,
                        "source_query_id": item["query_id"],
                        "merged_count": merged_count,
                        "source_count": source_count,
                        "difference": source_count - merged_count,
                        "merged_started_at": canonical[0]["started_at"],
                        "source_started_at": item["started_at"],
                    }
                )

    paths = [quality_json, quality_md, performance_json]
    if comparison_path.exists():
        paths.append(comparison_path)
    return [
        {
            "path": path.relative_to(run_dir).as_posix(),
            "sha256": sha256_file(path),
        }
        for path in paths
    ]
