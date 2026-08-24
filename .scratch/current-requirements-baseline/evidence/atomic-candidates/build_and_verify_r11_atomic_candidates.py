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
OUTPUT = Path(__file__).with_name("R11-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R11-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r11-pass"
EXPECTED_SOURCE_IDS = ["R11-03", "R11-04", "R11-05", "R11-07", "R11-09", "R11-11"]
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]

POINTER_DEFINITIONS = {
    "CF-R01-001": "TASK_TYPE + SUBLOT / TransportDemandKey 的跨批次业务键与冲突处置线索。",
    "CF-R01-002": "MES 只读边界与任何回写、DDL 或未登记 SQL 的跨批次线索。",
    "RES-R11-001": "“决定工厂 MES 验证的批准与完整性证据门槛”已固定：登记的只读查询可自行运行，但运行授权、run 观察和需求批准严格分离。",
    "BOUND-R11-001": "查询运行授权不赋予查询契约、业务筛选、容量、验收条件或性能阈值需求权威；这些仍须锁定来源版本、范围并逐项批准。",
    "EVID-R11-001": "2026-07-24 三份 run 只是在其时间、环境和 SQL 下的参考观察，不能形成正式验收、长期性能保证或需求批准。",
    "EVID-R11-002": "28 条 PACKAGE 容量只有迁移 CSV；原始客户表、逐行迁移对账、提供/批准人、厂区/产品/生效期和版本绑定仍缺失。",
    "SCOPE-R11-001": "活跃 MES 样本的 PACKAGE 覆盖不是产品全集；100 个未匹配聚合值和 TOLL- 字面前缀不得被近似推断或外推。",
    "GAP-R11-001": "OP_OPERATOR_IDENTITY 与 SUBLOT_BOX_COUNT 尚无各自独立的受控环境、查询版本绑定和脱敏 run 证据。",
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R11"]
    if len(batch_rows) != 11:
        raise RuntimeError(f"R11 batch boundary drift: expected=11 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R11"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R11 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 6, "excluded": 5}):
        raise RuntimeError("R11 route boundary drift; expected 6 candidate and 5 excluded documents")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows


def capacity_units(source: common.Source) -> list[common.Unit]:
    path = REPO / source.path
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"pattern", "match_type", "max_boxes_per_basket", "source", "status", "note"}
    if not rows or set(rows[0]) != required:
        raise RuntimeError("R11 capacity CSV schema drift")
    units: list[common.Unit] = []
    for index, row in enumerate(rows, start=2):
        context = " | ".join(f"{key}={common.normalize(value)}" for key, value in row.items())
        statement = (
            f"PACKAGE {row['pattern']} 使用 {row['match_type']} 字面匹配，"
            f"每花篮最多 {row['max_boxes_per_basket']} 盒，状态为 {row['status']}。"
        )
        units.append(common.Unit(
            source.record_id,
            f"CSV line {index}",
            "PACKAGE / 花篮容量迁移快照 > capacity rule",
            common.normalize(statement),
            context,
            "csv-capacity-rule-row",
        ))
    return units


def extract_units(source: common.Source) -> list[common.Unit]:
    path = REPO / source.path
    if path.suffix.lower() == ".csv":
        return capacity_units(source)
    return common.markdown_units(source.record_id, path)


def section_has(unit: common.Unit, pattern: str) -> bool:
    return bool(re.search(pattern, unit.section, re.I))


def classify_factory_checklist(unit: common.Unit) -> tuple[str, str]:
    text = unit.statement
    if re.search(r"不再要求客户批准文件|无需.*SHA-256|不必.*SHA-256|可选写入实验记录|可选.*experiment-record|可省略.*experiment-record|experiment-record.*可省略|省略时 manifest", text, re.I):
        return "superseded-factory-run-governance-claim", "historical-governance-evidence-only"
    if re.search(r"密码|凭据|连接字符串|mes-config\.ini|脱敏", text, re.I):
        return "factory-credential-or-sensitive-data-handling-candidate", "needs-security-owner-and-explicit-approval"
    if re.search(
        r"run-2026|673 行|672 行|平均 2\.91|最大 3\.50|少 1|difference.*0|软提醒|去重 PACKAGE 120|未匹配.*100|"
        r"对应 494 行|已导入三个 run|latest 来自|completed|硬失败：否",
        text,
        re.I,
    ):
        return "limited-factory-run-observation", "limited-environment-observation-evidence-only"
    if re.search(
        r"输出列恰为|逐项记录时间差|不并发|不重叠|平均不超过|最大不超过|超时或停止信号|立即停止|"
        r"保留三个独立|不能合并|重复导入被拒绝|不为近似字符串|不得按归并|活跃结果不能称全集|"
        r"不得.*继承容量|只匹配|回传|质量检查|客户六分支对比|性能测试",
        text,
        re.I,
    ):
        return "factory-acceptance-condition-candidate", "needs-acceptance-owner-and-explicit-approval"
    if re.search(r"运行结构检查|运行测试|构建.*bundle|安装依赖|进入.*目录|确认存在|复制为|使用 Python|mode=thick|Instant Client|命令|output-root|输出目录|拷|导入|查看|生成|刷新|对每个 run 分别执行", text, re.I):
        return "factory-run-procedure-or-local-tooling-design", "exclude-from-requirement-approval"
    if re.search(r"没有另一轮.*并发|每轮完成后才等待|实时变化与逻辑差异分开|日期解析口径告警不影响硬失败|每个目录含", text, re.I):
        return "factory-acceptance-condition-candidate", "needs-acceptance-owner-and-explicit-approval"
    if re.search(r"反馈客户补表", text, re.I):
        return "capacity-gap-governance-workflow-candidate", "needs-capacity-source-scope-and-explicit-approval"
    if re.search(r"TOLL-.*仅匹配", text, re.I):
        return "capacity-matching-and-fail-closed-behavior-candidate", "needs-loading-safety-owner-bound-data-source-and-explicit-approval"
    if re.search(r"本机不能连接 MES|用于验证|本清单|另行处理", text, re.I):
        return "factory-validation-scope-or-provenance-evidence", "source-or-traceability-evidence-only"
    return "factory-checklist-claim-needing-owner-classification", "needs-responsible-owner-and-explicit-approval"


def classify_query_readme(source: common.Source, unit: common.Unit) -> tuple[str, str]:
    text = unit.statement
    if re.search(r"正式 SQL 见.*query\.sql.*query\.toml", text, re.I):
        return "query-contract-location-and-versioning-evidence", "source-or-traceability-evidence-only"
    if section_has(unit, r"实验与证据关系"):
        if re.search(r"不得作为运行时依赖|不复制 SQL", text, re.I):
            return "query-source-governance-or-local-design", "exclude-from-requirement-approval"
        return "query-source-or-experiment-traceability-evidence", "source-or-traceability-evidence-only"

    if source.record_id == "R11-04":
        if re.search(r"UNION ALL|不得用 UNION|不上线时间过滤|应用层处理", text, re.I):
            return "derived-unified-query-design-decision", "exclude-from-requirement-approval"
        if re.search(r"幂等键|硬失败|阻断冲突键|其余继续", text, re.I):
            return "mes-data-quality-and-conflict-behavior-candidate", "needs-business-owner-bound-data-contract-and-explicit-approval"
        if re.search(r"参数|输出顺序|TASK_TYPE.*取值|六类|Oracle|只读", text, re.I):
            return "external-mes-unified-query-contract-candidate", "needs-bound-external-data-contract-and-explicit-approval"

    if source.record_id == "R11-05":
        if re.search(r"无结果|不得建立操作会话", text, re.I):
            return "operator-identity-session-behavior-candidate", "needs-identity-owner-bound-data-contract-and-explicit-approval"
        if re.search(r"不声明岗位权限|身份核验|操作会话|审计关联", text, re.I):
            return "operator-identity-versus-authorization-boundary-candidate", "needs-identity-and-security-owner-and-explicit-approval"
        if re.search(r"脱敏|绑定变量|只读执行", text, re.I):
            return "operator-query-security-and-privacy-boundary-candidate", "needs-security-owner-bound-data-contract-and-explicit-approval"
        if re.search(r"user_id|usercode|OPERATOR_NAME|username|参数|输出", text, re.I):
            return "external-operator-identity-data-contract-candidate", "needs-bound-external-data-contract-and-explicit-approval"

    if source.record_id == "R11-07":
        if re.search(r"ExpectedBasketCount|不取消已有运输任务|本次装载必须报错|不分配仓位|不发送开锁|不回退|冻结.*PACKAGE", text, re.I):
            return "capacity-and-loading-safety-behavior-candidate", "needs-loading-safety-owner-bound-data-source-and-explicit-approval"
        if re.search(r"不参与六类运输任务轮询", text, re.I):
            return "query-product-scope-boundary-candidate", "needs-product-owner-and-explicit-approval"
        if re.search(r"绑定变量|只读执行", text, re.I):
            return "box-count-query-safety-boundary-candidate", "needs-security-owner-bound-data-contract-and-explicit-approval"
        if re.search(r"sublot|fw_wip_box_his|MAX_BOX_COUNT|各工序|参数|输出", text, re.I):
            return "external-sublot-box-count-data-contract-candidate", "needs-bound-external-data-contract-and-explicit-approval"

    return "mixed-query-contract-or-product-claim", "needs-responsible-owner-bound-source-and-explicit-approval"


def classify_capacity_readme(unit: common.Unit) -> tuple[str, str]:
    text = unit.statement
    if section_has(unit, r"校验与生成视图") or re.search(r"命令|generate_package|Markdown 仅供审阅|不是规则源", text, re.I):
        return "capacity-rule-local-tooling-or-generated-view-design", "exclude-from-requirement-approval"
    if re.search(r"来自客户对照表|迁移快照|来源|旧 Markdown|唯一可执行规则源", text, re.I):
        return "capacity-source-provenance-or-governance-evidence", "source-or-traceability-evidence-only"
    if section_has(unit, r"字段"):
        return "capacity-reference-data-schema-candidate", "needs-capacity-source-scope-and-explicit-approval"
    if re.search(r"禁止模糊|未命中|不能推断|空值不匹配|精确匹配.*优先|最长前缀|TOLL-|区分大小写", text, re.I):
        return "capacity-matching-and-fail-closed-behavior-candidate", "needs-loading-safety-owner-bound-data-source-and-explicit-approval"
    return "capacity-reference-data-behavior-candidate", "needs-capacity-source-scope-and-explicit-approval"


def classify(source: common.Source, unit: common.Unit) -> tuple[str, str]:
    if source.record_id == "R11-03":
        return classify_factory_checklist(unit)
    if source.record_id in {"R11-04", "R11-05", "R11-07"}:
        return classify_query_readme(source, unit)
    if source.record_id == "R11-09":
        return "external-package-capacity-rule-candidate", "needs-capacity-source-scope-and-explicit-approval"
    if source.record_id == "R11-11":
        return classify_capacity_readme(unit)
    raise RuntimeError(f"Unhandled R11 source: {source.record_id}")


def scope_for(source: common.Source) -> str:
    return {
        "R11-03": "8005-factory-MES-readonly-run-and-limited-observation",
        "R11-04": "8005-MesIngest-six-task-unified-query-contract",
        "R11-05": "8005-operator-identity-resolution-only",
        "R11-07": "8005-Sublot-box-count-and-ExpectedBasketCount-loading-gate",
        "R11-09": "8005-PACKAGE-to-basket-capacity-migrated-data",
        "R11-11": "8005-PACKAGE-capacity-matching-and-rule-governance",
    }[source.record_id]


def source_status_for(source: common.Source) -> str:
    if source.record_id == "R11-03":
        return "mixed-unapproved-acceptance-plan-and-limited-run-summary;run-authorization-is-not-requirement-approval"
    if source.record_id == "R11-09":
        return "unapproved-migrated-customer-table-without-original-version-scope-or-row-reconciliation"
    return "unapproved-internal-derived-query-or-guidance-without-complete-approval-chain"


def pointers_for(source: common.Source, unit: common.Unit, candidate_class: str) -> str:
    text = f"{unit.section} {unit.statement}"
    pointers: list[str] = []
    if re.search(r"TASK_TYPE\s*\+\s*SUBLOT|幂等键|重复键|冲突键", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"只读|SELECT|DDL|DML|SQL", text, re.I):
        pointers.append("CF-R01-002")
    if source.record_id == "R11-03" or re.search(r"只读执行|实验|run|批准|SHA-256", text, re.I):
        pointers.extend(["RES-R11-001", "BOUND-R11-001"])
    if "limited-factory-run-observation" in candidate_class or re.search(r"run-2026|平均 2\.91|最大 3\.50|673 行|672 行", text, re.I):
        pointers.append("EVID-R11-001")
    if source.record_id in {"R11-09", "R11-11"}:
        pointers.append("EVID-R11-002")
    if re.search(r"未匹配|不能称全集|全量 PACKAGE|TOLL-|近似|模糊|相似", text, re.I):
        pointers.append("SCOPE-R11-001")
    if source.record_id in {"R11-05", "R11-07"}:
        pointers.append("GAP-R11-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


def approval_gap_for(candidate_class: str, route: str) -> str:
    if route.endswith("evidence-only"):
        gaps = ["evidence-only-not-an-approval-unit"]
    elif route == "exclude-from-requirement-approval":
        gaps = ["authoritative-requirement-source-if-behavior-is-required", "separate-query-or-tooling-design-review"]
    elif "acceptance-owner" in route:
        gaps = ["responsible-acceptance-owner", "approved-test-object-and-environment-scope", "acceptance-evidence-package"]
    elif "loading-safety-owner" in route:
        gaps = ["responsible-loading-and-safety-owner", "bound-MES-query-and-capacity-source", "failure-path-validation"]
    elif "identity" in route:
        gaps = ["responsible-identity-owner", "authorized-MES-data-owner", "identity-versus-role-authorization-boundary"]
    elif "security-owner" in route:
        gaps = ["responsible-security-owner", "bound-readonly-query-and-sensitive-data-handling-scope"]
    elif "external-data-contract" in route:
        gaps = ["authorized-MES-data-owner", "bound-Oracle-instance-schema-query-version-and-field-semantics"]
    elif "capacity-source" in route:
        gaps = ["original-customer-capacity-table", "row-by-row-migration-reconciliation", "site-product-effective-period"]
    elif "product-owner" in route:
        gaps = ["responsible-product-owner", "approved-product-scope-source"]
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
        units = extract_units(source)
        if not units:
            raise RuntimeError(f"No atomic units extracted from {source.record_id}")
        for unit in units:
            candidate_class, route = classify(source, unit)
            derivation = (
                f"document-route:R11-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                f"ledger-history:{common.normalize(source.derivation)}"
            )
            rows.append({
                "candidate_id": "", "batch_id": "R11", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest, "exact_location": unit.location,
                "section_path": unit.section, "statement_text": unit.statement, "source_context": unit.context,
                "statement_fingerprint": common.fingerprint(unit.statement), "candidate_class": candidate_class,
                "source_claim_status": source_status_for(source), "applicable_scope": scope_for(source),
                "baseline_route": route, "duplicate_or_derivation": derivation,
                "conflict_pointer": pointers_for(source, unit, candidate_class),
                "approval_state": "not-approved", "approval_gap": approval_gap_for(candidate_class, route),
            })
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R11-A{index:04d}"
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
    capacity_rows = [row for row in rows if row["source_record_id"] == "R11-09"]
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_batch_documents_not_extracted": 5,
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "pointer_counts": dict(sorted(pointers.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "capacity_rule_rows": len(capacity_rows),
        "capacity_exact_rules": sum(" 使用 exact " in row["statement_text"] for row in capacity_rows),
        "capacity_prefix_rules": sum(" 使用 prefix " in row["statement_text"] for row in capacity_rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "permanent_requirement_ids": sum(bool(re.search(r"\bREQ-\d{4}\b", row["candidate_id"])) for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if summary["source_documents"] != 6 or summary["excluded_batch_documents_not_extracted"] != 5:
        raise RuntimeError(f"R11 source coverage mismatch: {summary}")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R11 approval isolation failed")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R11 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R11-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R11 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R11 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R11 contains an unauthorized approval upgrade")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R11 approval gap is incomplete")
    if (summary["capacity_rule_rows"], summary["capacity_exact_rules"], summary["capacity_prefix_rules"]) != (28, 27, 1):
        raise RuntimeError("R11 capacity rule extraction drift")
    for route in (
        "exclude-from-requirement-approval",
        "limited-environment-observation-evidence-only",
        "needs-bound-external-data-contract-and-explicit-approval",
        "needs-capacity-source-scope-and-explicit-approval",
    ):
        if summary["by_route"].get(route, 0) <= 0:
            raise RuntimeError(f"Required R11 route missing: {route}")
    for required in POINTER_DEFINITIONS:
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R11 pointer missing: {required}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R11 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R11 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R11 summary JSON differs from a clean rebuild")


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
        "R11 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} "
        f"excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"capacity_rules={summary['capacity_rule_rows']} exact_duplicate_rows={summary['exact_duplicate_rows']} "
        f"approval_upgrades={summary['approval_upgrades']} pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
