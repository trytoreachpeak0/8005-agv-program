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
OUTPUT = Path(__file__).with_name("R05-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R05-atomic-candidates-summary.json")
EXPECTED_IDS = [f"R05-{index:02d}" for index in range(1, 68)]
FIELDS = common.FIELDS
NONE = "none-found-within-r05-pass"
APPROVAL_GAP = "authoritative-upstream-version;named-approver;approval-date;approved-scope;version-or-sha256-binding"

NAME_DRIFT_IDS = {
    "R05-01", "R05-02", "R05-11", "R05-13", "R05-21", "R05-30",
    "R05-33", "R05-34", "R05-35", "R05-36", "R05-37",
}


def load_sources() -> list[common.Source]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["candidate_group_id"] == "R05"]
    ids = [row["record_id"] for row in rows]
    if ids != EXPECTED_IDS:
        raise RuntimeError(f"R05 source identity drift: expected={EXPECTED_IDS} actual={ids}")
    classes = Counter(row["document_class"] for row in rows)
    if classes != Counter({"R05-C1": 38, "R05-C2": 29}):
        raise RuntimeError(f"R05 source classification drift: {dict(classes)}")
    return [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in rows
    ]


def frontmatter_traceability(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8-sig")
    block = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""

    def ids(field: str, prefix: str) -> str:
        match = re.search(rf"^{field}:\s*(.+)$", block, re.M)
        if not match:
            return "none"
        values = sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", match.group(1))))
        return ",".join(values) or "none"

    tc = ids("id", "TC")
    return tc, ids("related_fr", "FR"), ids("related_uc", "UC")


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


def candidate_class(unit: common.Unit) -> str:
    role = scenario_role(unit)
    text = unit.statement
    if role == "verification":
        return "verification-traceability-evidence"
    if is_unresolved(unit):
        return "unresolved-acceptance-question"
    if re.search(r"工号|身份|岗位|角色|权限|越权|认证|刷卡|登录|信息安全|\bR-\d{2}\b|原因码", text, re.I):
        return "identity-security-acceptance-candidate"
    if re.search(
        r"安全|联锁|DepartureSafe|StationOperationGuard|锁\s*DI|光幕|\bIO\b|硬件|故障|UNKNOWN|"
        r"弹簧|弹门|Modbus|0x0F|反馈无效|输出复位|仓门.*(?:锁闭|未锁)|移动中",
        text,
        re.I,
    ):
        return "safety-hardware-acceptance-candidate"
    if re.search(r"界面|显示|黄色|红色|闪烁|声音|入口|面板|页面|按钮|点击|提示|倒计时", text, re.I):
        return "operator-HMI-acceptance-candidate"
    if re.search(
        r"原子|持久化|事务|幂等|竞态|串行|并发|回滚|冻结|截止时间|投影|预留|不复活|"
        r"ProvisionalLoadState|MessageId|SlotOperationAttemptId|LoadCompensationDecision|"
        r"LoadCompensationRequired|VehicleRecoveryRequired|LoadCompensationRecovery|StopClosureCommit|"
        r"StationDepartureWaiting|OperationSession|CurrentStopWorklist",
        text,
        re.I,
    ):
        return "internal-state-or-architecture-derivation"
    if re.search(r"\bMES\b|服务端|车载端|上报|下发|响应|断联|重连|接口|调用|授权后", text, re.I):
        return "interface-integration-acceptance-candidate"
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
    if class_name == "internal-state-or-architecture-derivation":
        return "exclude-from-requirement-approval"
    if class_name == "interface-integration-acceptance-candidate":
        return "needs-interface-owner-source-and-explicit-approval"
    return "needs-upstream-source-and-explicit-approval"


def scope_for(class_name: str) -> str:
    return {
        "identity-security-acceptance-candidate": "8005-identity-role-and-session",
        "safety-hardware-acceptance-candidate": "8005-site-safety-slot-hardware-and-recovery",
        "operator-HMI-acceptance-candidate": "8005-onboard-HMI-and-site-operation",
        "internal-state-or-architecture-derivation": "8005-internal-site-operation-state-model",
        "interface-integration-acceptance-candidate": "8005-onboard-server-MES-interface",
    }.get(class_name, "8005-site-operation-and-stop-closure")


def conflict_pointer(source: common.Source, unit: common.Unit) -> str:
    text = unit.statement
    pointers: list[str] = []
    if re.search(r"(?:TASK_TYPE|任务类型).{0,40}SUBLOT|SUBLOT.{0,40}(?:TASK_TYPE|任务类型)|TransportDemandKey|业务键|取消抑制", text, re.I):
        pointers.append("CF-R01-001")
    if source.record_id in NAME_DRIFT_IDS:
        pointers.append("TQ-R05-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


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
    return ";".join(dict.fromkeys(additions + parts))


def build_rows() -> list[dict[str, str]]:
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
        class_name = candidate_class(unit)
        route = route_for(class_name)
        pointer = conflict_pointer(source, unit)
        if "CF-R01" in pointer and route not in {"evidence-only", "exclude-from-requirement-approval", "needs-question-resolution"}:
            route = "hold-for-conflict-decision"
        tc, frs, ucs = traceability[source.record_id]
        history = "H1:ecd0fd8-to-493ac5a" if " / H1" in source.derivation else ("H2:493ac5a" if " / H2" in source.derivation else "H3:ecd0fd8")
        derivation = (
            f"document-route:{source.document_class}; scenario:{tc}; scenario-role:{scenario_role(unit)}; "
            f"upstream-fr:{frs}; upstream-uc:{ucs}; formation-history:{history}; {common.normalize(source.derivation)}"
        )
        rows.append({
            "candidate_id": f"R05-A{index:04d}",
            "batch_id": "R05",
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
            "applicable_scope": scope_for(class_name),
            "baseline_route": route,
            "duplicate_or_derivation": derivation,
            "conflict_pointer": pointer,
            "approval_state": "not-approved",
            "approval_gap": approval_gap_for(class_name),
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
    source_classes = {source.record_id: source.document_class for source in load_sources()}
    conflicts = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "source_documents_by_class": dict(sorted(Counter(source_classes.values()).items())),
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "by_scenario_role": dict(sorted(Counter(re.search(r"scenario-role:([^;]+)", row["duplicate_or_derivation"]).group(1) for row in rows).items())),
        "conflict_and_traceability_pointers": dict(sorted(conflicts.items())),
        "name_drift_sources": len(NAME_DRIFT_IDS),
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
    role_coverage: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        match = re.search(r"scenario-role:([^;]+)", row.get("duplicate_or_derivation", ""))
        if match:
            role_coverage[row.get("source_record_id", "")].add(match.group(1))
    if not rows:
        errors.append("candidate ledger is empty")
    if rows and list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if ids != [f"R05-A{index:04d}" for index in range(1, len(rows) + 1)]:
        errors.append("candidate_id sequence is not contiguous")
    if actual_sources != set(EXPECTED_IDS):
        errors.append("source coverage mismatch")
    required_roles = {"precondition", "action", "outcome", "verification"}
    for source_id in EXPECTED_IDS:
        if not required_roles.issubset(role_coverage[source_id]):
            errors.append(f"scenario section coverage mismatch: {source_id} has {sorted(role_coverage[source_id])}")
    for row in rows:
        missing = [field for field in FIELDS if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != common.fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")
        if "upstream-fr:" not in row.get("duplicate_or_derivation", ""):
            errors.append(f"missing upstream traceability: {row.get('candidate_id')}")
    if errors:
        raise RuntimeError("Verification failed:\n- " + "\n- ".join(errors[:40]))
    return {
        "total": len(rows),
        "sources": len(actual_sources),
        "source_counts": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "duplicates": len(ids) - len(set(ids)),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "conflict_or_traceability_rows": sum(row["conflict_pointer"] != NONE for row in rows),
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
