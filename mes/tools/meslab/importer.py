"""校验并导入工厂运行证据。"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
from typing import Any

from .bundle import BundleError, load_bundle, utc_now, write_json
from .hashing import sha256_file
from .samples import csv_to_markdown


class ImportRunError(ValueError):
    """运行证据不能安全导入。"""


def _inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ImportRunError(f"运行文件路径越界: {relative}") from exc
    return path


def _atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    shutil.copyfile(source, temporary)
    os.replace(temporary, target)


def import_run(
    run_dir: str | Path, bundle_dir: str | Path, mes_root: str | Path
) -> Path:
    source = Path(run_dir).resolve()
    bundle = Path(bundle_dir).resolve()
    root = Path(mes_root).resolve()
    manifest_path = source / "run-manifest.json"
    if not manifest_path.is_file():
        raise ImportRunError(f"缺少 run-manifest.json: {source}")
    try:
        run_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ImportRunError(f"无法读取 run manifest: {exc}") from exc
    if run_manifest.get("schema_version") != 1 or run_manifest.get("status") != "completed":
        raise ImportRunError("只允许导入已完成的 schema_version=1 运行")
    run_id = run_manifest.get("run_id")
    if (
        not isinstance(run_id, str)
        or not run_id.startswith("run-")
        or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in run_id)
    ):
        raise ImportRunError("run_id 无效")

    try:
        bundle_manifest = load_bundle(bundle, verify=True)
    except BundleError as exc:
        raise ImportRunError(str(exc)) from exc
    if run_manifest.get("bundle_id") != bundle_manifest.get("bundle_id"):
        raise ImportRunError("run 与 bundle_id 不匹配")
    if run_manifest.get("bundle_manifest_sha256") != sha256_file(
        bundle / "bundle-manifest.json"
    ):
        raise ImportRunError("bundle manifest 哈希不匹配")

    bundle_entries = {entry["id"]: entry for entry in bundle_manifest["queries"]}
    run_queries = run_manifest.get("queries")
    if not isinstance(run_queries, list) or not run_queries:
        raise ImportRunError("运行没有查询哈希记录")
    validated_query_ids: set[str] = set()
    for query in run_queries:
        bundled = bundle_entries.get(query.get("id"))
        if not bundled:
            raise ImportRunError(f"bundle 不含运行查询: {query.get('id')}")
        if query["id"] in validated_query_ids:
            raise ImportRunError(f"运行含重复查询: {query['id']}")
        validated_query_ids.add(query["id"])
        if query.get("sql") != bundled.get("sql") or query.get("query_manifest") != bundled.get(
            "query_manifest"
        ):
            raise ImportRunError(f"查询路径不匹配: {query.get('id')}")
        if query.get("sha256") != bundled.get("sha256"):
            raise ImportRunError(f"查询哈希不匹配: {query.get('id')}")

    executions = run_manifest.get("executions")
    if not isinstance(executions, list) or not executions:
        raise ImportRunError("运行没有可导入的输出")
    latest: dict[str, dict[str, Any]] = {}
    for execution in executions:
        query_id = execution.get("query_id")
        if query_id not in validated_query_ids:
            raise ImportRunError(f"输出引用未知查询: {query_id}")
        output = _inside(source, execution.get("output", ""))
        if not output.is_file() or output.suffix.lower() != ".csv":
            raise ImportRunError(f"输出文件无效: {execution.get('output')}")
        if execution.get("output_sha256") != sha256_file(output):
            raise ImportRunError(f"输出哈希不匹配: {execution.get('output')}")
        if not bundle_entries[query_id].get("promote_sample", True):
            continue
        if (
            bundle_entries[query_id].get("requires_approval", False)
            and run_manifest.get("approval", {}).get("status") != "approved"
        ):
            continue
        previous = latest.get(query_id)
        if previous is None or int(execution.get("round", 0)) >= int(previous.get("round", 0)):
            latest[query_id] = execution

    derived_outputs = run_manifest.get("derived_outputs", [])
    if not isinstance(derived_outputs, list):
        raise ImportRunError("derived_outputs 必须是数组")
    for artifact in derived_outputs:
        if not isinstance(artifact, dict):
            raise ImportRunError("derived_outputs 项必须是对象")
        artifact_path = _inside(source, artifact.get("path", ""))
        if not artifact_path.is_file():
            raise ImportRunError(f"派生报告不存在: {artifact.get('path')}")
        if artifact.get("sha256") != sha256_file(artifact_path):
            raise ImportRunError(f"派生报告哈希不匹配: {artifact.get('path')}")

    target = root / "evidence" / "runs" / run_id
    if target.exists():
        raise ImportRunError(f"目标运行已存在，拒绝覆盖: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{run_id}.", dir=target.parent))
    shutil.rmtree(temporary)
    coverage_relative: str | None = None
    try:
        shutil.copytree(source, temporary)
        canonical = latest.get("MES_TASK_UNION")
        if canonical is not None:
            repository_root = root.parent
            if str(repository_root) not in sys.path:
                sys.path.insert(0, str(repository_root))
            from mes.analysis.analyze_package_coverage import (  # type: ignore
                analyze_mes_task_union,
            )

            coverage_dir = temporary / "reports" / "package-coverage"
            analyze_mes_task_union(
                _inside(temporary, canonical["output"]),
                coverage_dir,
            )
            coverage_relative = coverage_dir.relative_to(temporary).as_posix()
        os.replace(temporary, target)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    for query_id, execution in latest.items():
        sample_dir = root / "samples" / bundle_entries[query_id]["slug"]
        sample_dir.mkdir(parents=True, exist_ok=True)
        imported_output = _inside(target, execution["output"])
        latest_csv = sample_dir / "latest.csv"
        _atomic_copy(imported_output, latest_csv)
        markdown_temporary = sample_dir / f".latest.md.{uuid.uuid4().hex}.tmp"
        csv_to_markdown(latest_csv, markdown_temporary)
        os.replace(markdown_temporary, sample_dir / "latest.md")
        metadata = {
            "schema_version": 1,
            "imported_at": utc_now(),
            "run_id": run_id,
            "query_id": query_id,
            "sourceEvidence": f"evidence/runs/{run_id}",
            "round": execution.get("round"),
            "row_count": execution.get("row_count"),
            "source_output": execution["output"],
            "output_sha256": execution["output_sha256"],
        }
        if query_id == "MES_TASK_UNION" and coverage_relative is not None:
            sample_coverage = sample_dir / "package-coverage"
            shutil.rmtree(sample_coverage, ignore_errors=True)
            shutil.copytree(target / coverage_relative, sample_coverage)
            metadata["package_coverage"] = {
                "source": f"evidence/runs/{run_id}/{coverage_relative}",
                "local": "package-coverage/summary.md",
            }
        write_json(
            sample_dir / "latest.meta.json",
            metadata,
        )
    return target
