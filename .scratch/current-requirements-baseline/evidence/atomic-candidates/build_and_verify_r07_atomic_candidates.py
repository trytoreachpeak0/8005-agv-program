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
OUTPUT = Path(__file__).with_name("R07-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R07-atomic-candidates-summary.json")
EXPECTED_SOURCE_IDS = ["R07-03", "R07-04"]
FIELDS = common.FIELDS
NONE = "none-found-within-r07-pass"
CORE_APPROVAL_GAP = [
    "authoritative-source",
    "named-approver",
    "approval-date",
    "approved-scope",
    "version-or-sha256-binding",
    "measurement-definition",
    "verification-evidence",
]


SPECS = [
    {
        "source_record_id": "R07-03",
        "nfr_id": "NFR-002",
        "fit_criterion": "FC-1",
        "quality_attribute": "auditability-completeness",
        "candidate_class": "audit-completeness-fit-criterion-candidate",
        "scope": "8005-critical-business-write-and-rejection-audit",
        "route": "needs-quality-security-it-policy-and-explicit-approval",
        "metric": "critical-event-audit-record-presence-and-minimum-field-set-completeness",
        "measurement": "frozen-event-catalog + business-result-to-audit-record-correspondence + field-completeness-assertion + UC-034-query-export-sampling",
        "source_basis": "internal-vision-traceability-target + unapproved-UC-034 + internal-no-audit-bypass-constraint",
        "inclusions": "critical-business-writes-and-critical-rejections-during-production-and-trial-run",
        "exclusions": "permanent-retention-of-debug-level-traces + external-MES-RCS-logs",
        "related_uc": "UC-001,UC-002,UC-005,UC-006,UC-010,UC-013,UC-014,UC-015,UC-016,UC-017,UC-018,UC-019,UC-020,UC-034,UC-038,UC-039,UC-043,UC-044",
        "related_fr": "FR-001..FR-009,FR-011..FR-014,FR-016..FR-028",
        "pointers": "SC-R07-001,Q-R07-001,EX-R07-001",
        "gap": [
            "customer-quality-security-it-policy",
            "frozen-critical-event-catalog",
            "approved-minimum-audit-field-set",
            "success-rejection-and-aggregation-correspondence-rule",
            "UC-034-authorized-query-export-scope",
            "FR-029-UC-021-audit-scope-resolution",
        ],
        "required_fragments": ["关键操作", "最低字段集", "静默成功/失败"],
    },
    {
        "source_record_id": "R07-03",
        "nfr_id": "NFR-002",
        "fit_criterion": "FC-2",
        "quality_attribute": "auditability-retention",
        "candidate_class": "audit-retention-fit-criterion-candidate",
        "scope": "8005-audit-record-query-export-retention",
        "route": "needs-quality-security-it-policy-and-explicit-approval",
        "metric": "minimum-queryable-and-exportable-retention-days-from-record-write",
        "measurement": "timestamped-sample-data + approved-retention-configuration + expiry-or-time-simulation + query-export-verification",
        "source_basis": "internal-vision-traceability-target + unapproved-UC-034 + internal-no-audit-bypass-constraint",
        "inclusions": "written-critical-operation-audit-records",
        "exclusions": "debug-level-trace-retention + external-MES-RCS-logs",
        "related_uc": "UC-034",
        "related_fr": "FR-001..FR-009,FR-011..FR-014,FR-016..FR-028",
        "pointers": "TBD-R07-001,EX-R07-001",
        "gap": [
            "customer-data-classification-and-retention-policy",
            "retention-clock-start-and-expiry-semantics",
            "archival-deletion-and-query-export-guarantee",
            "quality-security-it-owner",
            "approved-retention-days",
        ],
        "required_fragments": ["留存期", "180 天", "TBD"],
    },
    {
        "source_record_id": "R07-03",
        "nfr_id": "NFR-002",
        "fit_criterion": "FC-3",
        "quality_attribute": "auditability-query-visibility",
        "candidate_class": "audit-query-visibility-fit-criterion-candidate",
        "scope": "8005-authorized-audit-query-and-export",
        "route": "needs-quality-security-it-policy-and-explicit-approval",
        "metric": "elapsed-time-from-audit-record-write-to-authorized-query-visibility",
        "measurement": "record-write-timestamp-to-UC-034-authorized-query-visible-timestamp",
        "source_basis": "internal-vision-traceability-target + unapproved-UC-034 + internal-no-audit-bypass-constraint",
        "inclusions": "newly-written-critical-operation-audit-records-visible-to-authorized-users",
        "exclusions": "external-MES-RCS-logs + undefined-unauthorized-query-paths",
        "related_uc": "UC-034",
        "related_fr": "FR-001..FR-009,FR-011..FR-014,FR-016..FR-028",
        "pointers": "TBD-R07-001,EX-R07-001",
        "gap": [
            "customer-query-visibility-SLA",
            "write-commit-timestamp-definition",
            "query-visible-definition-and-consistency-scope",
            "UC-034-authorized-role-scope",
            "quality-security-it-owner",
            "approved-visibility-delay",
        ],
        "required_fragments": ["授权用户", "5 分钟", "TBD"],
    },
    {
        "source_record_id": "R07-04",
        "nfr_id": "NFR-001",
        "fit_criterion": "FC-1",
        "quality_attribute": "availability",
        "candidate_class": "service-availability-fit-criterion-candidate",
        "scope": "8005-business-service-during-agreed-production-shifts",
        "route": "needs-operations-it-sla-and-explicit-approval",
        "metric": "business-service-available-time-divided-by-agreed-production-shift-time",
        "measurement": "fixed-interval-health-readiness-sampling + core-interface-failure-timeout-5xx-logs + registered-maintenance-exclusion + shift-report",
        "source_basis": "internal-vision-stability-goal + internal-continuous-site-operation-analysis",
        "inclusions": "business-service-health-and-core-task-validation-slot-unlock-state-query-interfaces-during-agreed-shifts",
        "exclusions": "registered-planned-maintenance + external-MES-RCS-RIoT-AP-IO-AGV-originated-unavailability-subject-to-approved-attribution",
        "related_uc": "global-site-operation-representative-UC-not-frozen",
        "related_fr": "FR-001,FR-002-and-other-core-FR-not-enumerated",
        "pointers": "TBD-R07-002,SC-R07-002,EX-R07-001",
        "gap": [
            "customer-operations-it-SLA-source",
            "agreed-production-shift-calendar-and-time-boundaries",
            "available-state-core-interface-set-and-timeout-error-thresholds",
            "sampling-interval-and-outage-interval-merging-rule",
            "planned-maintenance-registration-rule",
            "external-dependency-root-cause-attribution-rule",
            "approved-availability-percentage",
        ],
        "required_fragments": ["可用性", "99.5%", "TBD"],
    },
    {
        "source_record_id": "R07-04",
        "nfr_id": "NFR-001",
        "fit_criterion": "FC-2",
        "quality_attribute": "recoverability-RTO",
        "candidate_class": "service-recovery-time-fit-criterion-candidate",
        "scope": "8005-business-service-unplanned-interruption-recovery",
        "route": "needs-operations-it-sla-and-explicit-approval",
        "metric": "elapsed-recovery-time-per-unplanned-business-service-interruption",
        "measurement": "incident-start-to-approved-restored-service-endpoint-using-operations-runbook-and-health-interface-logs",
        "source_basis": "internal-vision-stability-goal + internal-continuous-site-operation-analysis",
        "inclusions": "unplanned-business-service-interruption-restored-by-operations-runbook",
        "exclusions": "registered-planned-maintenance + external-MES-RCS-RIoT-AP-IO-AGV-originated-unavailability-subject-to-approved-attribution",
        "related_uc": "global-site-operation-representative-UC-not-frozen",
        "related_fr": "FR-001,FR-002-and-other-core-FR-not-enumerated",
        "pointers": "TBD-R07-002,SC-R07-002,EX-R07-001",
        "gap": [
            "customer-operations-it-SLA-source",
            "incident-start-and-restored-service-endpoint-definitions",
            "operations-runbook-version-and-owner",
            "partial-service-and-recurrence-treatment",
            "external-dependency-root-cause-attribution-rule",
            "approved-RTO",
        ],
        "required_fragments": ["非计划中断", "15 分钟", "TBD"],
    },
]


POINTER_DEFINITIONS = {
    "EX-R07-001": "5 个 FC 均无 related_tc、实际执行结果、构建/环境与附件哈希；建议测量法不是验证证据。",
    "Q-R07-001": "UC-021 正常流记录操作人/时间/原因是否足以把 FR-029 纳入关键审计目录存在未决范围歧义。",
    "SC-R07-001": "NFR-002 FC-1 的关键事件目录、最低字段集与 1:1/聚合对应规则未冻结。",
    "SC-R07-002": "NFR-001 将外部依赖不可用排除或分开统计，但未固定责任归因及部分降级口径。",
    "TBD-R07-001": "NFR-002 的 180 天留存和 5 分钟可见性是草稿阈值，待客户质量/IT/安全方批准。",
    "TBD-R07-002": "NFR-001 的 99.5% 可用性和 15 分钟 RTO 是草稿阈值，待客户运维/IT 批准。",
}


def normalize_markdown(value: str) -> str:
    value = re.sub(r"\*\*|__", "", value)
    return common.normalize(value)


def load_r07_ledger() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R07"]
    if len(batch_rows) != 15:
        raise RuntimeError(f"R07 batch boundary drift: expected=15 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R07"]
    if [row["record_id"] for row in candidate_rows] != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R07 candidate source drift: {[row['record_id'] for row in candidate_rows]}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 2, "excluded": 13}):
        raise RuntimeError("R07 route boundary drift; expected 2 candidate and 13 excluded documents")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows


def frontmatter_ids(text: str, field: str, prefix: str) -> str:
    block = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""
    match = re.search(rf"^{field}:\s*(.+)$", block, re.M)
    if not match:
        return "none"
    values = re.findall(rf"\b{prefix}-\d{{3}}\b", match.group(1))
    return ",".join(dict.fromkeys(values)) or "none"


def extract_fc_blocks(path: Path) -> tuple[str, dict[str, dict[str, str]]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    title = next((normalize_markdown(line[2:]) for line in lines if line.startswith("# ")), path.name)
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s*-\s+\*\*(FC-\d+)(?:（[^\uff09]+）)?\*\*\s*$", line)
        if match:
            starts.append((index, match.group(1)))
    blocks: dict[str, dict[str, str]] = {}
    for pos, (start, fc_id) in enumerate(starts):
        next_fc = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        end = next_fc
        for index in range(start + 1, next_fc):
            if lines[index].startswith("## "):
                end = index
                break
        parts: dict[str, str] = {}
        for line in lines[start + 1:end]:
            match = re.match(r"^\s*-\s+\*\*(Given|When|Then)\*\*\s*(.+)$", line)
            if match:
                parts[match.group(1)] = normalize_markdown(match.group(2))
        if set(parts) != {"Given", "When", "Then"}:
            raise RuntimeError(f"Incomplete GWT block in {path}: {fc_id} -> {parts}")
        blocks[fc_id] = {
            "location": f"lines {start + 1}-{end}",
            "statement": f"Given {parts['Given']}；When {parts['When']}；Then {parts['Then']}",
            "context": normalize_markdown(" ".join(lines[start:end])),
        }
    return title, blocks


def build_rows() -> list[dict[str, str]]:
    sources, _ = load_r07_ledger()
    source_by_id = {source.record_id: source for source in sources}
    extracted: dict[str, tuple[str, dict[str, dict[str, str]], str, str]] = {}
    for source in sources:
        path = REPO / source.path
        actual = common.sha256_file(path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        text = path.read_text(encoding="utf-8-sig")
        title, blocks = extract_fc_blocks(path)
        expected_fc_count = 3 if source.record_id == "R07-03" else 2
        if len(blocks) != expected_fc_count:
            raise RuntimeError(f"Fit criterion count drift: {source.record_id} expected={expected_fc_count} actual={len(blocks)}")
        extracted[source.record_id] = (
            title,
            blocks,
            frontmatter_ids(text, "related_uc", "UC"),
            frontmatter_ids(text, "related_fr", "FR"),
        )

    rows: list[dict[str, str]] = []
    for index, spec in enumerate(SPECS, start=1):
        source = source_by_id[spec["source_record_id"]]
        title, blocks, actual_ucs, actual_frs = extracted[source.record_id]
        block = blocks[spec["fit_criterion"]]
        combined = f"{block['statement']} {block['context']}"
        missing = [fragment for fragment in spec["required_fragments"] if fragment not in combined]
        if missing:
            raise RuntimeError(f"Required FC evidence drift: {source.record_id}/{spec['fit_criterion']} missing={missing}")
        derivation = (
            f"document-route:R07-candidate; nfr:{spec['nfr_id']}; fit-criterion:{spec['fit_criterion']}; "
            f"quality-attribute:{spec['quality_attribute']}; metric:{spec['metric']}; measurement:{spec['measurement']}; "
            f"source-basis:{spec['source_basis']}; inclusions:{spec['inclusions']}; exclusions:{spec['exclusions']}; "
            f"related-uc:{actual_ucs}; related-fr:{actual_frs}; related-tc:none; ledger-history:{common.normalize(source.derivation)}"
        )
        gap = ";".join(dict.fromkeys(spec["gap"] + CORE_APPROVAL_GAP))
        rows.append({
            "candidate_id": f"R07-A{index:04d}",
            "batch_id": "R07",
            "source_record_id": source.record_id,
            "source_path": source.path,
            "source_sha256": source.digest,
            "exact_location": block["location"],
            "section_path": f"{title} > Target / Fit Criterion > {spec['fit_criterion']}",
            "statement_text": block["statement"],
            "source_context": block["context"],
            "statement_fingerprint": common.fingerprint(block["statement"]),
            "candidate_class": spec["candidate_class"],
            "source_claim_status": "unapproved-internal-derived-nfr-draft",
            "applicable_scope": spec["scope"],
            "baseline_route": spec["route"],
            "duplicate_or_derivation": derivation,
            "conflict_pointer": spec["pointers"],
            "approval_state": "not-approved",
            "approval_gap": gap,
        })

    fingerprints = Counter(row["statement_fingerprint"] for row in rows)
    if any(count > 1 for count in fingerprints.values()):
        raise RuntimeError("Unexpected exact duplicate fit criteria within R07")
    return rows


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    pointer_counts = Counter(
        pointer
        for row in rows
        for pointer in row["conflict_pointer"].split(",")
        if pointer and pointer != NONE
    )
    nfr_counts = Counter(re.search(r"nfr:([^;]+)", row["duplicate_or_derivation"]).group(1) for row in rows)
    attribute_counts = Counter(re.search(r"quality-attribute:([^;]+)", row["duplicate_or_derivation"]).group(1) for row in rows)
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_documents_not_extracted": 13,
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_nfr": dict(sorted(nfr_counts.items())),
        "by_quality_attribute": dict(sorted(attribute_counts.items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "pointer_counts": dict(sorted(pointer_counts.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "exact_duplicate_rows": 0,
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "missing_related_tc_rows": sum("related-tc:none" in row["duplicate_or_derivation"] for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    expected_ids = [f"R07-A{index:04d}" for index in range(1, 6)]
    if [row["candidate_id"] for row in rows] != expected_ids:
        raise RuntimeError("R07 candidate ID sequence drift")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R07 field schema drift")
    if summary["total"] != 5 or summary["source_documents"] != 2:
        raise RuntimeError(f"R07 total/source mismatch: {summary}")
    if summary["by_source"] != {"R07-03": 3, "R07-04": 2}:
        raise RuntimeError(f"R07 source coverage mismatch: {summary['by_source']}")
    if summary["by_nfr"] != {"NFR-001": 2, "NFR-002": 3}:
        raise RuntimeError(f"R07 NFR coverage mismatch: {summary['by_nfr']}")
    if summary["approval_upgrades"] != 0 or summary["missing_related_tc_rows"] != 5:
        raise RuntimeError("R07 approval or verification isolation failed")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R07 approval upgrade detected")
    if any(re.search(r"\bREQ-\d{4}\b", row["candidate_id"]) for row in rows):
        raise RuntimeError("Permanent baseline requirement ID assigned prematurely")
    if any(not row["approval_gap"] or "version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R07 approval gap is incomplete")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R07 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R07 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R07 summary JSON differs from a clean rebuild")


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
        "R07 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} excluded_not_extracted={summary['excluded_documents_not_extracted']} "
        f"duplicates={summary['exact_duplicate_rows']} approval_upgrades={summary['approval_upgrades']} "
        f"missing_related_tc_rows={summary['missing_related_tc_rows']} pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
