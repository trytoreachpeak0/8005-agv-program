from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from meslab.quality import (  # noqa: E402
    EXPECTED_COLUMNS,
    QualityError,
    analyze_task_union,
    build_factory_reports,
)


BASE_ROW = {
    "TASK_TYPE": "DIE_TO_OVEN",
    "SUBLOT": "S1",
    "AREA": "A1",
    "EQP": "E1",
    "STEP": "装片烘烤",
    "DATES": "2026-07-16 12:00:00",
    "PACKAGE": "TO-126",
}


def write_union(path: Path, rows: list[dict[str, str]] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(
            rows
            or [
                dict(BASE_ROW),
                {
                    "TASK_TYPE": "WIRE_TO_GATE",
                    "SUBLOT": "S2",
                    "AREA": "",
                    "EQP": "E2",
                    "STEP": "焊线关卡",
                    "DATES": "bad-date",
                    "PACKAGE": "TOLL-8L",
                },
            ]
        )


class TaskUnionQualityTests(unittest.TestCase):
    def test_quality_and_factory_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            result = run_dir / "results" / "MES_TASK_UNION-round-001.csv"
            write_union(result)
            report = analyze_task_union(result)
            self.assertEqual(report["row_count"], 2)
            self.assertEqual(report["counts"]["DIE_TO_OVEN"], 1)
            self.assertEqual(report["nulls"]["AREA"], 1)
            self.assertEqual(report["invalid_date_count"], 1)
            self.assertEqual(report["before_go_live_count"], 1)
            self.assertEqual(report["suspicious_short_areas"], ["A1"])
            self.assertFalse(report["hard_failure"])
            self.assertEqual(report["hard_failures"], [])
            self.assertEqual(report["task_sublot_duplicate_count"], 0)

            artifacts = build_factory_reports(
                run_dir,
                [
                    {
                        "query_id": "MES_TASK_UNION",
                        "round": 1,
                        "duration_seconds": 3.0,
                        "row_count": 2,
                        "started_at": "2026-07-16T04:00:00+00:00",
                        "output": "results/MES_TASK_UNION-round-001.csv",
                    },
                    {
                        "query_id": "CUSTOMER_BASELINE_DIE_TO_OVEN",
                        "round": 1,
                        "duration_seconds": 1.0,
                        "row_count": 2,
                        "started_at": "2026-07-16T04:00:04+00:00",
                        "output": "results/source.csv",
                    },
                ],
            )
            self.assertEqual(len(artifacts), 4)
            self.assertTrue(
                (run_dir / "reports" / "customer-baseline-counts.csv").is_file()
            )
            quality_md = (run_dir / "reports" / "mes-task-union-quality.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("硬失败：否", quality_md)
            self.assertIn("TASK_TYPE+SUBLOT 重复键（硬失败）：0", quality_md)

    def test_identical_task_sublot_rows_are_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "dup.csv"
            write_union(path, [dict(BASE_ROW), dict(BASE_ROW)])
            report = analyze_task_union(path)
            self.assertTrue(report["hard_failure"])
            self.assertEqual(report["hard_failures"], ["TASK_TYPE_SUBLOT_DUPLICATE"])
            self.assertEqual(report["task_sublot_duplicate_count"], 1)
            self.assertEqual(report["task_sublot_duplicate_extra_rows"], 1)
            sample = report["task_sublot_duplicate_samples"][0]
            self.assertEqual(sample["row_count"], 2)
            self.assertEqual(sample["distinct_row_count"], 1)

    def test_same_key_different_columns_are_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "conflict.csv"
            other = dict(BASE_ROW)
            other["STEP"] = "另一工序"
            other["PACKAGE"] = "OTHER-PKG"
            write_union(path, [dict(BASE_ROW), other])
            report = analyze_task_union(path)
            self.assertTrue(report["hard_failure"])
            self.assertEqual(report["task_sublot_duplicate_count"], 1)
            sample = report["task_sublot_duplicate_samples"][0]
            self.assertEqual(sample["distinct_row_count"], 2)

    def test_rejects_six_column_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "old.csv"
            path.write_text(
                "TASK_TYPE,SUBLOT,AREA,EQP,STEP,DATES\n", encoding="utf-8"
            )
            with self.assertRaises(QualityError):
                analyze_task_union(path)


if __name__ == "__main__":
    unittest.main()
