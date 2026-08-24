from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.text.paragraph import Paragraph


REPO = Path(__file__).resolve().parents[4]
OUTPUT = Path(__file__).with_name("R01-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R01-atomic-candidates-summary.json")

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
    ("R01-03", "mes/docs/待处理事项清单-MES-RIOT-应用.docx", "966aec692696684299439c170b1a88dab7e9a3b3c0820c8c6417542d6c83980e"),
    ("R01-04", "mes/docs/宿迁长电AGV项目MES数据接口需求确认.md", "294f2fff9b8bf58ff30b74f44dd1aab6f3551fcc505efed571890c0c23e9109b"),
    ("R01-05", "mes/docs/AGV系统业务与MES任务模型.md", "8d9210c25ea5f260131b42d60eb0734b09d2db89b8258b20f7ce5fdbe88da487"),
    ("R01-07", "mes/sources/customer/2026-07-16/operator-identity/README.md", "ff0298b681634bf0bfea2be00b3caef471e1472a3499b25efb265e04edeb1a15"),
    ("R01-08", "mes/sources/customer/2026-07-16/sublot-box-count/README.md", "019aa8030935017b0ed86982f1fe76d5ef9ff39d54a9a28c36ebff0885988cd2"),
    ("R01-09", "mes/sources/customer/2026-07-24/mes-task-original-queries/README.md", "3c94d4580f4f4e25ab3cf4a34ad4b1675384a07da70a19d78f98b0986c55b070"),
    ("R01-10", "project_agreements/20260527-新基智能AGV小车技术协议-TR前线.docx", "695a2a10310e53d6b15df52e865a0222127943ec204bdd46269b36dcd28ef32f"),
    ("R01-11", "project_agreements/生产指令书-8005 多仓位AGV.docx", "be81a977929b6a3ae78488cc7fac7c9a9d16d2ba11c1b594cf2c505adc6cb4a9"),
    ("R01-13", "requirement-documents/07-customer-deliverables/客户需求讨论稿-多仓位AGV系统.md", "8cdfda0e780e60ac096ac03f5864134c5584611804305ddf4bd3e4ef58082118"),
    ("R01-14", "requirement-documents/07-customer-deliverables/宿迁长电多仓位AGV系统-需求讨论稿-2026-07-14.docx", "b9d895560341b089f6849ccedb038ec6edb34faa783b617a667bb8c121214828"),
    ("R01-15", "requirement-documents/07-customer-deliverables/assets/system-context.png", "917293dd7ca12a988e881c6565056830b0e8ed3e1197bf7e579da00290b67559"),
    ("R01-17", "requirement-documents/简易需求文档.md", "058ada6be83bb9f97adb481880b424dd77859f18a819f2d92df39ffc5838cd50"),
    ("R01-19", "requirement-documents/user case.md", "9d682f471346f5fa2b75bad68003f984ad8816b55110df0c35711c92a2f35da5"),
]

SOURCE_BY_ID = {record_id: (path, digest) for record_id, path, digest in SOURCES}
DERIVATION = {
    "R01-03": "historical-worklist; statements that prescribe a suggested action are not customer requirements",
    "R01-04": "mixed-internal-summary; customer-source and confirmed labels remain unsupported",
    "R01-05": "internal-integration-of:R01-04; overlaps:R01-13,R01-17",
    "R01-07": "source-snapshot-index-for:R01-04; runtime-query-package-distinct",
    "R01-08": "source-snapshot-index-for:R01-04; runtime-query-package-distinct",
    "R01-09": "incremental-source-snapshot-for:R01-04,R01-05; does-not-replace-five-task-snapshot",
    "R01-10": "unsigned-agreement-candidate; generic-template-clauses-separated-from-project-filled-clauses",
    "R01-11": "project-identity-and-plan; R01-12-excluded-is-row-level-derivative",
    "R01-13": "current-discussion-draft; source-for:R01-14@2026-07-14; references:R01-15; overlaps:R01-04,R01-05,R01-17,R01-19",
    "R01-14": "generated-from:R01-13@2026-07-14; embeds:R01-15; not-equivalent-to-current-R01-13",
    "R01-15": "embedded-in:R01-14; referenced-by:R01-13; diagram-claims-transcribed-manually",
    "R01-17": "early-internal-draft; overlaps:R01-04,R01-05,R01-13,R01-19",
    "R01-19": "incomplete-internal-draft; references:R01-17; overlaps:R01-13",
}

APPROVAL_GAP = "named-approver;approval-date;approved-scope;version-or-sha256-binding"


@dataclass
class Unit:
    record_id: str
    location: str
    section: str
    statement: str
    context: str
    source_kind: str


def normalize(value: str) -> str:
    value = value.replace("\u00a0", " ").replace("\t", " ")
    return " ".join(value.split()).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fingerprint(statement: str) -> str:
    normalized = re.sub(r"[`*_#>\[\]()]", "", normalize(statement)).casefold()
    normalized = re.sub(r"\s+", "", normalized)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def parse_table_cells(line: str) -> list[str]:
    return [normalize(cell) for cell in line.strip().strip("|").split("|")]


def split_atomic(statement: str) -> list[str]:
    statement = normalize(statement)
    if not statement:
        return []
    parts = re.split(r"(?<=[。！？；])\s+|(?<=[。！？；])(?=[^）])", statement)
    atoms = [normalize(part) for part in parts if len(normalize(part)) >= 2]
    return atoms or [statement]


def markdown_units(record_id: str, path: Path) -> list[Unit]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    headings: list[tuple[int, str]] = []
    units: list[Unit] = []
    in_code = False
    i = 0

    def section_path() -> str:
        return " > ".join(title for _, title in headings) or "document-root"

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        line_no = i + 1
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            i += 1
            continue
        if in_code or not stripped or stripped == "---" or stripped.startswith("<!--"):
            i += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = normalize(heading_match.group(2))
            headings = [entry for entry in headings if entry[0] < level]
            headings.append((level, title))
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            headers = parse_table_cells(stripped)
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = parse_table_cells(lines[i])
                if any(cells):
                    pairs = [f"{headers[index] if index < len(headers) else f'col{index + 1}'}={cell}" for index, cell in enumerate(cells) if cell]
                    context = " | ".join(pairs)
                    if not all(re.fullmatch(r"[-—.。·\s]*", cell) for cell in cells):
                        if {"场景", "起点", "终点"}.issubset(set(headers)):
                            payload = context
                        else:
                            payload_indexes = [
                                index
                                for index, header in enumerate(headers)
                                if re.search(r"需求|验收|说明/职责|职责|说明$|内容$|处理方式|处理$|结论|问题$|目标$|风险$|业务含义", header)
                            ]
                            payload = "；".join(cells[index] for index in payload_indexes if index < len(cells) and cells[index]) or context
                        for atom in split_atomic(payload):
                            units.append(Unit(record_id, f"line {i + 1}", section_path(), atom, context, "markdown-table-row"))
                i += 1
            continue

        if stripped.startswith("!["):
            i += 1
            continue

        list_match = re.match(r"^\s*(?:[-*+]\s+|\d+[.)、]\s*)(.+)$", raw)
        if list_match:
            statement = normalize(list_match.group(1))
            for atom in split_atomic(statement):
                units.append(Unit(record_id, f"line {line_no}", section_path(), atom, statement, "markdown-list-item"))
            i += 1
            continue

        start = i
        paragraph = [stripped.lstrip("> ")]
        i += 1
        while i < len(lines):
            follow = lines[i].strip()
            if not follow or follow.startswith("#") or follow.startswith("|") or follow.startswith("```") or follow == "---":
                break
            if re.match(r"^\s*(?:[-*+]\s+|\d+[.)、]\s+)", lines[i]):
                break
            paragraph.append(follow.lstrip("> "))
            i += 1
        statement = normalize(" ".join(paragraph))
        end = i if i > start + 1 else start + 1
        location = f"lines {start + 1}-{end}" if end > start + 1 else f"line {start + 1}"
        for atom in split_atomic(statement):
            units.append(Unit(record_id, location, section_path(), atom, statement, "markdown-paragraph"))
    return units


def iter_docx_blocks(parent: DocumentObject) -> Iterable[Paragraph | Table]:
    for child in parent.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("}tbl"):
            yield Table(child, parent)


def docx_units(record_id: str, path: Path) -> list[Unit]:
    document = Document(path)
    units: list[Unit] = []
    headings: list[tuple[int, str]] = []
    paragraph_no = 0
    table_no = 0
    section = "document-root"

    def section_path() -> str:
        return " > ".join(title for _, title in headings) or section

    for block in iter_docx_blocks(document):
        if isinstance(block, Paragraph):
            paragraph_no += 1
            text = normalize(block.text)
            if not text:
                continue
            style = normalize(block.style.name)
            heading_match = re.search(r"Heading\s+(\d+)", style, re.I)
            if heading_match:
                level = int(heading_match.group(1))
                headings = [entry for entry in headings if entry[0] < level]
                headings.append((level, text))
                continue
            if record_id == "R01-10" and re.match(r"^(?:第[一二三四五六七八九十]+条|10\.\d)", text):
                section = text
                headings = []
                continue
            for atom in split_atomic(text):
                units.append(Unit(record_id, f"paragraph P{paragraph_no:04d}", section_path(), atom, text, "docx-paragraph"))
            continue

        table_no += 1
        rows = block.rows
        if record_id == "R01-11" and table_no == 1:
            for row_no, row in enumerate(rows, start=1):
                cells = [normalize(cell.text) for cell in row.cells]
                pairs = []
                for index in range(0, len(cells) - 1, 2):
                    if cells[index] or cells[index + 1]:
                        pairs.append(f"{cells[index]}={cells[index + 1]}")
                context = " | ".join(pairs)
                if context:
                    units.append(Unit(record_id, f"table T{table_no:02d} row R{row_no:03d}", section_path(), context, context, "docx-key-value-row"))
            continue
        headers = [normalize(cell.text) for cell in rows[0].cells] if rows else []
        for row_no, row in enumerate(rows[1:], start=2):
            cells = [normalize(cell.text) for cell in row.cells]
            if not any(cells):
                continue
            pairs = [f"{headers[index] if index < len(headers) and headers[index] else f'col{index + 1}'}={cell}" for index, cell in enumerate(cells) if cell]
            context = " | ".join(pairs)
            payload_indexes = [
                index
                for index, header in enumerate(headers)
                if re.search(r"需求|验收内容|说明/职责|说明$|内容$|处理方式|沟通事项|新增需求|待处理事项|要点", header)
            ]
            payload = "；".join(cells[index] for index in payload_indexes if index < len(cells) and cells[index]) or context
            for atom in split_atomic(payload):
                units.append(Unit(record_id, f"table T{table_no:02d} row R{row_no:03d}", section_path(), atom, context, "docx-table-row"))
    return units


IMAGE_UNITS = [
    ("diagram boundary", "系统上下文示意", "“多仓位 AGV 系统”位于“本系统边界”内。"),
    ("diagram edge user-to-system", "系统上下文示意", "现场用户向系统执行认证、扫码、装卸确认、任务操作和配置维护。"),
    ("diagram edge system-to-user", "系统上下文示意", "系统向现场用户提供作业引导、任务状态、设备状态和告警。"),
    ("diagram edge mes-to-system", "系统上下文示意", "MES 向系统提供搬运任务及生产相关数据。"),
    ("diagram edge mes-boundary", "系统上下文示意", "MES 接入的当前阶段边界是只读、不回写。"),
    ("diagram edge system-to-riot", "系统上下文示意", "系统向 RCS / RIOT 请求指定目标 AGV 的移动、充电、取消等操作。"),
    ("diagram edge riot-to-system", "系统上下文示意", "RCS / RIOT 向系统提供车辆列表、任务队列、位置、到站、电量及执行状态。"),
    ("diagram edge riot-to-agv", "系统上下文示意", "RCS / RIOT 对 AGV 执行调度、导航及运动控制。"),
    ("diagram edge agv-to-riot", "系统上下文示意", "AGV 向 RCS / RIOT 返回运行位置、状态及执行结果。"),
    ("diagram edge system-to-io", "系统上下文示意", "系统向 IO 模块发送开锁指令及输出控制。"),
    ("diagram edge io-to-system", "系统上下文示意", "IO 模块向系统返回 DI 状态及故障信息。"),
    ("diagram edge io-to-lock", "系统上下文示意", "IO 模块驱动电子锁开锁。"),
    ("diagram edge lock-to-io", "系统上下文示意", "电子锁向 IO 模块返回锁门/开状态信号。"),
    ("diagram edge curtain-to-io", "系统上下文示意", "光幕向 IO 模块返回遮挡/通行状态信号。"),
]


def filter_unit(unit: Unit) -> bool:
    statement = normalize(unit.statement)
    if len(statement) < 2 or re.fullmatch(r"[\W_]+", statement):
        return False
    if unit.record_id == "R01-10":
        if unit.location.startswith("paragraph"):
            match = re.search(r"P(\d+)", unit.location)
            number = int(match.group(1)) if match else 0
            return number in {100, 102, 103, 133, 135}
        table_match = re.search(r"T(\d+)", unit.location)
        return bool(table_match and int(table_match.group(1)) in {6, 9, 11, 12, 13, 14, 15, 16})
    if unit.record_id == "R01-11":
        return not re.search(r"=\s*(?:NA)?(?:\s*\|\s*[^=]+=\s*)*$", statement)
    if re.match(r"^(?:相关入口|各任务类型的业务问题|流程要点|整体流程如下|系统需记录以下内容)[:：]?$", statement):
        return False
    if re.fullmatch(r"(?:Actor|Trigger|基本流程|可能的 user case|维护类 user case)[:：]?", statement, re.I):
        return False
    return True


def section_number(section: str) -> str:
    matches = re.findall(r"(?:^| > )(\d+(?:\.\d+)*)", section)
    return matches[-1] if matches else ""


def classify(unit: Unit) -> tuple[str, str, str, str]:
    rid = unit.record_id
    text = unit.statement
    section = unit.section
    sec = section_number(section)

    if rid == "R01-03":
        if re.search(r"客户新增功能|A-0[1-4]|需求口头提出", unit.context + section):
            return "customer-attributed-draft-candidate", "customer-attributed-without-record", "cross-domain", "needs-source-and-explicit-approval"
        if re.search(r"待确认|等待|需沟通|未反馈|未提供|阻塞", text + unit.context):
            return "unresolved-question", "historical-worklist", "project-governance", "needs-question-resolution"
        return "historical-state-evidence", "historical-worklist", "project-governance", "evidence-only"

    if rid == "R01-04":
        if sec.startswith("5"):
            return "unresolved-question", "explicitly-pending", "cross-domain", "needs-question-resolution"
        if sec.startswith("4"):
            return "business-requirement-candidate", "self-asserted-confirmed-without-evidence", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("6"):
            return "evidence-governance-claim", "internal-derived", "project-governance", "evidence-only"
        if sec.startswith("3"):
            return "nonfunctional-or-safety-candidate", "mixed-internal-summary", "MES-integration", "needs-source-and-explicit-approval"
        if sec.startswith("2"):
            return "interface-data-contract-candidate", "customer-attributed-without-record", "MES-integration", "needs-source-and-explicit-approval"
        if sec.startswith("1.1"):
            return "domain-fact-candidate", "mixed-internal-summary", "MES-integration", "needs-source-and-explicit-approval"
        if sec.startswith("0"):
            return "external-constraint-candidate", "customer-attributed-without-record", "MES-integration", "needs-source-and-explicit-approval"
        return "business-requirement-candidate", "mixed-internal-summary", "MES-integration", "needs-source-and-explicit-approval"

    if rid == "R01-05":
        if sec.startswith("13.3") or re.search(r"已关闭", section):
            return "self-asserted-closed-decision", "self-asserted-closed-without-evidence", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("13.1") or sec.startswith("13.2") or re.search(r"待确认|尚未", section):
            return "unresolved-question", "explicitly-pending", "cross-domain", "needs-question-resolution"
        if sec.startswith("14") or sec.startswith("11") or sec.startswith("6"):
            return "internal-design-derivation", "internal-derived", "MES-and-dispatch-design", "exclude-from-requirement-approval"
        if sec.startswith("4") or sec.startswith("5") or sec.startswith("7"):
            return "interface-data-contract-candidate", "mixed-internal-summary", "MES-integration", "needs-source-and-explicit-approval"
        if sec.startswith("2"):
            return "domain-fact-candidate", "mixed-internal-summary", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("12"):
            return "system-scope-candidate", "self-asserted-confirmed-without-evidence", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("1"):
            return "document-or-implementation-governance", "internal-derived", "project-governance", "evidence-only"
        return "business-requirement-candidate", "mixed-internal-summary", "cross-domain", "needs-source-and-explicit-approval"

    if rid in {"R01-07", "R01-08", "R01-09"}:
        if re.search(r"不得|只能|运行时|使用边界", text + section):
            return "internal-runtime-boundary", "source-snapshot-claim", "MES-integration", "exclude-from-requirement-approval"
        return "source-provenance-evidence", "customer-attributed-without-record", "MES-integration", "evidence-only"

    if rid == "R01-10":
        if "T06" in unit.location or re.search(r"P0(?:100|102|103)", unit.location):
            return "unsigned-project-scope-or-configuration-candidate", "unsigned-agreement", "8005-project", "needs-signature-source-and-explicit-approval"
        if "T09" in unit.location:
            return "unsigned-performance-or-configuration-candidate", "unsigned-agreement", "8005-project", "needs-signature-source-and-explicit-approval"
        if "T14" in unit.location or "T15" in unit.location or "T16" in unit.location:
            return "unsigned-acceptance-criterion-candidate", "unsigned-agreement", "8005-acceptance", "needs-signature-source-and-explicit-approval"
        if "T11" in unit.location or "T12" in unit.location or "T13" in unit.location:
            return "unsigned-template-obligation-candidate", "unsigned-agreement-template", "commercial-and-support", "needs-signature-scope-and-explicit-approval"
        return "unsigned-agreement-governance-clause", "unsigned-agreement", "commercial-and-support", "needs-signature-source-and-explicit-approval"

    if rid == "R01-11":
        if "T01" in unit.location:
            return "project-identity-or-scope-candidate", "internal-production-order", "8005-project", "needs-source-and-explicit-approval"
        return "project-plan-evidence", "internal-production-order", "project-management", "evidence-only"

    if rid in {"R01-13", "R01-14"}:
        source_status = "discussion-draft" if rid == "R01-13" else "frozen-derived-discussion-draft"
        if sec.startswith("7.3") or re.search(r"已关闭", section):
            return "self-asserted-closed-decision", "self-asserted-closed-without-evidence", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("7.1") or sec.startswith("7.2") or re.search(r"待客户确认", section):
            return "unresolved-question", "explicitly-pending", "cross-domain", "needs-question-resolution"
        if sec.startswith("1"):
            return "document-governance-evidence", source_status, "project-governance", "evidence-only"
        if sec.startswith("2.3"):
            return "acceptance-or-success-criterion-candidate", source_status, "8005-project", "needs-source-and-explicit-approval"
        if sec.startswith("2") or sec.startswith("3"):
            return "system-scope-or-goal-candidate", source_status, "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("4"):
            return "actor-or-responsibility-candidate", source_status, "site-operations", "needs-source-and-explicit-approval"
        if sec.startswith("5"):
            return "business-rule-candidate", source_status, "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("6"):
            return "use-case-behavior-candidate", source_status, "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("8"):
            return "domain-term-candidate", source_status, "cross-domain", "needs-source-and-explicit-approval"
        return "discussion-draft-candidate", source_status, "cross-domain", "needs-source-and-explicit-approval"

    if rid == "R01-15":
        return "system-context-candidate", "unapproved-diagram", "cross-domain", "needs-source-and-explicit-approval"

    if rid == "R01-17":
        if re.search(r"待确认|后续.*确定|需 IT|由供应商确认|具体.*确认", text):
            return "unresolved-question", "early-internal-draft", "cross-domain", "needs-question-resolution"
        if sec.startswith("1") or sec.startswith("3"):
            return "project-scope-or-hardware-candidate", "early-internal-draft", "8005-project", "needs-source-and-explicit-approval"
        if sec.startswith("2") or sec.startswith("5"):
            return "business-process-candidate", "early-internal-draft", "site-operations", "needs-source-and-explicit-approval"
        if sec.startswith("4"):
            return "domain-fact-candidate", "early-internal-draft", "site-operations", "needs-source-and-explicit-approval"
        if sec.startswith("6"):
            return "functional-requirement-candidate", "early-internal-draft", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("7"):
            return "interface-candidate", "early-internal-draft", "cross-domain", "needs-source-and-explicit-approval"
        if sec.startswith("8"):
            return "safety-or-exception-candidate", "early-internal-draft", "cross-domain", "needs-source-and-explicit-approval"
        return "early-draft-candidate", "early-internal-draft", "cross-domain", "needs-source-and-explicit-approval"

    if rid == "R01-19":
        if re.search(r"待确认|待补充", text + section):
            return "unresolved-question", "incomplete-internal-draft", "site-operations", "needs-question-resolution"
        if re.search(r"角色|Actor", section + text, re.I):
            return "actor-or-responsibility-candidate", "incomplete-internal-draft", "site-operations", "needs-source-and-explicit-approval"
        return "use-case-behavior-candidate", "incomplete-internal-draft", "site-operations", "needs-source-and-explicit-approval"

    raise AssertionError(f"Unhandled record: {rid}")


def infer_conflict(unit: Unit) -> str:
    text = unit.statement + " " + unit.context + " " + unit.section
    pointers: list[str] = []
    if re.search(r"product_lot\s*\+\s*machine_no\s*\+\s*finish_time|MES\s*事务\s*ID", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"TASK_TYPE\s*\+\s*SUBLOT", text, re.I) and re.search(r"幂等|去重|抑制|唯一", text):
        pointers.append("CF-R01-001")
    if re.search(r"MES\s*回写|回写\s*MES|完工回写|当前阶段不做\s*MES\s*回写|只读、不回写|只读 MES", text, re.I):
        pointers.append("CF-R01-002")
    if re.search(r"人工维护显式版本化映射|人工维护、版本化.*显式映射|现行\s*UC-024/BR-003|两者需要后续(?:统一评审|合并)", text, re.I):
        pointers.append("CF-R01-003")
    if unit.record_id == "R01-14" and ("table T04" in unit.location or re.search(r"五类运输任务|当前五类|五个任务", unit.statement)):
        pointers.append("AD-R01-001")
    return ",".join(dict.fromkeys(pointers))


def infer_scope(unit: Unit, fallback: str) -> str:
    text = unit.statement + " " + unit.section
    scopes: list[str] = []
    if re.search(r"MES|Oracle|SUBLOT|PACKAGE|QUERY_ID", text, re.I):
        scopes.append("MES-integration")
    if re.search(r"RIOT|RCS|AGV|派车|充电|移动任务", text, re.I):
        scopes.append("dispatch-and-fleet")
    if re.search(r"仓位|电子锁|光幕|IO|装料|卸料|扫码|操作员", text, re.I):
        scopes.append("onboard-and-site-operations")
    if re.search(r"验收|协议|保修|售后|设备", text):
        scopes.append("equipment-agreement-and-acceptance")
    return ",".join(dict.fromkeys(scopes)) or fallback


def build_rows() -> list[dict[str, str]]:
    units: list[Unit] = []
    for record_id, relative_path, expected_hash in SOURCES:
        path = REPO / relative_path
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise RuntimeError(f"Source hash drift: {record_id} {relative_path} expected={expected_hash} actual={actual_hash}")
        if record_id == "R01-15":
            units.extend(Unit(record_id, location, section, statement, statement, "image-transcription") for location, section, statement in IMAGE_UNITS)
        elif path.suffix.lower() == ".docx":
            units.extend(docx_units(record_id, path))
        else:
            units.extend(markdown_units(record_id, path))

    units = [unit for unit in units if filter_unit(unit)]

    rows: list[dict[str, str]] = []
    for index, unit in enumerate(units, start=1):
        source_path, source_hash = SOURCE_BY_ID[unit.record_id]
        candidate_class, claim_status, fallback_scope, baseline_route = classify(unit)
        conflict_pointer = infer_conflict(unit)
        if conflict_pointer.startswith("CF-") and baseline_route not in {"evidence-only", "exclude-from-requirement-approval", "needs-question-resolution"}:
            baseline_route = "hold-for-conflict-decision"
        rows.append(
            {
                "candidate_id": f"R01-A{index:04d}",
                "batch_id": "R01",
                "source_record_id": unit.record_id,
                "source_path": source_path,
                "source_sha256": source_hash,
                "exact_location": unit.location,
                "section_path": unit.section,
                "statement_text": unit.statement,
                "source_context": unit.context,
                "statement_fingerprint": fingerprint(unit.statement),
                "candidate_class": candidate_class,
                "source_claim_status": claim_status,
                "applicable_scope": infer_scope(unit, fallback_scope),
                "baseline_route": baseline_route,
                "duplicate_or_derivation": DERIVATION[unit.record_id],
                "conflict_pointer": conflict_pointer or "none-found-within-r01-pass",
                "approval_state": "not-approved",
                "approval_gap": APPROVAL_GAP,
            }
        )

    first_by_fingerprint: dict[str, str] = {}
    counts = Counter(row["statement_fingerprint"] for row in rows)
    for row in rows:
        fp = row["statement_fingerprint"]
        if counts[fp] > 1:
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
    conflicts = Counter(pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer != "none-found-within-r01-pass")
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
    if list(rows[0].keys()) != FIELDS:
        errors.append("field order mismatch")
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    if ids != [f"R01-A{index:04d}" for index in range(1, len(rows) + 1)]:
        errors.append("candidate_id sequence is not contiguous")

    expected_sources = {record_id for record_id, _, _ in SOURCES}
    actual_sources = {row["source_record_id"] for row in rows}
    if actual_sources != expected_sources:
        errors.append(f"source coverage mismatch expected={sorted(expected_sources)} actual={sorted(actual_sources)}")
    for record_id, relative_path, expected_hash in SOURCES:
        if sha256_file(REPO / relative_path) != expected_hash:
            errors.append(f"source hash drift: {record_id}")
        source_rows = [row for row in rows if row["source_record_id"] == record_id]
        if not source_rows:
            errors.append(f"source has no atomic rows: {record_id}")
        if any(row["source_path"] != relative_path or row["source_sha256"] != expected_hash for row in source_rows):
            errors.append(f"source identity mismatch in rows: {record_id}")

    required_nonempty = [field for field in FIELDS if field not in {"conflict_pointer"}]
    for row in rows:
        missing = [field for field in required_nonempty if not row.get(field)]
        if missing:
            errors.append(f"{row.get('candidate_id', '?')} missing {','.join(missing)}")
        if row.get("approval_state") != "not-approved":
            errors.append(f"classification upgraded approval: {row.get('candidate_id')}")
        if row.get("approval_gap") != APPROVAL_GAP:
            errors.append(f"approval gap drift: {row.get('candidate_id')}")
        if row.get("statement_fingerprint") != fingerprint(row.get("statement_text", "")):
            errors.append(f"fingerprint mismatch: {row.get('candidate_id')}")

    counts = Counter(row["source_record_id"] for row in rows)
    result: dict[str, object] = {
        "total": len(rows),
        "sources": len(counts),
        "source_counts": dict(sorted(counts.items())),
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
            raise RuntimeError(
                f"Generated ledger drift: existing={len(rows)} rebuilt={len(rebuilt)} first_difference_index={first_difference}"
            )
    else:
        rows = build_rows()
        write_outputs(rows)
    print(json.dumps(verify(rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
