"""MES Lab 统一命令行入口。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib
from typing import Any

from .bundle import build_bundle
from .importer import import_run
from .manifest import QueryCatalog, QuerySpec, load_query_manifest
from .runner import run_factory
from .textio import read_local_text


MES_ROOT = Path(__file__).resolve().parents[2]


def _experiment_queries(path: str | None) -> tuple[list[str], list[QuerySpec]]:
    if not path:
        return [], []
    source = Path(path)
    if source.suffix.lower() == ".json":
        data = json.loads(source.read_text(encoding="utf-8"))
    else:
        with source.open("rb") as stream:
            data = tomllib.load(stream)
    values = (
        data.get("query_ids", data.get("queries", []))
        if isinstance(data, dict)
        else data
    )
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise ValueError("实验文件必须提供字符串数组 query_ids（或 queries）")
    source_values = data.get("source_manifests", []) if isinstance(data, dict) else []
    if not isinstance(source_values, list) or not all(
        isinstance(value, str) for value in source_values
    ):
        raise ValueError("source_manifests 必须是字符串数组")
    source_queries = [
        load_query_manifest((source.parent / value).resolve())
        for value in source_values
    ]
    return values, source_queries


def _parameters(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    if value.startswith("@"):
        text = read_local_text(value[1:])
    else:
        possible_path = Path(value)
        text = read_local_text(possible_path) if possible_path.is_file() else value
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("参数 JSON 顶层必须是对象")
    return data


def _experiment_record(*values: str | None) -> dict[str, Any] | None:
    """Parse optional experiment record JSON.

    ``--approval-json`` remains as a deprecated alias for the same payload.
    Customer approval is no longer required; any provided fields are recorded only.
    """
    provided = [value for value in values if value]
    if not provided:
        return None
    if len(provided) > 1:
        raise ValueError("请只提供 --experiment-record 或 --approval-json 之一")
    data = _parameters(provided[0])
    allowed = {
        "status",
        "reference",
        "recorded_by",
        "recorded_at",
        "approved_by",
        "approved_at",
        "expires_at",
        "execution_window",
        "scope",
        "notes",
    }
    unexpected = sorted(set(data) - allowed)
    if unexpected:
        raise ValueError(f"实验记录含未允许字段: {', '.join(unexpected)}")
    return data


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mes-lab",
        description="MES 查询的离线打包、工厂只读执行和证据导入工具",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    build = commands.add_parser("build-bundle", help="构建可带入工厂的查询 bundle")
    build.add_argument("--queries-root", default=str(MES_ROOT / "queries"))
    build.add_argument("--output", required=True)
    build.add_argument("--query-id", action="append", dest="query_ids")
    build.add_argument("--experiment", help="含 query_ids/queries 数组的 JSON 或 TOML")

    run = commands.add_parser("run-factory", help="在工厂环境执行只读查询")
    run.add_argument("--bundle", required=True)
    run.add_argument("--config", required=True, help="本地 config.ini（不会写入输出）")
    run.add_argument("--output-root", required=True)
    run.add_argument("--query-id", action="append", dest="query_ids")
    run.add_argument(
        "--params-json",
        help="JSON 对象、JSON 文件路径或 @JSON文件；多查询可按 query id 嵌套",
    )
    run.add_argument(
        "--experiment-record",
        help="可选实验记录 JSON/文件（谁、何时、备注、范围等；不进密码）",
    )
    run.add_argument(
        "--approval-json",
        help="已废弃别名，等同 --experiment-record；不再要求客户批准",
    )
    run.add_argument("--rounds", type=int, default=1)
    run.add_argument("--wait-seconds", type=float, default=0)
    mode = run.add_mutually_exclusive_group()
    mode.add_argument(
        "--phase1",
        action="store_true",
        help="执行 MES_TASK_UNION 第一阶段（固定单轮）",
    )
    mode.add_argument(
        "--compare-sources",
        nargs="+",
        metavar="QUERY_ID",
        help="依次执行客户源或其他来源查询并保留独立 CSV",
    )

    importing = commands.add_parser("import-run", help="校验并导入工厂运行证据")
    importing.add_argument("--run-dir", required=True)
    importing.add_argument("--bundle", required=True)
    importing.add_argument("--mes-root", default=str(MES_ROOT))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "build-bundle":
            catalog = QueryCatalog(args.queries_root)
            experiment_ids, source_queries = _experiment_queries(args.experiment)
            selected = list(args.query_ids or []) + experiment_ids
            selected = list(dict.fromkeys(selected)) or None
            queries = catalog.select(selected) + source_queries
            if len({query.id for query in queries}) != len(queries):
                raise ValueError("正式查询与实验来源查询存在重复 QUERY_ID")
            manifest = build_bundle(queries, args.output)
            print(f"已构建 bundle：{Path(args.output).resolve()}")
            print(f"bundle_id：{manifest['bundle_id']}，查询数：{len(manifest['queries'])}")
            return 0

        if args.command == "run-factory":
            query_ids = args.query_ids
            mode_name = "single"
            rounds = args.rounds
            if args.phase1:
                query_ids = ["MES_TASK_UNION"]
                rounds = 1
                mode_name = "phase1"
            elif args.compare_sources:
                query_ids = ["MES_TASK_UNION", *args.compare_sources]
                mode_name = "compare_sources"
            elif rounds > 1:
                mode_name = "performance"
            experiment_record = _experiment_record(
                getattr(args, "experiment_record", None),
                getattr(args, "approval_json", None),
            )
            run_dir = run_factory(
                bundle_dir=args.bundle,
                config_path=args.config,
                output_root=args.output_root,
                query_ids=query_ids,
                parameters=_parameters(args.params_json),
                rounds=rounds,
                wait_seconds=args.wait_seconds,
                mode=mode_name,
                experiment_record=experiment_record,
            )
            print(f"执行完成：{run_dir}")
            return 0

        imported = import_run(args.run_dir, args.bundle, args.mes_root)
        print(f"导入完成：{imported}")
        return 0
    except Exception as exc:
        if getattr(args, "command", None) == "run-factory":
            print(f"错误：工厂执行失败（{type(exc).__name__}）：{exc}", file=sys.stderr)
        else:
            print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
