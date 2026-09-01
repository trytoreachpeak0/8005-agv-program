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
OUTPUT = Path(__file__).with_name("R12-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R12-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r12-pass"
EXPECTED_SOURCE_IDS = ["R12-17", "R12-50"]
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]

POINTER_DEFINITIONS = {
    "CF-R01-001": "TransportDemandKey / DemandId / GONE 后同键再现的跨批次身份与取消边界线索。",
    "CF-R01-002": "MES 当前阶段只读、回写与不得改写客户 SQL 的跨批次边界线索。",
    "AD-R01-001": "五类/六类运输任务的版本差异；第六类不能由历史 spec 自动获批。",
    "RES-R08-003": "“确定领域词汇唯一入口与旧术语表关系”固定根 CONTEXT.md 的澄清—批准—即时写回闭环。",
    "RES-R11-001": "“决定工厂 MES 验证的批准与完整性证据门槛”固定查询运行授权不等于需求批准。",
    "BOUND-R11-001": "历史 spec 中“客户批准 SQL”的自述缺少具名批准人、日期、范围与版本/哈希绑定。",
    "EVID-R11-001": "工厂 run 与耗时数据只是限定环境观察，不形成正式验收或长期性能保证。",
    "BOUND-R12-001": "R12 只从 2 份混合 spec 提取；31 张实施/修复任务和 17 张评审修复票只作历史证据。",
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R12"]
    if len(batch_rows) != 50:
        raise RuntimeError(f"R12 batch boundary drift: expected=50 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R12"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R12 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 2, "excluded": 48}):
        raise RuntimeError("R12 route boundary drift; expected 2 candidate and 48 excluded documents")
    expected_roles = Counter({
        "R12-SPEC-MIXED": 2,
        "R12-IMPLEMENTATION-TASK": 26,
        "R12-IMPLEMENTATION-DEVIATION-FIX": 5,
        "R12-REVIEW-REMEDIATION": 17,
    })
    if Counter(row["document_class"] for row in batch_rows) != expected_roles:
        raise RuntimeError("R12 document-role boundary drift")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows


def section_has(unit: common.Unit, pattern: str) -> bool:
    return bool(re.search(pattern, unit.section, re.I))


def text_has(unit: common.Unit, pattern: str) -> bool:
    return bool(re.search(pattern, f"{unit.section} {unit.statement}", re.I))


def is_status_or_history(unit: common.Unit) -> bool:
    if unit.section.endswith("MesIngest Phase 1") and re.fullmatch(r"Status:\s*ready-for-agent", unit.statement, re.I):
        return True
    if unit.section.endswith("MesIngest Watch Operations and Scalable Read Model") and re.fullmatch(
        r"Status:\s*ready-for-agent", unit.statement, re.I
    ):
        return True
    return section_has(unit, r"Testing Decisions|Documentation Outputs|Further Notes")


def is_unresolved(unit: common.Unit) -> bool:
    return bool(re.search(r"\bTBD\b|待定|待确认|未确定|尚未|名称可调整|名称灵活", unit.statement, re.I))


def is_local_technical_design(unit: common.Unit) -> bool:
    text = f"{unit.section} {unit.statement}"
    if section_has(unit, r"User Stories|Confirmed Domain Semantics|Out of Scope|Defaults"):
        return False
    if section_has(unit, r"Implementation Decisions > Modules|Implementation Decisions > Schema"):
        return True
    if section_has(unit, r"Testing Decisions|Documentation Outputs"):
        return True
    return bool(re.search(
        r"C#|Windows Service|WPF|SQL Server|Kestrel|DateTimeOffset|DATETIMEOFFSET|Oracle (?:Thin|Thick)|"
        r"Instant Client|NuGet|physical DDL|DDL mandate|adapter|ViewModel|DataGrid|GridSplitter|"
        r"JSON Lines|%LocalAppData%|Swagger|OpenAPI JSON|INCLUDE 列|DELETE.*重建|INSERT|UPDATE|UPSERT|"
        r"BIGINT|transaction|事务中|correlation id|self-contained|install directory|schema|store|"
        r"HTTP client|control trees|mock|integration tests?|unit tests?",
        text,
        re.I,
    ))


def is_security(unit: common.Unit) -> bool:
    return text_has(unit, r"credentials?|凭证|密码|密钥|Bearer|SharedSecret|Auth:|鉴权|敏感信息|秘密|localhost.*远程")


def is_domain_semantic(unit: common.Unit) -> bool:
    if section_has(unit, r"Confirmed Domain Semantics"):
        return True
    return text_has(unit, r"MesCurrentStepEnteredAt|DATES.*当前工序|STEP.*下一工序|不是 DATES 所属工序")


def is_external_mes_contract(unit: common.Unit) -> bool:
    return text_has(
        unit,
        r"MES_TASK_UNION|客户.*SQL|批准.*SQL|Oracle/CSV|Oracle.*DATES|完整活动快照|"
        r"(?<![A-Za-z0-9_])(?:TASK_TYPE|SUBLOT|AREA|EQP|PACKAGE)(?![A-Za-z0-9_])",
    )


def is_demand_lifecycle(unit: common.Unit) -> bool:
    return text_has(unit, r"TransportDemand|DemandId|reconcile|VISIBLE|GONE|PAUSED_ZERO_DROP|PausedZeroDrop|DisappearCount|"
        r"disappear|消失|再现|reappear|字段冻结|freeze|FIELD_DRIFT|重复.*(?:TASK_TYPE|key)|"
        r"zero-drop|零掉落|业务键|抑制")


def is_incident_or_alert(unit: common.Unit) -> bool:
    return text_has(unit, r"IngestAlert|AlertId|POLL_FAILURE|POLL_INCOMPLETE|DUPLICATE_RECONCILE_KEY|FIELD_DRIFT|"
        r"REAPPEAR_AFTER_GONE|横幅|告警|报警|alert|WatchConnectionEvent|OccurrenceCount|ResolvedAt")


def is_api_or_sync_contract(unit: common.Unit) -> bool:
    return text_has(unit, r"/api/|HTTP API|read-only HTTP|分页|cursor|nextCursor|hasMore|DemandChangeFeed|"
        r"afterSequence|high watermark|SYNC_CURSOR_EXPIRED|Bootstrap|Swagger|OpenAPI|DTO|外部程序|下游镜像")


def is_operator_product_behavior(unit: common.Unit) -> bool:
    return text_has(unit, r"factory operator|operator|WPF user|Watch|盯盘|筛选|排序|复制|右键|状态栏|"
        r"tooltip|详情窗口|非模态|布局|分隔|显示|刷新|时区|时间格式|陈旧")


def is_acceptance(unit: common.Unit) -> bool:
    return text_has(unit, r"factory validation|工厂.*验证|验收|执行计划|execution plan|人工验证|manual acceptance|性能.*gate")


def is_default(unit: common.Unit) -> bool:
    return section_has(unit, r"Defaults") or text_has(unit, r"\bdefault\b|默认|tunable|可调范围|可配置范围")


def classify(unit: common.Unit) -> tuple[str, str]:
    if is_status_or_history(unit):
        return "source-status-test-or-implementation-history-evidence", "evidence-only"
    if is_unresolved(unit):
        return "unresolved-historical-spec-question", "needs-question-resolution"
    if section_has(unit, r"Out of Scope"):
        return "historical-product-scope-boundary-candidate", "needs-product-owner-and-explicit-approval"
    if is_domain_semantic(unit):
        return "historical-domain-semantic-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"
    if is_security(unit):
        return "security-or-credential-boundary-candidate", "needs-security-owner-and-explicit-approval"
    if is_default(unit):
        return "tunable-operational-default-candidate", "needs-responsible-owner-and-explicit-approval"
    if is_local_technical_design(unit):
        return "embedded-local-technical-design-or-test-decision", "exclude-from-requirement-approval"
    if is_incident_or_alert(unit):
        return "incident-alert-and-operability-semantics-candidate", "needs-operations-owner-and-explicit-approval"
    if is_api_or_sync_contract(unit):
        return "read-api-or-downstream-sync-contract-candidate", "needs-interface-owner-and-explicit-approval"
    if is_operator_product_behavior(unit) and not is_demand_lifecycle(unit):
        return "operator-watch-ux-and-operability-candidate", "needs-operator-product-owner-and-explicit-approval"
    if is_external_mes_contract(unit) and is_demand_lifecycle(unit):
        return "demand-behavior-relying-on-external-mes-contract-candidate", "needs-business-owner-bound-data-contract-and-explicit-approval"
    if is_external_mes_contract(unit):
        return "external-mes-data-contract-or-source-boundary-candidate", "needs-bound-external-data-contract-and-explicit-approval"
    if is_demand_lifecycle(unit):
        return "transport-demand-lifecycle-business-rule-candidate", "needs-business-owner-and-explicit-approval"
    if is_acceptance(unit):
        return "factory-or-product-acceptance-condition-candidate", "needs-acceptance-owner-and-explicit-approval"
    if is_operator_product_behavior(unit):
        return "operator-watch-ux-and-operability-candidate", "needs-operator-product-owner-and-explicit-approval"
    if section_has(unit, r"Problem Statement|Solution|User Stories|Functional Requirements"):
        return "historical-product-capability-or-operational-behavior-candidate", "needs-product-owner-and-explicit-approval"
    if section_has(unit, r"Implementation Decisions"):
        return "mixed-historical-spec-claim-needing-owner-classification", "needs-atomic-reframing-before-approval"
    return "source-rationale-or-traceability-evidence", "evidence-only"


def source_status_for(source: common.Source) -> str:
    if source.record_id == "R12-50":
        return "ready-for-agent-and-self-described-confirmed-internal-spec-without-four-factor-requirement-approval"
    return "ready-for-agent-internal-implementation-spec-without-four-factor-requirement-approval"


def scope_for(source: common.Source, unit: common.Unit) -> str:
    if source.record_id == "R12-17":
        return "historical-MesIngest-phase-1-scope-current-applicability-needs-source-binding-and-reapproval"
    return "historical-MesIngest-watch-operations-scope-current-applicability-needs-source-binding-and-reapproval"


def upstream_references(unit: common.Unit, source: common.Source) -> str:
    text = f"{unit.section} {unit.statement}"
    refs: list[str] = []
    if source.record_id == "R12-50":
        refs.append("MesIngest-Phase-1-spec")
    if re.search(r"ADR-mes-0006|MesIngest only|dispatch.*out", text, re.I):
        refs.append("ADR-mes-0006")
    if re.search(r"ADR-mes-0007|C#|Windows Service|WPF|SQL Server|Kestrel", text, re.I):
        refs.append("ADR-mes-0007")
    if re.search(r"MES_TASK_UNION|客户.*SQL|批准.*SQL|query\.sql", text, re.I):
        refs.append("MES_TASK_UNION-query-materials")
    if re.search(r"CONTEXT\.md|Domain vocabulary|Confirmed Domain Semantics|MesCurrentStepEnteredAt", text, re.I):
        refs.append("root-CONTEXT.md-vocabulary-loop")
    if re.search(r"factory evidence|meslab|plant evidence|工厂.*证据|工厂.*验证", text, re.I):
        refs.append("R11-factory-run-and-query-evidence")
    return ",".join(dict.fromkeys(refs)) or "no-explicit-upstream-reference-in-atomic-unit"


def pointers_for(unit: common.Unit, source: common.Source) -> str:
    text = f"{unit.section} {unit.statement}"
    pointers: list[str] = ["BOUND-R12-001"]
    if re.search(r"TASK_TYPE\+SUBLOT|DemandId|reconcile key|reappear|GONE.*同|TransportDemandKey|抑制", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"MES|Oracle|客户.*SQL|query\.sql", text, re.I) and re.search(
        r"只读|read-only|不回写|不修改|不编辑|不执行 DDL|无 write|No write", text, re.I
    ):
        pointers.append("CF-R01-002")
    if re.search(r"六类|six TASK_TYPE|WIRE_TO_NITROGEN|另外五类", text, re.I):
        pointers.append("AD-R01-001")
    if section_has(unit, r"Confirmed Domain Semantics") or re.search(r"CONTEXT\.md|Domain vocabulary|MesCurrentStepEnteredAt", text, re.I):
        pointers.append("RES-R08-003")
    if re.search(r"客户批准|批准的.*SQL|工厂.*(?:probe|验证)|Oracle.*查询|MES_TASK_UNION", text, re.I):
        pointers.extend(["RES-R11-001", "BOUND-R11-001"])
    if re.search(r"~3s|sub-5s|performance context|plant evidence|工厂.*耗时|工厂.*性能", text, re.I):
        pointers.append("EVID-R11-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


def approval_gap_for(route: str) -> str:
    if route == "evidence-only":
        gaps = ["evidence-only-not-an-approval-unit"]
    elif route == "exclude-from-requirement-approval":
        gaps = ["authoritative-requirement-source-if-behavior-is-required", "separate-technical-decision-review"]
    elif route == "needs-question-resolution":
        gaps = ["question-resolution", "responsible-decision-owner"]
    elif "before-context-update" in route:
        gaps = ["domain-owner", "authoritative-domain-source", "user-approved-context-update"]
    elif "bound-data-contract" in route:
        gaps = ["authoritative-business-owner", "bound-MES-environment-query-version-and-result-evidence"]
    elif "external-data-contract" in route:
        gaps = ["external-data-owner-or-authorized-delegate", "bound-MES-environment-and-query-version"]
    elif "security-owner" in route:
        gaps = ["security-owner", "credential-and-binding-scope"]
    elif "interface-owner" in route:
        gaps = ["responsible-interface-owner", "consumer-and-compatibility-scope"]
    elif "operations-owner" in route:
        gaps = ["responsible-operations-owner", "incident-lifecycle-and-retention-scope"]
    elif "operator-product-owner" in route:
        gaps = ["operator-workflow-owner", "approved-usability-and-operability-scope"]
    elif "acceptance-owner" in route:
        gaps = ["responsible-acceptance-owner", "approved-test-object-environment-and-evidence-package"]
    elif "business-owner" in route:
        gaps = ["authoritative-business-source", "responsible-business-owner"]
    elif "product-owner" in route:
        gaps = ["approved-product-scope-source", "responsible-product-owner"]
    elif "atomic-reframing" in route:
        gaps = ["separate-business-obligation-from-technical-mechanism", "responsible-owner-classification"]
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
        units = common.markdown_units(source.record_id, path)
        if not units:
            raise RuntimeError(f"No atomic units extracted from {source.record_id}")
        for unit in units:
            candidate_class, route = classify(unit)
            derivation = (
                f"document-route:R12-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                f"current-applicability:{common.normalize(source.applicability)}; ledger-history:{common.normalize(source.derivation)}; "
                f"upstream-reference:{upstream_references(unit, source)}"
            )
            rows.append({
                "candidate_id": "", "batch_id": "R12", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest, "exact_location": unit.location,
                "section_path": unit.section, "statement_text": unit.statement, "source_context": unit.context,
                "statement_fingerprint": common.fingerprint(unit.statement), "candidate_class": candidate_class,
                "source_claim_status": source_status_for(source), "applicable_scope": scope_for(source, unit),
                "baseline_route": route, "duplicate_or_derivation": derivation,
                "conflict_pointer": pointers_for(unit, source), "approval_state": "not-approved",
                "approval_gap": approval_gap_for(route),
            })
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R12-A{index:04d}"
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows


def source_item_count(rows: list[dict[str, str]], source_id: str, section_pattern: str) -> int:
    locations = {
        row["exact_location"] for row in rows
        if row["source_record_id"] == source_id and re.search(section_pattern, row["section_path"], re.I)
    }
    return len(locations)


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    pointers = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer and pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_batch_documents_not_extracted": 48,
        "excluded_implementation_or_deviation_tickets": 31,
        "excluded_review_remediation_tickets": 17,
        "phase1_user_story_source_items": source_item_count(rows, "R12-17", r"User Stories"),
        "watch_confirmed_domain_semantic_source_items": source_item_count(rows, "R12-50", r"Confirmed Domain Semantics"),
        "watch_functional_requirement_source_items": source_item_count(rows, "R12-50", r"Functional Requirements"),
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
    if summary["source_documents"] != 2 or summary["excluded_batch_documents_not_extracted"] != 48:
        raise RuntimeError(f"R12 source coverage mismatch: {summary}")
    if summary["excluded_implementation_or_deviation_tickets"] != 31 or summary["excluded_review_remediation_tickets"] != 17:
        raise RuntimeError("R12 excluded ticket boundary mismatch")
    if summary["phase1_user_story_source_items"] != 50:
        raise RuntimeError(f"R12 Phase 1 story coverage mismatch: {summary['phase1_user_story_source_items']}")
    if summary["watch_confirmed_domain_semantic_source_items"] != 8:
        raise RuntimeError(f"R12 confirmed semantic coverage mismatch: {summary['watch_confirmed_domain_semantic_source_items']}")
    if summary["watch_functional_requirement_source_items"] < 50:
        raise RuntimeError("R12 Watch functional requirement coverage unexpectedly small")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R12 approval isolation failed")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R12 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R12-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R12 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R12 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R12 contains an unauthorized approval upgrade")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R12 approval gap is incomplete")
    for required_route in (
        "exclude-from-requirement-approval",
        "needs-business-owner-and-explicit-approval",
        "needs-domain-owner-and-explicit-approval-before-context-update",
        "needs-interface-owner-and-explicit-approval",
        "needs-product-owner-and-explicit-approval",
    ):
        if summary["by_route"].get(required_route, 0) <= 0:
            raise RuntimeError(f"Required R12 route missing: {required_route}")
    for required in POINTER_DEFINITIONS:
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R12 pointer missing: {required}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R12 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R12 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R12 summary JSON differs from a clean rebuild")


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
        "R12 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} "
        f"excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"phase1_stories={summary['phase1_user_story_source_items']} "
        f"watch_semantics={summary['watch_confirmed_domain_semantic_source_items']} "
        f"watch_fr_items={summary['watch_functional_requirement_source_items']} "
        f"exact_duplicate_rows={summary['exact_duplicate_rows']} approval_upgrades={summary['approval_upgrades']} "
        f"pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
