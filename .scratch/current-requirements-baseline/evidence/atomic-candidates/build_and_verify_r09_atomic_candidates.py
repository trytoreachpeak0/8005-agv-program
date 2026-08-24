from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import build_and_verify_r03_atomic_candidates as common


REPO = common.REPO
SOURCE_LEDGER = common.SOURCE_LEDGER
OUTPUT = Path(__file__).with_name("R09-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R09-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r09-pass"
EXPECTED_SOURCE_IDS = [
    "R09-01", "R09-02", "R09-03", "R09-04", "R09-05", "R09-06",
    "R09-07", "R09-08", "R09-11", "R09-13", "R09-17", "R09-18",
]
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]

POINTER_DEFINITIONS = {
    "CF-R01-001": "TransportDemandKey / MES 需求业务键的跨批次冲突线索。",
    "CF-R01-002": "MES 当前阶段只读与回写主张的跨批次冲突线索。",
    "CF-R09-001": "QueueingStall 清积压策略与 UC-008 队列 0/1 口径须在跨批次去重后复核。",
    "CF-R09-002": "充电改派选桩策略与 BR-007 的可用、占用、预占及电量条件须在跨批次去重后复核。",
    "Q-R09-001": "充电改派 N=2 与 UC-012 的失败阶段/重试次数 TBD 必须分阶段澄清。",
    "RES-R09-001": "“决定工厂 MES 验证的批准与完整性证据门槛”固定 SQL/运行证据不能替代需求批准。",
    "RES-R09-002": "“决定 RIoT 项目 API 白名单与调用安全边界”固定项目调用、凭证与结果确认边界。",
    "EVID-R09-001": "“补齐 RIoT 目标环境与受控接口快照证据”绑定 8005 环境、build、导出人与 OpenAPI 哈希。",
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R09"]
    if len(batch_rows) != 18:
        raise RuntimeError(f"R09 batch boundary drift: expected=18 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R09"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R09 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 12, "excluded": 6}):
        raise RuntimeError("R09 route boundary drift; expected 12 candidate and 6 excluded documents")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows


def expand_named_list(statement: str) -> list[str]:
    value = common.normalize(statement)
    prefixes = [
        "第一版具名 Facade 覆盖 DispatchLoop 全量控制面：",
        "第一版具名 Facade 不包含：",
        "明确排除：",
    ]
    for prefix in prefixes:
        if value.startswith(prefix):
            body = value[len(prefix):]
            return [f"{prefix}{item}" for item in re.split(r"[、；]", body) if common.normalize(item)]
    if "第一期只实现接入——" in value:
        lead, body = value.split("第一期只实现接入——", 1)
        return [common.normalize(lead + "第一期只实现接入") ] + [f"第一期接入范围：{item}" for item in re.split(r"、", body) if common.normalize(item)]
    return [value]


def adr_units(source: common.Source) -> list[common.Unit]:
    path = REPO / source.path
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    title = common.normalize(lines[0].lstrip("# ")) if lines else "document-root"
    section = "Decision"
    units: list[common.Unit] = []
    for index, raw in enumerate(lines):
        stripped = raw.strip()
        if not stripped or stripped.startswith("# "):
            continue
        label = re.match(r"^\*\*(.+?)\*\*:\s*(.*)$", stripped)
        if label:
            section = common.normalize(label.group(1))
            stripped = common.normalize(label.group(2))
            if not stripped:
                continue
        else:
            stripped = re.sub(r"^[-*+]\s+", "", stripped)
        context = common.normalize(raw)
        starts_named_list = any(stripped.startswith(prefix) for prefix in (
            "第一版具名 Facade 覆盖 DispatchLoop 全量控制面：",
            "第一版具名 Facade 不包含：",
            "明确排除：",
        ))
        initial_units = expand_named_list(stripped) if starts_named_list else common.split_atomic(stripped)
        for initial in initial_units:
            expanded_atoms = common.split_atomic(initial) if starts_named_list else expand_named_list(initial)
            for atom in expanded_atoms:
                units.append(common.Unit(
                    source.record_id,
                    f"line {index + 1}",
                    f"{title} > {section}",
                    atom,
                    context,
                    "adr-decision-or-section-item",
                ))
    return units


def in_section(unit: common.Unit, name: str) -> bool:
    return bool(re.search(rf">\s*{re.escape(name)}$", unit.section, re.I))


def is_evidence(unit: common.Unit) -> bool:
    if any(in_section(unit, name) for name in ("Status", "Considered Options", "Implementation")):
        return True
    return bool(re.match(r"^(?:依据|对照表见|可再派纯判定辅助见)", unit.statement))


def is_unresolved(text: str) -> bool:
    return bool(re.search(r"\bTBD\b|待确认|待定|留待后续|另条决策", text, re.I))


def has_security_or_safety(text: str) -> bool:
    return bool(re.search(
        r"CallApiKey|AdminLogin|AccessToken|Bearer|refresh|鉴权|凭证|密钥|轮换|过期|EmergencyStop|急停|权限|安全",
        text,
        re.I,
    ))


def has_external_contract(text: str) -> bool:
    return bool(re.search(
        r"MES_TASK_UNION|Oracle|客户.*SQL|批准 SQL|SQL/DDL|执行 DDL|RIoT|BC-(?:ORDER|STATE|AUTH)|RouteCost|NearStationQuery|"
        r"CMD_ORDER_CANCEL|DispatchEnable|DispatchDisable|PriorityExec|OrderHold|OrderContinue|HangContinue|Map/Station|"
        r"byDefaultMissions|SUCCESS|procState|processingOrder|接口|API 契约|完整活动集合|只读 Oracle",
        text,
        re.I,
    ))


def has_business_behavior(text: str) -> bool:
    return bool(re.search(
        r"QUEUEING|HELD|HANG|Stall|清掉|确认 IDLE|再派|报警|转人工|自动 CANCEL|充电失败|改派|备用充电桩|"
        r"旧 HANG|终态|重试|无限重试|TransportDemand|demand_id|TASK_TYPE\+SUBLOT|VISIBLE|GONE|永久抑制|"
        r"不得建立|不得派车|消失语义|可再派|订单 SUCCESS|车 IDLE|调度.*超时|当前可派|顺序列表|硬映射",
        text,
        re.I,
    ))


def has_product_scope(text: str) -> bool:
    return bool(re.search(
        r"第一版|第一期|必须封装|具名 Facade|不包含|明确排除|仅作设备查询|派车发现必须|RawEscape|后续版本扩展",
        text,
        re.I,
    ))


def has_local_design(text: str) -> bool:
    return bool(re.search(
        r"全 C#|Windows Service|WPF|SQL Server|Kestrel|Thin|Thick|Instant Client|SQLite|FastAPI|Python|"
        r"MesIngest.*拆开|同一模块|投影库|安装目录|工程内|自包含|轮询实现|schema|store|HTTP|索引|游标分页|"
        r"幂等对账|重启恢复快照|字段冻结|PAUSED_ZERO_DROP|Kiota|SDK 内置|状态机塞进客户端|单次读写|"
        r"几何 path|mission 编排 DSL|流程引擎|RawEscape|技术选型|开发期|生产 MesIngest",
        text,
        re.I,
    ))


def content_class(unit: common.Unit, source: common.Source) -> tuple[str, str]:
    text = unit.statement
    if is_evidence(unit):
        return "source-status-options-or-implementation-evidence", "evidence-only"
    if is_unresolved(text):
        return "unresolved-product-or-contract-question", "needs-question-resolution"
    security = has_security_or_safety(text)
    external = has_external_contract(text)
    business = has_business_behavior(text)
    product = has_product_scope(text)
    local = has_local_design(text)

    if security:
        return "security-or-safety-boundary-candidate", "needs-security-authority-bound-contract-and-explicit-approval"
    if business and external:
        return "business-behavior-relying-on-external-contract-candidate", "needs-business-owner-bound-contract-and-explicit-approval"
    if external and not local:
        return "external-system-contract-candidate", "needs-bound-external-contract-and-explicit-approval"
    if business:
        return "mes-dispatch-or-demand-lifecycle-business-rule-candidate", "needs-business-owner-and-explicit-approval"
    if product and not local:
        return "product-capability-scope-candidate", "needs-product-owner-and-explicit-approval"
    if local:
        return "embedded-local-technical-design-decision", "exclude-from-requirement-approval"
    if product:
        return "product-capability-scope-candidate", "needs-product-owner-and-explicit-approval"
    if in_section(unit, "Consequences"):
        return "downstream-obligation-or-scope-candidate", "needs-responsible-owner-and-explicit-approval"
    return "adr-claim-needing-owner-classification", "needs-responsible-owner-and-explicit-approval"


def pointers_for(unit: common.Unit, source: common.Source) -> str:
    text = f"{unit.section} {unit.statement}"
    pointers: list[str] = []
    if re.search(r"TASK_TYPE\+SUBLOT|TransportDemandKey|永久抑制|GONE 后同键再现|抑制键", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"MES|Oracle|客户.*SQL|SQL/DDL|DDL", text, re.I) and re.search(r"只读|回写|不写入|不修改|未经授权", text, re.I):
        pointers.append("CF-R01-002")
    if source.record_id == "R09-01" and re.search(r"QUEUEING|HELD|队列|积压", text, re.I):
        pointers.append("CF-R09-001")
    if source.record_id == "R09-04" and re.search(r"允许.*集合|NearStationQuery|备用桩|站点", text, re.I):
        pointers.append("CF-R09-002")
    if source.record_id == "R09-05" and re.search(r"N=2|2 次|重试", text, re.I):
        pointers.append("Q-R09-001")
    if source.record_id in {"R09-07", "R09-08"} and re.search(r"工厂|客户.*SQL|Oracle|探针|DDL", text, re.I):
        pointers.append("RES-R09-001")
    if source.record_id in {"R09-11", "R09-13", "R09-17", "R09-18"} and re.search(
        r"CallApiKey|AdminLogin|AccessToken|Map/Station|RouteCost|NearStationQuery|CMD_ORDER_CANCEL|Dispatch|"
        r"EmergencyStop|PriorityExec|OrderHold|OrderContinue|HangContinue|SUCCESS|IDLE|devices|byDefaultMissions",
        text,
        re.I,
    ):
        pointers.extend(["RES-R09-002", "EVID-R09-001"])
    return ",".join(dict.fromkeys(pointers)) or NONE


def scope_for(source: common.Source, candidate_class: str) -> str:
    number = int(source.record_id.split("-")[1])
    if 1 <= number <= 5:
        return "8005-MES-dispatch-stall-hang-and-charge-recovery"
    if 6 <= number <= 8:
        return "8005-MES-ingest-demand-lifecycle-and-data-access"
    if "security" in candidate_class or "safety" in candidate_class:
        return "8005-RIoT-authentication-control-and-safety"
    return "8005-RIoT-SDK-and-dispatch-control-integration"


def approval_gap_for(candidate_class: str, route: str) -> str:
    gaps: list[str] = []
    if route == "evidence-only":
        gaps = ["evidence-only-not-an-approval-unit"]
    elif route == "exclude-from-requirement-approval":
        gaps = ["authoritative-requirement-source-if-behavior-is-required", "separate-technical-decision-review"]
    elif route == "needs-question-resolution":
        gaps = ["question-resolution", "responsible-decision-owner"]
    elif "security-authority" in route:
        gaps = ["security-or-safety-owner", "bound-target-environment-and-interface-contract", "credential-or-call-safety-governance"]
    elif "bound-contract" in route:
        gaps = ["authoritative-business-owner", "bound-external-system-version-or-contract", "observed-failure-path-evidence"]
    elif "external-contract" in route:
        gaps = ["external-system-owner-or-authorized-delegate", "bound-environment-build-and-contract-hash"]
    elif "business-owner" in route:
        gaps = ["authoritative-business-source", "responsible-business-or-operations-owner"]
    elif "product-owner" in route:
        gaps = ["approved-product-scope-source", "responsible-product-owner"]
    else:
        gaps = ["responsible-owner-classification", "authoritative-source"]
    return ";".join(dict.fromkeys(gaps + CORE_GAP))


def build_rows() -> list[dict[str, str]]:
    sources, _ = load_sources()
    rows: list[dict[str, str]] = []
    for source in sources:
        path = REPO / source.path
        actual = common.sha256_file(path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        units = adr_units(source)
        if not units:
            raise RuntimeError(f"No atomic units extracted from {source.record_id}")
        for unit in units:
            candidate_class, route = content_class(unit, source)
            derivation = (
                f"document-route:R09-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                f"ledger-history:{common.normalize(source.derivation)}"
            )
            rows.append({
                "candidate_id": "", "batch_id": "R09", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest, "exact_location": unit.location,
                "section_path": unit.section, "statement_text": unit.statement, "source_context": unit.context,
                "statement_fingerprint": common.fingerprint(unit.statement), "candidate_class": candidate_class,
                "source_claim_status": "unapproved-internal-adr-status-is-not-business-or-external-contract-approval",
                "applicable_scope": scope_for(source, candidate_class), "baseline_route": route,
                "duplicate_or_derivation": derivation, "conflict_pointer": pointers_for(unit, source),
                "approval_state": "not-approved", "approval_gap": approval_gap_for(candidate_class, route),
            })
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R09-A{index:04d}"
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    pointers = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer and pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_batch_documents_not_extracted": 6,
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "pointer_counts": dict(sorted(pointers.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "permanent_requirement_ids": sum(bool(re.search(r"\bREQ-\d{4}\b", row["candidate_id"])) for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if summary["source_documents"] != 12 or summary["excluded_batch_documents_not_extracted"] != 6:
        raise RuntimeError(f"R09 source coverage mismatch: {summary}")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R09 approval isolation failed")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R09 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R09-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R09 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R09 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R09 contains an unauthorized approval upgrade")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R09 approval gap is incomplete")
    if summary["by_route"].get("exclude-from-requirement-approval", 0) <= 0:
        raise RuntimeError("R09 failed to isolate local technical design")
    for required in ("CF-R01-001", "CF-R01-002", "RES-R09-001", "RES-R09-002", "EVID-R09-001"):
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R09 pointer missing: {required}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R09 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R09 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R09 summary JSON differs from a clean rebuild")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    rows = build_rows()
    summary = summary_for(rows)
    verify(rows, summary)
    if args.verify_only:
        verify_existing(rows, summary)
    else:
        write_outputs(rows, summary)
        verify_existing(rows, summary)
    print(
        "R09 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} "
        f"excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"exact_duplicate_rows={summary['exact_duplicate_rows']} approval_upgrades={summary['approval_upgrades']} "
        f"pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
