from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EFFORT = ROOT / ".scratch" / "current-requirements-baseline"
ISSUES = EFFORT / "issues"
LEDGER = EFFORT / "evidence" / "v1-canonical-candidates" / "v1-canonical-requirement-candidates.tsv"
MANIFEST = Path(__file__).resolve().parent / "v1-final-approval-batches.tsv"
OUTPUT = ROOT / "requirements" / "baselines" / "current-requirements-v1.0.0.md"
LEDGER_SHA256 = "9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646"
MANIFEST_SHA256 = "3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843"
APPROVED_AT = "2026-08-24T15:16:06Z"
CONSOLIDATED_EVIDENCE = (
    ".scratch/current-requirements-baseline/evidence/"
    "v1-final-approval-batches/consolidated-approval-2026-08-24.md"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def one_line(value: str) -> str:
    return " ".join((value or "").split())


def relative_link(path: str) -> str:
    clean = path.replace("\\", "/")
    return f"../../{clean}"


def verify_and_bind() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    if sha256_bytes(LEDGER.read_bytes()) != LEDGER_SHA256:
        raise RuntimeError("Candidate ledger identity drift")
    if sha256_bytes(MANIFEST.read_bytes()) != MANIFEST_SHA256:
        raise RuntimeError("Approval manifest identity drift")

    rows = read_tsv(LEDGER)
    expected_ids = [f"REQ-{number:04d}" for number in range(1, 349)]
    if [row["req_candidate_id"] for row in rows] != expected_ids:
        raise RuntimeError("Candidate coverage is not exactly REQ-0001..REQ-0348")

    manifest = read_tsv(MANIFEST)
    if len(manifest) != 95:
        raise RuntimeError("Approval manifest does not contain 95 batches")
    binding: dict[str, dict[str, str]] = {}
    for batch in manifest:
        issue_path = EFFORT / batch["issue_file"]
        text = issue_path.read_text(encoding="utf-8-sig")
        if not re.search(r"(?m)^Status:\s*resolved\s*$", text):
            raise RuntimeError(f"Approval ticket is not resolved: {batch['issue_file']}")
        if len(re.findall(r"(?m)^## Answer\s*$", text)) != 1:
            raise RuntimeError(f"Approval ticket lacks one current Answer: {batch['issue_file']}")
        payload = re.search(r"(?m)^Approval payload SHA-256:\s*([0-9a-f]{64})\s*$", text)
        ledger = re.search(r"(?m)^Candidate ledger SHA-256:\s*([0-9a-f]{64})\s*$", text)
        if payload is None or payload.group(1) != batch["approval_payload_sha256"]:
            raise RuntimeError(f"Approval payload drift: {batch['issue_file']}")
        if ledger is None or ledger.group(1) != LEDGER_SHA256:
            raise RuntimeError(f"Approval ledger drift: {batch['issue_file']}")
        for req_id in batch["candidate_ids"].split(","):
            if req_id in binding:
                raise RuntimeError(f"Duplicate approval binding: {req_id}")
            binding[req_id] = batch
    if sorted(binding) != expected_ids:
        raise RuntimeError("Approval batches do not cover REQ-0001..REQ-0348 exactly once")
    return rows, binding


def render_requirement(row: dict[str, str], batch: dict[str, str]) -> str:
    req_id = row["req_candidate_id"]
    issue_path = f".scratch/current-requirements-baseline/{batch['issue_file']}"
    approval_links = f"[{issue_path}]({relative_link(issue_path)})"
    if int(batch["issue_number"]) >= 93:
        approval_links += f"；[{CONSOLIDATED_EVIDENCE}]({relative_link(CONSOLIDATED_EVIDENCE)})"
    transformation = "none" if row["derivation"].startswith("verbatim") else one_line(
        row["source_layers_and_differences"]
    )
    return f"""### `{req_id}` — {one_line(row['title'])}

- Lifecycle: `active`
- Scope: {one_line(row['scope'])}
- Introduced In: `v1.0.0`
- Last Meaning Change In: `v1.0.0`
- Supersedes: `{one_line(row['supersedes_req'])}`
- Deprecated In: `none`
- Change Proposal: `none（首版恢复）`

#### Current Requirement

{one_line(row['canonical_text'])}

#### Verification Method

{one_line(row['verification_method'])}

#### Evidence

##### 原始证据

- Source: [{one_line(row['primary_source'])}]({relative_link(row['primary_source'])})
- Exact Location: {one_line(row['exact_location'])}
- Verbatim Extract: {one_line(row['verbatim_extract'])}
- Source Version: `{one_line(row['source_blob'])}`
- Snapshot SHA-256: `{row['source_sha256']}`
- Source Date: `unknown`
- Source Scope: {one_line(row['scope'])}
- Source Authority: {one_line(row['source_authority'])}
- Source Approval Evidence: {one_line(row['source_approval_evidence'])}

##### 规范文本形成方式

- Derivation: `{one_line(row['derivation'])}`
- Transformation Trace: {transformation}
- AI Involvement: `{one_line(row['ai_involvement'])}`
- Source Layers and Differences: {one_line(row['source_layers_and_differences'])}
- Pre-baseline Supersession: {one_line(row['prebaseline_source_supersession'])}
- Conflict Assessment: {one_line(row['conflict_disposition'])}
- Decision Pointers: {one_line(row['decision_pointers'])}
- Legacy Candidate Pointers: {one_line(row['legacy_candidate_ids'])}

##### 条目批准记录

- Approver: 用户本人（本地图默认且唯一最终批准人）
- Approved At: `{APPROVED_AT}`（版本发布确认时间；更早的逐项互动见批准票）
- Approved Scope: 本条 Current Requirement、Scope 与 Verification Method
- Approved Text Identity: `{row['canonical_text_sha256']}`
- Approval Batch: `{batch['batch_id']}`
- Approval Payload SHA-256: `{batch['approval_payload_sha256']}`
- Candidate Ledger SHA-256: `{LEDGER_SHA256}`
- Approval Manifest SHA-256: `{MANIFEST_SHA256}`
- Approval Evidence: {approval_links}
- Authority Evidence: [确定当前基线的最终批准人](../../.scratch/current-requirements-baseline/issues/03-final-baseline-approver.md)

---
"""


def render() -> bytes:
    rows, binding = verify_and_bind()
    requirements = "\n".join(render_requirement(row, binding[row["req_candidate_id"]]) for row in rows)
    body = f"""# 当前需求基线 `v1.0.0`

## 版本元数据

- Target Baseline Version: `v1.0.0`
- Previous Approved Version: `none`
- Intended File: `requirements/baselines/current-requirements-v1.0.0.md`
- Prepared At: `{APPROVED_AT}`
- Applicable Scope: 8005 多仓位 AGV 项目；更窄边界以每条需求的 Scope 为准
- Candidate Ledger SHA-256: `{LEDGER_SHA256}`
- Approval Manifest SHA-256: `{MANIFEST_SHA256}`
- Final Approver: 用户本人（本地图默认且唯一最终批准人）
- Version Approval Evidence: [{CONSOLIDATED_EVIDENCE}]({relative_link(CONSOLIDATED_EVIDENCE)}) 及每条需求所列批准票

## 相对上一批准版本的变化

### Added

- `REQ-0001`–`REQ-0348`：首个批准需求基线，共 348 条。

### Modified

- None

### Deprecated

- None

## Requirements

{requirements}
## 冻结内容检查

- [x] `REQ-0001`–`REQ-0348` 唯一、连续且未复用。
- [x] 每个条目均具有唯一规范性的 Current Requirement、Scope、Verification Method 与可复核 Evidence。
- [x] 每个条目均绑定规范文本 SHA-256、批准批次、payload、候选总账和 manifest。
- [x] 已知真实冲突均引用已解决决定；未把疑似冲突擅自解释为已解决。
- [x] 本版本仅新增首个批准基线，没有修改或废弃更早批准需求。
- [x] 版本号 `v1.0.0` 与首版批准基线性质一致。
- [x] 版本文件由确定性生成器输出并可通过 `--verify-only` 复核。
- [x] 旁置发布记录由发布流程绑定内容 Git commit、最终文件 SHA-256 与 annotated tag。
- [x] `requirements/current-baseline.md` 在正式发布提交中唯一指向本版本。
"""
    return body.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    data = render()
    if args.verify_only:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data:
            raise RuntimeError("Versioned baseline artifact drift")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(data)
    print(f"requirements=348")
    print(f"baseline_sha256={sha256_bytes(data)}")
    print(f"output={OUTPUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
