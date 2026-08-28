"""查询清单读取和目录索引。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
import tomllib


class ManifestError(ValueError):
    """查询清单无效。"""


@dataclass(frozen=True)
class QuerySpec:
    id: str
    title: str
    sql_name: str
    readonly: bool
    parameters: tuple[str, ...]
    expected_columns: tuple[str, ...]
    directory: Path
    manifest_path: Path
    sql_path: Path
    metadata: dict[str, Any]


def _parameter_names(value: Any) -> tuple[str, ...]:
    if isinstance(value, list):
        names: list[str] = []
        for item in value:
            if isinstance(item, str):
                names.append(item)
            elif isinstance(item, dict) and isinstance(item.get("name"), str):
                names.append(item["name"])
            else:
                raise ManifestError("parameters 必须是字符串列表或含 name 的表列表")
        return tuple(names)
    if isinstance(value, dict):
        return tuple(str(name) for name in value)
    raise ManifestError("parameters 必须是列表或表")


def load_query_manifest(path: str | Path) -> QuerySpec:
    """读取任意命名的查询清单；SQL 必须与清单位于同一目录。"""

    manifest_path = Path(path).resolve()
    directory = manifest_path.parent
    if not manifest_path.is_file():
        raise ManifestError(f"缺少查询清单: {manifest_path}")
    with manifest_path.open("rb") as stream:
        data = tomllib.load(stream)

    required = ("id", "title", "sql", "readonly", "parameters", "expected_columns")
    missing = [key for key in required if key not in data]
    if missing:
        raise ManifestError(f"{manifest_path} 缺少字段: {', '.join(missing)}")
    if not isinstance(data["id"], str) or not data["id"].strip():
        raise ManifestError("id 必须是非空字符串")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", data["id"].strip()):
        raise ManifestError("id 只能包含字母、数字、点、下划线和连字符")
    if not isinstance(data["title"], str) or not data["title"].strip():
        raise ManifestError("title 必须是非空字符串")
    if not isinstance(data["sql"], str) or not data["sql"].strip():
        raise ManifestError("sql 必须是文件名")
    if Path(data["sql"]).name != data["sql"]:
        raise ManifestError("sql 必须是查询目录内的文件名，不得包含路径")
    if not isinstance(data["readonly"], bool):
        raise ManifestError("readonly 必须是布尔值")
    if not data["readonly"]:
        raise ManifestError(f"查询 {data['id']} 未声明 readonly=true")
    if not isinstance(data["expected_columns"], list) or not all(
        isinstance(column, str) and column for column in data["expected_columns"]
    ):
        raise ManifestError("expected_columns 必须是非空字符串列表")

    sql_name = data["sql"]
    sql_path = (directory / sql_name).resolve()
    try:
        sql_path.relative_to(directory)
    except ValueError as exc:
        raise ManifestError("sql 路径不得离开查询目录") from exc
    if not sql_path.is_file():
        raise ManifestError(f"缺少 SQL 文件: {sql_path}")

    return QuerySpec(
        id=data["id"].strip(),
        title=data["title"].strip(),
        sql_name=sql_name,
        readonly=True,
        parameters=_parameter_names(data["parameters"]),
        expected_columns=tuple(data["expected_columns"]),
        directory=directory,
        manifest_path=manifest_path,
        sql_path=sql_path,
        metadata=data,
    )


def load_query(query_dir: str | Path) -> QuerySpec:
    """读取并验证查询目录中的 ``query.toml``。"""

    return load_query_manifest(Path(query_dir) / "query.toml")


class QueryCatalog:
    """按查询 ID 索引 ``mes/queries/*``。"""

    def __init__(self, queries_root: str | Path):
        self.root = Path(queries_root).resolve()
        self._queries: dict[str, QuerySpec] = {}
        if not self.root.is_dir():
            raise ManifestError(f"查询根目录不存在: {self.root}")
        for manifest in sorted(self.root.glob("*/query.toml")):
            query = load_query(manifest.parent)
            if query.id in self._queries:
                raise ManifestError(f"重复查询 ID: {query.id}")
            self._queries[query.id] = query

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._queries))

    def get(self, query_id: str) -> QuerySpec:
        try:
            return self._queries[query_id]
        except KeyError as exc:
            raise ManifestError(f"未知查询 ID: {query_id}") from exc

    def select(self, query_ids: list[str] | tuple[str, ...] | None) -> list[QuerySpec]:
        ids = list(query_ids) if query_ids else list(self.ids())
        if not ids:
            raise ManifestError("没有可打包的查询")
        return [self.get(query_id) for query_id in ids]
