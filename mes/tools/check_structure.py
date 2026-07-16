"""检查 MES 目录的 SSOT、文档链接和查询清单。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


MES_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = MES_ROOT.parent
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

sys.path.insert(0, str(MES_ROOT / "tools"))
from meslab.manifest import QueryCatalog  # noqa: E402
from meslab.sqlguard import validate_readonly_sql  # noqa: E402


LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SQL_FENCE_PATTERN = re.compile(r"```sql\b", re.IGNORECASE)


def check() -> list[str]:
    errors: list[str] = []
    for document in MES_ROOT.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        if document.is_relative_to(MES_ROOT / "docs") and SQL_FENCE_PATTERN.search(text):
            errors.append(f"业务文档不得内嵌 SQL：{document.relative_to(MES_ROOT)}")
        for raw_target in LINK_PATTERN.findall(text):
            target_text = raw_target.split("#", 1)[0].strip()
            if (
                not target_text
                or "://" in target_text
                or target_text.startswith("mailto:")
            ):
                continue
            target = (document.parent / target_text).resolve()
            try:
                target.relative_to(MES_ROOT)
            except ValueError:
                continue  # 允许业务文档引用仓库其他受治理目录
            if not target.exists():
                errors.append(
                    f"链接不存在：{document.relative_to(MES_ROOT)} -> {raw_target}"
                )

    sql_root = MES_ROOT / "sql"
    if sql_root.exists() and any(path.is_file() for path in sql_root.rglob("*")):
        errors.append("旧 mes/sql 目录仍包含文件")

    allowed_sql_roots = (
        MES_ROOT / "queries",
        MES_ROOT / "sources",
    )
    for sql_file in MES_ROOT.rglob("*.sql"):
        if ".dist" in sql_file.parts:
            continue
        if not any(sql_file.is_relative_to(root) for root in allowed_sql_roots):
            errors.append(f"SQL 位于未治理目录：{sql_file.relative_to(MES_ROOT)}")

    try:
        catalog = QueryCatalog(MES_ROOT / "queries")
        for query_id in catalog.ids():
            query = catalog.get(query_id)
            validate_readonly_sql(query.sql_path.read_text(encoding="utf-8"))
    except Exception as exc:  # 作为命令行总检查，需要聚合为结构错误
        errors.append(f"查询清单或只读校验失败：{exc}")
    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("MES 目录结构、文档链接、查询清单和 SQL 边界检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
