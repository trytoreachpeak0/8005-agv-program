from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_and_verify_r03_atomic_candidates as common


REPO = common.REPO
SOURCE_LEDGER = common.SOURCE_LEDGER
OUTPUT = Path(__file__).with_name("R06-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R06-atomic-candidates-summary.json")
HISTORICAL_OUTPUT = Path(__file__).with_name("R06-drifted-historical-evidence.tsv")
FIELDS = common.FIELDS
NONE = "none-found-within-r06-pass"
APPROVAL_GAP = "authoritative-upstream-version;named-approver;approval-date;approved-scope;version-or-sha256-binding"
EXECUTION_GAP = "execution-build;execution-environment;executor;execution-time;actual-result;pass-fail;attachment-sha256"

EXPECTED_IDS = ["R06-01", "R06-02", *[f"R06-{index:02d}" for index in range(7, 57)]]
BLOCKED_IDS = [f"R06-{index:02d}" for index in range(3, 7)]
CURRENT_FR_RECORD_ID = "R04-17"
CURRENT_FR_ID = "FR-016"
CURRENT_FR_PATH = "requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-016-slot-enable-disable-batch-eligibility-and-state-update.md"
CURRENT_FR_SHA256 = "bd9df8d49efd21941ec36aade3976ca4a0e1ff58eb64cf2626a3796b8ca35920"
OLD_BINDING_COMMIT = "ecd0fd89c51c6602eda13f37b7c2e9fe181e5aad"
OLD_FR_BLOB = "c0cbfa4bfa3a61a9ace63315dbb4d757e0a8438f"
OLD_TC_BLOBS = {
    "R06-03": ("TC-044", "2ceef789d1341c3e6b21d98ae7da68e2eaacefc4", "R06-N001"),
    "R06-04": ("TC-045", "4beb9c1dc14c2ac6b12ca3491481b3d323b875c7", "R06-N002"),
    "R06-05": ("TC-046", "85f49edd3a7652b7fc8f039df5c0e757c8d63392", "R06-N003"),
    "R06-06": ("TC-047", "05e3f0e21c415cee601479dbe7b8b1c585b032a1", "R06-N004"),
}
NEW_CANDIDATE_LABELS = {
    "AC-1": "立即禁用",
    "AC-2": "待禁用",
    "AC-3": "启用不覆盖车载硬件不可操作",
    "AC-4": "批量独立结果",
}

HISTORICAL_FIELDS = [
    "source_record_id", "tc_id", "source_path", "current_sha256", "evidence_class",
    "bound_commit", "tc_blob", "old_fr_id", "old_fr_blob", "current_candidate_route",
    "new_candidate_id", "approval_state", "notes",
]


def read_ledger() -> list[dict[str, str]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_sources() -> list[common.Source]:
    rows = [row for row in read_ledger() if row["candidate_group_id"] == "R06"]
    ids = [row["record_id"] for row in rows]
    if ids != EXPECTED_IDS:
        raise RuntimeError(f"R06 source identity drift: expected={EXPECTED_IDS} actual={ids}")
    if Counter(row["document_class"] for row in rows) != Counter({"R06-A": 52}):
        raise RuntimeError("R06 source classification drift; expected 52 R06-A documents")
    return [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in rows
    ]


def load_current_fr_source() -> common.Source:
    matches = [row for row in read_ledger() if row["record_id"] == CURRENT_FR_RECORD_ID]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {CURRENT_FR_RECORD_ID} ledger row")
    row = matches[0]
    if row["path"] != CURRENT_FR_PATH or row["sha256"] != CURRENT_FR_SHA256:
        raise RuntimeError("Current FR-016 identity drift")
    return common.Source(
        row["record_id"], row["path"], row["sha256"], row["document_class"],
        row["source_type"], row["current_applicability"], row["history_or_derivation"],
    )


def frontmatter_traceability(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8-sig")
    block = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""

    def ids(field: str, prefix: str) -> str:
        match = re.search(rf"^{field}:\s*(.+)$", block, re.M)
        if not match:
            return "none"
        values = sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", match.group(1))))
        return ",".join(values) or "none"

    return ids("id", "TC"), ids("related_fr", "FR"), ids("related_uc", "UC")


def leaf_section(unit: common.Unit) -> str:
    return unit.section.rsplit(" > ", 1)[-1]


def scenario_role(unit: common.Unit) -> str:
    leaf = leaf_section(unit)
    if re.search(r"Preconditions|前置条件", leaf, re.I):
        return "precondition"
    if re.search(r"Test Steps|测试步骤", leaf, re.I):
        return "action"
    if re.search(r"Expected Result|预期结果", leaf, re.I):
        return "outcome"
    if re.search(r"Verifies|验证对象", leaf, re.I):
        return "verification"
    return "supporting-context"


def is_unresolved(unit: common.Unit) -> bool:
    return bool(re.search(r"\bTBD\b|待确认|待定|未明确|仍需确认|后续确认|尚未决定", unit.statement, re.I))


def candidate_class(source: common.Source, unit: common.Unit) -> str:
    role = scenario_role(unit)
    text = unit.statement
    if role == "verification":
        return "verification-traceability-evidence"
    if is_unresolved(unit):
        return "unresolved-acceptance-question"
    if re.search(r"二次认证|认证失败|认证通过|权限|身份|角色|授权|获准进入配置维护态", text, re.I):
        return "identity-security-acceptance-candidate"
    if re.search(
        r"安全|联锁|光幕|仓门|锁\s*DI|\bDI\b|\bDO\b|\bIO\b|硬件|故障|fail-closed|"
        r"不可操作|可操作性|弹开|闩合|通道|点位|遮挡|复位|无货|机构初始安全",
        text,
        re.I,
    ):
        return "safety-hardware-acceptance-candidate"
    if re.search(r"看板|界面|展示|显示|标注|提示|点击|差异|列表|页面|黄色|红色|过期", text, re.I):
        return "operator-HMI-acceptance-candidate"
    if re.search(r"\bRCS\b|\bRIOT\b|外部状态|同步|查询失败|指令下发|读取失败|映射", text, re.I):
        return "interface-integration-acceptance-candidate"
    if re.search(r"原子|事务|回滚|不可变|快照|审计记录|档案|自动转|状态机|可靠同步|对账", text, re.I):
        return "internal-state-or-architecture-derivation"
    if "/03-agv-fleet-management/" in source.path:
        return f"fleet-configuration-lifecycle-{role}-candidate"
    return f"business-acceptance-{role}-candidate"


def route_for(class_name: str) -> str:
    if class_name == "verification-traceability-evidence":
        return "evidence-only"
    if class_name == "unresolved-acceptance-question":
        return "needs-question-resolution"
    if class_name == "identity-security-acceptance-candidate":
        return "needs-security-role-owner-and-explicit-approval"
    if class_name == "safety-hardware-acceptance-candidate":
        return "needs-safety-hardware-authority-and-explicit-approval"
    if class_name == "operator-HMI-acceptance-candidate":
        return "needs-operator-product-owner-and-explicit-approval"
    if class_name == "interface-integration-acceptance-candidate":
        return "needs-interface-owner-source-and-explicit-approval"
    if class_name == "internal-state-or-architecture-derivation":
        return "exclude-from-requirement-approval"
    if class_name.startswith("fleet-configuration-lifecycle-"):
        return "needs-fleet-configuration-owner-and-explicit-approval"
    return "needs-upstream-source-and-explicit-approval"


def scope_for(source: common.Source, class_name: str) -> str:
    if class_name == "safety-hardware-acceptance-candidate":
        return "8005-slot-hardware-IO-safety-and-operability"
    if class_name == "operator-HMI-acceptance-candidate":
        return "8005-slot-and-fleet-operator-HMI"
    if class_name == "interface-integration-acceptance-candidate":
        return "8005-local-server-RIoT-RCS-integration"
    if class_name == "identity-security-acceptance-candidate":
        return "8005-fleet-maintenance-authorization-and-accountability"
    if class_name == "internal-state-or-architecture-derivation":
        return "8005-internal-slot-and-fleet-state-model"
    if "/03-agv-fleet-management/" in source.path:
        return "8005-AGV-fleet-and-local-configuration"
    return "8005-slot-management-and-hardware-acceptance"


def conflict_pointer(source: common.Source, unit: common.Unit) -> str:
    pointers: list[str] = []
    if scenario_role(unit) == "verification":
        pointers.append("EX-R06-001")
    if source.record_id in {"R06-41", "R06-42", "R06-43", "R06-44", "R06-45"}:
        pointers.append("SB-R06-001")
    return ",".join(pointers) or NONE


def approval_gap_for(class_name: str) -> str:
    parts = APPROVAL_GAP.split(";")
    additions = {
        "unresolved-acceptance-question": ["question-resolution"],
        "identity-security-acceptance-candidate": ["role-authorization-source", "security-or-business-owner"],
        "safety-hardware-acceptance-candidate": ["hardware-and-IO-version-binding", "safety-or-hardware-owner", "risk-review-evidence"],
        "operator-HMI-acceptance-candidate": ["operator-or-product-owner", "project-station-or-configuration-scope"],
        "internal-state-or-architecture-derivation": ["authoritative-requirement-source", "independent-approval-unit-reframing"],
        "interface-integration-acceptance-candidate": ["controlled-interface-version", "interface-owner"],
    }.get(class_name, [])
    if class_name.startswith("fleet-configuration-lifecycle-"):
        additions += ["fleet-configuration-owner", "model-or-vehicle-configuration-version"]
    return ";".join(dict.fromkeys(additions + parts + EXECUTION_GAP.split(";")))


def build_standard_rows() -> list[dict[str, str]]:
    sources = load_sources()
    source_by_id = {source.record_id: source for source in sources}
    traceability: dict[str, tuple[str, str, str]] = {}
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
        class_name = candidate_class(source, unit)
        tc, frs, ucs = traceability[source.record_id]
        derivation = (
            f"document-route:{source.document_class}; scenario:{tc}; scenario-role:{scenario_role(unit)}; "
            f"upstream-fr:{frs}; upstream-uc:{ucs}; formation-history:H3:ecd0fd8; {common.normalize(source.derivation)}"
        )
        rows.append({
            "candidate_id": f"R06-A{index:04d}",
            "batch_id": "R06",
            "source_record_id": source.record_id,
            "source_path": source.path,
            "source_sha256": source.digest,
            "exact_location": unit.location,
            "section_path": unit.section,
            "statement_text": unit.statement,
            "source_context": unit.context,
            "statement_fingerprint": common.fingerprint(unit.statement),
            "candidate_class": class_name,
            "source_claim_status": "unapproved-unexecuted-internal-derived-acceptance-draft",
            "applicable_scope": scope_for(source, class_name),
            "baseline_route": route_for(class_name),
            "duplicate_or_derivation": derivation,
            "conflict_pointer": conflict_pointer(source, unit),
            "approval_state": "not-approved",
            "approval_gap": approval_gap_for(class_name),
        })
    return rows


def build_new_identity_rows() -> list[dict[str, str]]:
    source = load_current_fr_source()
    path = REPO / source.path
    if common.sha256_file(path) != source.digest:
        raise RuntimeError("Current FR-016 hash drift")
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"\s*-\s*\*\*(AC-[1-4])（[^）]+）\*\*", line)
        if match:
            starts.append((index, match.group(1)))
    if [ac for _, ac in starts] != ["AC-1", "AC-2", "AC-3", "AC-4"]:
        raise RuntimeError(f"Current FR-016 AC identity drift: {starts}")

    rows: list[dict[str, str]] = []
    for offset, (start, ac_id) in enumerate(starts, start=1):
        end = starts[offset][0] if offset < len(starts) else next(
            (index for index in range(start + 1, len(lines)) if lines[index].startswith("## Notes")), len(lines)
        )
        context_lines = [common.normalize(re.sub(r"^\s*-\s*", "", line)) for line in lines[start:end] if line.strip()]
        context = " | ".join(context_lines)
        label = NEW_CANDIDATE_LABELS[ac_id]
        statement = f"{ac_id}（{label}） | " + " | ".join(context_lines[1:])
        rows.append({
            "candidate_id": f"R06-N{offset:03d}",
            "batch_id": "R06",
            "source_record_id": CURRENT_FR_RECORD_ID,
            "source_path": source.path,
            "source_sha256": source.digest,
            "exact_location": f"lines {start + 1}-{end}",
            "section_path": f"{CURRENT_FR_ID} > Acceptance Criteria > {ac_id} {label}",
            "statement_text": statement,
            "source_context": context,
            "statement_fingerprint": common.fingerprint(statement),
            "candidate_class": "current-fr016-new-identity-acceptance-candidate",
            "source_claim_status": "unapproved-current-fr016-acceptance-candidate-new-identity",
            "applicable_scope": "8005-slot-management-and-hardware-operability",
            "baseline_route": "needs-upstream-source-and-explicit-approval",
            "duplicate_or_derivation": (
                f"new-identity:{label}; decision-ticket:40; replaces-no-old-tc; "
                f"old-tc-history-only:TC-{43 + offset:03d}@{OLD_BINDING_COMMIT}; "
                f"upstream-fr:{CURRENT_FR_ID}; upstream-uc:UC-014; source-ledger:{CURRENT_FR_RECORD_ID}"
            ),
            "conflict_pointer": "AD-R06-001",
            "approval_state": "not-approved",
            "approval_gap": approval_gap_for("current-fr016-new-identity-acceptance-candidate"),
        })
    return rows


def mark_exact_duplicates(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"


def build_rows() -> list[dict[str, str]]:
    rows = build_standard_rows() + build_new_identity_rows()
    mark_exact_duplicates(rows)
    return rows


def build_historical_rows() -> list[dict[str, str]]:
    ledger_by_id = {row["record_id"]: row for row in read_ledger()}
    rows: list[dict[str, str]] = []
    for record_id in BLOCKED_IDS:
        row = ledger_by_id.get(record_id)
        if not row or row["route_class"] != "blocked":
            raise RuntimeError(f"Missing blocked historical evidence row: {record_id}")
        path = REPO / row["path"]
        if common.sha256_file(path) != row["sha256"]:
            raise RuntimeError(f"Historical source hash drift: {record_id}")
        tc_id, tc_blob, new_id = OLD_TC_BLOBS[record_id]
        rows.append({
            "source_record_id": record_id,
            "tc_id": tc_id,
            "source_path": row["path"],
            "current_sha256": row["sha256"],
            "evidence_class": "unapproved-historical-acceptance-draft",
            "bound_commit": OLD_BINDING_COMMIT,
            "tc_blob": tc_blob,
            "old_fr_id": CURRENT_FR_ID,
            "old_fr_blob": OLD_FR_BLOB,
            "current_candidate_route": "excluded-from-current-candidate",
            "new_candidate_id": new_id,
            "approval_state": "not-approved",
            "notes": "identity-and-content-preserved; bound-to-old-FR-016; not-rewritten; not-current-candidate",
        })
    return rows


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    standard = [row for row in rows if row["candidate_id"].startswith("R06-A")]
    new = [row for row in rows if row["candidate_id"].startswith("R06-N")]
    pointers = Counter(pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer != NONE)
    return {
        "total": len(rows),
        "scenario_atomic_rows": len(standard),
        "new_identity_candidates": len(new),
        "scenario_source_documents": len({row["source_record_id"] for row in standard}),
        "cross_batch_current_sources": len({row["source_record_id"] for row in new}),
        "historical_drifted_documents": len(BLOCKED_IDS),
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "by_scenario_role": dict(sorted(Counter(
            re.search(r"scenario-role:([^;]+)", row["duplicate_or_derivation"]).group(1)
            for row in standard
        ).items())),
        "evidence_and_scope_pointers": dict(sorted(pointers.items())),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
    }


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary_for(rows), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with HISTORICAL_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HISTORICAL_FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(build_historical_rows())


def read_existing() -> list[dict[str, str]]:
    with OUTPUT.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_historical_existing() -> list[dict[str, str]]:
    with HISTORICAL_OUTPUT.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify(rows: list[dict[str, str]]) -> dict[str, object]:
    errors: list[str] = []
    ids = [row.get("candidate_id", "") for row in rows]
    standard = [row for row in rows if row.get("candidate_id", "").startswith("R06-A")]
    new = [row for row in rows if row.get("candidate_id", "").startswith("R06-N")]
    standard_ids = [row["candidate_id"] for row in standard]
    role_coverage: dict[str, set[str]] = defaultdict(set)
    for row in standard:
        match = re.search(r"scenario-role:([^;]+)", row.get("duplicate_or_derivation", ""))
        if match:
            role_coverage[row.get("source_record_id", "")].add(match.group(1))
    if not rows:
        errors.append("candidate ledger is empty")
    if rows and list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if standard_ids != [f"R06-A{index:04d}" for index in range(1, len(standard) + 1)]:
        errors.append("standard candidate_id sequence is not contiguous")
    if [row["candidate_id"] for row in new] != [f"R06-N{index:03d}" for index in range(1, 5)]:
        errors.append("new identity candidate sequence mismatch")
    if {row["source_record_id"] for row in standard} != set(EXPECTED_IDS):
        errors.append("scenario source coverage mismatch")
    required_roles = {"precondition", "action", "outcome", "verification"}
    for source_id in EXPECTED_IDS:
        if not required_roles.issubset(role_coverage[source_id]):
            errors.append(f"scenario section coverage mismatch: {source_id} has {sorted(role_coverage[source_id])}")
    if {NEW_CANDIDATE_LABELS[f"AC-{index}"] for index in range(1, 5)} != {
        re.search(r"new-identity:([^;]+)", row["duplicate_or_derivation"]).group(1) for row in new
    }:
        errors.append("new FR-016 acceptance semantics mismatch")
    for row in rows:
        missing = [field for field in FIELDS if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != common.fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")
        if "upstream-fr:" not in row.get("duplicate_or_derivation", ""):
            errors.append(f"missing upstream FR traceability: {row.get('candidate_id')}")
        if not row["candidate_id"].startswith("R06-N") and not all(part in row.get("approval_gap", "") for part in EXECUTION_GAP.split(";")):
            errors.append(f"missing execution evidence gap: {row.get('candidate_id')}")
    historical = build_historical_rows()
    if read_historical_existing() != historical:
        errors.append("historical evidence ledger drift")
    if errors:
        raise RuntimeError("Verification failed:\n- " + "\n- ".join(errors[:50]))
    return {
        "total": len(rows),
        "scenario_rows": len(standard),
        "new_identity_candidates": len(new),
        "sources": len({row["source_record_id"] for row in standard}),
        "historical_sources": len(historical),
        "source_counts": dict(sorted(Counter(row["source_record_id"] for row in standard).items())),
        "duplicates": len(ids) - len(set(ids)),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "evidence_or_scope_rows": sum(row["conflict_pointer"] != NONE for row in rows),
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
