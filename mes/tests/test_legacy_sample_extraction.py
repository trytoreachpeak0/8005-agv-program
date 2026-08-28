from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mes.analysis.extract_legacy_task_samples import (
    LegacySampleError,
    extract_samples,
)


class LegacySampleExtractionTests(unittest.TestCase):
    def test_extracts_all_five_task_tables(self) -> None:
        sections = []
        for index in range(1, 6):
            sections.extend(
                [
                    f"## {index}. 测试",
                    "| SUBLOT | AREA | EQP | STEP | DATES | PACKAGE |",
                    "| --- | --- | --- | --- | --- | --- |",
                    f"| S{index} | A | E | STEP | 2026-01-01 | P{index} |",
                    "",
                ]
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy.md"
            path.write_text("\n".join(sections), encoding="utf-8")
            rows = extract_samples(path)

        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["TASK_TYPE"], "DIE_TO_WIRE_STAGING")
        self.assertEqual(rows[-1]["TASK_TYPE"], "STAGING_TO_WIRE")
        self.assertEqual(rows[-1]["PACKAGE"], "P5")

    def test_rejects_missing_task_section_sample(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "legacy.md"
            path.write_text(
                "## 1. 测试\n"
                "| SUBLOT | AREA | EQP | STEP | DATES | PACKAGE |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| S1 | A | E | STEP | 2026-01-01 | P1 |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(LegacySampleError, "未提取到样本"):
                extract_samples(path)


if __name__ == "__main__":
    unittest.main()
