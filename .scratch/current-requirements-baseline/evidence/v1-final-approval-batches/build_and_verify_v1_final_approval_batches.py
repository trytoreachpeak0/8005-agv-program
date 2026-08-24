from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EFFORT = ROOT / ".scratch" / "current-requirements-baseline"
ISSUES = EFFORT / "issues"
SOURCE_DIR = EFFORT / "evidence" / "v1-canonical-candidates"
LEGACY_DIR = EFFORT / "evidence" / "atomic-candidates"
OUT_DIR = Path(__file__).resolve().parent

CANDIDATES = SOURCE_DIR / "v1-canonical-requirement-candidates.tsv"
LEGACY_BATCHES = LEGACY_DIR / "R01-R13-approval-batch-suggestions.tsv"
EXPECTED_CANDIDATE_LEDGER_SHA256 = "9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646"
FIRST_APPROVAL_ISSUE = 89
MAX_ITEMS_PER_BATCH = 4

MANIFEST = OUT_DIR / "v1-final-approval-batches.tsv"
LEGACY_REVIEW = OUT_DIR / "legacy-102-batch-suggestion-review.tsv"
SUMMARY = OUT_DIR / "v1-final-approval-batches-summary.json"
README = OUT_DIR / "README.md"
HISTORY_HEADING = re.compile(r"(?m)^## (?:Superseded Answer[^\r\n]*|Answer|Comments)\s*$")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_bytes(fieldnames: list[str], rows: list[dict[str, object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def merge_approval_history(path: Path, generated: bytes) -> bytes:
    if not path.exists():
        return generated
    existing = path.read_text(encoding="utf-8-sig")
    match = HISTORY_HEADING.search(existing)
    if not match:
        return generated
    history = existing[match.start():].strip()
    history = re.sub(
        r"(?m)^## Answer\s*$",
        "## Superseded Answer — 2026-08-24 candidate-ledger SHA correction",
        history,
    )
    return generated.rstrip() + b"\n\n" + history.encode("utf-8") + b"\n"


def normalized_saved_approval_base(path: Path) -> bytes:
    existing = path.read_text(encoding="utf-8-sig")
    match = HISTORY_HEADING.search(existing)
    base = existing[:match.start()] if match else existing
    base = re.sub(r"(?m)^Status:\s*(?:open|claimed|resolved)\s*$", "Status: open", base)
    return (base.rstrip() + "\n").encode("utf-8")


def clean_inline(value: str) -> str:
    return " ".join((value or "").replace("|", "／").split())


def clean_exact_inline(value: str) -> str:
    return " ".join((value or "").split())


def source_label(source: str) -> str:
    labels = {
        ".scratch/new-mes-ingest/spec.md": "新版 MesIngest 当前规范",
        ".scratch/mes-ingest-bounded-storage-low-memory/spec.md": "有界存储与低内存规范",
        ".scratch/mes-ingest-watch-area-live-sync/spec.md": "Watch AREA 实时同步规范",
        ".scratch/demand-series-inspector-e/spec.md": "Demand Series Inspector E 规范",
    }
    if source in labels:
        return labels[source]
    issue_path = ROOT / source
    if issue_path.exists():
        first = issue_path.read_text(encoding="utf-8-sig").splitlines()[0]
        if first.startswith("# "):
            return first[2:].strip()
    return Path(source).stem


def review_role(row: dict[str, str]) -> str:
    layer = row["source_layer"]
    if layer == "L1-base-current-source":
        return "MesIngest 产品、数据契约责任人与最终批准人"
    if layer == "L2-partial-later-layer":
        return "SQL Server、容量与存储责任人与最终批准人"
    if layer in {"L3-partial-later-layer", "L4-partial-later-layer"}:
        return "MesIngestWatch 产品、现场运维责任人与最终批准人"
    return "该既有产品／领域决定的责任人与最终批准人"


def payload_sha(rows: list[dict[str, str]]) -> str:
    parts = []
    for row in rows:
        parts.append(
            "\x1f".join(
                [
                    row["req_candidate_id"],
                    row["canonical_text_sha256"],
                    row["scope"],
                    row["verification_method"],
                    row["primary_source"],
                    row["exact_location"],
                    row["source_sha256"],
                ]
            )
        )
    return sha256_bytes("\x1e".join(parts).encode("utf-8"))


def split_batches(rows: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    groups: list[list[dict[str, str]]] = []
    current_source = ""
    current: list[dict[str, str]] = []
    for row in rows:
        if current and (row["primary_source"] != current_source or len(current) == MAX_ITEMS_PER_BATCH):
            groups.append(current)
            current = []
        current_source = row["primary_source"]
        current.append(row)
    if current:
        groups.append(current)
    return groups


def render_candidate(row: dict[str, str]) -> str:
    req = row["req_candidate_id"]
    return f"""### {req} — {clean_inline(row['title'])}

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `{req}`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** {clean_exact_inline(row['canonical_text'])}
- **适用范围：** {clean_inline(row['scope'])}
- **验证方法：** {clean_inline(row['verification_method'])}
- **精确来源：** [{clean_inline(row['primary_source'])}](../../../{row['primary_source']})；`{clean_inline(row['exact_location'])}`；来源 SHA-256 `{row['source_sha256']}`。
- **来源批准边界：** {clean_inline(row['source_authority'])}；{clean_inline(row['source_approval_evidence'])}。
- **形成与 AI 边界：** `{clean_inline(row['derivation'])}`；AI 参与 `{clean_inline(row['ai_involvement'])}`；来源层差异：{clean_inline(row['source_layers_and_differences'])}。
- **首版前替代与冲突处置：** {clean_inline(row['prebaseline_source_supersession'])}；{clean_inline(row['conflict_disposition'])}。
- **决定／旧候选指针：** {clean_inline(row['decision_pointers'])}；{clean_inline(row['legacy_candidate_ids'])}。
- **规范文本 SHA-256：** `{row['canonical_text_sha256']}`。
"""


def render_ticket(issue_number: int, batch_index: int, rows: list[dict[str, str]]) -> tuple[str, str, str]:
    first = rows[0]["req_candidate_id"]
    last = rows[-1]["req_candidate_id"]
    batch_id = f"V1-APP-{batch_index:03d}"
    psha = payload_sha(rows)
    label = source_label(rows[0]["primary_source"])
    title = f"最终批准 {first}–{last}：{label}"
    candidates = "\n".join(render_candidate(row) for row in rows)
    checklist = "\n".join(f"- [ ] `{row['req_candidate_id']}`：批准／拒绝／修订（写明精确选择）" for row in rows)
    body = f"""# {title}

Type: grilling
Status: open
Blocked by: 88
Batch: {batch_id}
Approval payload SHA-256: {psha}
Candidate ledger SHA-256: {EXPECTED_CANDIDATE_LEDGER_SHA256}

## Question

用户是否逐条批准本批 {len(rows)} 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [{clean_inline(rows[0]['primary_source'])}](../../../{rows[0]['primary_source']})
- **责任角色：** {review_role(rows[0])}
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 {MAX_ITEMS_PER_BATCH} 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `{batch_id}` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

{candidates}
## Required HITL resolution

{checklist}

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。
"""
    filename = f"{issue_number:02d}-approve-{first.lower()}-{last.lower()}.md"
    return filename, title, body


def build() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    if sha256_file(CANDIDATES) != EXPECTED_CANDIDATE_LEDGER_SHA256:
        raise RuntimeError("Candidate ledger identity drift")
    rows = read_tsv(CANDIDATES)
    expected_ids = [f"REQ-{number:04d}" for number in range(1, 349)]
    if [row["req_candidate_id"] for row in rows] != expected_ids:
        raise RuntimeError("Candidate IDs are not exactly REQ-0001..REQ-0348")
    if any(row["candidate_status"] != "candidate-awaiting-final-item-approval" for row in rows):
        raise RuntimeError("A candidate was promoted before final approval")

    groups = split_batches(rows)
    manifest_rows: list[dict[str, object]] = []
    generated: dict[Path, bytes] = {}
    for index, group in enumerate(groups, start=1):
        issue_number = FIRST_APPROVAL_ISSUE + index - 1
        filename, title, body = render_ticket(issue_number, index, group)
        data = body.encode("utf-8")
        path = ISSUES / filename
        generated[path] = data
        manifest_rows.append(
            {
                "batch_id": f"V1-APP-{index:03d}",
                "issue_number": issue_number,
                "issue_file": f"issues/{filename}",
                "title": title,
                "required_role": review_role(group[0]),
                "primary_source": group[0]["primary_source"],
                "candidate_count": len(group),
                "first_req": group[0]["req_candidate_id"],
                "last_req": group[-1]["req_candidate_id"],
                "candidate_ids": ",".join(row["req_candidate_id"] for row in group),
                "approval_payload_sha256": payload_sha(group),
                "initial_ticket_sha256": sha256_bytes(data),
                "status": "awaiting-user-final-item-approval",
            }
        )

    legacy_rows = read_tsv(LEGACY_BATCHES)
    if len(legacy_rows) != 102 or sum(int(row["candidate_rows"]) for row in legacy_rows) != 6449:
        raise RuntimeError("Legacy 102-batch suggestion set drift")
    legacy_review_rows: list[dict[str, object]] = []
    for row in legacy_rows:
        legacy_review_rows.append(
            {
                **row,
                "recheck_disposition": "retired-as-final-approval-batch",
                "recheck_reason": "面向12452条旧来源中的6449条未批准候选，未绑定当前348个REQ、精确当前文本、范围与验证方法；保留其领域和责任角色作为分批参考，不继承批准单位。",
            }
        )

    release_number = FIRST_APPROVAL_ISSUE + len(groups)
    blockers = ", ".join(str(row["issue_number"]) for row in manifest_rows)
    release_name = f"{release_number:02d}-publish-v1-current-requirements-baseline.md"
    release_title = "生成并发布首个当前需求基线 v1.0.0"
    release_body = f"""# {release_title}

Type: task
Status: open
Blocked by: {blockers}

## Question

在全部最终批准批次均已关闭且每个 `REQ-0001`～`REQ-0348` 都有明确、可核查的逐项结论后，如何生成可独立阅读的 `requirements/baselines/current-requirements-v1.0.0.md`，记录批准人与批准证据，核验完整版本文件及 SHA-256，并完成 Git commit、带说明 tag `requirements-baseline-v1.0.0` 和 `requirements/current-baseline.md` 唯一当前指针？

发布任务必须失败式核对批准批次清单与 payload 身份；任何拒绝、待修订、缺失批准或身份漂移都阻止发布。不得修改、合并、删除或静默改写原始需求材料。

## Evidence

- [最终批准批次清单](../evidence/v1-final-approval-batches/v1-final-approval-batches.tsv)
- [首版规范需求候选总账](../evidence/v1-canonical-candidates/v1-canonical-requirement-candidates.tsv)
- [决定基线版本的存储与变更治理形式](09-baseline-release-storage-and-change-governance.md)
"""
    generated[ISSUES / release_name] = release_body.encode("utf-8")

    manifest_fields = list(manifest_rows[0])
    legacy_fields = list(legacy_review_rows[0])
    manifest_data = tsv_bytes(manifest_fields, manifest_rows)
    legacy_data = tsv_bytes(legacy_fields, legacy_review_rows)
    summary = {
        "schema_version": 1,
        "target_version": "v1.0.0",
        "candidate_ledger_sha256": EXPECTED_CANDIDATE_LEDGER_SHA256,
        "candidate_requirements": len(rows),
        "final_approval_batches": len(groups),
        "max_items_per_batch": MAX_ITEMS_PER_BATCH,
        "batch_candidate_rows": sum(len(group) for group in groups),
        "unique_batch_candidate_rows": len({row["req_candidate_id"] for group in groups for row in group}),
        "legacy_suggestions_rechecked": len(legacy_rows),
        "legacy_suggestion_candidate_rows": sum(int(row["candidate_rows"]) for row in legacy_rows),
        "legacy_suggestions_carried_forward_as_approval_units": 0,
        "approval_upgrades": 0,
        "release_issue_number": release_number,
        "release_blocker_count": len(groups),
        "source_batch_counts": dict(Counter(group[0]["primary_source"] for group in groups)),
        "manifest_sha256": sha256_bytes(manifest_data),
        "legacy_review_sha256": sha256_bytes(legacy_data),
    }
    readme = f"""# `v1.0.0` 最终批准批次

本目录记录票据《生成首版原子需求最终批准批次》的确定性产物。它只建立 HITL 审阅单位，不批准任何需求。

- `v1-final-approval-batches.tsv`：{len(groups)} 张最终批准票的规范清单；覆盖 `REQ-0001`～`REQ-0348`，每批至多 {MAX_ITEMS_PER_BATCH} 条。
- `legacy-102-batch-suggestion-review.tsv`：逐项复核旧 102 个建议批次。旧建议面向 6,449 条未批准旧来源声明，未绑定当前 `REQ`、精确规范文本、范围和验证方法，因此全部退出“最终批准单位”，只保留领域与责任角色参考价值。
- `v1-final-approval-batches-summary.json`：覆盖、唯一性、阻塞与零批准升级门禁摘要。
- `build_and_verify_v1_final_approval_batches.py`：确定性生成与 `--verify-only` 失败式核验入口。

批次身份由 `Batch`、`Approval payload SHA-256` 和候选总账 SHA-256 共同固定。批准票后续追加 `## Answer` 不改变被批准 payload；若任一候选绑定字段改变，必须重新生成 payload 并重新批准。
""".encode("utf-8")

    generated[MANIFEST] = manifest_data
    generated[LEGACY_REVIEW] = legacy_data
    generated[SUMMARY] = (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    generated[README] = readme
    return manifest_rows, legacy_review_rows, {"generated": generated, "summary": summary}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    manifest_rows, _, result = build()
    generated: dict[Path, bytes] = result["generated"]  # type: ignore[assignment]
    if args.verify_only:
        mismatches = []
        for path, data in generated.items():
            if not path.exists():
                mismatches.append(str(path.relative_to(ROOT)))
            elif path.parent == ISSUES and "-approve-" in path.name:
                if normalized_saved_approval_base(path) != data:
                    mismatches.append(str(path.relative_to(ROOT)))
            elif path.read_bytes() != data:
                mismatches.append(str(path.relative_to(ROOT)))
        if mismatches:
            raise RuntimeError("Generated artifact drift: " + ", ".join(mismatches))
    else:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for path, data in generated.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.parent == ISSUES and "-approve-" in path.name:
                data = merge_approval_history(path, data)
            path.write_bytes(data)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(f"verified approval batches: {len(manifest_rows)}")


if __name__ == "__main__":
    main()
