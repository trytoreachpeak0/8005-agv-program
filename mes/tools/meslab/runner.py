"""在工厂环境执行已校验 bundle。"""

from __future__ import annotations

from pathlib import Path
import platform
import sys
import time
from typing import Any

from .bundle import BundleError, load_bundle, utc_now
from .hashing import sha256_file
from .oracle import load_oracle_config, readonly_connection, runtime_info
from .quality import build_factory_reports
from .runtime import ExecutionLog, Timer, create_run_directory, write_run_manifest
from .samples import write_csv
from .sqlguard import validate_readonly_sql


def _entry_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["id"]: entry for entry in manifest["queries"]}


def _query_parameters(
    all_parameters: dict[str, Any], query_id: str, declared: list[str]
) -> dict[str, Any]:
    nested = all_parameters.get(query_id)
    values = nested if isinstance(nested, dict) else all_parameters
    expected = set(declared)
    actual = set(values)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        raise BundleError(f"查询 {query_id} 缺少绑定参数: {', '.join(missing)}")
    if unexpected:
        raise BundleError(f"查询 {query_id} 收到未声明参数: {', '.join(unexpected)}")
    return {name: values[name] for name in declared}


def run_factory(
    bundle_dir: str | Path,
    config_path: str | Path,
    output_root: str | Path,
    query_ids: list[str] | None = None,
    parameters: dict[str, Any] | None = None,
    rounds: int = 1,
    wait_seconds: float = 0,
    mode: str = "single",
    experiment_record: dict[str, Any] | None = None,
    approval: dict[str, Any] | None = None,
) -> Path:
    if rounds < 1:
        raise ValueError("rounds 必须大于等于 1")
    if wait_seconds < 0:
        raise ValueError("wait_seconds 不得为负数")

    # ``approval`` kept as deprecated alias for callers/tests.
    record = experiment_record if experiment_record is not None else approval

    bundle = Path(bundle_dir).resolve()
    bundle_manifest = load_bundle(bundle, verify=True)
    entries = _entry_map(bundle_manifest)
    selected = list(dict.fromkeys(query_ids)) if query_ids else sorted(entries)
    unknown = sorted(set(selected) - set(entries))
    if unknown:
        raise BundleError(f"bundle 中不存在查询: {', '.join(unknown)}")
    if not selected:
        raise BundleError("没有选择要执行的查询")

    config = load_oracle_config(config_path)
    run_id, run_dir = create_run_directory(output_root)
    log = ExecutionLog(run_id)
    executions: list[dict[str, Any]] = []
    parameters = parameters or {}
    try:
        with readonly_connection(config) as connection:
            environment = {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "oracle": runtime_info(config),
            }
            for round_number in range(1, rounds + 1):
                for query_id in selected:
                    entry = entries[query_id]
                    sql_path = (bundle / entry["sql"]).resolve()
                    sql = validate_readonly_sql(sql_path.read_text(encoding="utf-8"))
                    binds = _query_parameters(parameters, query_id, entry.get("parameters", []))
                    output = run_dir / "results" / f"{query_id}-round-{round_number:03d}.csv"
                    with Timer() as timer:
                        with connection.cursor() as cursor:
                            cursor.arraysize = 1000
                            cursor.execute(sql, binds)
                            columns = [description[0] for description in cursor.description or ()]
                            expected = entry.get("expected_columns", [])
                            if expected and [name.upper() for name in columns] != [
                                name.upper() for name in expected
                            ]:
                                raise RuntimeError(
                                    f"查询 {query_id} 返回列与 expected_columns 不一致"
                                )
                            row_count = write_csv(output, columns, cursor)
                    relative_output = output.relative_to(run_dir).as_posix()
                    executions.append(
                        {
                            "query_id": query_id,
                            "round": round_number,
                            "started_at": timer.started_at,
                            "ended_at": timer.ended_at,
                            "duration_seconds": timer.duration_seconds,
                            "row_count": row_count,
                            "parameter_names": sorted(binds),
                            "output": relative_output,
                            "output_sha256": sha256_file(output),
                        }
                    )
                    log.event(
                        f"`{query_id}` 第 {round_number} 轮：{row_count} 行，"
                        f"{timer.duration_seconds:.3f} 秒，输出 `{relative_output}`"
                    )
                if round_number < rounds and wait_seconds:
                    log.event(f"第 {round_number} 轮后等待 {wait_seconds:g} 秒")
                    time.sleep(wait_seconds)

        derived_outputs = build_factory_reports(run_dir, executions)
        experiment_payload = record or {"status": "not-provided"}
        run_manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "created_at": utc_now(),
            "status": "completed",
            "mode": mode,
            "rounds": rounds,
            "wait_seconds": wait_seconds,
            "environment": environment,
            "experiment_record": experiment_payload,
            # Deprecated alias for older importers/readers.
            "approval": experiment_payload,
            "bundle_id": bundle_manifest["bundle_id"],
            "bundle_manifest_sha256": sha256_file(bundle / "bundle-manifest.json"),
            "queries": [
                {
                    "id": entries[query_id]["id"],
                    "sql": entries[query_id]["sql"],
                    "query_manifest": entries[query_id]["query_manifest"],
                    "sha256": entries[query_id]["sha256"],
                }
                for query_id in selected
            ],
            "executions": executions,
            "derived_outputs": derived_outputs,
        }
        write_run_manifest(run_dir, run_manifest)
        log.write(run_dir / "execution-log.md", "completed")
        return run_dir
    except BaseException as exc:
        log.event(f"执行失败，异常类型：`{type(exc).__name__}`")
        log.write(run_dir / "execution-log.md", "failed")
        raise
