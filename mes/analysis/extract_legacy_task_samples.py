"""从旧版 MES 接口需求文档提取五类任务样本。

该工具只用于迁移历史证据。新样本必须来自工厂 runner 的 CSV，
不得继续从业务文档反向生成。
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


TASK_TYPES = {
    "1": "DIE_TO_WIRE_STAGING",
    "2": "DIE_TO_OVEN",
    "3": "WIRE_TO_GATE",
    "4": "WIRE_TO_OPTICAL",
    "5": "STAGING_TO_WIRE",
}
EXPECTED_COLUMNS = ("SUBLOT", "AREA", "EQP", "STEP", "DATES", "PACKAGE")
OUTPUT_COLUMNS = ("TASK_TYPE",) + EXPECTED_COLUMNS
SECTION_PATTERN = re.compile(r"^##\s+([1-5])\.")


class LegacySampleError(ValueError):
    """旧文档样本无法按已知格式提取。"""


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_samples(markdown_path: Path) -> list[dict[str, str]]:
    """提取 §1～§5 中表头为六个约定字段的 Markdown 表格。"""

    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    current_section: str | None = None
    rows: list[dict[str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        section = SECTION_PATTERN.match(line)
        if section:
            current_section = section.group(1)

        if (
            current_section in TASK_TYPES
            and line.lstrip().startswith("|")
            and tuple(_cells(line)) == EXPECTED_COLUMNS
        ):
            index += 2  # 跳过表头和 Markdown 分隔行
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                values = _cells(lines[index])
                if len(values) != len(EXPECTED_COLUMNS):
                    raise LegacySampleError(
                        f"第 {index + 1} 行样本列数错误：{len(values)}"
                    )
                row = dict(zip(EXPECTED_COLUMNS, values))
                row["TASK_TYPE"] = TASK_TYPES[current_section]
                rows.append(row)
                index += 1
            continue
        index += 1

    missing = set(TASK_TYPES.values()) - {row["TASK_TYPE"] for row in rows}
    if missing:
        raise LegacySampleError(f"以下任务类型未提取到样本：{sorted(missing)}")
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="迁移旧版 MES 五类任务样本")
    parser.add_argument("markdown", type=Path, help="旧需求确认 Markdown")
    parser.add_argument("output_csv", type=Path, help="输出历史样本 CSV")
    args = parser.parse_args()
    rows = extract_samples(args.markdown)
    write_csv(args.output_csv, rows)
    print(f"已提取 {len(rows)} 行：{args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
