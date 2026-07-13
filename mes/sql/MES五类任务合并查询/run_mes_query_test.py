#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MES五类任务合并查询自动化测试脚本
目标环境：Python 3.14.6 + oracledb thin 模式（Windows）
全程只读：仅执行预置 SELECT。
"""

from __future__ import annotations

import argparse
import configparser
import csv
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_PYTHON = (3, 14)
TARGET_PYTHON_TEXT = "3.14.6"
ALLOWED_TASK_TYPES = (
    "DIE_TO_WIRE_STAGING",
    "DIE_TO_OVEN",
    "WIRE_TO_GATE",
    "WIRE_TO_OPTICAL",
    "STAGING_TO_WIRE",
)
EXPECTED_COLUMNS = ("TASK_TYPE", "SUBLOT", "AREA", "EQP", "STEP", "DATES")
DECLARED_MAX_BYTES = {
    "SUBLOT": 40,
    "AREA": 30,
    "EQP": 50,
    "STEP": 255,
}
GO_LIVE = datetime(2026, 8, 1, 0, 0, 0)
FORBIDDEN_SQL_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE|CALL|EXECUTE|BEGIN)\b",
    re.IGNORECASE,
)


@dataclass
class QueryResult:
    started_at: datetime
    finished_at: datetime
    elapsed_seconds: float
    rows: list[dict[str, Any]]
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None

    @property
    def row_count(self) -> int:
        return len(self.rows)


def ensure_python_version() -> None:
    if sys.version_info[:2] != REQUIRED_PYTHON:
        raise SystemExit(
            f"需要 Python {TARGET_PYTHON_TEXT}（当前为 {sys.version.split()[0]}）。"
            f"请在远程机安装并使用 Python {TARGET_PYTHON_TEXT}。"
        )


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def load_config(path: Path) -> configparser.ConfigParser:
    if not path.exists():
        raise SystemExit(
            f"未找到配置文件：{path}\n"
            f"请先复制 config.example.ini 为 config.ini 并填写连接信息。"
        )
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    required = ("host", "port", "service_name", "user", "password")
    for key in required:
        if key not in cfg["oracle"] or not str(cfg["oracle"][key]).strip():
            raise SystemExit(f"config.ini 缺少 oracle.{key}")
    return cfg


def strip_sql_comments(sql_text: str) -> str:
    no_block = re.sub(r"/\*.*?\*/", " ", sql_text, flags=re.DOTALL)
    lines = []
    for line in no_block.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        lines.append(line)
    return "\n".join(lines).strip().rstrip(";").strip()


def assert_readonly_sql(sql_text: str, source_name: str) -> str:
    cleaned = strip_sql_comments(sql_text)
    if not cleaned:
        raise SystemExit(f"SQL 为空：{source_name}")
    if FORBIDDEN_SQL_PATTERN.search(cleaned):
        raise SystemExit(f"拒绝执行非只读 SQL：{source_name}")
    if not re.match(r"(?is)^\s*(WITH|SELECT)\b", cleaned):
        raise SystemExit(f"仅允许 SELECT/WITH 查询：{source_name}")
    return cleaned


def connect_oracle(cfg: configparser.ConfigParser):
    try:
        import oracledb
    except ImportError as exc:
        raise SystemExit(
            "未安装 oracledb。请先执行：python -m pip install -r requirements.txt"
        ) from exc

    section = cfg["oracle"]
    timeout = int(section.get("timeout_seconds", "30"))
    dsn = oracledb.makedsn(
        section["host"].strip(),
        int(section["port"]),
        service_name=section["service_name"].strip(),
    )
    conn = oracledb.connect(
        user=section["user"].strip(),
        password=section["password"],
        dsn=dsn,
        tcp_connect_timeout=timeout,
    )
    # 只读意图：禁止隐式提交写操作；本脚本也只执行 SELECT。
    conn.autocommit = False
    return conn, timeout


def cell_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value).strip()


def execute_select(
    conn,
    sql_text: str,
    *,
    timeout_seconds: int,
    expected_columns: tuple[str, ...] | None = None,
) -> QueryResult:
    started = datetime.now()
    cursor = conn.cursor()
    try:
        # call_timeout 单位为毫秒
        if hasattr(conn, "call_timeout"):
            conn.call_timeout = timeout_seconds * 1000
        cursor.execute(sql_text)
        colnames = [d[0].upper() for d in cursor.description]
        if expected_columns is not None and tuple(colnames) != expected_columns:
            finished = datetime.now()
            return QueryResult(
                started_at=started,
                finished_at=finished,
                elapsed_seconds=(finished - started).total_seconds(),
                rows=[],
                error=f"列不匹配：期望 {expected_columns}，实际 {tuple(colnames)}",
            )
        raw_rows = cursor.fetchall()
        rows = [
            {colnames[i]: cell_to_text(value) for i, value in enumerate(row)}
            for row in raw_rows
        ]
        finished = datetime.now()
        return QueryResult(
            started_at=started,
            finished_at=finished,
            elapsed_seconds=(finished - started).total_seconds(),
            rows=rows,
            error=None,
        )
    except Exception as exc:  # noqa: BLE001 - 需要完整记录 Oracle/网络错误
        finished = datetime.now()
        return QueryResult(
            started_at=started,
            finished_at=finished,
            elapsed_seconds=(finished - started).total_seconds(),
            rows=[],
            error=str(exc),
        )
    finally:
        cursor.close()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(columns))
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def parse_dates(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def quality_check(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(r["TASK_TYPE"] for r in rows)
    unknown_types = sorted(set(counts) - set(ALLOWED_TASK_TYPES))
    nulls = {col: sum(1 for r in rows if not r.get(col)) for col in EXPECTED_COLUMNS}

    exact = Counter(
        (r["TASK_TYPE"], r["SUBLOT"], r["EQP"], r["AREA"], r["STEP"], r["DATES"])
        for r in rows
    )
    exact_dup_groups = sum(1 for _, n in exact.items() if n > 1)
    exact_dup_extra = sum(n - 1 for _, n in exact.items() if n > 1)

    by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_sublot: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_eqp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_key[(row["TASK_TYPE"], row["SUBLOT"])].append(row)
        by_sublot[row["SUBLOT"]].append(row)
        by_eqp[row["EQP"]].append(row)

    key_conflicts = []
    for (task_type, sublot), items in by_key.items():
        pairs = {(x["EQP"], x["AREA"]) for x in items}
        if len(pairs) > 1:
            key_conflicts.append(
                {
                    "task_type": task_type,
                    "sublot": sublot,
                    "eqps": sorted({x["EQP"] for x in items}),
                    "areas": sorted({x["AREA"] for x in items}),
                }
            )

    cross_type = []
    for sublot, items in by_sublot.items():
        types = sorted({x["TASK_TYPE"] for x in items})
        if len(types) > 1:
            cross_type.append({"sublot": sublot, "types": types})

    gate_optical = []
    for sublot, items in by_sublot.items():
        types = {x["TASK_TYPE"] for x in items}
        if "WIRE_TO_GATE" in types and "WIRE_TO_OPTICAL" in types:
            gate_optical.append(sublot)

    eqp_multi_area = []
    for eqp, items in by_eqp.items():
        areas = sorted({x["AREA"] for x in items if x["AREA"]})
        if len(areas) > 1:
            eqp_multi_area.append({"eqp": eqp, "areas": areas})

    dates = [d for d in (parse_dates(r["DATES"]) for r in rows) if d is not None]
    max_lengths = {
        col: max((len(r.get(col, "")) for r in rows), default=0)
        for col in ("SUBLOT", "AREA", "EQP", "STEP")
    }
    over_declared = {
        col: max_lengths[col]
        for col, limit in DECLARED_MAX_BYTES.items()
        if max_lengths[col] > limit
    }
    suspicious_areas = sorted(
        {r["AREA"] for r in rows if r["AREA"] and len(r["AREA"]) <= 2}
    )

    return {
        "row_count": len(rows),
        "counts": dict(counts),
        "unknown_types": unknown_types,
        "nulls": nulls,
        "exact_dup_groups": exact_dup_groups,
        "exact_dup_extra": exact_dup_extra,
        "duplicate_task_keys": sum(1 for items in by_key.values() if len(items) > 1),
        "key_conflicts": key_conflicts,
        "cross_type_conflicts": cross_type,
        "gate_optical_conflicts": gate_optical,
        "eqp_multi_area": eqp_multi_area,
        "date_min": min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else "",
        "date_max": max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else "",
        "before_go_live": sum(1 for d in dates if d < GO_LIVE),
        "max_lengths": max_lengths,
        "over_declared": over_declared,
        "suspicious_areas": suspicious_areas,
        "column_count_ok": True,
    }


def write_phase1_record(path: Path, result: QueryResult) -> None:
    lines = [
        f"查询开始时间：{result.started_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"查询完成时间：{result.finished_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"查询耗时：{result.elapsed_seconds:.2f}s",
        f"返回总行数：{result.row_count}",
        f"Oracle错误：{result.error or '无'}",
        "使用的Oracle客户端：python-oracledb thin",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def phase1(conn, timeout: int, base: Path, output: Path) -> tuple[QueryResult, dict[str, Any]]:
    sql_path = base / "MES五类任务合并查询.sql"
    sql_text = assert_readonly_sql(sql_path.read_text(encoding="utf-8"), sql_path.name)
    print(f"[阶段1] 执行合并SQL：{sql_path.name}")
    result = execute_select(
        conn,
        sql_text,
        timeout_seconds=timeout,
        expected_columns=EXPECTED_COLUMNS,
    )
    if not result.success:
        write_phase1_record(output / "MES五类任务合并查询测试记录.md", result)
        raise SystemExit(f"阶段1失败：{result.error}")

    csv_path = output / "MES五类任务合并查询result.csv"
    write_csv(csv_path, result.rows, EXPECTED_COLUMNS)
    write_phase1_record(output / "MES五类任务合并查询测试记录.md", result)
    quality = quality_check(result.rows)
    print(
        f"[阶段1] 完成：行数={result.row_count}，耗时={result.elapsed_seconds:.2f}s，"
        f"CSV={csv_path.name}"
    )
    return result, quality


def phase2(
    conn,
    timeout: int,
    base: Path,
    output: Path,
    merged_counts: dict[str, int],
) -> list[dict[str, Any]]:
    mapping = [
        ("DIE_TO_WIRE_STAGING", "01_DIE_TO_WIRE_STAGING.sql"),
        ("DIE_TO_OVEN", "02_DIE_TO_OVEN.sql"),
        ("WIRE_TO_GATE", "03_WIRE_TO_GATE.sql"),
        ("WIRE_TO_OPTICAL", "04_WIRE_TO_OPTICAL.sql"),
        ("STAGING_TO_WIRE", "05_STAGING_TO_WIRE.sql"),
    ]
    rows_out: list[dict[str, Any]] = []
    print("[阶段2] 执行5组独立SQL并统计行数")
    for task_type, filename in mapping:
        sql_path = base / "sql" / "original_queries" / filename
        sql_text = assert_readonly_sql(sql_path.read_text(encoding="utf-8"), sql_path.name)
        result = execute_select(conn, sql_text, timeout_seconds=timeout)
        merged = merged_counts.get(task_type, 0)
        original = result.row_count if result.success else -1
        diff = (original - merged) if result.success else None
        rows_out.append(
            {
                "task_type": task_type,
                "sql_file": filename,
                "started_at": result.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "finished_at": result.finished_at.strftime("%Y-%m-%d %H:%M:%S"),
                "elapsed_seconds": f"{result.elapsed_seconds:.2f}",
                "original_count": original if result.success else "",
                "merged_count": merged,
                "diff": "" if diff is None else diff,
                "success": "Y" if result.success else "N",
                "error": result.error or "",
            }
        )
        status = "OK" if result.success else f"FAIL:{result.error}"
        print(
            f"  - {task_type}: original={original}, merged={merged}, "
            f"elapsed={result.elapsed_seconds:.2f}s, {status}"
        )

    out_path = output / "phase2_original_counts.csv"
    with out_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "task_type",
                "sql_file",
                "started_at",
                "finished_at",
                "elapsed_seconds",
                "original_count",
                "merged_count",
                "diff",
                "success",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"[阶段2] 完成：{out_path.name}")
    return rows_out


def phase3(
    conn,
    timeout: int,
    base: Path,
    output: Path,
    rounds: int,
    wait_seconds: int,
) -> list[dict[str, Any]]:
    sql_path = base / "MES五类任务合并查询.sql"
    sql_text = assert_readonly_sql(sql_path.read_text(encoding="utf-8"), sql_path.name)
    print(f"[阶段3] 连续执行合并SQL {rounds} 轮，每轮完成后等待 {wait_seconds}s")
    records: list[dict[str, Any]] = []
    for i in range(1, rounds + 1):
        result = execute_select(
            conn,
            sql_text,
            timeout_seconds=timeout,
            expected_columns=EXPECTED_COLUMNS,
        )
        success = result.success and result.elapsed_seconds <= timeout
        warn = result.elapsed_seconds > 10
        records.append(
            {
                "round": i,
                "started_at": result.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "finished_at": result.finished_at.strftime("%Y-%m-%d %H:%M:%S"),
                "elapsed_seconds": f"{result.elapsed_seconds:.2f}",
                "row_count": result.row_count if result.success else "",
                "success": "Y" if success else "N",
                "slow_warning": "Y" if warn else "N",
                "error": result.error or "",
            }
        )
        print(
            f"  - 第{i}轮: rows={result.row_count if result.success else 'N/A'}, "
            f"elapsed={result.elapsed_seconds:.2f}s, success={success}"
        )
        if i < rounds:
            time.sleep(wait_seconds)

    out_path = output / "phase3_perf_rounds.csv"
    with out_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "round",
                "started_at",
                "finished_at",
                "elapsed_seconds",
                "row_count",
                "success",
                "slow_warning",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(records)
    print(f"[阶段3] 完成：{out_path.name}")
    return records


def write_summary(
    path: Path,
    phase1_result: QueryResult | None,
    quality: dict[str, Any] | None,
    phase2_rows: list[dict[str, Any]] | None,
    phase3_rows: list[dict[str, Any]] | None,
) -> None:
    lines: list[str] = [
        "# MES五类任务合并查询测试汇总",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Python：{sys.version.split()[0]}",
        "",
    ]

    if phase1_result is not None and quality is not None:
        lines.extend(
            [
                "## 阶段1：单次合并查询",
                "",
                f"- 开始：{phase1_result.started_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- 完成：{phase1_result.finished_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- 耗时：{phase1_result.elapsed_seconds:.2f}s",
                f"- 行数：{phase1_result.row_count}",
                f"- 错误：{phase1_result.error or '无'}",
                f"- 性能目标(≤5s)：{'通过' if phase1_result.elapsed_seconds <= 5 else '未通过'}",
                "",
                "### 任务类型数量",
                "",
            ]
        )
        for task_type in ALLOWED_TASK_TYPES:
            lines.append(f"- `{task_type}`：{quality['counts'].get(task_type, 0)}")
        lines.extend(
            [
                "",
                "### 质量检查",
                "",
                f"- 未知TASK_TYPE：{quality['unknown_types'] or '无'}",
                f"- EQP空值：{quality['nulls']['EQP']}",
                f"- DATES空值：{quality['nulls']['DATES']}",
                f"- AREA空值：{quality['nulls']['AREA']}",
                f"- 完全重复组：{quality['exact_dup_groups']}",
                f"- TASK_TYPE+SUBLOT冲突：{len(quality['key_conflicts'])}",
                f"- 跨任务类型冲突：{len(quality['cross_type_conflicts'])}",
                f"- 关卡/三光互斥冲突：{len(quality['gate_optical_conflicts'])}",
                f"- 同一EQP多AREA：{len(quality['eqp_multi_area'])}",
                f"- DATES最早：{quality['date_min']}",
                f"- DATES最晚：{quality['date_max']}",
                f"- 早于上线时间2026-08-01：{quality['before_go_live']}",
                f"- 超过声明长度字段：{quality['over_declared'] or '无'}",
                f"- 可疑短AREA：{quality['suspicious_areas'] or '无'}",
                "",
            ]
        )

    if phase2_rows is not None:
        lines.extend(["## 阶段2：独立SQL对比", ""])
        for row in phase2_rows:
            lines.append(
                f"- `{row['task_type']}`：original={row['original_count']}，"
                f"merged={row['merged_count']}，diff={row['diff']}，"
                f"耗时={row['elapsed_seconds']}s，success={row['success']}"
            )
        lines.append("")

    if phase3_rows is not None:
        elapsed = [float(r["elapsed_seconds"]) for r in phase3_rows]
        success_count = sum(1 for r in phase3_rows if r["success"] == "Y")
        avg = sum(elapsed) / len(elapsed) if elapsed else 0.0
        mx = max(elapsed) if elapsed else 0.0
        lines.extend(
            [
                "## 阶段3：连续性能测试",
                "",
                f"- 轮次：{len(phase3_rows)}",
                f"- 成功轮次：{success_count}",
                f"- 平均耗时：{avg:.2f}s",
                f"- 最大耗时：{mx:.2f}s",
                f"- 全部成功：{'是' if success_count == len(phase3_rows) else '否'}",
                f"- 平均≤5s：{'是' if avg <= 5 else '否'}",
                f"- 最大≤10s：{'是' if mx <= 10 else '否'}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[汇总] 已写入 {path.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MES五类任务合并查询自动化测试")
    parser.add_argument(
        "--phase",
        choices=("1", "2", "3", "all"),
        default="all",
        help="执行阶段，默认 all",
    )
    parser.add_argument("--rounds", type=int, default=10, help="阶段3轮次，默认10")
    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=10,
        help="阶段3每轮完成后等待秒数，默认10",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=None,
        help="查询超时秒数，默认读取 config.ini",
    )
    parser.add_argument(
        "--config",
        default="config.ini",
        help="配置文件路径，默认当前目录 config.ini",
    )
    return parser.parse_args()


def main() -> None:
    ensure_python_version()
    args = parse_args()
    base = script_dir()
    output = base / "output"
    output.mkdir(parents=True, exist_ok=True)

    cfg = load_config(base / args.config)
    timeout = args.timeout_seconds
    if timeout is None:
        timeout = int(cfg["oracle"].get("timeout_seconds", "30"))

    print(f"Python={sys.version.split()[0]}  timeout={timeout}s  phase={args.phase}")
    conn, _ = connect_oracle(cfg)
    try:
        phase1_result: QueryResult | None = None
        quality: dict[str, Any] | None = None
        phase2_rows: list[dict[str, Any]] | None = None
        phase3_rows: list[dict[str, Any]] | None = None
        merged_counts: dict[str, int] = {}

        if args.phase in ("1", "all", "2"):
            # 阶段2需要合并数量；若只跑2，也先跑一次阶段1统计。
            phase1_result, quality = phase1(conn, timeout, base, output)
            merged_counts = quality["counts"]

        if args.phase in ("2", "all"):
            if not merged_counts and phase1_result is None:
                raise SystemExit("阶段2需要先有合并查询结果")
            phase2_rows = phase2(conn, timeout, base, output, merged_counts)

        if args.phase in ("3", "all"):
            phase3_rows = phase3(
                conn,
                timeout,
                base,
                output,
                rounds=args.rounds,
                wait_seconds=args.wait_seconds,
            )

        write_summary(
            output / "test_summary.md",
            phase1_result,
            quality,
            phase2_rows,
            phase3_rows,
        )
        print("全部完成。请将 output/ 目录拷回本机。")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
