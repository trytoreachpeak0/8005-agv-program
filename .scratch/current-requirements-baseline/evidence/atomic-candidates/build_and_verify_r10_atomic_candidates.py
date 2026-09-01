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
OUTPUT = Path(__file__).with_name("R10-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R10-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r10-pass"
EXPECTED_SOURCE_IDS = [f"R10-{number:02d}" for number in range(3, 19)]
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]

POINTER_DEFINITIONS = {
    "BOUND-R10-001": "模拟器材料只证明拟提供的硬件刺激，不得反推主系统 UC、业务状态、超时、任务或站点规则已获批准。",
    "EVID-R10-001": "“补齐 8005 仓位硬件身份与现场信号证据”已固定八仓点位、信号极性、500 ms 脉冲、无门磁/移动联锁及弹簧弹门的 8005 范围事实。",
    "SCOPE-R10-001": "用户已明确供应商手册可忽略；厂商型号、寄存器和功能码内容只保留清单/来源证据，不进入当前基线候选或外部约束。",
    "CF-R10-001": "R10 排除材料仍残留锁 DI 镜像 DO、故障枚举落后等不一致；候选语义不能据此认定已有稳定设计。",
    "GAP-R10-001": "Unit Identifier、地址换算、Pulse OFF、PDU 上限、多客户端/超时及库选型仍未冻结，协议透明/保真尚无完整可实施规格。",
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R10"]
    if len(batch_rows) != 46:
        raise RuntimeError(f"R10 batch boundary drift: expected=46 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R10"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R10 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 16, "excluded": 30}):
        raise RuntimeError("R10 route boundary drift; expected 16 candidate and 30 excluded documents")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows


def section_contains(unit: common.Unit, pattern: str) -> bool:
    return bool(re.search(pattern, unit.section, re.I))


def is_verification_plan(unit: common.Unit) -> bool:
    return section_contains(unit, r"Verification|验证方式") or bool(re.match(r"^TC-FR-", unit.statement, re.I))


def is_origin_or_traceability(unit: common.Unit) -> bool:
    return section_contains(unit, r"Origin|需求来源|Related Use Case|关联用例|Related 关联|决策依据")


def is_background_evidence(unit: common.Unit) -> bool:
    return section_contains(unit, r"背景 Background") or unit.statement.startswith("背景：")


def is_unresolved(text: str) -> bool:
    return bool(re.search(r"\bTBD\b|仍待确认|需要确认|尚待确认|待定|TODO|未冻结|未决定|留待后续", text, re.I))


def has_main_system_or_field_claim(text: str) -> bool:
    return bool(re.search(
        r"主系统.*(?:负责|判定|维护|发起|写|连接)|被测主系统|根目录\s*\[?UC-|现场(?:没有|需要|实际)|"
        r"一台\s*AGV.*(?:实际|必须)|真实(?:硬件|设备|物理模块|部署)|业务超时.*主系统|任务状态|目标站点|"
        r"产品身份|批次记录|异常锁定|已禁用|移动安全联锁|独立门磁|弹簧自动弹门|锁具",
        text,
        re.I,
    ))


def has_vendor_claim(text: str) -> bool:
    return bool(re.search(
        r"C2000-A2-KDDA0A0-AD6|康耐德|说明书|厂商|16\s*(?:个|路)?\s*(?:DO|DI)|"
        r"硬件寄存器表声明|来源说明书|真实设备寄存器表|首个模板.*reference/",
        text,
        re.I,
    ))


def has_protocol_interface(text: str) -> bool:
    return bool(re.search(
        r"Modbus|HTTP/JSON|控制 API|功能码|寄存器|DO|DI|监听|端口|连接|4xx|错误码|Slave|服务端点",
        text,
        re.I,
    ))


def has_configuration_validation(text: str) -> bool:
    return bool(re.search(
        r"配置|模板|Schema|校验|热重载|映射|通道|面标识|rowSpan|columnSpan|越界|重叠|默认值|原子",
        text,
        re.I,
    ))


def has_testability_or_operability(text: str) -> bool:
    return bool(re.search(
        r"reset|重置|健康检查|就绪探针|故障注入|结构化日志|终止信号|无人值守|CI|Headless|并行|串行|确定性",
        text,
        re.I,
    ))


def has_ui_behavior(text: str) -> bool:
    return bool(re.search(r"图形界面|可视化|界面|面板|状态卡片|布局|展示|显示|按钮|WPF", text, re.I))


def is_embedded_technical_design(text: str) -> bool:
    if re.search(r"WPF|JSON Schema|JSON 格式|HTTP/JSON|localhost|stdout|控制台程序|进程实例|热重载", text, re.I):
        return True
    return bool(re.search(r"不写死在代码|全局锁|内部状态|可选客户端|原子持久化", text, re.I))


def is_explicit_simulator_boundary(text: str) -> bool:
    return bool(re.search(
        r"模拟器(?:只|不|需要|应|可以|可|提供|支持|暴露|维护|作为)|模拟真实|本模拟器|本 FR|"
        r"控制 API|WPF|Headless|图形界面|界面(?:不|可|应)|面板(?:不|可|应)",
        text,
        re.I,
    ))


def content_class(unit: common.Unit, source: common.Source) -> tuple[str, str]:
    text = unit.statement
    if is_verification_plan(unit):
        return "reserved-verification-plan-evidence", "test-plan-evidence-only"
    if is_origin_or_traceability(unit) or is_background_evidence(unit):
        return "source-origin-background-or-traceability-evidence", "source-or-traceability-evidence-only"
    if has_vendor_claim(text) and not is_explicit_simulator_boundary(text):
        return "embedded-vendor-derived-claim", "vendor-content-out-of-scope-evidence-only"
    if has_main_system_or_field_claim(text) and not is_explicit_simulator_boundary(text):
        return "embedded-main-system-or-field-claim", "main-system-or-field-lead-evidence-only"
    if is_unresolved(text) and not is_explicit_simulator_boundary(text):
        return "unresolved-planning-or-evidence-question", "needs-question-resolution"
    if is_embedded_technical_design(text):
        return "embedded-simulator-technical-design-choice", "exclude-from-requirement-approval"
    if has_testability_or_operability(text):
        return "simulator-testability-or-operability-candidate", "needs-simulator-product-owner-and-explicit-approval"
    if has_ui_behavior(text):
        return "simulator-operator-ui-behavior-candidate", "needs-simulator-product-owner-and-explicit-approval"
    if has_configuration_validation(text):
        return "simulator-configuration-or-validation-candidate", "needs-simulator-product-owner-and-explicit-approval"
    if has_protocol_interface(text):
        return "simulator-interface-or-protocol-behavior-candidate", "needs-simulator-interface-owner-and-explicit-approval"
    if re.search(r"开锁|关门|放料|取出|光幕|锁状态|仓位|状态迁移|占用|故障", text, re.I):
        return "simulator-slot-behavior-or-fault-stimulus-candidate", "needs-simulator-hardware-behavior-owner-and-explicit-approval"
    if is_explicit_simulator_boundary(text) or section_contains(unit, r"范围|Purpose|目的|Description|需求描述|Acceptance Criteria|验收标准"):
        return "simulator-capability-or-scope-candidate", "needs-simulator-product-owner-and-explicit-approval"
    return "planning-claim-needing-owner-classification", "needs-responsible-owner-classification"


def pointers_for(unit: common.Unit, source: common.Source) -> str:
    text = f"{unit.section} {unit.statement}"
    pointers: list[str] = []
    if re.search(r"主系统|UC-\d+|任务|业务超时|目标站点|产品身份|批次记录|异常锁定|已禁用|RIOT|MES", text, re.I):
        pointers.append("BOUND-R10-001")
    if re.search(
        r"八仓|8\s*个仓位|DO1|DI1|DI9|500\s*ms|门磁|移动.*联锁|弹簧.*弹门|锁状态 DI|光幕 DI|"
        r"开锁.*DO|脉冲.*复位|多个物理 IO 模块",
        text,
        re.I,
    ):
        pointers.append("EVID-R10-001")
    if has_vendor_claim(text) or re.search(r"0x01|0x02|0x03|0x05|0x06|0x0F|0x10|模板值|寄存器表", text, re.I):
        pointers.append("SCOPE-R10-001")
    if re.search(r"锁状态 DI|DO=0|DO.*复位|开锁失败|弹门失败|闩锁失败|不跟随", text, re.I):
        pointers.append("CF-R10-001")
    if re.search(r"协议层透明|完全相同|协议保真|功能码|地址|Unit Identifier|Modbus", text, re.I):
        pointers.append("GAP-R10-001")
    return ",".join(dict.fromkeys(pointers)) or NONE


def scope_for(candidate_class: str, route: str) -> str:
    if route == "vendor-content-out-of-scope-evidence-only":
        return "excluded-vendor-material-and-derived-register-content"
    if route == "main-system-or-field-lead-evidence-only":
        return "8005-main-system-or-field-evidence-lead-not-simulator-approval"
    if "interface" in candidate_class or "protocol" in candidate_class:
        return "slots-simulator-test-control-and-modbus-interface"
    if "ui" in candidate_class:
        return "slots-simulator-internal-developer-ui"
    if "configuration" in candidate_class:
        return "slots-simulator-configuration-layout-and-module-topology"
    return "slots-simulator-development-test-tool-only"


def approval_gap_for(route: str) -> str:
    if route in {"test-plan-evidence-only", "source-or-traceability-evidence-only"}:
        gaps = ["evidence-only-not-an-approval-unit"]
    elif route == "vendor-content-out-of-scope-evidence-only":
        gaps = ["out-of-scope-by-user-direction", "do-not-use-as-current-baseline-external-constraint"]
    elif route == "main-system-or-field-lead-evidence-only":
        gaps = ["authoritative-main-system-source", "do-not-reverse-infer-from-simulator-planning"]
    elif route == "exclude-from-requirement-approval":
        gaps = ["separate-technical-design-review", "approved-simulator-behavior-source-if-mechanism-is-mandatory"]
    elif route == "needs-question-resolution":
        gaps = ["question-resolution", "responsible-decision-owner"]
    elif "interface-owner" in route:
        gaps = ["simulator-interface-owner", "complete-versioned-interface-or-protocol-contract"]
    elif "hardware-behavior-owner" in route:
        gaps = ["simulator-hardware-behavior-owner", "bound-8005-field-evidence-and-polarity-normalization"]
    elif "product-owner" in route:
        gaps = ["simulator-product-owner", "approved-tool-scope-source"]
    else:
        gaps = ["responsible-owner-classification", "authoritative-source"]
    return ";".join(dict.fromkeys(gaps + CORE_GAP))


def build_rows() -> list[dict[str, str]]:
    sources, _ = load_sources()
    rows: list[dict[str, str]] = []
    for source in sources:
        actual = common.sha256_file(REPO / source.path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        units = common.markdown_units(source.record_id, REPO / source.path)
        if not units:
            raise RuntimeError(f"No atomic units extracted from {source.record_id}")
        for unit in units:
            candidate_class, route = content_class(unit, source)
            rows.append({
                "candidate_id": "", "batch_id": "R10", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest, "exact_location": unit.location,
                "section_path": unit.section, "statement_text": unit.statement, "source_context": unit.context,
                "statement_fingerprint": common.fingerprint(unit.statement), "candidate_class": candidate_class,
                "source_claim_status": "review-planning-source-without-verifiable-approval-chain",
                "applicable_scope": scope_for(candidate_class, route), "baseline_route": route,
                "duplicate_or_derivation": (
                    f"document-route:R10-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                    f"ledger-history:{common.normalize(source.derivation)}"
                ),
                "conflict_pointer": pointers_for(unit, source), "approval_state": "not-approved",
                "approval_gap": approval_gap_for(route),
            })
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R10-A{index:04d}"
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows


def summary_for(rows: list[dict[str, str]]) -> dict[str, object]:
    pointers = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer and pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_batch_documents_not_extracted": 30,
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "pointer_counts": dict(sorted(pointers.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "permanent_requirement_ids": sum(bool(re.search(r"\bREQ-\d{4}\b", row["candidate_id"])) for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if summary["source_documents"] != 16 or summary["excluded_batch_documents_not_extracted"] != 30:
        raise RuntimeError(f"R10 source coverage mismatch: {summary}")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R10 approval isolation failed")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R10 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R10-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R10 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R10 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R10 contains an unauthorized approval upgrade")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R10 approval gap is incomplete")
    for required_route in (
        "exclude-from-requirement-approval", "main-system-or-field-lead-evidence-only",
        "vendor-content-out-of-scope-evidence-only", "test-plan-evidence-only",
        "needs-simulator-product-owner-and-explicit-approval",
    ):
        if summary["by_route"].get(required_route, 0) <= 0:
            raise RuntimeError(f"Required R10 route missing: {required_route}")
    for required in POINTER_DEFINITIONS:
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R10 pointer missing: {required}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R10 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R10 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R10 summary JSON differs from a clean rebuild")


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
        "R10 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} "
        f"excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"exact_duplicate_rows={summary['exact_duplicate_rows']} approval_upgrades={summary['approval_upgrades']} "
        f"pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
