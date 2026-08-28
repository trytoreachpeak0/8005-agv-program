"""CSV 和 Markdown 样例生成。"""

from __future__ import annotations

import csv
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Sequence


def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, bytes):
        return value.hex()
    return str(value)


def write_csv(
    path: str | Path, columns: Sequence[str], rows: Iterable[Sequence[Any]]
) -> int:
    """以 Excel 兼容的 UTF-8 BOM 编码写结果。"""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with target.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow(_cell(value) for value in row)
            count += 1
    return count


def csv_to_markdown(csv_path: str | Path, markdown_path: str | Path) -> int:
    """将 CSV 转为便于审阅的 Markdown 表格。"""
    source = Path(csv_path)
    target = Path(markdown_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream))
    if not rows:
        raise ValueError(f"CSV 没有表头: {source}")

    def escape(value: str) -> str:
        return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace(
            "\n", "<br>"
        )

    header = rows[0]
    lines = [
        "| " + " | ".join(escape(value) for value in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in rows[1:]:
        padded = list(row) + [""] * max(0, len(header) - len(row))
        lines.append("| " + " | ".join(escape(value) for value in padded[: len(header)]) + " |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return max(0, len(rows) - 1)
