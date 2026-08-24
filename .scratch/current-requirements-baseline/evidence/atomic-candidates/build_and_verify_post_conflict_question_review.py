from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
SOURCE = ARTIFACT_DIR / "R01-R13-consolidated-atomic-candidates.tsv"
OUTPUT = ARTIFACT_DIR / "R01-R13-post-conflict-question-review.tsv"
SUMMARY = ARTIFACT_DIR / "R01-R13-post-conflict-question-review-summary.json"
EXPECTED_SOURCE_SHA256 = "b176262228842f6e5564f1f5d227321bb28932e498b254890a48cff952fd37f4"
EXPECTED_REVIEW_ROWS = 241

OUTPUT_FIELDS = [
    "review_id",
    "candidate_id",
    "batch_id",
    "source_record_id",
    "source_path",
    "exact_location",
    "section_path",
    "statement_text",
    "source_context",
    "statement_fingerprint",
    "original_candidate_class",
    "original_baseline_route",
    "original_review_disposition",
    "original_conflict_pointer",
    "original_approval_state",
    "post_conflict_disposition",
    "resolution_pointer",
    "review_rationale",
    "review_fingerprint",
]

TICKETS = {
    "64": (
        "决定 MES 运输候选的业务纳入与排除边界",
        "64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md",
        {"R01-A0045", "R01-A0047", "R01-A0048", "R01-A0051"},
    ),
    "65": (
        "决定复合运输、分区与多 SUBLOT 组合边界",
        "65-decide-composite-transport-zoning-and-multi-sublot-boundary.md",
        {
            "R01-A0096", "R01-A0097", "R01-A0296", "R01-A1891",
            "R02-A0242", "R02-A0987",
        },
    ),
    "66": (
        "决定派车评分、路网成本与无车响应升级规则",
        "66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md",
        {
            "R01-A0095", "R01-A0294", "R01-A0295", "R01-A0729",
            "R01-A0732", "R01-A1887", "R01-A1889", "R02-A0304",
            "R02-A0988", "R02-A0990", "R02-A1007", "R02-A1009",
            "R03-A1541",
        },
    ),
    "67": (
        "决定同站多任务取消与人工选任务开门边界",
        "67-decide-same-station-cancellation-and-operator-task-opening.md",
        {"R01-A0098", "R01-A0099", "R01-A0120", "R01-A0122"},
    ),
    "68": (
        "决定到站拒收、取消与完工后纠错边界",
        "68-decide-destination-rejection-cancellation-and-post-completion-correction.md",
        {"R01-A1903", "R01-A1909", "R01-A1911"},
    ),
    "69": (
        "决定故障车辆隔离、货物处置与人工越权边界",
        "69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md",
        {
            "R01-A1899", "R03-A1587", "R03-A1595", "R03-A1597",
            "R03-A1601", "R03-A1616", "R03-A1618", "R03-A1628",
        },
    ),
    "70": (
        "决定安全联锁失败升级与紧急停止边界",
        "70-decide-safety-interlock-failure-escalation-and-emergency-stop.md",
        {"R01-A1901", "R03-A2943", "R03-A2947", "R03-A2951", "R03-A2955"},
    ),
    "71": (
        "决定人员登录、维护操作与高风险权限边界",
        "71-decide-human-login-maintenance-and-high-risk-permission-boundary.md",
        {
            "R01-A1905", "R01-A1907", "R02-A0222", "R03-A0670",
            "R03-A0742", "R03-A0796", "R03-A0892", "R03-A0958",
        },
    ),
    "72": (
        "决定仓位模型与 IO 映射配置、验证和启用门禁",
        "72-decide-slot-io-mapping-activation-and-maintenance-policy.md",
        {"R01-A1893", "R01-A1925", "R03-A0948", "R03-A0961", "R03-A0977"},
    ),
    "73": (
        "决定监控新鲜度、告警升级、重试与日志留存规则",
        "73-decide-monitoring-freshness-alert-retry-and-log-retention.md",
        {
            "R01-A0119", "R01-A1913", "R01-A1915", "R01-A1923",
            "R01-A2951", "R01-A3047", "R03-A0121", "R03-A0677",
            "R03-A1505", "R03-A1561", "R03-A3078", "R03-A3080",
        },
    ),
    "74": (
        "决定账户恢复与密码增强策略",
        "74-decide-account-recovery-and-password-hardening-policy.md",
        {"R02-A0773", "R02-A0808"},
    ),
    "75": (
        "决定充电阈值、配置变更与异常生命周期",
        "75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md",
        {
            "R03-A1672", "R03-A1673", "R03-A1711", "R03-A1712",
            "R03-A1749", "R03-A1758",
        },
    ),
    "76": (
        "决定空闲返回、停靠点资格与调度竞争边界",
        "76-decide-idle-return-parking-point-eligibility-and-arbitration.md",
        {"R03-A2993", "R03-A3049", "R03-A3072"},
    ),
    "77": (
        "决定地图拓扑同步与历史快照产品边界",
        "77-decide-map-topology-sync-and-snapshot-product-boundary.md",
        {"R03-A1880", "R03-A1885", "R03-A1889"},
    ),
    "78": (
        "决定归档 AGV 的恢复与身份连续性",
        "78-decide-archived-agv-restoration-and-identity-continuity.md",
        {"R03-A1102", "R03-A1186"},
    ),
    "79": (
        "决定 AREA 显式覆盖的维护与生效治理",
        "79-decide-area-override-maintenance-and-effectivity-governance.md",
        {"R01-A1897"},
    ),
    "80": (
        "决定 RIoT 建单未确认时任务绑定、重试与释放边界",
        "80-decide-riot-order-creation-uncertainty-binding-retry-release.md",
        {"R03-A1571"},
    ),
}

DECISION_COVERED = {
    "R01-A0094": ("56", "同站取消仍受 TransportDemandKey 永久抑制规则约束。"),
    "R01-A0739": ("35", "8005 全部 AGV 当前为八仓，且未来车型不得直接继承该绑定。"),
    "R01-A1926": ("35", "8005 没有独立门磁，门相关事实只能来自已批准的锁反馈和光幕信号。"),
    "R01-A2990": ("35", "锁反馈与光幕输入点位及极性已经用户确认。"),
    "R01-A2991": ("35", "开锁输出点位、脉冲复位和禁止长时间通电已经用户确认。"),
    "R01-A3008": ("57", "当前 8005 严格只读 MES，搬运完成后不得执行 MES 写回。"),
}

NEEDS_EVIDENCE = {
    "R01-A0044", "R01-A0046", "R01-A0049", "R01-A0050", "R01-A0071",
    "R01-A0072", "R01-A0288", "R01-A0289", "R01-A0290", "R01-A0291",
    "R01-A0292", "R01-A0293", "R01-A0297", "R01-A0298", "R01-A0299",
    "R01-A0300", "R01-A0738", "R01-A0744", "R01-A0746", "R01-A0748",
    "R01-A0751", "R01-A1895", "R01-A1921", "R01-A2914", "R01-A2922", "R01-A2930",
    "R01-A2939", "R01-A2989", "R03-A1659", "R03-A1883",
}

NEEDS_REFRAMING = {
    "R01-A0604": "issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md",
    "R01-A1919": "issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md;issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md;issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md",
    "R01-A1928": "issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md",
    "R01-A2914": "issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md;issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md",
    "R01-A2922": "issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md;issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md",
    "R01-A2930": "issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md;issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md",
    "R01-A2939": "issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md;issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md",
    "R01-A3091": "issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md;issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md",
    "R02-A0105": "map.md#Destination",
    "R02-A0106": "map.md#Out-of-scope",
    "R02-A0234": "issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md",
    "R03-A1529": "issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md",
    "R03-A1714": "issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md;issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md",
    "R03-A1901": "issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md",
    "R03-A3030": "issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md",
    "R09-A0027": "issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md;issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md",
}

OUT_OF_SCOPE = {
    "R01-A0741": "未来 AREA 审批流增强超出首个当前基线的现时边界。",
    "R01-A1917": "界面布局、字段摆放和筛选交互属于后续正式 spec/系统设计。",
    "R02-A1133": "内部派生工作流步骤目录不是独立业务需求问题。",
    "R03-A1010": "本地缓存或即时接口查询是实现机制选择。",
    "R03-A1021": "文档已明确 RIoT 设备级禁用不在当前 UC 范围。",
    "R03-A3059": "是否复用某轮询实现属于后续系统设计。",
    "R09-A0085": "Web UI、连接池和超时细项属于实现与交付设计。",
    "R12-A0061": "历史 MesIngest 交付边界不是当前需求基线的业务问题。",
    "R12-A0095": "历史实验工具技术边界不是当前需求基线的业务问题。",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def read_source() -> list[dict[str, str]]:
    if sha256_bytes(SOURCE.read_bytes()) != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("Consolidated ledger hash drift; re-review is required before rebuilding")
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    held = [row for row in rows if row["review_disposition"] == "hold-for-question-or-reframing"]
    if len(held) != EXPECTED_REVIEW_ROWS:
        raise RuntimeError(f"Hold row-count drift: expected={EXPECTED_REVIEW_ROWS} actual={len(held)}")
    ids = [row["candidate_id"] for row in held]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate candidate IDs in held rows")
    if any(row["approval_state"] != "not-approved" for row in held):
        raise RuntimeError("A held source row was silently approval-upgraded")
    return held


def ticket_for(candidate_id: str) -> tuple[str, str] | None:
    matches = [
        (number, title, filename)
        for number, (title, filename, candidate_ids) in TICKETS.items()
        if candidate_id in candidate_ids
    ]
    if len(matches) > 1:
        raise RuntimeError(f"Candidate mapped to multiple HITL tickets: {candidate_id}")
    if not matches:
        return None
    _, title, filename = matches[0]
    return title, f"issues/{filename}"


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    candidate_id = row["candidate_id"]
    ticket = ticket_for(candidate_id)
    if ticket:
        title, pointer = ticket
        return (
            "graduate-hitl-question",
            pointer,
            f"问题已能按业务后果精确表述，并由《{title}》统一承载；原声明保持未批准。",
        )
    if candidate_id in DECISION_COVERED:
        decision, rationale = DECISION_COVERED[candidate_id]
        issue = next((path for path in (REPO / ".scratch/current-requirements-baseline/issues").glob(f"{decision}-*.md")), None)
        if issue is None:
            raise RuntimeError(f"Missing decision ticket {decision}")
        return "covered-by-approved-decision", f"issues/{issue.name}", rationale
    if candidate_id in NEEDS_REFRAMING:
        return (
            "needs-atomic-reframing",
            NEEDS_REFRAMING[candidate_id],
            "原声明混合多个业务后果、实现机制、历史状态或已决与未决部分，不能整体批准；相关原子问题已另行指向。",
        )
    if candidate_id in NEEDS_EVIDENCE:
        return (
            "needs-evidence-before-candidacy",
            row["source_path"],
            "该记录要求目标环境、接口、字段、配置值或版本绑定事实；现有材料不足，不能由批准人猜测或由实现反推。",
        )
    if candidate_id in OUT_OF_SCOPE:
        return "out-of-current-destination", "map.md#Out-of-scope", OUT_OF_SCOPE[candidate_id]

    # The remaining fixed-hash rows were manually reviewed as headings, worklist state,
    # category labels, duplicate question indexes, already-converged version notes, or
    # evidence that does not itself state an approvable requirement. Input hash + row-count
    # checks make this closed remainder fail when the upstream ledger changes.
    pointer = row.get("semantic_review_cluster_id") or row.get("relation_to_cluster_representative") or row["source_path"]
    return (
        "duplicate-or-evidence-only",
        pointer,
        "该行只记录标题、分类、历史待办/阻塞状态、问题索引、重复标签或收敛说明；保留作证据，不单独形成需求决定。",
    )


def build() -> tuple[list[dict[str, str]], dict[str, object]]:
    source_rows = read_source()
    output: list[dict[str, str]] = []
    for index, source in enumerate(source_rows, 1):
        disposition, pointer, rationale = classify(source)
        review_fingerprint = sha256_text("\x1f".join([
            source["candidate_id"], source["statement_fingerprint"], disposition, pointer, rationale,
        ]))
        output.append({
            "review_id": f"PCR-{index:04d}",
            "candidate_id": source["candidate_id"],
            "batch_id": source["batch_id"],
            "source_record_id": source["source_record_id"],
            "source_path": source["source_path"],
            "exact_location": source["exact_location"],
            "section_path": source["section_path"],
            "statement_text": source["statement_text"],
            "source_context": source["source_context"],
            "statement_fingerprint": source["statement_fingerprint"],
            "original_candidate_class": source["candidate_class"],
            "original_baseline_route": source["baseline_route"],
            "original_review_disposition": source["review_disposition"],
            "original_conflict_pointer": source["conflict_pointer"],
            "original_approval_state": source["approval_state"],
            "post_conflict_disposition": disposition,
            "resolution_pointer": pointer,
            "review_rationale": rationale,
            "review_fingerprint": review_fingerprint,
        })

    ticket_counts = Counter()
    for row in output:
        if row["post_conflict_disposition"] == "graduate-hitl-question":
            ticket_counts[row["resolution_pointer"]] += 1
    summary = {
        "schema_version": 1,
        "input_ledger": SOURCE.name,
        "input_ledger_sha256": EXPECTED_SOURCE_SHA256,
        "input_hold_rows": len(source_rows),
        "review_rows": len(output),
        "batch_counts": dict(sorted(Counter(row["batch_id"] for row in output).items())),
        "source_record_counts": dict(sorted(Counter(row["source_record_id"] for row in output).items())),
        "disposition_counts": dict(sorted(Counter(row["post_conflict_disposition"] for row in output).items())),
        "decision_covered_counts": dict(sorted(Counter(
            row["resolution_pointer"] for row in output
            if row["post_conflict_disposition"] == "covered-by-approved-decision"
        ).items())),
        "new_hitl_tickets": {
            pointer: {
                "title": next(title for title, filename, _ in TICKETS.values() if pointer == f"issues/{filename}"),
                "candidate_rows": count,
            }
            for pointer, count in sorted(ticket_counts.items())
        },
        "invariants": {
            "source_rows_preserved": len(output),
            "source_statement_fingerprints_changed": 0,
            "approval_upgrades": 0,
            "unmapped_rows": 0,
            "new_hitl_ticket_count": len(ticket_counts),
        },
        "guardrail": (
            "The post-conflict ledger classifies but never edits, deletes, merges, approves, or assigns a permanent "
            "requirement ID to any source statement. HITL tickets carry questions only."
        ),
    }
    return output, summary


def write_tsv(rows: list[dict[str, str]]) -> None:
    temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(OUTPUT)


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("Missing generated review artifact")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != OUTPUT_FIELDS:
            raise RuntimeError("Review ledger field drift")
        actual = list(reader)
    if actual != rows:
        raise RuntimeError("Generated review ledger drift")
    if json.loads(SUMMARY.read_text(encoding="utf-8-sig")) != summary:
        raise RuntimeError("Generated review summary drift")
    if len(rows) != EXPECTED_REVIEW_ROWS:
        raise RuntimeError("Review ledger is not zero-omission")
    if len({row["candidate_id"] for row in rows}) != EXPECTED_REVIEW_ROWS:
        raise RuntimeError("Review ledger candidate coverage is not one-to-one")
    if any(row["original_approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("Review ledger leaked an approval upgrade")
    allowed = {
        "covered-by-approved-decision", "duplicate-or-evidence-only", "out-of-current-destination",
        "graduate-hitl-question", "needs-atomic-reframing", "needs-evidence-before-candidacy",
    }
    if {row["post_conflict_disposition"] for row in rows} != allowed:
        raise RuntimeError("Review disposition coverage drift")
    for number, (_, filename, candidate_ids) in TICKETS.items():
        ticket_path = REPO / ".scratch/current-requirements-baseline/issues" / filename
        body = ticket_path.read_text(encoding="utf-8-sig")
        allowed_statuses = ("Status: open", "Status: claimed", "Status: resolved")
        if "Type: grilling" not in body or not any(status in body for status in allowed_statuses) or "Blocked by: 63" not in body:
            raise RuntimeError(f"HITL ticket metadata drift: {number}")
        ledger_ids = {
            row["candidate_id"] for row in rows
            if row["resolution_pointer"] == f"issues/{filename}"
            and row["post_conflict_disposition"] == "graduate-hitl-question"
        }
        if ledger_ids != candidate_ids:
            raise RuntimeError(f"HITL ticket candidate mapping drift: {number}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    rows, summary = build()
    if not args.verify_only:
        write_tsv(rows)
        summary_temporary = SUMMARY.with_suffix(SUMMARY.suffix + ".tmp")
        summary_temporary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary_temporary.replace(SUMMARY)
    verify(rows, summary)
    print(
        "Post-conflict review verified: "
        f"rows={summary['review_rows']} dispositions={summary['disposition_counts']} "
        f"new_hitl={summary['invariants']['new_hitl_ticket_count']} approval_upgrades=0"
    )


if __name__ == "__main__":
    main()
