from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
CONTEXT_PATH = REPO / "CONTEXT.md"

INPUT_FIELDS = [
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

OUTPUT_FIELDS = INPUT_FIELDS + [
    "exact_text_sha256",
    "semantic_normalized_sha256",
    "exact_text_cluster_id",
    "normalized_text_cluster_id",
    "semantic_review_cluster_id",
    "relation_to_cluster_representative",
    "review_disposition",
    "approval_batch_id",
    "graduate_conflict_pointers",
    "version_scope_pointers",
]

RELATION_FIELDS = [
    "relation_id",
    "relation_type",
    "left_candidate_id",
    "right_candidate_id",
    "left_batch_id",
    "right_batch_id",
    "left_source_record_id",
    "right_source_record_id",
    "semantic_score",
    "trigram_dice",
    "bigram_dice",
    "identifier_jaccard",
    "scope_relation",
    "version_relation",
    "shared_identifiers",
    "review_action",
]

CLUSTER_FIELDS = [
    "cluster_id",
    "representative_candidate_id",
    "member_count",
    "batch_count",
    "source_count",
    "relation_types",
    "review_dispositions",
    "applicable_scopes",
    "version_scope_pointers",
    "member_candidate_ids",
    "representative_statement",
    "review_note",
]

DERIVATION_FIELDS = [
    "derivation_id",
    "child_source_record_id",
    "parent_source_record_id",
    "child_batch_id",
    "parent_batch_id",
    "candidate_rows_carrying_link",
    "sample_candidate_ids",
    "evidence_fragments",
    "review_note",
]

CONFLICT_FIELDS = [
    "conflict_pointer",
    "title",
    "classification",
    "candidate_rows",
    "approval_relevant_rows",
    "batches",
    "sources",
    "decision_ticket_title",
    "disposition_reason",
]

APPROVAL_BATCH_FIELDS = [
    "approval_batch_id",
    "review_domain",
    "required_owner_or_evidence_role",
    "candidate_rows",
    "semantic_review_units",
    "source_documents",
    "blocking_conflict_pointers",
    "suggested_sequence",
    "review_instruction",
]

CONSOLIDATED = ARTIFACT_DIR / "R01-R13-consolidated-atomic-candidates.tsv"
RELATIONS = ARTIFACT_DIR / "R01-R13-semantic-relations.tsv"
CLUSTERS = ARTIFACT_DIR / "R01-R13-semantic-review-clusters.tsv"
DERIVATIONS = ARTIFACT_DIR / "R01-R13-source-derivations.tsv"
CONFLICTS = ARTIFACT_DIR / "R01-R13-conflict-review.tsv"
APPROVAL_BATCHES = ARTIFACT_DIR / "R01-R13-approval-batch-suggestions.tsv"
SUMMARY = ARTIFACT_DIR / "R01-R13-consolidated-atomic-candidates-summary.json"

NONE_POINTER_RE = re.compile(r"^none(?:-found-within-r\d\d-pass)?$", re.IGNORECASE)
CONFLICT_RE = re.compile(r"\bCF-R\d{2}-\d{3}\b")
VERSION_SCOPE_RE = re.compile(r"\b(?:AD|SCOPE|BOUND)-R\d{2}-\d{3}\b")
SOURCE_RECORD_RE = re.compile(r"\bR\d{2}-\d{2}\b")
IDENTIFIER_RE = re.compile(
    r"(?:[A-Za-z][A-Za-z0-9]*(?:[_./:-][A-Za-z0-9]+)+|"
    r"[A-Z][A-Za-z0-9]{2,}|[A-Z]{2,}[0-9]*|\d+(?:\.\d+){1,3})"
)


CONFLICT_POLICY = {
    "CF-R01-001": {
        "title": "运输需求身份、对账键与取消抑制边界",
        "classification": "graduate-hitl-real-conflict",
        "ticket": "决定运输需求身份、对账键与取消抑制边界",
        "reason": (
            "TASK_TYPE+SUBLOT 与 product_lot+machine_no+finish_time/MES 事务 ID 会产生不同的"
            "重复、GONE 后再现和永久抑制结果；现有证据没有版本绑定足以自动择一。"
        ),
    },
    "CF-R01-002": {
        "title": "当前 MES 只读与卸货/完工回写边界",
        "classification": "graduate-hitl-real-conflict",
        "ticket": "决定当前 MES 只读与卸货、完工回写边界",
        "reason": (
            "多数材料主张当前阶段只读，早期简易需求仍主张服务器回写或由 OP/PDA 后续处理；"
            "二选一措辞不能被自动解释为只读，也不能由当前实现替代批准。"
        ),
    },
    "CF-R01-003": {
        "title": "AREA 到站点映射模型",
        "classification": "apparent-version-difference-converged",
        "ticket": "",
        "reason": (
            "冲突说明指向旧版纯人工显式映射；当前 BR-003 与 UC-024 已一致采用地图同步、"
            "命名规则自动派生和少量显式覆盖。保留旧差异为版本证据，不再生成 HITL。"
        ),
    },
    "CF-R09-001": {
        "title": "QUEUEING 滞留与下单前清积压策略",
        "classification": "graduate-hitl-real-conflict",
        "ticket": "决定 QUEUEING 滞留与下单前清积压策略",
        "reason": (
            "ADR 主张下新单前清除 QUEUEING/HELD 积压，而 UC-008 假定 RIoT 始终只有 0/1 个移动单；"
            "自动清理还会影响受控取消与未知结果边界，需要业务决定。"
        ),
    },
    "CF-R09-002": {
        "title": "充电失败改派的备用桩筛选与排队关系",
        "classification": "graduate-hitl-real-conflict",
        "ticket": "决定充电失败改派的备用桩筛选与排队关系",
        "reason": (
            "ADR 只明确允许集合、排除失败站并按 Near 选择，BR-007 还要求有效、空闲、未占用/未预占"
            "及电量排队；两者是否为同一筛选链会改变抢占、等待和改派结果。"
        ),
    },
    "CF-R10-001": {
        "title": "模拟器排除材料中的锁 DI 与故障枚举不一致",
        "classification": "out-of-scope-technical-review",
        "ticket": "",
        "reason": (
            "该指针只保留被排除的模拟器技术材料内部不一致；票据 50 已明确它不毕业为本地图的"
            "主系统需求决定，后续技术设计复核另行处理。"
        ),
    },
}

GRADUATE_CONFLICTS = {
    pointer for pointer, policy in CONFLICT_POLICY.items()
    if policy["classification"] == "graduate-hitl-real-conflict"
}


@dataclass(frozen=True)
class Similarity:
    score: float
    tri: float
    bi: float
    identifiers: float
    shared_identifiers: tuple[str, ...]


class UnionFind:
    def __init__(self, values: Iterable[str]):
        self.parent = {value: value for value in values}
        self.rank = {value: 0 for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        a, b = self.find(left), self.find(right)
        if a == b:
            return
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != INPUT_FIELDS:
            raise RuntimeError(f"Unexpected input fields for {path.name}: {reader.fieldnames}")
        return list(reader)


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def normalize_exact(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"[`*_#>\[\]()]", "", value)
    return re.sub(r"\s+", "", value)


def load_term_aliases() -> list[tuple[str, str]]:
    text = CONTEXT_PATH.read_text(encoding="utf-8-sig")
    aliases: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\*\*(.+?)\*\*:$", line.strip())
        if not match:
            continue
        display = match.group(1).strip()
        bilingual = re.match(r"^(.+?)（([^（）]+)）$", display)
        if bilingual:
            chinese, code = bilingual.group(1).strip(), bilingual.group(2).strip()
            canonical = code.casefold()
            aliases[chinese.casefold()] = canonical
            aliases[code.casefold()] = canonical
            aliases[display.casefold()] = canonical
        else:
            canonical = re.sub(r"\s+", "", display).casefold()
            aliases[display.casefold()] = canonical
    return sorted(aliases.items(), key=lambda pair: (-len(pair[0]), pair[0]))


def semantic_normalize(value: str, aliases: list[tuple[str, str]]) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    for alias, canonical in aliases:
        if len(alias) >= 2:
            if re.fullmatch(r"[a-z0-9_.:/+ -]+", alias):
                value = re.sub(
                    rf"(?<![a-z0-9_]){re.escape(alias)}(?![a-z0-9_])",
                    f" {canonical} ",
                    value,
                )
            else:
                value = value.replace(alias, f" {canonical} ")
    value = value.replace("不得", " 禁止 ").replace("不能", " 禁止 ").replace("不允许", " 禁止 ")
    value = value.replace("仅允许", " 仅 ").replace("只允许", " 仅 ")
    value = re.sub(r"[^0-9a-z\u4e00-\u9fff_.:/+-]+", " ", value)
    return " ".join(value.split())


def compact_chars(value: str) -> str:
    return re.sub(r"\s+", "", value)


def ngrams(value: str, size: int) -> set[str]:
    compact = compact_chars(value)
    if len(compact) < size:
        return {compact} if compact else set()
    return {compact[index:index + size] for index in range(len(compact) - size + 1)}


def identifiers(value: str) -> set[str]:
    return {token.casefold() for token in IDENTIFIER_RE.findall(value) if len(token) >= 3}


def dice(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return 2.0 * len(left & right) / (len(left) + len(right))


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def negation_signature(value: str) -> tuple[bool, bool]:
    return (
        bool(re.search(r"(?:禁止|不得|不能|不允许|不应|不|无|未|not|never|must not)", value)),
        bool(re.search(r"(?:仅|只|唯一|only)", value)),
    )


def pointer_tokens(value: str, pattern: re.Pattern[str]) -> list[str]:
    return sorted(set(pattern.findall(value or "")))


def domain_tags(row: dict[str, str]) -> set[str]:
    value = " ".join((row["applicable_scope"], row["candidate_class"], row["statement_text"])).casefold()
    tags: set[str] = set()
    checks = [
        ("simulator", r"simulator|模拟器"),
        ("charging-parking", r"charg|充电|停车|停靠点|parking"),
        ("identity-security", r"identity|security|auth|credential|operator|角色|身份|权限|凭证|审计"),
        ("mes-demand-data", r"\bmes\b|transportdemand|sublot|oracle|sql|数据契约|回写|工序"),
        ("riot-control", r"\briot\b|openapi|routecost|nearstation|orderhold|emergenc|物模型"),
        ("slot-hardware-safety", r"slot|hardware|仓位|仓门|光幕|开锁|安全|io\b|modbus"),
        ("site-operations", r"site-operation|loadbatch|unload|stopclosure|装货|卸货|离站|站点作业"),
        ("fleet-dispatch", r"dispatch|fleet|agv|车辆|派车|调度|路径|地图|station"),
        ("cross-domain-language", r"domain-term|canonical-term|vocabulary|cross-domain|词汇|术语|领域"),
        ("workflow-governance", r"workflow|governance|流程模板|治理|版本基线"),
        ("nonfunctional", r"nonfunctional|nfr|performance|availability|性能|可用性|恢复时间"),
    ]
    for tag, pattern in checks:
        if re.search(pattern, value):
            tags.add(tag)
    return tags or {"general-project-scope"}


def scope_relation(left: dict[str, str], right: dict[str, str]) -> str:
    if left["applicable_scope"] == right["applicable_scope"]:
        return "same-scope"
    overlap = domain_tags(left) & domain_tags(right)
    return "compatible-domain-scope" if overlap else "different-domain-scope"


def version_markers(row: dict[str, str]) -> set[str]:
    value = " ".join((row["applicable_scope"], row["duplicate_or_derivation"], row["conflict_pointer"]))
    markers = set(VERSION_SCOPE_RE.findall(value))
    markers.update(re.findall(r"\b20\d{2}-\d{2}-\d{2}\b|\bv?\d+\.\d+(?:\.\d+){0,2}\b", value, re.IGNORECASE))
    return {marker.casefold() for marker in markers}


def version_relation(left: dict[str, str], right: dict[str, str]) -> str:
    a, b = version_markers(left), version_markers(right)
    if not a and not b:
        return "no-explicit-version-marker"
    if a == b:
        return "same-version-markers"
    if a & b:
        return "overlapping-version-markers"
    return "different-version-or-scope-markers"


def similarity(
    left: dict[str, object],
    right: dict[str, object],
) -> Similarity:
    tri = dice(left["_tri"], right["_tri"])
    bi = dice(left["_bi"], right["_bi"])
    id_score = jaccard(left["_ids"], right["_ids"])
    shared = tuple(sorted(left["_ids"] & right["_ids"]))
    score = 0.55 * tri + 0.30 * bi + 0.15 * id_score
    return Similarity(score, tri, bi, id_score, shared)


def review_disposition(row: dict[str, str]) -> str:
    route = row["baseline_route"]
    if route == "exclude-from-requirement-approval":
        return "excluded-not-for-requirement-approval"
    if "evidence-only" in route or route in {"test-plan-evidence-only", "source-or-traceability-evidence-only"}:
        return "evidence-only"
    conflicts = set(pointer_tokens(row["conflict_pointer"], CONFLICT_RE)) & GRADUATE_CONFLICTS
    if route == "hold-for-conflict-decision" or conflicts:
        return "hold-for-hitl-conflict-decision"
    if route in {"needs-question-resolution", "needs-atomic-reframing-before-approval"}:
        return "hold-for-question-or-reframing"
    return "approval-candidate-not-approved"


def review_domain(row: dict[str, str]) -> str:
    tags = domain_tags(row)
    priority = [
        "simulator",
        "nonfunctional",
        "charging-parking",
        "identity-security",
        "mes-demand-data",
        "riot-control",
        "slot-hardware-safety",
        "site-operations",
        "cross-domain-language",
        "fleet-dispatch",
        "workflow-governance",
        "general-project-scope",
    ]
    return next(tag for tag in priority if tag in tags)


def owner_role(route: str) -> str:
    checks = [
        (r"simulator.*interface", "simulator-interface-owner"),
        (r"simulator.*hardware", "simulator-hardware-owner"),
        (r"simulator", "simulator-product-owner"),
        (r"domain-owner", "domain-owner-and-final-approver"),
        (r"hardware|safety|capacity|loading-safety", "hardware-safety-authority-and-final-approver"),
        (r"security|identity|role", "security-identity-owner-and-final-approver"),
        (r"interface|contract|data-source|data-contract", "interface-or-data-contract-owner-and-final-approver"),
        (r"operations|acceptance", "operations-or-acceptance-owner-and-final-approver"),
        (r"operator-product|product-owner", "product-owner-and-final-approver"),
        (r"business-owner", "business-owner-and-final-approver"),
        (r"responsible-owner", "assigned-responsible-owner-and-final-approver"),
        (r"signature", "agreement-custodian-and-final-approver"),
    ]
    for pattern, role in checks:
        if re.search(pattern, route):
            return role
    return "source-custodian-and-final-approver"


DOMAIN_CODES = {
    "simulator": "SIM",
    "nonfunctional": "NFR",
    "charging-parking": "CHG",
    "identity-security": "IAM",
    "mes-demand-data": "MES",
    "riot-control": "RIOT",
    "slot-hardware-safety": "SLOT",
    "site-operations": "SITE",
    "cross-domain-language": "LANG",
    "fleet-dispatch": "DSP",
    "workflow-governance": "WF",
    "general-project-scope": "GEN",
}


OWNER_CODES = {
    "simulator-interface-owner": "IF",
    "simulator-hardware-owner": "HW",
    "simulator-product-owner": "PO",
    "domain-owner-and-final-approver": "DOM",
    "hardware-safety-authority-and-final-approver": "SAFE",
    "security-identity-owner-and-final-approver": "SEC",
    "interface-or-data-contract-owner-and-final-approver": "IF",
    "operations-or-acceptance-owner-and-final-approver": "OPS",
    "product-owner-and-final-approver": "PO",
    "business-owner-and-final-approver": "BO",
    "assigned-responsible-owner-and-final-approver": "OWN",
    "agreement-custodian-and-final-approver": "AGR",
    "source-custodian-and-final-approver": "SRC",
}


def approval_batch_id(row: dict[str, str]) -> str:
    if review_disposition(row) != "approval-candidate-not-approved":
        return ""
    domain = review_domain(row)
    owner = owner_role(row["baseline_route"])
    return f"AP-{DOMAIN_CODES[domain]}-{OWNER_CODES[owner]}"


def load_inputs() -> tuple[list[dict[str, str]], dict[str, str]]:
    rows: list[dict[str, str]] = []
    input_hashes: dict[str, str] = {}
    for index in range(1, 14):
        batch = f"R{index:02d}"
        path = ARTIFACT_DIR / f"{batch}-atomic-candidates.tsv"
        batch_rows = read_tsv(path)
        if any(row["batch_id"] != batch for row in batch_rows):
            raise RuntimeError(f"Batch identity drift in {path.name}")
        rows.extend(batch_rows)
        input_hashes[path.name] = sha256_file(path)
    return rows, input_hashes


def group_ids(groups: dict[str, list[str]], prefix: str) -> dict[str, str]:
    result: dict[str, str] = {}
    ordered = sorted(
        (members for members in groups.values() if len(members) > 1),
        key=lambda members: tuple(sorted(members)),
    )
    for index, members in enumerate(ordered, 1):
        cluster_id = f"{prefix}-{index:04d}"
        for candidate_id in members:
            result[candidate_id] = cluster_id
    return result


def build_relations(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, str], dict[str, str]]:
    exact_groups: dict[str, list[str]] = defaultdict(list)
    normalized_groups: dict[str, list[str]] = defaultdict(list)
    by_id = {row["candidate_id"]: row for row in rows}
    for row in rows:
        exact_groups[row["exact_text_sha256"]].append(row["candidate_id"])
        normalized_groups[row["semantic_normalized_sha256"]].append(row["candidate_id"])
    exact_cluster = group_ids(exact_groups, "EX")
    normalized_cluster = group_ids(normalized_groups, "NX")

    relations: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()

    def add_relation(left_id: str, right_id: str, relation_type: str, sim: Similarity | None = None) -> None:
        left_id, right_id = sorted((left_id, right_id))
        key = (left_id, right_id)
        if key in seen:
            return
        seen.add(key)
        left, right = by_id[left_id], by_id[right_id]
        sim = sim or similarity(left, right)
        scope = scope_relation(left, right)
        version = version_relation(left, right)
        action = "review-together-never-auto-merge"
        if version == "different-version-or-scope-markers":
            action = "retain-separate-version-scope-and-review-link"
        elif scope == "different-domain-scope":
            action = "retain-separate-scope-and-review-link"
        relations.append({
            "relation_id": "",
            "relation_type": relation_type,
            "left_candidate_id": left_id,
            "right_candidate_id": right_id,
            "left_batch_id": left["batch_id"],
            "right_batch_id": right["batch_id"],
            "left_source_record_id": left["source_record_id"],
            "right_source_record_id": right["source_record_id"],
            "semantic_score": f"{sim.score:.4f}",
            "trigram_dice": f"{sim.tri:.4f}",
            "bigram_dice": f"{sim.bi:.4f}",
            "identifier_jaccard": f"{sim.identifiers:.4f}",
            "scope_relation": scope,
            "version_relation": version,
            "shared_identifiers": ",".join(sim.shared_identifiers),
            "review_action": action,
        })

    for members in exact_groups.values():
        if len(members) > 1:
            anchor = sorted(members)[0]
            for member in sorted(members)[1:]:
                add_relation(anchor, member, "exact-text-duplicate")

    for members in normalized_groups.values():
        if len(members) > 1:
            anchor = sorted(members)[0]
            for member in sorted(members)[1:]:
                if by_id[anchor]["exact_text_sha256"] != by_id[member]["exact_text_sha256"]:
                    add_relation(anchor, member, "normalized-text-duplicate")

    # Semantic-near discovery works on one representative per normalized text.
    representatives = [by_id[sorted(members)[0]] for members in normalized_groups.values()]
    trigram_df: Counter[str] = Counter()
    for row in representatives:
        trigram_df.update(row["_tri"])
    postings: dict[str, list[str]] = defaultdict(list)
    for row in representatives:
        rare = sorted(row["_tri"], key=lambda gram: (trigram_df[gram], gram))[:16]
        for gram in rare:
            if trigram_df[gram] <= 90:
                postings[gram].append(row["candidate_id"])
    pair_hits: Counter[tuple[str, str]] = Counter()
    for member_ids in postings.values():
        member_ids = sorted(set(member_ids))
        for left_index, left_id in enumerate(member_ids):
            for right_id in member_ids[left_index + 1:]:
                pair_hits[(left_id, right_id)] += 1

    proposals: list[tuple[float, str, str, Similarity]] = []
    for (left_id, right_id), hits in pair_hits.items():
        if hits < 2:
            continue
        left, right = by_id[left_id], by_id[right_id]
        if left["source_record_id"] == right["source_record_id"]:
            continue
        approval_reviewable = {
            "approval-candidate-not-approved",
            "hold-for-hitl-conflict-decision",
            "hold-for-question-or-reframing",
        }
        if review_disposition(left) not in approval_reviewable or review_disposition(right) not in approval_reviewable:
            continue
        if scope_relation(left, right) == "different-domain-scope":
            continue
        compact_left, compact_right = compact_chars(left["_semantic_norm"]), compact_chars(right["_semantic_norm"])
        length_ratio = min(len(compact_left), len(compact_right)) / max(len(compact_left), len(compact_right), 1)
        if length_ratio < 0.52:
            continue
        sim = similarity(left, right)
        same_negation = negation_signature(left["_semantic_norm"]) == negation_signature(right["_semantic_norm"])
        qualifies = (
            sim.score >= 0.76 and sim.tri >= 0.58 and same_negation
        ) or (
            sim.score >= 0.70 and sim.tri >= 0.52 and len(sim.shared_identifiers) >= 2 and same_negation
        )
        if qualifies:
            proposals.append((sim.score, left_id, right_id, sim))

    degree: Counter[str] = Counter()
    for score, left_id, right_id, sim in sorted(proposals, reverse=True):
        if score < 0.88 and (degree[left_id] >= 4 or degree[right_id] >= 4):
            continue
        add_relation(left_id, right_id, "semantic-near-review", sim)
        degree[left_id] += 1
        degree[right_id] += 1

    relations.sort(key=lambda row: (
        row["relation_type"], row["left_candidate_id"], row["right_candidate_id"]
    ))
    for index, relation in enumerate(relations, 1):
        relation["relation_id"] = f"REL-{index:05d}"
    return relations, exact_cluster, normalized_cluster


def build_clusters(
    rows: list[dict[str, object]], relations: list[dict[str, object]]
) -> tuple[list[dict[str, object]], dict[str, str], dict[str, str]]:
    by_id = {row["candidate_id"]: row for row in rows}
    union = UnionFind(by_id)
    relation_types_by_root: dict[str, set[str]] = defaultdict(set)
    for relation in relations:
        union.union(relation["left_candidate_id"], relation["right_candidate_id"])
    members_by_root: dict[str, list[str]] = defaultdict(list)
    for candidate_id in by_id:
        members_by_root[union.find(candidate_id)].append(candidate_id)
    for relation in relations:
        root = union.find(relation["left_candidate_id"])
        relation_types_by_root[root].add(relation["relation_type"])

    multi = [sorted(members) for members in members_by_root.values() if len(members) > 1]
    multi.sort(key=lambda members: tuple(members))
    cluster_rows: list[dict[str, object]] = []
    cluster_by_candidate: dict[str, str] = {}
    representative_by_candidate: dict[str, str] = {}
    for index, members in enumerate(multi, 1):
        cluster_id = f"SC-{index:04d}"
        representative = min(
            members,
            key=lambda candidate_id: (
                0 if review_disposition(by_id[candidate_id]) == "approval-candidate-not-approved" else 1,
                candidate_id,
            ),
        )
        root = union.find(members[0])
        for member in members:
            cluster_by_candidate[member] = cluster_id
            representative_by_candidate[member] = representative
        relation_types = sorted(relation_types_by_root[root])
        version_pointers = sorted({
            pointer
            for member in members
            for pointer in pointer_tokens(by_id[member]["conflict_pointer"], VERSION_SCOPE_RE)
        })
        note = "仅供共同审阅；保留每条来源、范围、版本与批准状态，不自动合并或删除。"
        if version_pointers:
            note += " 含显式版本/范围指针，任何统一文本必须另行证明适用范围。"
        cluster_rows.append({
            "cluster_id": cluster_id,
            "representative_candidate_id": representative,
            "member_count": len(members),
            "batch_count": len({by_id[member]["batch_id"] for member in members}),
            "source_count": len({by_id[member]["source_record_id"] for member in members}),
            "relation_types": ",".join(relation_types),
            "review_dispositions": ",".join(sorted({review_disposition(by_id[member]) for member in members})),
            "applicable_scopes": " | ".join(sorted({by_id[member]["applicable_scope"] for member in members})),
            "version_scope_pointers": ",".join(version_pointers),
            "member_candidate_ids": ",".join(members),
            "representative_statement": by_id[representative]["statement_text"],
            "review_note": note,
        })
    return cluster_rows, cluster_by_candidate, representative_by_candidate


def build_derivations(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    source_batches = {row["source_record_id"]: row["batch_id"] for row in rows}
    links: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        child = row["source_record_id"]
        for parent in SOURCE_RECORD_RE.findall(row["duplicate_or_derivation"]):
            if parent != child and parent in source_batches:
                links[(child, parent)].append(row)
    output: list[dict[str, object]] = []
    for index, ((child, parent), evidence_rows) in enumerate(sorted(links.items()), 1):
        fragments = sorted({
            fragment.strip()
            for row in evidence_rows
            for fragment in row["duplicate_or_derivation"].split(";")
            if parent in fragment
        })
        output.append({
            "derivation_id": f"DRV-{index:04d}",
            "child_source_record_id": child,
            "parent_source_record_id": parent,
            "child_batch_id": source_batches[child],
            "parent_batch_id": source_batches[parent],
            "candidate_rows_carrying_link": len(evidence_rows),
            "sample_candidate_ids": ",".join(row["candidate_id"] for row in evidence_rows[:12]),
            "evidence_fragments": " | ".join(fragments[:8]),
            "review_note": "文档声明的来源/重叠关系；不传递权威性或批准，逐条声明仍保留独立身份。",
        })
    return output


def build_conflicts(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for pointer, policy in CONFLICT_POLICY.items():
        matched = [row for row in rows if pointer in pointer_tokens(row["conflict_pointer"], CONFLICT_RE)]
        relevant = [
            row for row in matched
            if review_disposition(row) not in {"evidence-only", "excluded-not-for-requirement-approval"}
        ]
        output.append({
            "conflict_pointer": pointer,
            "title": policy["title"],
            "classification": policy["classification"],
            "candidate_rows": len(matched),
            "approval_relevant_rows": len(relevant),
            "batches": ",".join(sorted({row["batch_id"] for row in matched})),
            "sources": ",".join(sorted({row["source_record_id"] for row in matched})),
            "decision_ticket_title": policy["ticket"],
            "disposition_reason": policy["reason"],
        })
    return output


def build_approval_batches(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        batch_id = row["approval_batch_id"]
        if batch_id:
            grouped[batch_id].append(row)
    output: list[dict[str, object]] = []
    for batch_id, members in sorted(grouped.items()):
        domain = review_domain(members[0])
        owner = owner_role(members[0]["baseline_route"])
        blockers = sorted({
            pointer
            for row in members
            for pointer in pointer_tokens(row["conflict_pointer"], CONFLICT_RE)
            if pointer in GRADUATE_CONFLICTS
        })
        semantic_units = {
            row["semantic_review_cluster_id"] or row["candidate_id"]
            for row in members
        }
        output.append({
            "approval_batch_id": batch_id,
            "review_domain": domain,
            "required_owner_or_evidence_role": owner,
            "candidate_rows": len(members),
            "semantic_review_units": len(semantic_units),
            "source_documents": len({row["source_record_id"] for row in members}),
            "blocking_conflict_pointers": ",".join(blockers),
            "suggested_sequence": "after-conflict-decisions" if blockers else "after-candidate-baseline-entry-formation",
            "review_instruction": (
                "按语义审阅簇共同查看多来源证据，但逐条确认范围、版本/哈希和规范文本；"
                "本建议不分配 REQ ID、不合并声明、不构成批准。"
            ),
        })
    return output


def segment_approval_batches(rows: list[dict[str, object]]) -> None:
    """Split broad owner/domain suggestions into reviewable, cluster-safe parts."""
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        if row["approval_batch_id"]:
            grouped[row["approval_batch_id"]].append(row)
    for base_id, members in grouped.items():
        units: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in members:
            unit_id = row["semantic_review_cluster_id"] or row["candidate_id"]
            units[unit_id].append(row)
        ordered_units = [units[unit_id] for unit_id in sorted(units)]
        parts: list[list[list[dict[str, object]]]] = []
        current: list[list[dict[str, object]]] = []
        current_rows = 0
        for unit in ordered_units:
            if current and (len(current) >= 120 or current_rows + len(unit) > 180):
                parts.append(current)
                current = []
                current_rows = 0
            current.append(unit)
            current_rows += len(unit)
        if current:
            parts.append(current)
        for part_index, part in enumerate(parts, 1):
            part_id = base_id if len(parts) == 1 else f"{base_id}-{part_index:02d}"
            for unit in part:
                for row in unit:
                    row["approval_batch_id"] = part_id


def build_all() -> tuple[dict[str, object], dict[Path, tuple[list[str], list[dict[str, object]]]]]:
    input_rows, input_hashes = load_inputs()
    if len(input_rows) != 12452:
        raise RuntimeError(f"Input row-count drift: expected=12452 actual={len(input_rows)}")
    ids = [row["candidate_id"] for row in input_rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Candidate IDs are not globally unique")
    if any(row["approval_state"] != "not-approved" for row in input_rows):
        raise RuntimeError("Approval isolation violated in input ledgers")

    aliases = load_term_aliases()
    context_sha256 = sha256_file(CONTEXT_PATH)
    rows: list[dict[str, object]] = []
    for source in input_rows:
        row: dict[str, object] = dict(source)
        semantic_norm = semantic_normalize(source["statement_text"], aliases)
        row["exact_text_sha256"] = sha256_text(unicodedata.normalize("NFC", source["statement_text"]))
        row["semantic_normalized_sha256"] = sha256_text(semantic_norm)
        row["_semantic_norm"] = semantic_norm
        row["_tri"] = ngrams(semantic_norm, 3)
        row["_bi"] = ngrams(semantic_norm, 2)
        row["_ids"] = identifiers(semantic_norm)
        row["review_disposition"] = review_disposition(source)
        row["approval_batch_id"] = approval_batch_id(source)
        row["graduate_conflict_pointers"] = ",".join(sorted(
            set(pointer_tokens(source["conflict_pointer"], CONFLICT_RE)) & GRADUATE_CONFLICTS
        ))
        row["version_scope_pointers"] = ",".join(pointer_tokens(source["conflict_pointer"], VERSION_SCOPE_RE))
        rows.append(row)

    relations, exact_cluster, normalized_cluster = build_relations(rows)
    clusters, semantic_cluster, representative = build_clusters(rows, relations)
    for row in rows:
        candidate_id = row["candidate_id"]
        row["exact_text_cluster_id"] = exact_cluster.get(candidate_id, "")
        row["normalized_text_cluster_id"] = normalized_cluster.get(candidate_id, "")
        row["semantic_review_cluster_id"] = semantic_cluster.get(candidate_id, "")
        cluster_rep = representative.get(candidate_id, candidate_id)
        if cluster_rep == candidate_id:
            relation = "cluster-representative" if candidate_id in semantic_cluster else "singleton"
        else:
            relation = f"review-with:{cluster_rep}"
        row["relation_to_cluster_representative"] = relation

    segment_approval_batches(rows)

    derivations = build_derivations(rows)
    conflicts = build_conflicts(rows)
    approval_batches = build_approval_batches(rows)
    clean_rows = [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows]

    output_payloads = {
        CONSOLIDATED: (OUTPUT_FIELDS, clean_rows),
        RELATIONS: (RELATION_FIELDS, relations),
        CLUSTERS: (CLUSTER_FIELDS, clusters),
        DERIVATIONS: (DERIVATION_FIELDS, derivations),
        CONFLICTS: (CONFLICT_FIELDS, conflicts),
        APPROVAL_BATCHES: (APPROVAL_BATCH_FIELDS, approval_batches),
    }

    relation_counts = Counter(row["relation_type"] for row in relations)
    disposition_counts = Counter(row["review_disposition"] for row in rows)
    summary = {
        "schema_version": 1,
        "total": len(rows),
        "batches": dict(sorted(Counter(row["batch_id"] for row in rows).items())),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "input_ledger_sha256": input_hashes,
        "context_sha256_for_semantic_vocabulary": context_sha256,
        "context_term_aliases": len(aliases),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "review_dispositions": dict(sorted(disposition_counts.items())),
        "relation_counts": dict(sorted(relation_counts.items())),
        "relation_total": len(relations),
        "semantic_review_clusters": len(clusters),
        "clustered_candidate_rows": sum(int(row["member_count"]) for row in clusters),
        "source_derivation_links": len(derivations),
        "conflict_classifications": dict(sorted(Counter(row["classification"] for row in conflicts).items())),
        "graduate_hitl_conflicts": sorted(GRADUATE_CONFLICTS),
        "approval_batch_suggestions": len(approval_batches),
        "approval_candidate_rows": disposition_counts["approval-candidate-not-approved"],
        "approval_batch_candidate_rows": sum(int(row["candidate_rows"]) for row in approval_batches),
        "artifacts": {path.name: len(payload[1]) for path, payload in output_payloads.items()},
        "semantic_method": {
            "exact": "NFC-identical statement_text SHA-256",
            "normalized": "NFKC/casefold/Markdown-whitespace normalization plus CONTEXT.md canonical-term aliases",
            "near": "rare character-trigram candidate generation; weighted trigram/bigram/identifier similarity; same negation signature; compatible domain scope",
            "guardrail": "relations are review links only; no source row is merged, deleted, approved, or assigned a permanent REQ ID",
        },
    }
    return summary, output_payloads


def compare_tsv(path: Path, fields: list[str], expected: list[dict[str, object]]) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing output: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != fields:
            raise RuntimeError(f"Output field drift: {path.name}")
        actual = list(reader)
    normalized_expected = [{field: str(row.get(field, "")) for field in fields} for row in expected]
    if actual != normalized_expected:
        raise RuntimeError(f"Generated output drift: {path.name}")


def verify(summary: dict[str, object], payloads: dict[Path, tuple[list[str], list[dict[str, object]]]]) -> None:
    for path, (fields, rows) in payloads.items():
        compare_tsv(path, fields, rows)
    if not SUMMARY.exists():
        raise RuntimeError(f"Missing output: {SUMMARY}")
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8-sig"))
    if actual_summary != summary:
        raise RuntimeError("Generated summary drift")

    consolidated_rows = payloads[CONSOLIDATED][1]
    if len(consolidated_rows) != 12452:
        raise RuntimeError("Consolidated total must remain 12452")
    if any(row["approval_state"] != "not-approved" for row in consolidated_rows):
        raise RuntimeError("Consolidation upgraded an approval state")
    approval_candidates = [row for row in consolidated_rows if row["review_disposition"] == "approval-candidate-not-approved"]
    if any(not row["approval_batch_id"] for row in approval_candidates):
        raise RuntimeError("An approval candidate lacks an approval batch suggestion")
    if any(row["approval_batch_id"] for row in consolidated_rows if row["review_disposition"] != "approval-candidate-not-approved"):
        raise RuntimeError("A hold/evidence/excluded row leaked into an approval batch")
    conflict_rows = payloads[CONFLICTS][1]
    graduates = {row["conflict_pointer"] for row in conflict_rows if row["classification"] == "graduate-hitl-real-conflict"}
    if graduates != GRADUATE_CONFLICTS:
        raise RuntimeError(f"Conflict graduation drift: {graduates}")
    relation_ids = [row["relation_id"] for row in payloads[RELATIONS][1]]
    if len(relation_ids) != len(set(relation_ids)):
        raise RuntimeError("Duplicate semantic relation IDs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    summary, payloads = build_all()
    if args.verify_only:
        verify(summary, payloads)
        print(
            "R01-R13 consolidated candidates verified: "
            f"total={summary['total']} sources={summary['source_documents']} "
            f"relations={summary['relation_total']} clusters={summary['semantic_review_clusters']} "
            f"approval_candidates={summary['approval_candidate_rows']} "
            f"approval_batches={summary['approval_batch_suggestions']} "
            f"graduate_hitl={len(summary['graduate_hitl_conflicts'])} "
            f"approval_upgrades={summary['approval_upgrades']}"
        )
        return
    for path, (fields, rows) in payloads.items():
        write_tsv(path, fields, rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verify(summary, payloads)
    print(
        "R01-R13 consolidated candidates built and verified: "
        f"total={summary['total']} relations={summary['relation_total']} "
        f"clusters={summary['semantic_review_clusters']} "
        f"approval_batches={summary['approval_batch_suggestions']}"
    )


if __name__ == "__main__":
    main()
