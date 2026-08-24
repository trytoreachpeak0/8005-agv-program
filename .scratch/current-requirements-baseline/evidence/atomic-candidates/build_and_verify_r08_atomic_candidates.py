from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

import build_and_verify_r03_atomic_candidates as common


REPO = common.REPO
SOURCE_LEDGER = common.SOURCE_LEDGER
OUTPUT = Path(__file__).with_name("R08-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R08-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r08-pass"
EXPECTED_SOURCE_IDS = [
    "R08-01", "R08-16", "R08-19", "R08-37", "R08-38", "R08-40", "R08-41",
    "R08-42", "R08-43", "R08-44", "R08-45", "R08-47", "R08-48", "R08-50",
    "R08-53", "R08-54", "R08-55", "R08-56", "R08-57",
]
ADR_SOURCE_IDS = set(EXPECTED_SOURCE_IDS) - {"R08-01", "R08-57"}
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]
SNAPSHOT_COMMIT = "1469d6309d00b0abb792f6cd686aed68286e638e"
SNAPSHOT_CONTEXT_NORMALIZED_SHA256 = "140b4893a601a6a705adfa5c24c60c74f9028131716af4272c276f2efeb85827"

POINTER_DEFINITIONS = {
    "CF-R01-001": "TransportDemandKey / MES 需求业务键的跨批次冲突线索。",
    "CF-R01-002": "MES 当前阶段只读与回写主张的跨批次冲突线索。",
    "RES-R08-001": "“决定操作员上下文的清除时点”已以 StopClosureCommit 解决 ADR 0018/0055 冲突。",
    "RES-R08-002": "“决定装货待整批确认阶段是否存在”已排除待整批确认阶段。",
    "RES-R08-003": "“确定领域词汇唯一入口与旧术语表关系”已固定根 CONTEXT.md 唯一入口闭环。",
    "EVID-R08-001": "“补齐 8005 仓位硬件身份与现场信号证据”已绑定用户直接确认，但原文档本身不因此整份获批。",
}

# Ticket 54 mechanically separates the 29 source statements that the first pass
# deliberately quarantined as mixed.  The replacement text stays within the
# meaning of the captured source_context.  It is not an approval or a rewrite of
# CONTEXT/ADR source material: every replacement row retains the source location,
# original statement fingerprint and original candidate identity as provenance.
REFRAMINGS: dict[str, list[tuple[str, str, str, str]]] = {
    "R08-A0170": [
        ("technical", "Sublot（子批次）：车载端只提交该值。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "Sublot（子批次）：车载端在活动操作的最小恢复记录中保留该值引用。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "Sublot（子批次）：服务端负责查询关联信息、校验站点与任务并维护完整生命周期。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0177": [
        ("domain", "SublotReservation（子批号占用）将一个 DemandId、SUBLOT、当前 AGV、OperationSession 和仓位操作尝试编号绑定为一个占用关系。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("domain", "SublotReservation（子批号占用）在项目范围内全局唯一。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "SublotReservation（子批号占用）由服务端持久化。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0199": [
        ("product", "CurrentStopWorklist（当前停靠作业清单）：车载端可以展示清单并提交操作请求。", "operator-facing-product-behavior-candidate", "needs-operator-product-owner-and-explicit-approval"),
        ("domain", "CurrentStopWorklist（当前停靠作业清单）：车载端不拥有任务事实。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
    ],
    "R08-A0201": [
        ("domain", "CurrentStopWorklistSnapshot（当前停靠作业清单快照）是针对当前 AGV 与站点的完整作业投影。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "CurrentStopWorklistSnapshot（当前停靠作业清单快照）由服务端生成。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "CurrentStopWorklistSnapshot（当前停靠作业清单快照）携带 worklistRevision。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0204": [
        ("business", "站点离站等待态（StationDepartureWaiting）只在车辆位于可继续装货的当前站点、没有必须完成的卸货或活动及未收敛的仓位操作、满足 DepartureSafe 且处于 VehicleBusinessReadiness 时成立。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "进入站点离站等待态（StationDepartureWaiting）还要求车载端的当前作业与后续计划投影均为最新。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0214": [
        ("business", "站点离站等待超时（StationDepartureWaitTimeout）：截止瞬间的装货开始与超时结束只能有一项生效。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "站点离站等待超时（StationDepartureWaitTimeout）：服务端以原子互斥和先成功持久化者生效来裁定装货开始与超时结束。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0215": [
        ("business", "站点离站等待超时（StationDepartureWaitTimeout）：车载端断联时本轮截止时间失效，重新进入 StationDepartureWaiting 后从完整时长重新计时。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "站点离站等待超时（StationDepartureWaitTimeout）：重新计时前须完成恢复握手与最新投影对账。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0234": [
        ("domain", "UpcomingStopPlanSnapshot（后续停靠计划快照）是完整的后续停靠投影。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "UpcomingStopPlanSnapshot（后续停靠计划快照）由服务端生成。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "UpcomingStopPlanSnapshot（后续停靠计划快照）携带 planRevision。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0235": [
        ("technical", "UpcomingStopPlanSnapshot（后续停靠计划快照）在计划增删、换序或状态变化时整体替换。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("product", "UpcomingStopPlanSnapshot（后续停靠计划快照）在断联后只能作为明确标记过期的只读信息。", "operator-facing-product-behavior-candidate", "needs-operator-product-owner-and-explicit-approval"),
    ],
    "R08-A0265": [
        ("business", "整站结束提交（StopClosureCommit）后，只有采用最新作业清单与后续计划并重新通过 PreDepartureSafetyCheck 才能请求移动。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "整站结束提交（StopClosureCommit）后由车载端采用最新作业清单与后续计划再请求移动。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("business", "整站结束提交（StopClosureCommit）后移动下发失败不撤销已提交的整站结束，也不重新开放本站操作。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
    ],
    "R08-A0329": [
        ("business", "LoadCompensationCommand（装货补偿指令）只能用于原操作确实处于 LoadCompensationRequired 的情形。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "LoadCompensationCommand（装货补偿指令）由服务端核验后使用原仓位操作尝试编号可靠下发。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0431": [
        ("domain", "TransportDemand 携带冻结的任务类型与 SUBLOT。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "TransportDemand 携带 MES 字段投影。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0472": [
        ("technical", "初稿 §23 的通用 OperationCancelCommand 不进入正式协议。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "装货取消在正式协议中使用 LoadCancellationStartRequested、LoadCancellationAuthorization 和 LoadCancellationResult。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0544": [
        ("technical", "补偿结果必须可靠传递。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "补偿结果必须可去重。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("technical", "补偿结果必须关联原 SlotOperationAttemptId，以支持重启和断线恢复。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0548": [
        ("business", "本站可卸仓位由当前站点、任务目标和在车仓位业务状态共同确定。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("business", "本站一次卸货目标集合可以跨多个 Sublot。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "服务端把本站全部可卸仓位组成一个 UnloadBatch 下发给车载端批量开锁。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0601": [
        ("business", "只有补偿结果完成持久化和核验后才释放整批仓位预留。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("domain", "补偿完成后原 SlotOperationAttemptId 终结为 COMPENSATED。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("domain", "补偿完成后原 DemandId 终结为 CANCELLED_BY_LOAD_COMPENSATION，并且不再进入后续派车。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "补偿完成时服务端持久化取消抑制。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0604": [
        ("business", "任一目标仓位未证明 EMPTY、锁闭反馈无效、开锁输出未复位或结果未被服务端可靠接受时，不得提前取消 DemandId 或释放预留。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "取消终态与取消抑制无法原子持久化时，不得提前取消 DemandId 或释放预留。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0608": [
        ("technical", "LoadCompensationCommand 不改变初稿 §20 的 SlotOperationAttemptId 去重规则。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("business", "LoadCompensationCommand 不是通用取消能力。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
    ],
    "R08-A0714": [
        ("technical", "车载端只在活动装货的最小恢复记录中保留提交的 Sublot 引用。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
        ("domain", "车载端不拥有 Sublot 的任务详情、产品标识或业务生命周期。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
    ],
    "R08-A0723": [
        ("business", "Sublot 不存在、对应任务不唯一或任务状态不允许装货时，拒绝本次输入。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("business", "当前站点不满足 StationTaskTypeAdmission 时，拒绝本次 Sublot 输入。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("business", "料盒数查询失败或结果不是正整数，或者冻结 PACKAGE 缺失、无法唯一匹配批准容量、花篮数量无法换算或为零时，拒绝本次 Sublot 输入。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("business", "Sublot 已存在 SublotReservation 时，拒绝本次输入。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("business", "可用仓位不足以容纳整批时，拒绝本次 Sublot 输入。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "服务端拒绝 Sublot 输入时不分配仓位，也不下发 SlotOperationCommand。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0736": [
        ("product", "装货时车载端只提交 SUBLOT。", "operator-facing-product-behavior-candidate", "needs-operator-product-owner-and-explicit-approval"),
        ("business", "服务端根据 SUBLOT 解析唯一任务和权威花篮数。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
    ],
    "R08-A0772": [
        ("domain", "SUBLOT 的活动占用覆盖待发送、执行中、待取消清空、待补偿和卸货中状态。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "服务端以可持久化的 SUBLOT 活动状态或等效唯一索引实现活动占用。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0807": [
        ("business", "已核验操作员可以提交装货任务取消请求。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "服务端负责验证并持久化取消请求、更新调度并返回新快照。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0828": [
        ("business", "只有车载端可靠上报 LoadCancellationResult 后，服务端才终结任务并释放 SublotReservation 与仓位占用。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("domain", "操作员取消完成时任务终态为 CANCELLED_BY_OPERATOR，且该任务不再进入后续派车。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("technical", "服务端在操作员取消完成时持久化取消抑制记录。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0830": [
        ("business", "只有 ALL_EMPTY 被服务端接受且取消完成后，本次释放的仓位才重新成为可分配仓位。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "取消完成后服务端下发更高 revision 的 CurrentStopWorklistSnapshot。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0865": [
        ("business", "已取消的相同站点任务不得因重启、断线或 MES 再次轮询而重新创建。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "取消必须形成服务端持久化的抑制依据。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0889": [
        ("domain", "取消状态用于解释任务取消原因。", "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"),
        ("business", "运输需求业务键决定调度是否接受后续 MesIngest 投影。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "任务取消不改变 MES 轮询与接入对账。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
    "R08-A0994": [
        ("business", "过期投影不得用于开始、取消或扩展新的业务。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
    ],
    "R08-A1041": [
        ("business", "装货开始、纠错开始与超时提交只能有一项生效。", "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"),
        ("technical", "服务端以原子互斥和先成功持久化者生效来裁定装货开始、纠错开始与超时提交。", "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"),
    ],
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R08"]
    if len(batch_rows) != 57:
        raise RuntimeError(f"R08 batch boundary drift: expected=57 actual={len(batch_rows)}")
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R08"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R08 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 19, "excluded": 38}):
        raise RuntimeError("R08 route boundary drift; expected 19 candidate and 38 excluded documents")
    return [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ], batch_rows


def section_paths(lines: list[str]) -> list[str]:
    headings: list[tuple[int, str]] = []
    result: list[str] = []
    for raw in lines:
        match = re.match(r"^(#{1,6})\s+(.+)$", raw.strip())
        if match:
            level = len(match.group(1))
            headings = [entry for entry in headings if entry[0] < level]
            headings.append((level, common.normalize(match.group(2))))
        result.append(" > ".join(title for _, title in headings) or "document-root")
    return result


def snapshot_context_text() -> str:
    result = subprocess.run(
        ["git", "show", f"{SNAPSHOT_COMMIT}:CONTEXT.md"], cwd=REPO, capture_output=True, check=True,
    )
    digest = hashlib.sha256(result.stdout).hexdigest()
    if digest != SNAPSHOT_CONTEXT_NORMALIZED_SHA256:
        raise RuntimeError(
            f"R08 CONTEXT semantic snapshot drift: expected={SNAPSHOT_CONTEXT_NORMALIZED_SHA256} actual={digest}"
        )
    return result.stdout.decode("utf-8-sig")


def context_units(record_id: str, text: str) -> tuple[list[common.Unit], int, int]:
    lines = text.splitlines()
    sections = section_paths(lines)
    units: list[common.Unit] = []
    term_count = 0
    avoid_count = 0

    # Preserve the scope claim separately; it is evidence about the carrier, not a term approval.
    for index, line in enumerate(lines[:8]):
        if index and line.strip() and not line.startswith("#"):
            units.append(common.Unit(record_id, f"line {index + 1}", sections[index], common.normalize(line), common.normalize(line), "context-carrier-scope"))

    index = 0
    while index < len(lines):
        match = re.match(r"^\*\*(.+?)\*\*:\s*$", lines[index].strip())
        if not match:
            index += 1
            continue
        term_count += 1
        term = common.normalize(match.group(1))
        start = index
        index += 1
        body: list[tuple[int, str]] = []
        avoids: list[tuple[int, str]] = []
        while index < len(lines) and lines[index].strip():
            value = common.normalize(lines[index])
            if re.match(r"^_Avoid_\s*:", value, re.I):
                avoids.append((index, re.sub(r"^_Avoid_\s*:\s*", "", value, flags=re.I)))
            else:
                body.append((index, value))
            index += 1
        context = common.normalize(" ".join(lines[start:index]))
        body_text = common.normalize(" ".join(value for _, value in body))
        for atom in common.split_atomic(body_text):
            location = f"lines {start + 1}-{index}" if index > start + 1 else f"line {start + 1}"
            units.append(common.Unit(record_id, location, sections[start], f"{term}：{atom}", context, "context-definition"))
        for line_index, value in avoids:
            avoid_count += 1
            units.append(common.Unit(record_id, f"line {line_index + 1}", sections[start], f"{term} 禁用同义词：{value}", context, "context-avoid"))
    return units, term_count, avoid_count


def glossary_units(record_id: str, path: Path) -> tuple[list[common.Unit], int]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    sections = section_paths(lines)
    units = [unit for unit in common.markdown_units(record_id, path) if unit.kind != "markdown-table-cell"]
    table_rows = 0
    index = 0
    while index + 1 < len(lines):
        if lines[index].strip().startswith("|") and common.is_table_separator(lines[index + 1]):
            headers = common.split_table(lines[index])
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = common.split_table(lines[index])
                pairs = [f"{headers[pos] if pos < len(headers) else f'col{pos + 1}'}={cell}" for pos, cell in enumerate(cells) if cell]
                if pairs:
                    table_rows += 1
                    statement = " | ".join(pairs)
                    units.append(common.Unit(record_id, f"line {index + 1}", sections[index], statement, statement, "glossary-table-row"))
                index += 1
            continue
        index += 1
    units.sort(key=lambda unit: (int(re.search(r"\d+", unit.location).group()), unit.kind))
    return units, table_rows


def is_metadata_or_rationale(unit: common.Unit) -> bool:
    text = unit.statement
    return bool(
        unit.kind == "context-carrier-scope"
        or re.match(r"^\*\*(?:Status|Considered Options|Consequences)\*\*", text, re.I)
        or re.search(r"（(?:拒绝|采纳)：", text)
        or re.match(r"^(?:同事初稿|为了|为避免|项目允许|本 ADR )", text)
        or re.search(r"后续接口确认稿应|初稿.*应改为", text)
    )


def is_unresolved(text: str) -> bool:
    if re.search(r"待确认(?:应答|结果|消息|回执)", text):
        return False
    return bool(re.search(r"\bTBD\b|待确认术语|待定|尚未确定|尚待|仍需确认|未明确|待补充|是否.*待", text, re.I))


def has_physical_fact(text: str) -> bool:
    return bool(re.search(
        r"一仓一篮|花篮.*(?:尺寸|检测|遮挡|一个)|仓内光幕|光幕.*(?:OCCUPIED|EMPTY|有货|空仓|遮挡|无遮挡)|独立门磁|弹簧弹门|硬件移动联锁|\bDI\d*\b|\bDO\d*\b|500\s*ms|烧锁", text, re.I,
    ))


def has_security_or_role_rule(text: str) -> bool:
    return bool(re.search(r"工号|身份核验|权限|授权|凭证|\bTLS\b|账号|角色|R-\d{2}|维护人员.*确认|生产管理.*批准", text, re.I))


def has_hmi_rule(text: str) -> bool:
    return bool(re.search(r"界面|显示|倒计时|闪烁|黄色|红色|提示|可展开|车载端展示|HMI", text, re.I))


def has_business_rule(text: str) -> bool:
    return bool(re.search(
        r"取消|装货|卸货|离站|停靠|作业|任务类型|站点.*准入|全局唯一占用|整批|纠错|补偿|终态|花篮|子批|无下一.*站|停车点|一台 AGV 对应一台", text, re.I,
    ))


def has_technical_design(text: str) -> bool:
    return bool(re.search(
        r"\b(?:API|HTTP|NDJSON|DTO|SQL|Modbus|ACK|revision|snapshot|messageId|correlationId|protocolVersion|reasonCode)\b"
        r"|数据库|状态机|持久化|投影|快照|协议|消息|字段|唯一键|长连接|去重|幂等|服务端.*下发|车载端.*提交|归服务端|归车载端|单一多对多表|管理端|受控脚本", text, re.I,
    ))


def content_class(unit: common.Unit, source: common.Source) -> tuple[str, str]:
    text = unit.statement
    if source.record_id == "R08-57":
        if unit.kind == "glossary-table-row":
            return "legacy-vocabulary-or-domain-claim-evidence", "evidence-only"
        return "legacy-vocabulary-governance-or-history-evidence", "evidence-only"
    if unit.kind == "context-carrier-scope" or is_metadata_or_rationale(unit):
        return "source-status-rationale-or-derivation-evidence", "evidence-only"
    if unit.kind == "context-avoid":
        return "canonical-term-and-prohibited-synonym-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"
    if is_unresolved(text):
        return "unresolved-domain-or-business-question", "needs-question-resolution"
    physical = has_physical_fact(text)
    security = has_security_or_role_rule(text)
    hmi = has_hmi_rule(text)
    business = has_business_rule(text)
    technical = has_technical_design(text)
    if physical:
        return "physical-fact-or-hardware-constraint-candidate", "needs-hardware-field-evidence-and-explicit-approval"
    if security:
        return "identity-role-or-authorization-rule-candidate", "needs-role-authority-and-explicit-approval"
    if hmi:
        return "operator-facing-product-behavior-candidate", "needs-operator-product-owner-and-explicit-approval"
    if business and technical:
        return "mixed-business-rule-and-technical-design-claim", "needs-atomic-reframing-before-approval"
    if business:
        return "cross-domain-business-rule-candidate", "needs-business-owner-and-explicit-approval"
    if technical:
        return "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"
    if unit.kind == "context-definition":
        return "domain-term-or-invariant-definition-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"
    if source.record_id in ADR_SOURCE_IDS:
        return "embedded-cross-domain-technical-design-decision", "exclude-from-requirement-approval"
    return "domain-or-business-claim-candidate", "needs-domain-owner-and-explicit-approval-before-context-update"


def pointers_for(unit: common.Unit, source: common.Source) -> str:
    text = f"{unit.section} {unit.statement}"
    pointers: list[str] = []
    if source.record_id in {"R08-19", "R08-56"} and re.search(r"操作员|工号|OnboardOperatorContext|OperationSession|清除|离站", text, re.I):
        pointers.append("RES-R08-001")
    if re.search(r"AWAITING_LOAD_CONFIRMATION|LoadFinalConfirmation|待整批确认|最终确认", text, re.I):
        pointers.append("RES-R08-002")
    if source.record_id in {"R08-01", "R08-57"}:
        pointers.append("RES-R08-003")
    if has_physical_fact(text):
        pointers.append("EVID-R08-001")
    if re.search(r"TransportDemandKey|TASK_TYPE.{0,20}SUBLOT|SUBLOT.{0,20}TASK_TYPE|业务键|抑制键", text, re.I):
        pointers.append("CF-R01-001")
    if re.search(r"MES.{0,40}(?:只读|回写|写操作)|(?:只读|回写|写操作).{0,40}MES", text, re.I):
        pointers.append("CF-R01-002")
    return ",".join(dict.fromkeys(pointers)) or NONE


def source_claim_status(source: common.Source) -> str:
    if source.record_id == "R08-01":
        return "unapproved-ai-modified-runtime-vocabulary-carrier"
    if source.record_id == "R08-57":
        return "unapproved-legacy-vocabulary-carrier-retained-as-history"
    return "unapproved-internal-adr-status-is-not-business-approval"


def scope_for(candidate_class: str, route: str) -> str:
    if "physical" in candidate_class or "hardware" in route:
        return "8005-current-AGV-fleet-hardware-and-field-signals"
    if "operator-facing" in candidate_class:
        return "8005-onboard-operator-experience"
    if "identity-role" in candidate_class:
        return "8005-identity-role-and-operation-authorization"
    if route == "exclude-from-requirement-approval":
        return "8005-internal-cross-domain-technical-design"
    if "domain" in candidate_class or "term" in candidate_class or "vocabulary" in candidate_class:
        return "8005-cross-domain-language-and-model"
    return "8005-cross-domain-business-operation"


def approval_gap_for(candidate_class: str, route: str, source: common.Source) -> str:
    gaps = list(CORE_GAP)
    if source.record_id == "R08-57":
        gaps = ["historical-carrier-only", "reconcile-against-approved-context-term"] + gaps
    elif route == "needs-question-resolution":
        gaps.insert(0, "question-resolution")
    elif "hardware" in route:
        gaps = ["bound-hardware-or-field-evidence", "responsible-hardware-authority"] + gaps
    elif "role-authority" in route:
        gaps = ["authorized-role-policy-source", "responsible-security-or-business-authority"] + gaps
    elif "product-owner" in route:
        gaps = ["operator-workflow-source", "responsible-product-or-operations-owner"] + gaps
    elif "business-owner" in route:
        gaps = ["authoritative-business-source", "responsible-business-owner"] + gaps
    elif "domain-owner" in route:
        gaps = ["domain-concept-resolution", "context-update-after-explicit-approval"] + gaps
    elif route == "needs-atomic-reframing-before-approval":
        gaps = ["split-business-obligation-from-technical-mechanism", "authoritative-business-source", "separate-technical-decision-review"] + gaps
    elif route == "exclude-from-requirement-approval":
        gaps = ["authoritative-requirement-source-if-behavior-is-required", "separate-technical-decision-review"] + gaps
    return ";".join(dict.fromkeys(gaps))


def apply_reframings(rows: list[dict[str, str]], sources: list[common.Source]) -> list[dict[str, str]]:
    source_by_id = {source.record_id: source for source in sources}
    mixed = {row["candidate_id"]: row for row in rows if row["baseline_route"] == "needs-atomic-reframing-before-approval"}
    if set(mixed) != set(REFRAMINGS):
        raise RuntimeError(
            f"R08 mixed-reframing boundary drift: expected={sorted(REFRAMINGS)} actual={sorted(mixed)}"
        )
    result: list[dict[str, str]] = []
    for row in rows:
        origin_id = row["candidate_id"]
        replacements = REFRAMINGS.get(origin_id)
        if not replacements:
            result.append(row)
            continue
        source = source_by_id[row["source_record_id"]]
        for facet, statement, candidate_class, route in replacements:
            replacement = dict(row)
            replacement["statement_text"] = statement
            replacement["statement_fingerprint"] = common.fingerprint(statement)
            replacement["candidate_class"] = candidate_class
            replacement["applicable_scope"] = scope_for(candidate_class, route)
            replacement["baseline_route"] = route
            replacement["duplicate_or_derivation"] += (
                f"; reframed-from:{origin_id}; original-statement-fingerprint:{row['statement_fingerprint']}; "
                f"reframed-facet:{facet}"
            )
            replacement["approval_gap"] = approval_gap_for(candidate_class, route, source)
            result.append(replacement)
    return result


def build_rows() -> tuple[list[dict[str, str]], dict[str, int]]:
    sources, _ = load_sources()
    rows: list[dict[str, str]] = []
    structure = {"context_terms": 0, "context_avoid_entries": 0, "glossary_table_rows": 0}
    for source in sources:
        path = REPO / source.path
        if source.record_id == "R08-01":
            # CONTEXT evolved through later approved wayfinder tickets. Rebuild this batch from the fixed
            # Git semantic snapshot while retaining the inventory's exact original worktree-byte SHA-256.
            units, term_count, avoid_count = context_units(source.record_id, snapshot_context_text())
            structure["context_terms"] = term_count
            structure["context_avoid_entries"] = avoid_count
        else:
            actual = common.sha256_file(path)
            if actual != source.digest:
                raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        if source.record_id == "R08-57":
            units, table_rows = glossary_units(source.record_id, path)
            structure["glossary_table_rows"] = table_rows
        elif source.record_id != "R08-01":
            units = common.markdown_units(source.record_id, path)
        if not units:
            raise RuntimeError(f"No atomic units extracted from {source.record_id}")
        for unit in units:
            candidate_class, route = content_class(unit, source)
            pointer = pointers_for(unit, source)
            derivation = (
                f"document-route:R08-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                f"ledger-history:{common.normalize(source.derivation)}"
            )
            rows.append({
                "candidate_id": "", "batch_id": "R08", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest, "exact_location": unit.location,
                "section_path": unit.section, "statement_text": unit.statement, "source_context": unit.context,
                "statement_fingerprint": common.fingerprint(unit.statement), "candidate_class": candidate_class,
                "source_claim_status": source_claim_status(source), "applicable_scope": scope_for(candidate_class, route),
                "baseline_route": route, "duplicate_or_derivation": derivation, "conflict_pointer": pointer,
                "approval_state": "not-approved", "approval_gap": approval_gap_for(candidate_class, route, source),
            })

    # Assign the pre-reframing identities once so provenance can point to the exact
    # quarantined row from the first-pass ledger, then resequence the final ledger.
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R08-A{index:04d}"
    rows = apply_reframings(rows, sources)
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R08-A{index:04d}"
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows, structure


def summary_for(rows: list[dict[str, str]], structure: dict[str, int]) -> dict[str, object]:
    pointers = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer and pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "excluded_batch_documents_not_extracted": 38,
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "pointer_counts": dict(sorted(pointers.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "context_terms": structure["context_terms"],
        "context_avoid_entries": structure["context_avoid_entries"],
        "glossary_table_rows": structure["glossary_table_rows"],
        "legacy_glossary_rows": sum(row["source_record_id"] == "R08-57" for row in rows),
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "reframing_original_rows": len(REFRAMINGS),
        "reframing_output_rows": sum(len(replacements) for replacements in REFRAMINGS.values()),
        "mixed_route_remaining": sum(row["baseline_route"] == "needs-atomic-reframing-before-approval" for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "permanent_requirement_ids": sum(bool(re.search(r"\bREQ-\d{4}\b", row["candidate_id"])) for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if summary["total"] != 1217:
        raise RuntimeError(f"R08 total drift after ticket 54 reframing: {summary['total']}")
    if summary["source_documents"] != 19 or summary["excluded_batch_documents_not_extracted"] != 38:
        raise RuntimeError(f"R08 source coverage mismatch: {summary}")
    if summary["context_terms"] < 80 or summary["context_terms"] != summary["context_avoid_entries"]:
        raise RuntimeError("CONTEXT term / Avoid coverage drift")
    if summary["glossary_table_rows"] < 50:
        raise RuntimeError("Legacy glossary table coverage drift")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R08 approval isolation failed")
    if summary["reframing_original_rows"] != 29 or summary["reframing_output_rows"] != 72:
        raise RuntimeError(f"R08 reframing coverage drift: {summary}")
    if summary["mixed_route_remaining"] != 0:
        raise RuntimeError("R08 mixed statements escaped ticket 54 reframing")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R08 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R08-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R08 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R08 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R08 contains an unauthorized approval upgrade")
    if any(row["source_record_id"] == "R08-57" and row["baseline_route"] != "evidence-only" for row in rows):
        raise RuntimeError("Legacy glossary escaped historical-evidence isolation")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R08 approval gap is incomplete")
    reframed_rows = [row for row in rows if "reframed-from:" in row["duplicate_or_derivation"]]
    if len(reframed_rows) != 72:
        raise RuntimeError("R08 reframed row count does not match the explicit split plan")
    origin_counts = Counter(
        re.search(r"reframed-from:(R08-A\d{4})", row["duplicate_or_derivation"]).group(1)
        for row in reframed_rows
    )
    if origin_counts != Counter({origin: len(replacements) for origin, replacements in REFRAMINGS.items()}):
        raise RuntimeError(f"R08 reframing origin coverage mismatch: {origin_counts}")
    if any("original-statement-fingerprint:" not in row["duplicate_or_derivation"] for row in reframed_rows):
        raise RuntimeError("R08 reframed row lost its original statement fingerprint")
    for required in ("RES-R08-001", "RES-R08-002", "RES-R08-003", "EVID-R08-001"):
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R08 context pointer missing: {required}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R08 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R08 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R08 summary JSON differs from a clean rebuild")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    rows, structure = build_rows()
    summary = summary_for(rows, structure)
    verify(rows, summary)
    if args.verify_only:
        verify_existing(rows, summary)
    else:
        write_outputs(rows, summary)
        verify_existing(rows, summary)
    print(
        "R08 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"context_terms={summary['context_terms']} glossary_table_rows={summary['glossary_table_rows']} "
        f"exact_duplicate_rows={summary['exact_duplicate_rows']} reframed={summary['reframing_original_rows']}->{summary['reframing_output_rows']} "
        f"mixed_route_remaining={summary['mixed_route_remaining']} approval_upgrades={summary['approval_upgrades']} "
        f"pointers={summary['pointer_counts']}"
    )


if __name__ == "__main__":
    main()
