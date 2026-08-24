#!/usr/bin/env python3
"""Build the v1.0.0 canonical requirement candidate and source-disposition ledgers.

The output is deliberately a candidate ledger, not an approved baseline. Permanent-looking
REQ numbers are reservations for final item approval; legacy R01-R13 rows are never promoted
by this program.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ISSUES = ROOT / ".scratch/current-requirements-baseline/issues"
ATOMIC = ROOT / ".scratch/current-requirements-baseline/evidence/atomic-candidates"

SPEC_SOURCES = [
    {
        "path": ".scratch/new-mes-ingest/spec.md",
        "blob": "9104575426c60f71ed8020d3d231c3332e2c0589",
        "sha256": "bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f",
        "layer": "L1-base-current-source",
        "scope": "8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录",
        "supersession": "整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84",
    },
    {
        "path": ".scratch/mes-ingest-bounded-storage-low-memory/spec.md",
        "blob": "099feeef433a0b356c41c90e221ee7d5bafcface",
        "sha256": "23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6",
        "layer": "L2-partial-later-layer",
        "scope": "8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界",
        "supersession": "仅在声明范围内替代 L1；L1 其余领域语义继续有效",
    },
    {
        "path": ".scratch/mes-ingest-watch-area-live-sync/spec.md",
        "blob": "c6050a6102abc6b24f330187af7010fad15736b4",
        "sha256": "8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0",
        "layer": "L3-partial-later-layer",
        "scope": "8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照",
        "supersession": "仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围",
    },
    {
        "path": ".scratch/demand-series-inspector-e/spec.md",
        "blob": "2b4a2b326a3df2635e56977b22feb8686d0c0cca",
        "sha256": "c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657",
        "layer": "L4-partial-later-layer",
        "scope": "8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构",
        "supersession": "仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变",
    },
]

# Product/domain decisions. Governance-only HITL tickets remain method/evidence and do not
# become product requirement candidates.
PRODUCT_DECISION_NUMBERS = {
    27, 28, 37, 39, 56, 57, 58, 59, 62, 64, 65, 66, 67, 68, 69, 70,
    71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 83,
}

# Direct user-confirmed hardware facts are also current source material even though their
# tracker type is task rather than grilling.
PRODUCT_EVIDENCE_NUMBERS = {35}

# User Stories and Solution remain source evidence. Implementation Decisions are the selected
# canonical layer because they restate the effective obligations after the specs' internal
# trade-offs and therefore avoid assigning two candidate REQ identities to the same obligation.
IN_SCOPE_SPEC_SECTIONS = {"Implementation Decisions"}
SKIP_HEADING_WORDS = ("Out of Scope", "Further Notes", "Testing Decisions", "Golden renderer")
GOVERNANCE_POINTER = "issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_pointer(value: str) -> str:
    value = value.strip().replace("\\", "/")
    if value.startswith("../"):
        value = value[3:]
    if "/issues/" in value:
        value = "issues/" + value.split("/issues/", 1)[1]
    return value


def clean_markdown(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", value).strip()


def title_for(text: str) -> str:
    value = re.sub(r"^(系统|服务端|车载端|Watch|用户|实现)应当", "", text)
    return value[:54] + ("…" if len(value) > 54 else "")


def verification_for(text: str, source_path: str) -> str:
    lower = text.casefold()
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("遵循 ADR-mes-0007 的技术栈："):
        return "以发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API；Oracle 源用 fake executor 验证单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，并以受控工厂 Oracle 11g Thin 探针、必要时 Thick 复验；未执行现场项必须明确为 skip，不得宣称已通过"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("每个 SUCCESS 使用一个 ProjectionCommit 原子提交"):
        return "以脚本化 SUCCESS 轮次进入生产 Host/领域入口，在真实 SQL Server 的 ProjectionCommit 多个阶段注入失败并经正式 API 读回，证明 PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 共同提交或共同回滚；重试同一完整轮次只能提交一次"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("DemandSeries 由大小写与空白规则明确的 TransportDemandKey"):
        return "以同一组由版本化契约明确给出的大小写与空白等价／非等价表驱动样例，经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询读回，证明 TransportDemandKey 在各层作出相同的合并或区分且无层内自行正规化；任一层结果不一致即失败"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("归档是不可逆生命周期转换"):
        return "以脚本化完整 SUCCESS 轮次经生产 Host／领域入口，在真实 SQL Server 中驱动同一 TransportDemandKey 由 GONE 满 12 小时归档后再次出现，并通过正式 API、ExternallyReadableDemandCatalog 与 Watch 查询读回，证明原 SeriesId 不变、新建 Demand 世代、产生 LONG_GONE_BUT_VISIBLE，且该 Demand 在后续轮次与服务重启后仍不进入外部可读目录；公开 WPF／会话 seam 仅补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("SeriesErrorCatalog 由领域契约版本化发布"):
        return "以至少两个连续领域契约／Host／API 版本及真实 SQL Server 升级验收，先写入第一版五个代码、四个主分类和历史错误证据，再经生产 Host／领域入口、正式 API/OpenAPI 与 Watch 查询核对新增和 deprecated 行为；证明已发布代码的含义、主分类、作用域与严重度均未改变或复用，旧历史未被回扫重写，任何非法换义、复用、重分类或改作用域的契约变更都由兼容性门禁失败阻止"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("DemandSeriesCurrentCondition 是 DemandSeriesEvent 的当前投影"):
        return "以脚本化完整 SUCCESS 轮次经生产 Host／领域入口产生、更新、清除并复发 Series 错误事件，在真实 SQL Server 中核对 DemandSeriesEvent 与 DemandSeriesCurrentCondition，并通过正式 API 及 Watch 查询读回；证明当前条件可由事件确定性重建且不拥有独立聚合身份、修订序列或 incident 生命周期，IngestAlert 不再为 Series 错误另建、续期或关闭独立 incident"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("DemandSeriesErrorPeriod 从事件推导并永久保留"):
        return "以脚本化完整 SUCCESS 轮次经生产 Host／领域入口驱动错误出现、证据变化、条件消失、复发、Demand 世代更替与服务重启，在真实 SQL Server 中核对 DemandSeriesEvent、DemandSeriesErrorPeriod 和逐世代证据，并通过正式 API 及 Watch 查询读回；证明期间由事件确定性推导且结束后永久保留，Demand 级期间绝不跨 DemandId，Series 级期间可以跨世代但每个涉及世代都有可读证据"
    if source_path.endswith("new-mes-ingest/spec.md") and text.startswith("Series 错误证据使用 Host 在完整成功轮次中的 UTC 时间"):
        return "以可控时钟为 Host 完整 SUCCESS 轮次注入与 MesSourceDate、Watch 本机时区／时间彼此不同的时间值，经生产 Host／领域入口写入真实 SQL Server，并通过正式 API、错误期间历史与 Watch 查询读回；证明期间开始、证据与结束边界只等于 Host 轮次 UTC，失败或不完整轮次不产生边界，服务重启和 Watch 时区变化不改变既有边界；公开 WPF／会话 seam 仅补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准"
    if source_path.endswith("mes-ingest-watch-area-live-sync/spec.md"):
        if text.startswith("跨进程事务锁："):
            return "以隔离配置目录中的真实锁文件和并发进程／Store 实例验证所有读写均受同一跨进程事务锁保护，并覆盖竞争、超时、异常释放与恢复；不得用 SQL Server 事务替代文件锁证据"
        if text == "只有应用动作才把解析结果写入快照":
            return "通过隔离配置目录、可注入时钟与公开 WatchAreaFilterProfileStore／会话 seam，证明文件编辑、外部同步、非法化和删除均不改写活动快照，只有显式应用动作原子持久化解析后的 AREA 序列"
        if text == "快照不依赖文件存在或合法，进程重启后仍然有效":
            return "通过公开 WatchAreaFilterProfileStore seam 在文件存在、非法、删除及重新创建 Store／进程重启场景中读回 .active-profile，证明最后已应用 AREA 快照保持有效；不得用 SQL Server 或 Oracle 结果替代本地活动标记证据"
    if any(k in lower for k in ("急停", "安全", "光幕", "仓门", "隔离", "充电")):
        return "以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过"
    if any(k in lower for k in ("watch", "窗口", "界面", "焦点", "键盘", "automation", "布局", "显示")):
        return "以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准"
    if any(k in lower for k in ("api", "dto", "openapi", "cursor", "分页", "etag", "catalog")):
        return "以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对"
    if any(k in lower for k in ("sql", "oracle", "poll", "轮次", "快照", "事务", "持久")):
        return "以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明"
    if source_path.endswith("35-supply-slot-hardware-and-field-signal-evidence.md"):
        return "以具名用户确认记录为身份/语义证据；实施验收时逐车逐仓核对 IO、有效电平和物理动作"
    return "按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then"


def iter_markdown_units(path: Path, mode: str):
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[tuple[int, str]] = []
    active = False
    for line_no, raw in enumerate(lines, 1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", raw)
        if match:
            level = len(match.group(1))
            heading = clean_markdown(match.group(2))
            headings = [item for item in headings if item[0] < level]
            headings.append((level, heading))
            if mode == "spec" and level == 2:
                active = heading in IN_SCOPE_SPEC_SECTIONS
            elif mode == "answer" and level == 2:
                active = heading == "Answer"
            continue
        if not active or any(word in " > ".join(h for _, h in headings) for word in SKIP_HEADING_WORDS):
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+?)\s*$", raw)
        numbered = re.match(r"^\s*\d+[.)]\s+(.+?)\s*$", raw)
        table = re.match(r"^\s*\|(.+)\|\s*$", raw)
        text = None
        kind = "verbatim-list-item"
        if bullet or numbered:
            text = clean_markdown((bullet or numbered).group(1))
        elif table:
            cells = [clean_markdown(cell) for cell in table.group(1).split("|")]
            if cells and not all(re.fullmatch(r":?-+:?", cell or "-") for cell in cells):
                if not any(cell in {"规则", "内容", "行为", "按钮", "运行"} for cell in cells):
                    text = "；".join(cell for cell in cells if cell)
                    kind = "table-row-preserved"
        if text and len(text) >= 4:
            yield {
                "line": line_no,
                "section": " > ".join(h for _, h in headings),
                "verbatim": text,
                "canonical": text,
                "derivation": kind,
            }


def source_identity(path_text: str) -> tuple[str, str]:
    path = ROOT / path_text
    data = path.read_bytes()
    return sha256_bytes(data), "git blob recorded separately where available"


def collect_candidates():
    rows = []
    source_index = defaultdict(list)

    for spec in SPEC_SOURCES:
        path = ROOT / spec["path"]
        actual = sha256_bytes(path.read_bytes())
        if actual != spec["sha256"]:
            raise SystemExit(f"approved source drift: {spec['path']} expected {spec['sha256']} got {actual}")
        for unit in iter_markdown_units(path, "spec"):
            rows.append({
                "title": title_for(unit["canonical"]),
                "canonical_text": unit["canonical"],
                "scope": spec["scope"],
                "source_layer": spec["layer"],
                "primary_source": spec["path"],
                "exact_location": f"{unit['section']}; line {unit['line']}",
                "verbatim_extract": unit["verbatim"],
                "source_blob": spec["blob"],
                "source_sha256": spec["sha256"],
                "source_authority": "用户本人；票据 84 将该精确文件身份批准为首版候选来源",
                "source_approval_evidence": GOVERNANCE_POINTER,
                "derivation": unit["derivation"],
                "ai_involvement": "none" if unit["canonical"] == unit["verbatim"] else "generated",
                "source_layers_and_differences": spec["supersession"],
                "prebaseline_source_supersession": spec["supersession"],
                "decision_pointers": GOVERNANCE_POINTER,
                "legacy_candidate_ids": "",
                "conflict_disposition": "按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并",
                "verification_method": verification_for(unit["canonical"], spec["path"]),
                "candidate_status": "candidate-awaiting-final-item-approval",
                "final_approval_gap": "需用户在票据 88 对该精确规范文本、范围和验证方法逐项或按可核查批次最终批准",
            })

    issue_files = sorted(ISSUES.glob("*.md"))
    for path in issue_files:
        number_match = re.match(r"(\d+)-", path.name)
        if not number_match:
            continue
        number = int(number_match.group(1))
        if number not in PRODUCT_DECISION_NUMBERS | PRODUCT_EVIDENCE_NUMBERS:
            continue
        text = path.read_text(encoding="utf-8")
        if "Status: resolved" not in text:
            continue
        rel = path.relative_to(ROOT / ".scratch/current-requirements-baseline").as_posix()
        digest = sha256_bytes(path.read_bytes())
        kind = "L5-resolved-product-decision" if number in PRODUCT_DECISION_NUMBERS else "L5-user-confirmed-domain-evidence"
        for unit in iter_markdown_units(path, "answer"):
            # Meta statements describe the wayfinding process, not the product.
            if any(phrase in unit["canonical"] for phrase in (
                "本票", "本决定只", "没有形成新的领域词汇", "无需修改 CONTEXT.md",
                "Assets", "后续票据", "解除", "推荐值授权",
            )):
                continue
            rows.append({
                "title": title_for(unit["canonical"]),
                "canonical_text": unit["canonical"],
                "scope": "8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准",
                "source_layer": kind,
                "primary_source": f".scratch/current-requirements-baseline/{rel}",
                "exact_location": f"{unit['section']}; line {unit['line']}",
                "verbatim_extract": unit["verbatim"],
                "source_blob": "worktree-markdown-issue",
                "source_sha256": digest,
                "source_authority": "用户本人作为默认且唯一最终批准人；决定内容记录于来源票据",
                "source_approval_evidence": rel,
                "derivation": unit["derivation"],
                "ai_involvement": "none" if unit["canonical"] == unit["verbatim"] else "generated",
                "source_layers_and_differences": "该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账",
                "prebaseline_source_supersession": "resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated",
                "decision_pointers": rel,
                "legacy_candidate_ids": "",
                "conflict_disposition": f"resolved real conflict or ambiguity by {rel}",
                "verification_method": verification_for(unit["canonical"], path.name),
                "candidate_status": "candidate-awaiting-final-item-approval",
                "final_approval_gap": "来源决定已获确认，但首版仍需对本条精确规范文本、范围和验证方法作原子/可核查批次批准",
            })

    # Exact canonical duplicates collapse only when text and scope agree. All source layers stay visible.
    merged = []
    by_key = {}
    for row in rows:
        key = (row["canonical_text"].casefold(), row["scope"])
        if key not in by_key:
            by_key[key] = row
            merged.append(row)
        else:
            prior = by_key[key]
            for field in ("primary_source", "exact_location", "source_sha256", "source_approval_evidence", "decision_pointers"):
                values = [v for v in (prior[field].split(" | ") + [row[field]]) if v]
                prior[field] = " | ".join(dict.fromkeys(values))
            prior["source_layers_and_differences"] += " | exact duplicate source retained"

    for index, row in enumerate(merged, 1):
        row["req_candidate_id"] = f"REQ-{index:04d}"
        row["introduced_in"] = "v1.0.0-candidate"
        row["lifecycle"] = "candidate-active"
        row["supersedes_req"] = "none (no earlier approved baseline)"
        row["canonical_text_sha256"] = sha256_bytes(row["canonical_text"].encode("utf-8"))
        for pointer in row["decision_pointers"].split(" | "):
            source_index[normalize_pointer(pointer)].append(row["req_candidate_id"])
    return merged, source_index


def collect_source_dispositions(source_index):
    post_by_candidate = {}
    post_path = ATOMIC / "R01-R13-post-conflict-question-review.tsv"
    with post_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            post_by_candidate[row["candidate_id"]] = row

    conflict_to_issue = {
        "CF-R01-001": "issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md",
        "CF-R01-002": "issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md",
        "CF-R09-001": "issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md",
        "CF-R09-002": "issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md",
    }
    rows = []
    source_path = ATOMIC / "R01-R13-consolidated-atomic-candidates.tsv"
    with source_path.open(encoding="utf-8", newline="") as handle:
        for source in csv.DictReader(handle, delimiter="\t"):
            candidate_id = source["candidate_id"]
            post = post_by_candidate.get(candidate_id)
            pointers = []
            rationale = ""
            if post:
                ptr = normalize_pointer(post["resolution_pointer"])
                if ptr.startswith("issues/"):
                    pointers.append(ptr)
                rationale = post["review_rationale"]
            for conflict in filter(None, source.get("graduate_conflict_pointers", "").split(",")):
                if conflict.strip() in conflict_to_issue:
                    pointers.append(conflict_to_issue[conflict.strip()])
            refs = []
            for pointer in dict.fromkeys(pointers):
                refs.extend(source_index.get(pointer, []))
            refs = list(dict.fromkeys(refs))
            disposition = source["review_disposition"]
            if post:
                disposition = post["post_conflict_disposition"]
            if refs:
                trace = "trace-to-current-candidate-source"
            elif disposition in {"evidence-only", "duplicate-or-evidence-only"}:
                trace = "preserved-evidence-only"
            elif disposition in {"excluded-not-for-requirement-approval", "out-of-current-destination"}:
                trace = "preserved-excluded-or-out-of-scope"
            else:
                trace = "preserved-unapproved-not-promoted"
            rows.append({
                "legacy_candidate_id": candidate_id,
                "source_path": source["source_path"],
                "exact_location": source["exact_location"],
                "statement_sha256": source["exact_text_sha256"],
                "original_approval_state": source["approval_state"],
                "original_review_disposition": source["review_disposition"],
                "post_conflict_disposition": post["post_conflict_disposition"] if post else "not-in-post-conflict-review",
                "resolution_pointers": " | ".join(dict.fromkeys(pointers)),
                "candidate_req_refs": " | ".join(refs),
                "v1_traceability_disposition": trace,
                "rationale": rationale or "原声明保持原文、原批准状态和原适用范围；只有当前规范层文本可取得候选 REQ 身份",
                "promotion_effect": "none",
            })
    return rows


def write_tsv(path: Path, rows):
    if not rows:
        raise SystemExit(f"refusing to write empty output: {path}")
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify(candidates, dispositions):
    expected_ids = [f"REQ-{index:04d}" for index in range(1, len(candidates) + 1)]
    actual_ids = [row["req_candidate_id"] for row in candidates]
    if actual_ids != expected_ids or len(actual_ids) != len(set(actual_ids)):
        raise SystemExit("candidate REQ reservations are not unique and contiguous")
    required = set(candidates[0])
    for row in candidates:
        if set(row) != required or any(value is None or value == "" for key, value in row.items() if key not in {"legacy_candidate_ids"}):
            raise SystemExit(f"candidate row has missing fields: {row.get('req_candidate_id')}")
        if sha256_bytes(row["canonical_text"].encode("utf-8")) != row["canonical_text_sha256"]:
            raise SystemExit(f"canonical text hash mismatch: {row['req_candidate_id']}")
        if row["candidate_status"] != "candidate-awaiting-final-item-approval":
            raise SystemExit("generator may not final-approve candidates")
    if len(dispositions) != 12452 or len({row["legacy_candidate_id"] for row in dispositions}) != 12452:
        raise SystemExit("legacy source ledger must preserve exactly 12,452 unique rows")
    if any(row["promotion_effect"] != "none" for row in dispositions):
        raise SystemExit("legacy source row was promoted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    candidates, source_index = collect_candidates()
    dispositions = collect_source_dispositions(source_index)
    legacy_by_req = defaultdict(list)
    for row in dispositions:
        for req_id in filter(None, row["candidate_req_refs"].split(" | ")):
            legacy_by_req[req_id].append(row["legacy_candidate_id"])
    for row in candidates:
        linked = legacy_by_req.get(row["req_candidate_id"], [])
        row["legacy_candidate_ids"] = " | ".join(linked) if linked else "none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv"
    verify(candidates, dispositions)
    candidate_path = OUT / "v1-canonical-requirement-candidates.tsv"
    source_path = OUT / "v1-legacy-source-disposition.tsv"
    if args.verify_only:
        if read_tsv(candidate_path) != candidates:
            raise SystemExit("saved candidate ledger differs from deterministic rebuild")
        if read_tsv(source_path) != dispositions:
            raise SystemExit("saved source-disposition ledger differs from deterministic rebuild")
        summary = json.loads((OUT / "v1-canonical-requirement-candidates-summary.json").read_text(encoding="utf-8"))
        if summary["candidate_ledger_sha256"] != sha256_bytes(candidate_path.read_bytes()):
            raise SystemExit("candidate ledger hash differs from saved summary")
        if summary["source_disposition_ledger_sha256"] != sha256_bytes(source_path.read_bytes()):
            raise SystemExit("source-disposition ledger hash differs from saved summary")
    else:
        write_tsv(candidate_path, candidates)
        write_tsv(source_path, dispositions)
        summary = {
            "schema_version": 1,
            "target_version": "v1.0.0",
            "candidate_status": "awaiting-final-item-approval",
            "candidate_requirements": len(candidates),
            "candidate_sources_by_layer": dict(sorted(Counter(row["source_layer"] for row in candidates).items())),
            "legacy_source_rows": len(dispositions),
            "legacy_traceability_dispositions": dict(sorted(Counter(row["v1_traceability_disposition"] for row in dispositions).items())),
            "legacy_promotion_upgrades": 0,
            "approved_source_identity_drift": 0,
            "candidate_ledger_sha256": sha256_bytes(candidate_path.read_bytes()),
            "source_disposition_ledger_sha256": sha256_bytes(source_path.read_bytes()),
            "method": "current-layer extraction + exact text/scope dedupe + explicit source-layer preservation; no semantic auto-merge",
            "guardrail": "REQ numbers are candidate reservations only until ticket 88 records final approval of exact text, scope, verification method, and batch identity.",
        }
        (OUT / "v1-canonical-requirement-candidates-summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps({
        "candidate_requirements": len(candidates),
        "legacy_source_rows": len(dispositions),
        "linked_legacy_rows": sum(bool(row["candidate_req_refs"]) for row in dispositions),
        "approved_source_identity_drift": 0,
        "legacy_promotion_upgrades": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
