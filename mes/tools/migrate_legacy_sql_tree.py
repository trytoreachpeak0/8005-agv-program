"""把旧程序 SQL 代码树迁入只读研究来源区。

该工具仅做文件迁移和静态分类，绝不执行 SQL。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


WRITE_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|CREATE|ALTER|DROP|TRUNCATE|"
    r"BEGIN|DECLARE|CALL|EXECUTE|COMMIT|ROLLBACK)\b",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    without_comments = re.sub(r"/\*.*?\*/|--[^\r\n]*", " ", text, flags=re.DOTALL)
    if WRITE_PATTERN.search(without_comments):
        return "WRITE_OR_PROCEDURAL_RESEARCH_ONLY"
    if re.match(r"^\s*(SELECT|WITH)\b", without_comments, flags=re.IGNORECASE):
        return "READ_ONLY_CANDIDATE_UNVERIFIED"
    return "UNKNOWN_RESEARCH_ONLY"


def write_metadata(target: Path) -> None:
    """重建来源清单；README/catalog/manifest 自身不计入来源文件。"""
    sql_files = sorted(target.rglob("*.sql"))
    if not sql_files:
        raise ValueError("源目录没有 SQL 文件")

    sql_entries = []
    for path in sql_files:
        relative = path.relative_to(target).as_posix()
        sql_entries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "classification": classify(path),
            }
        )

    with (target / "catalog.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("path", "bytes", "sha256", "classification"),
        )
        writer.writeheader()
        writer.writerows(sql_entries)

    generated_names = {"README.md", "catalog.csv", "source-manifest.json"}
    source_files = sorted(
        path
        for path in target.rglob("*")
        if path.is_file()
        and not (
            path.parent == target and path.name in generated_names
        )
    )
    source_entries = [
        {
            "path": path.relative_to(target).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "kind": "sql" if path.suffix.lower() == ".sql" else "supporting",
        }
        for path in source_files
    ]

    manifest = {
        "schema_version": 1,
        "kind": "legacy-program-sql-source-snapshot",
        "migrated_at": datetime.now(timezone.utc).isoformat(),
        "source_label": "旧程序sql访问代码",
        "source_file_count": len(source_entries),
        "sql_count": len(sql_entries),
        "files": source_entries,
    }
    (target / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    readonly_count = sum(
        entry["classification"] == "READ_ONLY_CANDIDATE_UNVERIFIED"
        for entry in sql_entries
    )
    write_count = sum(
        entry["classification"] == "WRITE_OR_PROCEDURAL_RESEARCH_ONLY"
        for entry in sql_entries
    )
    (target / "README.md").write_text(
        "# 旧程序 SQL 访问代码快照\n\n"
        "本目录是旧程序 SQL 的原样研究快照，不是正式查询目录，也不是客户当前批准"
        "版本。文件可能包含写操作、存储过程式语句或已失效业务假设；任何工具、应用"
        "和部署流程都不得直接加载或执行。\n\n"
        "- `catalog.csv`：静态分类与哈希。分类仅用于确定研究优先级，不等于安全批准。\n"
        "- `source-manifest.json`：迁移时间和逐文件 SHA-256。\n"
        f"- 当前静态分类：{readonly_count} 个未验证只读候选，"
        f"{write_count} 个写/过程式研究文件。\n"
        "- `READ_ONLY_CANDIDATE_UNVERIFIED` 仍须建立实验、确认对象和负载后才可执行。\n"
        "- `WRITE_OR_PROCEDURAL_RESEARCH_ONLY` 禁止进入 MES Lab 只读 bundle。\n\n"
        "研究结论必须进入 `mes/experiments` 与 `mes/evidence`，不能直接修改本快照；"
        "客户提供新版本时应建立新的日期快照。\n",
        encoding="utf-8",
    )

    for entry in source_entries:
        copied = target / entry["path"]
        if sha256(copied) != entry["sha256"]:
            raise RuntimeError(f"迁移后哈希校验失败：{entry['path']}")


def migrate(source: Path, target: Path, remove_source: bool) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"源目录不存在：{source}")
    if target.exists():
        raise FileExistsError(f"目标目录已存在，拒绝覆盖：{target}")
    shutil.copytree(source, target)
    try:
        write_metadata(target)
    except BaseException:
        shutil.rmtree(target, ignore_errors=True)
        raise
    if remove_source:
        shutil.rmtree(source)


def main() -> int:
    parser = argparse.ArgumentParser(description="迁移旧程序 SQL 来源树")
    parser.add_argument("source", type=Path, nargs="?")
    parser.add_argument("target", type=Path, nargs="?")
    parser.add_argument("--remove-source", action="store_true")
    parser.add_argument("--refresh-target", type=Path)
    args = parser.parse_args()
    if args.refresh_target is not None:
        write_metadata(args.refresh_target.resolve())
        print(f"已刷新旧 SQL 来源清单：{args.refresh_target}")
        return 0
    if args.source is None or args.target is None:
        parser.error("迁移时必须提供 source 和 target")
    migrate(args.source.resolve(), args.target.resolve(), args.remove_source)
    print(f"已迁移旧 SQL 来源树：{args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
