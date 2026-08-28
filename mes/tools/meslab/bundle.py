"""离线执行 bundle 构建与校验。"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import uuid
from typing import Any, Iterable

from .hashing import sha256_file
from .manifest import QuerySpec
from .sqlguard import validate_readonly_sql


class BundleError(ValueError):
    """Bundle 无效或不能安全创建。"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: str | Path, data: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, target)


def _safe_bundle_path(bundle_dir: Path, relative: str) -> Path:
    path = (bundle_dir / relative).resolve()
    try:
        path.relative_to(bundle_dir.resolve())
    except ValueError as exc:
        raise BundleError(f"bundle 路径越界: {relative}") from exc
    return path


def _git_metadata(start: Path) -> dict[str, Any]:
    """尽力记录源提交；Git 不可用时显式写 UNKNOWN。"""

    try:
        commit = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "-C", str(start), "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return {"commit": commit, "dirty": dirty}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "UNKNOWN", "dirty": None}


def build_bundle(queries: Iterable[QuerySpec], output_dir: str | Path) -> dict[str, Any]:
    """在临时目录完整生成后，原子地放置 bundle。"""
    query_list = list(queries)
    output = Path(output_dir).resolve()
    if output.exists():
        raise BundleError(f"输出目录已存在，拒绝覆盖: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        entries: list[dict[str, Any]] = []
        for query in query_list:
            sql = query.sql_path.read_text(encoding="utf-8")
            validate_readonly_sql(sql)
            promote_sample = query.metadata.get("promote_sample", True)
            if not isinstance(promote_sample, bool):
                raise BundleError(
                    f"查询 {query.id} 的 promote_sample 必须是布尔值"
                )
            requires_approval = query.metadata.get("requires_approval", False)
            if not isinstance(requires_approval, bool):
                raise BundleError(
                    f"查询 {query.id} 的 requires_approval 必须是布尔值"
                )
            destination = temporary / "queries" / query.id
            destination.mkdir(parents=True)
            sql_target = destination / query.sql_name
            manifest_target = destination / "query.toml"
            shutil.copyfile(query.sql_path, sql_target)
            shutil.copyfile(query.manifest_path, manifest_target)
            entries.append(
                {
                    "id": query.id,
                    "slug": query.directory.name,
                    "title": query.title,
                    "sql": sql_target.relative_to(temporary).as_posix(),
                    "query_manifest": manifest_target.relative_to(temporary).as_posix(),
                    "sha256": {
                        "sql": sha256_file(sql_target),
                        "query_manifest": sha256_file(manifest_target),
                    },
                    "parameters": list(query.parameters),
                    "expected_columns": list(query.expected_columns),
                    "promote_sample": promote_sample,
                    "requires_approval": requires_approval,
                }
            )
        if not entries:
            raise BundleError("bundle 至少需要一个查询")

        tools_root = Path(__file__).resolve().parents[1]
        runner_root = temporary / "runner"
        shutil.copytree(
            tools_root / "meslab",
            runner_root / "meslab",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        shutil.copyfile(tools_root / "mes_lab.py", runner_root / "mes_lab.py")
        shutil.copyfile(
            tools_root / "config.example.ini",
            temporary / "config.example.ini",
        )
        (temporary / "requirements.txt").write_text(
            "oracledb>=3.4.2,<5\n",
            encoding="utf-8",
        )
        runner_files = []
        for path in sorted(
            (
                *runner_root.rglob("*.py"),
                temporary / "config.example.ini",
                temporary / "requirements.txt",
            ),
            key=lambda item: item.as_posix(),
        ):
            runner_files.append(
                {
                    "path": path.relative_to(temporary).as_posix(),
                    "sha256": sha256_file(path),
                }
            )
        manifest = {
            "schema_version": 1,
            "bundle_id": f"bundle-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}",
            "created_at": utc_now(),
            "source_git": _git_metadata(query_list[0].directory),
            "runner_files": runner_files,
            "queries": sorted(entries, key=lambda entry: entry["id"]),
        }
        write_json(temporary / "bundle-manifest.json", manifest)
        for attempt in range(5):
            try:
                os.replace(temporary, output)
                break
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.2 * (attempt + 1))
        return manifest
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def load_bundle(bundle_dir: str | Path, verify: bool = True) -> dict[str, Any]:
    bundle = Path(bundle_dir).resolve()
    manifest_path = bundle / "bundle-manifest.json"
    if not manifest_path.is_file():
        raise BundleError(f"缺少 bundle-manifest.json: {bundle}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise BundleError(f"无法读取 bundle manifest: {exc}") from exc
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("queries"), list):
        raise BundleError("不支持或无效的 bundle manifest")
    if verify:
        runner_files = manifest.get("runner_files")
        if not isinstance(runner_files, list) or not runner_files:
            raise BundleError("bundle 缺少 runner_files")
        for file_entry in runner_files:
            if not isinstance(file_entry, dict):
                raise BundleError("runner_files 项无效")
            runner_path = _safe_bundle_path(bundle, file_entry.get("path", ""))
            if not runner_path.is_file():
                raise BundleError(f"bundle 缺少 runner 文件: {file_entry.get('path')}")
            if file_entry.get("sha256") != sha256_file(runner_path):
                raise BundleError(
                    f"bundle runner 哈希不匹配: {file_entry.get('path')}"
                )
        seen: set[str] = set()
        for entry in manifest["queries"]:
            query_id = entry.get("id")
            if (
                not isinstance(query_id, str)
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", query_id)
                or query_id in seen
            ):
                raise BundleError(f"无效或重复查询 ID: {query_id!r}")
            seen.add(query_id)
            slug = entry.get("slug")
            if not isinstance(slug, str) or not re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9_.-]*", slug
            ):
                raise BundleError(f"无效查询目录名: {slug!r}")
            if not isinstance(entry.get("promote_sample"), bool):
                raise BundleError(f"查询 {query_id} 的 promote_sample 无效")
            if not isinstance(entry.get("requires_approval"), bool):
                raise BundleError(f"查询 {query_id} 的 requires_approval 无效")
            for key, hash_key in (("sql", "sql"), ("query_manifest", "query_manifest")):
                path = _safe_bundle_path(bundle, entry.get(key, ""))
                if not path.is_file():
                    raise BundleError(f"bundle 缺少文件: {entry.get(key)}")
                expected = entry.get("sha256", {}).get(hash_key)
                if expected != sha256_file(path):
                    raise BundleError(f"bundle 文件哈希不匹配: {entry.get(key)}")
            validate_readonly_sql(_safe_bundle_path(bundle, entry["sql"]).read_text(encoding="utf-8"))
    return manifest
