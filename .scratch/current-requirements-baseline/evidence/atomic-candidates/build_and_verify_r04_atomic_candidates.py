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
OUTPUT = Path(__file__).with_name("R04-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R04-atomic-candidates-summary.json")
EXPECTED_IDS = [f"R04-{index:02d}" for index in range(1, 32)]
FIELDS = common.FIELDS
NONE = "none-found-within-r04-pass"
APPROVAL_GAP = "authoritative-upstream-version;named-approver;approval-date;approved-scope;version-or-sha256-binding"
VERSION_REPLACED_IDS = {
    "R04-02", "R04-03", "R04-04", "R04-05", "R04-06", "R04-07", "R04-08",
    "R04-09", "R04-10", "R04-11", "R04-12", "R04-13", "R04-14", "R04-15",
    "R04-17", "R04-18", "R04-20", "R04-22",
}


def load_sources() -> list[common.Source]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["candidate_group_id"] == "R04"]
    ids = [row["record_id"] for row in rows]
    if ids != EXPECTED_IDS:
        raise RuntimeError(f"R04 source identity drift: expected={EXPECTED_IDS} actual={ids}")
    expected_class = "internal-derived-draft-functional-requirement-candidate"
    if any(row["document_class"] != expected_class for row in rows):
        raise RuntimeError("R04 source classification drift")
    return [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in rows
    ]


def frontmatter_traceability(path: Path) -> tuple[str, str, str, str]:
    text = path.read_text(encoding="utf-8-sig")
    block = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""

    def ids(field: str, prefix: str) -> str:
        match = re.search(rf"^{field}:\s*(.+)$", block, re.M)
        if not match:
            return "none"
        values = sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", match.group(1))))
        return ",".join(values) or "none"

    return ids("related_uc", "UC"), ids("related_br", "BR"), ids("related_fr", "FR"), ids("related_nfr", "NFR")


def section_contains(unit: common.Unit, pattern: str) -> bool:
    return bool(re.search(pattern, unit.section, re.I))


def is_unresolved(unit: common.Unit) -> bool:
    return bool(re.search(r"\bTBD\b|待确认|待建|尚待|待定|未明确|未最终确认|仍需确认|后续确认|另拆|可另拆", unit.statement, re.I))


def is_evidence(unit: common.Unit) -> bool:
    leaf = unit.section.rsplit(" > ", 1)[-1]
    return bool(re.match(r"^(?:Rationale|制定原因|Origin|需求来源|Related|关联|Verification|验证方式|Notes|备注)\b", leaf, re.I))


def evidence_class(unit: common.Unit) -> str:
    leaf = unit.section.rsplit(" > ", 1)[-1]
    if re.match(r"^(?:Origin|需求来源)\b", leaf, re.I):
        return "upstream-traceability-evidence"
    if re.match(r"^(?:Related|关联)\b", leaf, re.I):
        return "cross-document-traceability-evidence"
    if re.match(r"^(?:Verification|验证方式)\b", leaf, re.I):
        return "verification-pointer-evidence"
    if re.match(r"^(?:Rationale|制定原因)\b", leaf, re.I):
        return "internal-rationale-evidence"
    return "derivation-version-or-author-note-evidence"


def is_internal_implementation(unit: common.Unit) -> bool:
    text = f"{unit.section} {unit.statement}"
    return bool(re.search(
        r"\b(?:DTO|SQL|SELECT|HTTP|JSON|schema|repository|adapter|MessageId|revision|attemptNo)\b"
        r"|数据库表|表结构|代码实现|类名|方法名|接口路径|序列化|ORM|缓存键|消息队列|轮询实现|技术栈",
        text,
        re.I,
    ))


def functional_dimension(unit: common.Unit) -> str:
    text = unit.statement
    if re.search(r"权限|认证|角色|越权|授权|登录人|(?<!F)\bR-\d{2}\b", text):
        return "functional-permission-control-candidate"
    if re.search(r"联锁|急停|移动中|安全核验|光幕|锁 DI|危险|故障反馈", text, re.I):
        return "functional-safety-interlock-candidate"
    if re.search(r"状态|终态|迁移|进入|保持|恢复|关闭会话|结束本站", text):
        return "functional-state-transition-candidate"
    if re.search(r"原子|幂等|并发|竞态|回滚|不可修改|一次性|不复活", text):
        return "functional-atomicity-or-consistency-candidate"
    if re.search(r"错误|失败|异常|拒绝|阻断|告警|重试|超时", text):
        return "functional-error-handling-candidate"
    if re.search(r"界面|显示|提示|页面|HMI|倒计时|闪烁", text, re.I):
        return "functional-HMI-candidate"
    if re.search(r"审计|日志|追溯|记录.*(?:人|时间|原因)", text):
        return "functional-audit-candidate"
    if re.match(r"^\*\*Given\*\*", unit.statement, re.I):
        return "acceptance-precondition-candidate"
    if re.match(r"^\*\*When\*\*", unit.statement, re.I):
        return "acceptance-trigger-candidate"
    if re.match(r"^\*\*Then\*\*", unit.statement, re.I):
        return "acceptance-outcome-candidate"
    if section_contains(unit, r"Acceptance Criteria|验收标准"):
        return "acceptance-condition-candidate"
    return "derived-functional-behavior-candidate"


def classify(unit: common.Unit) -> tuple[str, str]:
    if is_evidence(unit):
        return evidence_class(unit), "evidence-only"
    if re.match(r"^\*\*AC-", unit.statement, re.I):
        return "acceptance-criterion-locator-evidence", "evidence-only"
    if is_unresolved(unit):
        return "unresolved-question", "needs-question-resolution"
    if is_internal_implementation(unit):
        return "embedded-internal-implementation-derivation", "exclude-from-requirement-approval"
    return functional_dimension(unit), "needs-upstream-source-and-explicit-approval"


def scope_for(source: common.Source, unit: common.Unit) -> str:
    if "/01-site-operations/" in source.path:
        return "8005-site-operation-and-stop-closure"
    if "/02-slot-and-hardware/" in source.path:
        return "8005-slot-hardware-and-IO"
    if "/03-agv-fleet-management/" in source.path:
        return "8005-AGV-fleet-and-slot-model"
    return "8005-project-cross-domain"


def conflict_pointer(source: common.Source, unit: common.Unit) -> str:
    text = unit.statement
    pointers: list[str] = []
    if re.search(r"(?:TASK_TYPE|任务类型).{0,30}SUBLOT|SUBLOT.{0,30}(?:TASK_TYPE|任务类型)|业务键|幂等键", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"MES.{0,40}(?:只读|回写|写操作)|(?:只读|回写|写操作).{0,40}MES", text, re.I):
        pointers.append("CF-R01-002")
    if re.search(r"AREA.{0,40}(?:映射|解析|派生|覆盖)|(?:映射|解析|派生|覆盖).{0,40}AREA|表 A|表 B", text, re.I):
        pointers.append("CF-R01-003")
    if re.search(r"五类|六类|WIRE_TO_NITROGEN", text, re.I):
        pointers.append("AD-R01-001")
    if source.record_id in VERSION_REPLACED_IDS and is_evidence(unit) and re.search(r"替代|旧|改写|保留编号|2026-07-3[01]|ADR", text, re.I):
        pointers.append("AD-R04-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


def approval_gap_for(candidate_class: str) -> str:
    parts = APPROVAL_GAP.split(";")
    if candidate_class == "unresolved-question":
        parts.insert(0, "question-resolution")
    if candidate_class == "embedded-internal-implementation-derivation":
        parts.extend(["authoritative-requirement-source", "independent-approval-unit-reframing"])
    return ";".join(dict.fromkeys(parts))


def build_rows() -> list[dict[str, str]]:
    sources = load_sources()
    source_by_id = {source.record_id: source for source in sources}
    traceability: dict[str, tuple[str, str, str, str]] = {}
    units: list[common.Unit] = []
    for source in sources:
        path = REPO / source.path
        actual = common.sha256_file(path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        traceability[source.record_id] = frontmatter_traceability(path)
        units.extend(common.markdown_units(source.record_id, path))

    rows: list[dict[str, str]] = []
    for index, unit in enumerate(units, start=1):
        source = source_by_id[unit.record_id]
        candidate_class, route = classify(unit)
        pointer = conflict_pointer(source, unit)
        if "CF-R01" in pointer and route not in {"evidence-only", "exclude-from-requirement-approval", "needs-question-resolution"}:
            route = "hold-for-conflict-decision"
        ucs, brs, frs, nfrs = traceability[source.record_id]
        derivation = (
            f"document-route:R04-C; upstream-uc:{ucs}; upstream-br:{brs}; "
            f"related-fr:{frs}; related-nfr:{nfrs}; {common.normalize(source.derivation)}"
        )
        if source.record_id in VERSION_REPLACED_IDS:
            derivation += "; version-scope:AD-R04-001"
        rows.append({
            "candidate_id": f"R04-A{index:04d}",
            "batch_id": "R04",
            "source_record_id": source.record_id,
            "source_path": source.path,
            "source_sha256": source.digest,
            "exact_location": unit.location,
            "section_path": unit.section,
            "statement_text": unit.statement,
            "source_context": unit.context,
            "statement_fingerprint": common.fingerprint(unit.statement),
            "candidate_class": candidate_class,
            "source_claim_status": "unapproved-internal-derived-functional-requirement",
            "applicable_scope": scope_for(source, unit),
            "baseline_route": route,
            "duplicate_or_derivation": derivation,
            "conflict_pointer": pointer,
            "approval_state": "not-approved",
            "approval_gap": approval_gap_for(candidate_class),
        })

    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fp = row["statement_fingerprint"]
        if counts[fp] > 1:
            first = first_by_fingerprint.setdefault(fp, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    conflicts = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "source_documents_by_class": {"R04-C": len({row["source_record_id"] for row in rows})},
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "conflict_pointers": dict(sorted(conflicts.items())),
        "version_scoped_sources": len(VERSION_REPLACED_IDS),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
    }


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary_for(rows), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_existing() -> list[dict[str, str]]:
    with OUTPUT.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify(rows: list[dict[str, str]]) -> dict[str, object]:
    errors: list[str] = []
    ids = [row.get("candidate_id", "") for row in rows]
    actual_sources = {row.get("source_record_id") for row in rows}
    if not rows:
        errors.append("candidate ledger is empty")
    if rows and list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if ids != [f"R04-A{index:04d}" for index in range(1, len(rows) + 1)]:
        errors.append("candidate_id sequence is not contiguous")
    if actual_sources != set(EXPECTED_IDS):
        errors.append("source coverage mismatch")
    if sum(bool(re.match(r"^\*\*AC-", row.get("statement_text", ""), re.I)) for row in rows) != 146:
        errors.append("acceptance-criterion locator count drift; expected 146")
    for row in rows:
        missing = [field for field in FIELDS if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != common.fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")
        if not re.search(r"upstream-uc:|upstream-br:", row.get("duplicate_or_derivation", "")):
            errors.append(f"missing upstream traceability: {row.get('candidate_id')}")
    if errors:
        raise RuntimeError("Verification failed:\n- " + "\n- ".join(errors[:30]))
    return {
        "total": len(rows),
        "sources": len(actual_sources),
        "source_counts": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "duplicates": len(ids) - len(set(ids)),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "conflict_rows": sum(row["conflict_pointer"] != NONE for row in rows),
        "errors": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        rows = read_existing()
        rebuilt = build_rows()
        if rows != rebuilt:
            limit = min(len(rows), len(rebuilt))
            first_difference = next((index for index in range(limit) if rows[index] != rebuilt[index]), limit)
            raise RuntimeError(
                f"Generated ledger drift: existing={len(rows)} rebuilt={len(rebuilt)} first_difference_index={first_difference}"
            )
    else:
        rows = build_rows()
        write_outputs(rows)
    print(json.dumps(verify(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
