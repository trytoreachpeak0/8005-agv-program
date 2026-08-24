from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
OUTPUT = Path(__file__).with_name("R02-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R02-atomic-candidates-summary.json")

FIELDS = [
    "candidate_id",
    "batch_id",
    "source_record_id",
    "source_path",
    "source_sha256",
    "exact_location",
    "section_path",
    "statement_text",
    "source_context",
    "statement_fingerprint",
    "candidate_class",
    "source_claim_status",
    "applicable_scope",
    "baseline_route",
    "duplicate_or_derivation",
    "conflict_pointer",
    "approval_state",
    "approval_gap",
]

SOURCES = [
    ("R02-07", "requirement-documents/00-vision/system-context.md", "60e2206dc80d105c92db91f519b4ffb7df50cadcca9340eb9481bb3777aeee65"),
    ("R02-08", "requirement-documents/00-vision/vision-and-scope.md", "c5dbdd400b9952e886ab2ef3e12f1ddcfafb7fb90175e9e366973d82f6912070"),
    ("R02-09", "requirement-documents/01-stakeholders/stakeholders-and-user-classes.md", "f8d5f0ca428fa84e6f21f6d3a43d375577b6fe3d567316f3ea9221c880894f74"),
    ("R02-10", "requirement-documents/02-business-rules/br-001-dispatch-task-range.md", "e90caa36f48029ea6c6f7f5129c6a11f898833154fd82daaa44ec3154e1ceb8b"),
    ("R02-11", "requirement-documents/02-business-rules/br-002-agv-allocation-eligibility.md", "dd3acb8484ed4d26397e43671c7f5c2af1e3cee32657ebeab0deaba861aa3045"),
    ("R02-12", "requirement-documents/02-business-rules/br-003-area-station-mapping.md", "7b25e92d5e6617801e0b477479bcfe8c4371d6806049aa00e7ceca0c09b4b70e"),
    ("R02-13", "requirement-documents/02-business-rules/br-004-workflow-template-matching.md", "e10d2a634aded29032d0ab939a9b48f7baadb338ea7adca9bc412f9f50220a2b"),
    ("R02-14", "requirement-documents/02-business-rules/br-005-workflow-template-versioning.md", "798aad13791f06d7db6e7a1043b4c3439817311bd15ade6e152a872adcc22e53"),
    ("R02-15", "requirement-documents/02-business-rules/br-006-workflow-step-execution.md", "0ff765a61ad43e3ad9b30fdcf43b7c1c3c8999837c7bc7213a7dd45cda22c7a4"),
    ("R02-16", "requirement-documents/02-business-rules/br-007-charging-pile-allocation-and-queueing.md", "a5cef3093c15f6e7f1040aa8b46fa4899659e97c30fb0818c7d064d58a94bed7"),
    ("R02-17", "requirement-documents/02-business-rules/br-008-agv-slot-model-versioning.md", "5f8911ad0f36732819a9cfeb6a64103e170d2a6b03cf4f15eb7e852b3fecad0b"),
    ("R02-18", "requirement-documents/02-business-rules/br-009-parking-point-allocation-and-queueing.md", "bc212f95287faec261b05a3ee5e8c9468e009fedfb6ec24840863df52e371c5a"),
    ("R02-19", "requirement-documents/02-business-rules/br-010-default-administrator-account.md", "9843f98e918e6fba1eb35c064596f9d01815e23b21e582183dbb9a239482d0c3"),
    ("R02-20", "requirement-documents/02-business-rules/br-011-account-and-password-format.md", "e5a2ae6c041daa436a26edfbf8987982495d4e510c55c656aeef75d29911c394"),
    ("R02-21", "requirement-documents/02-business-rules/br-012-mes-task-idempotency-and-reconciliation.md", "d8f77fc533fd7e3bbf4b86a6800f7fe0b410d58f42a7a354ed41c14b0d289260"),
    ("R02-22", "requirement-documents/02-business-rules/br-013-multi-basket-loading.md", "ac51b3a50f7b1740bf7f51c2f6d0d7a9e299037d724bed8e7931a75e89b82bef"),
    ("R02-23", "requirement-documents/02-business-rules/br-014-transport-task-types-and-fixed-stations.md", "98cd58e70e4a3f97d333b8cd5b29278363c6105ee8de10b63b4ba90f48c7090e"),
    ("R02-24", "requirement-documents/02-business-rules/br-015-path-cost-and-dispatch-ranking.md", "5b6708cec8474a45735292a7e028ee341f00d4840bb8256a57c1e44ab0cad1dd"),
    ("R02-26", "requirement-documents/02-business-rules/workflow-step-catalog.md", "c62f70569c041c9c22101dced98b85e792fef9a343252537a43f2ae56332bb85"),
]

SOURCE_BY_ID = {record_id: (path, digest) for record_id, path, digest in SOURCES}
APPROVAL_GAP = "named-approver;approval-date;approved-scope;version-or-sha256-binding"

DERIVATION = {
    "R02-07": "unknown-source-internal-boundary-synthesis; references:R02-09,R02-12,R02-13,R02-14,R02-15,R02-24,R02-26",
    "R02-08": "unknown-source-mixed-vision-draft; references:R02-07,R02-09",
    "R02-09": "internal-role-and-permission-synthesis; derived-from:vision-and-scope,early-scenario-drafts,and-later-UC-BR-materials",
    "R02-10": "partially-derived-from-unapproved-MES-model; earlier-customer-interview-attribution-has-no-source-record",
    "R02-11": "unknown-source-internal-rule-synthesis; ranking-derived-from:R02-23,R02-24",
    "R02-12": "unknown-source-internal-model; self-asserted-confirmation-summary-without-record; conflicts-with:R01-CF-R01-003",
    "R02-13": "unknown-source-internal-workflow-model; self-asserted-confirmation-summary-without-record",
    "R02-14": "unknown-source-internal-workflow-version-model; self-asserted-confirmation-summary-without-record",
    "R02-15": "unknown-source-internal-workflow-execution-model; formed-with:R02-26",
    "R02-16": "unknown-source-internal-queueing-model; self-asserted-confirmation-summary-without-record",
    "R02-17": "mixed-user-attribution-and-simulator-design-analogy; versioning-derived-from:R02-14",
    "R02-18": "unknown-source-analogy-derived-rule; queueing-model-derived-from:R02-16",
    "R02-19": "user-clarification-summary-without-original-dialogue-or-authority-binding",
    "R02-20": "mixed-self-asserted-user-summary-and-requirements-engineering-baseline; must-not-be-approved-as-one-document",
    "R02-21": "derived-from-unapproved-internal-MES-model:R01-05; performance-observation-is-not-requirement-approval",
    "R02-22": "derived-from-unapproved-internal-MES-model:R01-05",
    "R02-23": "derived-from-unapproved-internal-MES-model:R01-05-and-interface-summary:R01-04",
    "R02-24": "unknown-source-internal-dispatch-ranking-model; RIOT-map-version-not-bound",
    "R02-26": "internal-derived-step-specification; catalog-version-stale-relative-to-content-changes; no-release-or-safety-review-binding",
}


@dataclass
class Unit:
    record_id: str
    location: str
    section: str
    statement: str
    context: str
    kind: str


def normalize(value: str) -> str:
    return " ".join(value.replace("\u00a0", " ").replace("\t", " ").split()).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(statement: str) -> str:
    cleaned = re.sub(r"[`*_#>\[\]()]", "", normalize(statement)).casefold()
    cleaned = re.sub(r"\s+", "", cleaned)
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()


def split_table(line: str) -> list[str]:
    value = line.strip().strip("|")
    return [normalize(cell.replace("\\|", "|")) for cell in re.split(r"(?<!\\)\|", value)]


def is_table_separator(line: str) -> bool:
    cells = split_table(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_atomic(value: str) -> list[str]:
    value = normalize(value)
    if not value:
        return []
    parts = re.split(r"(?<=[。！？；])(?=[^）])", value)
    return [normalize(part) for part in parts if len(normalize(part)) >= 2] or [value]


def identity_prefix(headers: list[str], cells: list[str]) -> str:
    identity_headers = {"编号", "角色名称", "代码", "步骤类型", "项目维度"}
    parts = [f"{header}={cells[index]}" for index, header in enumerate(headers) if index < len(cells) and header in identity_headers and cells[index]]
    return " | ".join(parts)


def markdown_units(record_id: str, path: Path) -> list[Unit]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    headings: list[tuple[int, str]] = []
    units: list[Unit] = []
    in_code = False
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    index = 1 if in_frontmatter else 0

    def section_path() -> str:
        return " > ".join(title for _, title in headings) or "document-root"

    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        line_no = index + 1
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            index += 1
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            index += 1
            continue
        if in_code or not stripped or stripped == "---" or stripped.startswith("<!--"):
            index += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = normalize(heading_match.group(2))
            headings = [entry for entry in headings if entry[0] < level]
            headings.append((level, title))
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            headers = split_table(stripped)
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = split_table(lines[index])
                context = " | ".join(f"{headers[pos] if pos < len(headers) else f'col{pos + 1}'}={cell}" for pos, cell in enumerate(cells) if cell)
                prefix = identity_prefix(headers, cells)
                for pos, cell in enumerate(cells):
                    header = headers[pos] if pos < len(headers) else f"col{pos + 1}"
                    if not cell or header in {"编号", "角色名称", "代码", "步骤类型", "项目维度"}:
                        continue
                    statement = f"{prefix} | {header}={cell}" if prefix else f"{header}={cell}"
                    units.append(Unit(record_id, f"line {index + 1}", section_path(), statement, context, "markdown-table-cell"))
                index += 1
            continue

        list_match = re.match(r"^\s*(?:[-*+]\s+|\d+[.)、]\s*)(.+)$", raw)
        if list_match:
            context = normalize(list_match.group(1))
            for atom in split_atomic(context):
                units.append(Unit(record_id, f"line {line_no}", section_path(), atom, context, "markdown-list-item"))
            index += 1
            continue

        start = index
        paragraph = [stripped.lstrip("> ")]
        index += 1
        while index < len(lines):
            follow = lines[index].strip()
            if not follow or follow.startswith("#") or follow.startswith("|") or follow.startswith("```") or follow == "---":
                break
            if re.match(r"^\s*(?:[-*+]\s+|\d+[.)、]\s+)", lines[index]):
                break
            paragraph.append(follow.lstrip("> "))
            index += 1
        context = normalize(" ".join(paragraph))
        end = index if index > start + 1 else start + 1
        location = f"lines {start + 1}-{end}" if end > start + 1 else f"line {start + 1}"
        for atom in split_atomic(context):
            units.append(Unit(record_id, location, section_path(), atom, context, "markdown-paragraph"))
    return units


def section_contains(unit: Unit, pattern: str) -> bool:
    return bool(re.search(pattern, unit.section, re.I))


def is_unresolved(unit: Unit) -> bool:
    text = unit.statement
    return bool(re.search(r"\bTBD\b|尚待确认|未定$|待确认|远期评估|后续确认|具体.*未.*定义|默认如下", text, re.I))


def scope_for(unit: Unit) -> str:
    text = f"{unit.section} {unit.statement}"
    if re.search(r"密码|账号|登录|权限|认证|角色", text):
        return "identity-access-and-audit"
    if re.search(r"MES|SUBLOT|EQP|TASK_TYPE|moveType|Oracle|PAUSED_ZERO_DROP", text, re.I):
        return "MES-integration-and-transport-demand"
    if re.search(r"RCS|RIOT|地图|station_|AREA|路径|派车|调度", text, re.I):
        return "dispatch-map-and-RIoT"
    if re.search(r"仓位|格口|花篮|光幕|仓门|门锁|IO", text, re.I):
        return "slot-hardware-and-material-handling"
    if re.search(r"流程|模板|步骤|workflow", text, re.I):
        return "workflow-engine-and-governance"
    if re.search(r"充电桩|充电", text):
        return "charging"
    if re.search(r"停靠点|驻点", text):
        return "parking-and-staging"
    return "8005-project-cross-domain"


def claim_status_for(record_id: str, unit: Unit) -> str:
    if section_contains(unit, r"Source 来源"):
        return "source-attribution-only-without-approval-binding"
    if record_id == "R02-19":
        return "user-clarification-summary-without-original-record"
    if record_id == "R02-20":
        confirmed_password_rule = bool(
            re.search(r"英文|数字|复杂度|定期更换", unit.statement)
            and section_contains(unit, r"密码格式")
        )
        return "self-asserted-confirmed-without-evidence" if confirmed_password_rule else "requirements-engineering-baseline-proposal"
    if record_id in {"R02-10", "R02-12", "R02-13", "R02-14", "R02-15", "R02-16", "R02-17", "R02-18", "R02-24"}:
        return "self-asserted-confirmed-or-internal-derived-without-evidence"
    if record_id in {"R02-21", "R02-22", "R02-23"}:
        return "upstream-derived-from-unapproved-internal-summary"
    if record_id == "R02-26":
        return "internal-derived-draft-reference-specification"
    return "unknown-source-internal-synthesis"


def classify(unit: Unit) -> tuple[str, str]:
    section = unit.section
    rid = unit.record_id
    if section_contains(unit, r"Source 来源"):
        return "source-provenance-evidence", "evidence-only"
    if section_contains(unit, r"Rationale 制定原因"):
        return "rationale-evidence", "evidence-only"
    if section_contains(unit, r"Related Use Cases|Related Rules"):
        return "traceability-evidence", "evidence-only"
    if is_unresolved(unit):
        return "unresolved-question", "needs-question-resolution"

    if rid == "R02-07":
        if section_contains(unit, r"文档目的"):
            return "document-governance-evidence", "evidence-only"
        if section_contains(unit, r"流程引擎与能力适配器"):
            return "internal-modeling-derivation", "exclude-from-requirement-approval"
        if section_contains(unit, r"MES|RCS/RIOT|IO 模块|系统边界总结|本系统负责|明确不负责|现场用户"):
            return "system-boundary-or-interface-candidate", "needs-source-and-explicit-approval"
        return "system-scope-candidate", "needs-source-and-explicit-approval"

    if rid == "R02-08":
        if section_contains(unit, r"背景|业务机会"):
            return "business-context-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"业务目标"):
            return "business-objective-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"成功指标"):
            return "success-metric-candidate", "needs-source-measurement-and-explicit-approval"
        if section_contains(unit, r"愿景宣言"):
            return "business-vision-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"业务风险"):
            return "business-risk-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"假设|依赖"):
            return "business-assumption-or-dependency-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"限制|范围"):
            return "system-scope-or-exclusion-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"利益相关方"):
            return "stakeholder-role-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"项目优先权"):
            return "project-priority-candidate", "needs-source-and-explicit-approval"
        if section_contains(unit, r"部署考虑"):
            return "deployment-constraint-candidate", "needs-source-and-explicit-approval"

    if rid == "R02-09":
        return "role-and-permission-candidate", "needs-source-and-explicit-approval"

    if rid == "R02-19":
        return "user-clarification-summary-candidate", "needs-original-clarification-and-explicit-approval"

    if rid == "R02-20":
        confirmed_password_rule = bool(
            re.search(r"英文|数字|复杂度|定期更换", unit.statement)
            and section_contains(unit, r"密码格式")
        )
        if confirmed_password_rule:
            return "user-clarification-summary-candidate", "needs-original-clarification-and-explicit-approval"
        return "analyst-proposed-internal-modeling", "exclude-from-requirement-approval"

    if rid in {"R02-21", "R02-22", "R02-23"}:
        return "upstream-derived-business-rule-candidate", "needs-upstream-source-and-explicit-approval"

    if rid == "R02-26":
        return "internal-specification-derivation", "exclude-from-requirement-approval"

    if rid in {"R02-12", "R02-13", "R02-14", "R02-15", "R02-16", "R02-17", "R02-18", "R02-24"}:
        return "internal-modeling-candidate", "needs-source-and-explicit-approval"

    return "business-rule-candidate", "needs-source-and-explicit-approval"


def conflict_pointer(unit: Unit) -> str:
    pointers: list[str] = []
    text = f"{unit.section} {unit.statement}"
    if section_contains(unit, r"Source 来源|Rationale 制定原因|Related Use Cases|Related Rules"):
        return "none-found-within-r02-pass"
    r02_12_mapping = unit.record_id == "R02-12" and section_contains(unit, r"两表解析模型|站点来源与有效性|显式覆盖记录|任务使用规则")
    r02_26_mapping = unit.record_id == "R02-26" and "DISPATCH_RESOLVE_AREA_STATION" in unit.statement
    if (r02_12_mapping or r02_26_mapping) and re.search(r"AREA|station_|站点|映射|解析|表 A|表 B", text, re.I):
        pointers.append("CF-R01-003")
    r02_21_key = unit.record_id == "R02-21" and section_contains(unit, r"幂等键与任务来源|字段校验、归并与冻结")
    r02_26_key = unit.record_id == "R02-26" and "MES_CANDIDATE_DEDUPLICATE" in unit.statement
    if (r02_21_key or r02_26_key) and re.search(r"幂等键|TASK_TYPE|moveType\s*\+\s*SUBLOT|SUBLOT\s*\+\s*STEP", text, re.I):
        pointers.append("CF-R01-001")
    r02_26_mes_boundary = unit.record_id == "R02-26" and "MES_WRITEBACK_TBD" in unit.statement
    if (unit.record_id in {"R02-07", "R02-08", "R02-21"} or r02_26_mes_boundary) and re.search(r"MES.*(?:只读|回写|写操作)|(?:只读|回写).*MES", text, re.I):
        pointers.append("CF-R01-002")
    r02_23_task_type = unit.record_id == "R02-23" and section_contains(unit, r"1\. 任务类型")
    if unit.record_id == "R02-23" and (r02_23_task_type or re.search(r"WIRE_TO_NITROGEN|2026-07-24", unit.statement, re.I)):
        pointers.append("AD-R01-001")
    return ",".join(dict.fromkeys(pointers)) or "none-found-within-r02-pass"


def approval_gap_for(unit: Unit, candidate_class: str) -> str:
    parts = APPROVAL_GAP.split(";")
    if candidate_class == "success-metric-candidate":
        parts.extend(["measurement-definition", "denominator", "time-window", "measurement-owner"])
    if candidate_class == "user-clarification-summary-candidate":
        parts.extend(["original-dialogue-or-meeting-record", "speaker-identity-and-authority"])
    if candidate_class.startswith("upstream-derived"):
        parts.append("approved-upstream-version-binding")
    return ";".join(dict.fromkeys(parts))


def build_rows() -> list[dict[str, str]]:
    units: list[Unit] = []
    for record_id, relative_path, expected_hash in SOURCES:
        path = REPO / relative_path
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise RuntimeError(f"Source hash drift: {record_id} expected={expected_hash} actual={actual_hash}")
        units.extend(markdown_units(record_id, path))

    rows: list[dict[str, str]] = []
    for index, unit in enumerate(units, start=1):
        candidate_class, route = classify(unit)
        pointer = conflict_pointer(unit)
        if pointer.startswith("CF-") and route not in {"evidence-only", "exclude-from-requirement-approval", "needs-question-resolution"}:
            route = "hold-for-conflict-decision"
        source_path, source_hash = SOURCE_BY_ID[unit.record_id]
        rows.append(
            {
                "candidate_id": f"R02-A{index:04d}",
                "batch_id": "R02",
                "source_record_id": unit.record_id,
                "source_path": source_path,
                "source_sha256": source_hash,
                "exact_location": unit.location,
                "section_path": unit.section,
                "statement_text": unit.statement,
                "source_context": unit.context,
                "statement_fingerprint": fingerprint(unit.statement),
                "candidate_class": candidate_class,
                "source_claim_status": claim_status_for(unit.record_id, unit),
                "applicable_scope": scope_for(unit),
                "baseline_route": route,
                "duplicate_or_derivation": DERIVATION[unit.record_id],
                "conflict_pointer": pointer,
                "approval_state": "not-approved",
                "approval_gap": approval_gap_for(unit, candidate_class),
            }
        )

    first_by_fingerprint: dict[str, str] = {}
    fingerprint_counts = Counter(row["statement_fingerprint"] for row in rows)
    for row in rows:
        fp = row["statement_fingerprint"]
        if fingerprint_counts[fp] > 1:
            first = first_by_fingerprint.setdefault(fp, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    by_source = Counter(row["source_record_id"] for row in rows)
    by_class = Counter(row["candidate_class"] for row in rows)
    by_route = Counter(row["baseline_route"] for row in rows)
    conflicts = Counter(pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer != "none-found-within-r02-pass")
    summary = {
        "total": len(rows),
        "source_documents": len(by_source),
        "by_source": dict(sorted(by_source.items())),
        "by_class": dict(sorted(by_class.items())),
        "by_route": dict(sorted(by_route.items())),
        "conflict_pointers": dict(sorted(conflicts.items())),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_existing() -> list[dict[str, str]]:
    with OUTPUT.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify(rows: list[dict[str, str]]) -> dict[str, object]:
    errors: list[str] = []
    if not rows:
        errors.append("candidate ledger is empty")
    if rows and list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if ids != [f"R02-A{index:04d}" for index in range(1, len(rows) + 1)]:
        errors.append("candidate_id sequence is not contiguous")

    expected_sources = {record_id for record_id, _, _ in SOURCES}
    actual_sources = {row["source_record_id"] for row in rows}
    if expected_sources != actual_sources:
        errors.append(f"source coverage mismatch expected={sorted(expected_sources)} actual={sorted(actual_sources)}")
    for record_id, relative_path, expected_hash in SOURCES:
        if sha256_file(REPO / relative_path) != expected_hash:
            errors.append(f"source hash drift: {record_id}")
        source_rows = [row for row in rows if row["source_record_id"] == record_id]
        if not source_rows:
            errors.append(f"source has no atomic rows: {record_id}")
        if any(row["source_path"] != relative_path or row["source_sha256"] != expected_hash for row in source_rows):
            errors.append(f"source identity mismatch in rows: {record_id}")

    for row in rows:
        missing = [field for field in FIELDS if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")
        if row.get("source_record_id") == "R02-20" and row.get("source_claim_status") == "requirements-engineering-baseline-proposal" and row.get("baseline_route") not in {"exclude-from-requirement-approval", "evidence-only", "needs-question-resolution"}:
            errors.append(f"analyst baseline leaked into approval route: {row.get('candidate_id')}")

    result: dict[str, object] = {
        "total": len(rows),
        "sources": len(actual_sources),
        "source_counts": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "duplicates": len(ids) - len(set(ids)),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "conflict_rows": sum(row["conflict_pointer"].startswith("CF-") for row in rows),
        "errors": errors,
    }
    if errors:
        raise RuntimeError("Verification failed:\n- " + "\n- ".join(errors[:30]))
    return result


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
            raise RuntimeError(f"Generated ledger drift: existing={len(rows)} rebuilt={len(rebuilt)} first_difference_index={first_difference}")
    else:
        rows = build_rows()
        write_outputs(rows)
    print(json.dumps(verify(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
