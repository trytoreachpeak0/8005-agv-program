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
SOURCE_LEDGER = REPO / ".scratch/current-requirements-baseline/evidence/document-classification/R01-R13-document-evidence-ledger.tsv"
OUTPUT = Path(__file__).with_name("R03-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R03-atomic-candidates-summary.json")
EXPECTED_IDS = [f"R03-{index:02d}" for index in range(1, 47)]
APPROVAL_GAP = "named-approver;approval-date;approved-scope;version-or-sha256-binding"
NONE = "none-found-within-r03-pass"

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


@dataclass(frozen=True)
class Source:
    record_id: str
    path: str
    digest: str
    document_class: str
    source_type: str
    applicability: str
    derivation: str


@dataclass(frozen=True)
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


def load_sources() -> list[Source]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["candidate_group_id"] == "R03"]
    ids = [row["record_id"] for row in rows]
    if ids != EXPECTED_IDS:
        raise RuntimeError(f"R03 source identity drift: expected={EXPECTED_IDS} actual={ids}")
    sources = [
        Source(
            row["record_id"],
            row["path"],
            row["sha256"],
            row["document_class"],
            row["source_type"],
            row["current_applicability"],
            row["history_or_derivation"],
        )
        for row in rows
    ]
    if Counter(source.document_class for source in sources) != Counter({"R03-C": 22, "R03-I": 24}):
        raise RuntimeError("R03 source classification drift; expected 22 R03-C and 24 R03-I documents")
    return sources


def split_table(line: str) -> list[str]:
    return [normalize(cell.replace("\\|", "|")) for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def is_table_separator(line: str) -> bool:
    cells = split_table(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_atomic(value: str) -> list[str]:
    value = normalize(value)
    if not value:
        return []
    parts = re.split(r"(?<=[。！？；])(?=[^）])", value)
    return [normalize(part) for part in parts if len(normalize(part)) >= 2] or [value]


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
        if stripped.startswith(("```", "~~~")):
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
                context = " | ".join(
                    f"{headers[pos] if pos < len(headers) else f'col{pos + 1}'}={cell}"
                    for pos, cell in enumerate(cells)
                    if cell
                )
                identity = " | ".join(
                    f"{headers[pos]}={cell}"
                    for pos, cell in enumerate(cells)
                    if pos < len(headers) and cell and re.search(r"编号|步骤|角色|场景|状态|类型", headers[pos])
                )
                for pos, cell in enumerate(cells):
                    header = headers[pos] if pos < len(headers) else f"col{pos + 1}"
                    if not cell or (identity and f"{header}={cell}" in identity):
                        continue
                    statement = f"{identity} | {header}={cell}" if identity else f"{header}={cell}"
                    units.append(Unit(record_id, f"line {index + 1}", section_path(), statement, context, "markdown-table-cell"))
                index += 1
            continue

        list_match = re.match(r"^\s*(?:[-*+]\s+|\d+(?:\.\d+)*(?:[.)、]|\s+)\s*)(.+)$", raw)
        if list_match:
            context = normalize(list_match.group(1))
            for atom in split_atomic(context):
                units.append(Unit(record_id, f"line {line_no}", section_path(), atom, context, "markdown-flow-or-list-item"))
            index += 1
            continue

        start = index
        paragraph = [stripped.lstrip("> ")]
        index += 1
        while index < len(lines):
            follow = lines[index].strip()
            if not follow or follow.startswith(("#", "|", "```", "~~~")) or follow == "---":
                break
            if re.match(r"^\s*(?:[-*+]\s+|\d+(?:\.\d+)*(?:[.)、]|\s+)\s*)", lines[index]):
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
    return bool(
        re.search(
            r"\bTBD\b|待确认|尚待|待定|未明确|未最终确认|仍需确认|后续确认|远期评估|是否需要.*(?:待|TBD)",
            unit.statement,
            re.I,
        )
    )


def is_evidence(unit: Unit) -> bool:
    return section_contains(unit, r"备注|关联用例|其他信息|Other Information|来源|Source|制定原因|Rationale")


def is_internal_technical(unit: Unit) -> bool:
    text = unit.statement
    return bool(
        re.search(
            r"\b(?:API|SQL|SELECT|Oracle|DTO|revision|MessageId|attemptNo|station_name|area_code|moveType|TASK_TYPE)\b"
            r"|`[^`]+`|数据库|落库|持久化|事务|状态机|轮询|队列|幂等|快照|投影|适配器|接口调用|字段映射|版本号|哈希|自动重试|并发锁|审计事务",
            text,
            re.I,
        )
    )


def scope_for(source: Source, unit: Unit) -> str:
    path = source.path
    text = f"{unit.section} {unit.statement}"
    if "/01-site-operations/" in path:
        return "site-operation-and-slot-closure"
    if "/02-slot-and-hardware/" in path:
        return "slot-hardware-and-IO"
    if "/03-agv-fleet-management/" in path:
        return "AGV-fleet-and-local-configuration"
    if "/04-transport-task-dispatch/" in path:
        return "MES-dispatch-and-RIoT"
    if "/05-agv-charging/" in path:
        return "AGV-charging"
    if "/06-area-station-mapping/" in path:
        return "AREA-station-map-and-routing"
    if "/07-workflow-engine/" in path:
        return "workflow-engine-and-governance"
    if "/08-user-and-access/" in path or re.search(r"账号|角色|权限|登录|会话", text):
        return "identity-access-and-session"
    if "/09-logs-and-audit/" in path:
        return "logs-audit-and-traceability"
    if "/10-safety-and-interlock/" in path:
        return "movement-safety-and-interlock"
    if "/11-agv-parking/" in path:
        return "AGV-parking"
    return "8005-project-cross-domain"


def classify(source: Source, unit: Unit) -> tuple[str, str]:
    if is_evidence(unit):
        if section_contains(unit, r"关联用例"):
            return "traceability-evidence", "evidence-only"
        if section_contains(unit, r"来源|Source"):
            return "source-provenance-evidence", "evidence-only"
        return "derivation-or-author-annotation-evidence", "evidence-only"
    if is_unresolved(unit):
        return "unresolved-question", "needs-question-resolution"
    if source.document_class == "R03-I":
        if re.search(r"安全|联锁|急停|危险|故障|应急", f"{unit.section} {unit.statement}"):
            return "internal-safety-design-derivation", "exclude-from-requirement-approval"
        if re.search(r"MES|RIOT|RCS|接口|API|通信|Oracle|IO", unit.statement, re.I):
            return "internal-interface-design-derivation", "exclude-from-requirement-approval"
        if re.search(r"用户|账号|角色|权限|会话|认证|审计|日志", unit.statement):
            return "internal-access-or-audit-design-derivation", "exclude-from-requirement-approval"
        return "internal-process-design-derivation", "exclude-from-requirement-approval"
    if is_internal_technical(unit):
        return "embedded-internal-design-derivation", "exclude-from-requirement-approval"
    if section_contains(unit, r"描述|触发条件|前置条件|后置条件|正常流程|备选流程|异常流程|假设"):
        return "business-use-case-behavior-candidate", "needs-source-and-explicit-approval"
    return "business-use-case-context-candidate", "needs-source-and-explicit-approval"


def conflict_pointer(source: Source, unit: Unit) -> str:
    pointers: list[str] = []
    text = unit.statement
    if source.record_id in {"R03-05", "R03-23"} and re.search(r"任务类型\s*\+\s*SUBLOT|TASK_TYPE.*SUBLOT|幂等键|业务键", text, re.I):
        pointers.append("CF-R01-001")
    if source.record_id in {"R03-06", "R03-23", "R03-27"} and re.search(r"MES.{0,30}(?:只读|回写|写操作)|(?:只读|回写|写操作).{0,30}MES", text, re.I):
        pointers.append("CF-R01-002")
    if source.record_id in {"R03-23", "R03-30", "R03-31"} and re.search(r"AREA.{0,40}(?:映射|解析|派生|覆盖)|(?:映射|解析|派生|覆盖).{0,40}AREA|表 A|表 B|station_name.{0,40}area_code", text, re.I):
        pointers.append("CF-R01-003")
    if source.record_id in {"R03-06", "R03-23"} and re.search(r"六类|五类|WIRE_TO_NITROGEN", text, re.I):
        pointers.append("AD-R01-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


def approval_gap_for(candidate_class: str) -> str:
    parts = APPROVAL_GAP.split(";")
    if candidate_class == "unresolved-question":
        parts.insert(0, "question-resolution")
    if candidate_class.startswith("internal-") or candidate_class.startswith("embedded-internal-"):
        parts.extend(["authoritative-business-or-safety-source", "independent-approval-unit-reframing"])
    return ";".join(dict.fromkeys(parts))


def build_rows() -> list[dict[str, str]]:
    sources = load_sources()
    source_by_id = {source.record_id: source for source in sources}
    units: list[Unit] = []
    for source in sources:
        path = REPO / source.path
        actual = sha256_file(path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        units.extend(markdown_units(source.record_id, path))

    rows: list[dict[str, str]] = []
    for index, unit in enumerate(units, start=1):
        source = source_by_id[unit.record_id]
        candidate_class, route = classify(source, unit)
        pointer = conflict_pointer(source, unit)
        if pointer.startswith("CF-") and route not in {"evidence-only", "exclude-from-requirement-approval", "needs-question-resolution"}:
            route = "hold-for-conflict-decision"
        source_claim = "unapproved-human-review-candidate" if source.document_class == "R03-C" else "unapproved-internal-design-exploration"
        rows.append(
            {
                "candidate_id": f"R03-A{index:04d}",
                "batch_id": "R03",
                "source_record_id": source.record_id,
                "source_path": source.path,
                "source_sha256": source.digest,
                "exact_location": unit.location,
                "section_path": unit.section,
                "statement_text": unit.statement,
                "source_context": unit.context,
                "statement_fingerprint": fingerprint(unit.statement),
                "candidate_class": candidate_class,
                "source_claim_status": source_claim,
                "applicable_scope": scope_for(source, unit),
                "baseline_route": route,
                "duplicate_or_derivation": f"document-route:{source.document_class}; {normalize(source.derivation)}",
                "conflict_pointer": pointer,
                "approval_state": "not-approved",
                "approval_gap": approval_gap_for(candidate_class),
            }
        )

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
        pointer
        for row in rows
        for pointer in row["conflict_pointer"].split(",")
        if pointer != NONE
    )
    source_classes = {
        row["source_record_id"]: row["duplicate_or_derivation"].split(";", 1)[0].split(":", 1)[1]
        for row in rows
    }
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "source_documents_by_class": dict(sorted(Counter(source_classes.values()).items())),
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "conflict_pointers": dict(sorted(conflicts.items())),
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
    if not rows:
        errors.append("candidate ledger is empty")
    if rows and list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if ids != [f"R03-A{index:04d}" for index in range(1, len(rows) + 1)]:
        errors.append("candidate_id sequence is not contiguous")
    actual_sources = {row.get("source_record_id") for row in rows}
    if actual_sources != set(EXPECTED_IDS):
        errors.append("source coverage mismatch")
    for row in rows:
        missing = [field for field in FIELDS if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")
        if "document-route:R03-I" in row.get("duplicate_or_derivation", "") and row.get("baseline_route") not in {"exclude-from-requirement-approval", "evidence-only", "needs-question-resolution"}:
            errors.append(f"internal design leaked into approval route: {row.get('candidate_id')}")
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
            raise RuntimeError(f"Generated ledger drift: existing={len(rows)} rebuilt={len(rebuilt)} first_difference_index={first_difference}")
    else:
        rows = build_rows()
        write_outputs(rows)
    print(json.dumps(verify(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
