from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import build_and_verify_r03_atomic_candidates as common


REPO = common.REPO
SOURCE_LEDGER = common.SOURCE_LEDGER
OUTPUT = Path(__file__).with_name("R13-atomic-candidates.tsv")
SUMMARY = Path(__file__).with_name("R13-atomic-candidates-summary.json")
FIELDS = common.FIELDS
NONE = "none-found-within-r13-pass"
CORE_GAP = ["named-approver", "approval-date", "approved-scope", "version-or-sha256-binding"]
HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")
EXPECTED_SOURCE_IDS = ["R13-01", "R13-04"] + [f"R13-{index:02d}" for index in range(5, 19)]

TSL_PATH = Path("rcs/riot_ithing_model/standard.oasis.300ul/standard.oasis.300ul.tsl")
TSL_SHA256 = "3b93756ad18896c278cffc1c13711b289aa8236bc79a35e178180581c9faee36"
TSL_BYTES = 53458
SNAPSHOT_ID = "RIOT-OPENAPI-8005-202607-EARLY-01"
SNAPSHOT_ENVIRONMENT = "RIOT-8005-RUNTIME"
SNAPSHOT_BUILD = "v2.2.0.14"

POINTER_DEFINITIONS = {
    "BOUND-R13-001": "R13 只从总账固定的 16 份候选提取；10 份排除材料不从自身生成需求候选。",
    "RES-R13-ENV-001": "“补齐 RIoT 目标环境与受控接口快照证据”绑定环境、build、快照来源与适用范围。",
    "RES-R13-API-001": "“决定 RIoT 项目 API 白名单与调用安全边界”形成封闭操作白名单及调用安全规则。",
    "RES-R13-TSL-001": "“补齐 standard.oasis.300ul 物模型枚举证据”固定原始 TSL 字节内容及未知证据边界。",
    "RES-R13-ENUM-001": "“决定未知物模型枚举值的项目处理规则”固定 UnrecognizedThingModelValue 与最小范围阻断规则。",
    "DEDUP-R13-001": "四份 SDK specs schema 与受控原始 swagger 字节相同，只保留原始快照 operation 候选。",
    "SECRET-R13-001": "项目说明中的 admin/admin 只是不安全示例，不得成为生产凭据或基线配置。",
    "ALIAS-R13-001": "受控 schema 的订单命令路径参数名是 orderKey；批准决策使用 orderId 业务称呼，两者不得静默当作不同 API。",
    "OVERRIDE-R13-001": "物模型问题清单中的补枚举、黑盒反推和应用层处置建议不构成权威语义，冲突处由票据 38/39 的答案覆盖。",
}

# Operation identity is the controlled snapshot's exact method + path. A generic
# service/command operation can represent several separately constrained actions;
# the resolution pointer, not the schema, carries those project constraints.
ALLOWLIST: dict[tuple[str, str], str] = {
    ("GET", "/api/device/v1/devices"): "approved-observation",
    ("GET", "/api/device/v1/devices/statistics/status"): "approved-observation",
    ("POST", "/api/device/v1/command/sync/service/{deviceKey}/{serviceId}"): "approved-safety-critical-state-change",
    ("GET", "/api/task/vehicles/getAllVehicleSimpleInfo"): "approved-observation",
    ("GET", "/api/task/v1/task/getVehicleInfo/{deviceKey}"): "approved-observation",
    ("GET", "/api/task/v1/route/"): "approved-observation",
    ("GET", "/api/task/v1/route/curRemainCost/{orderKey}"): "approved-observation",
    ("GET", "/api/task/v1/route/getCostUnit"): "approved-observation",
    ("POST", "/api/task/v1/route/getRouteCostsBy"): "approved-observation-via-post",
    ("POST", "/api/task/v1/route/queryNearEnd"): "approved-observation-via-post",
    ("POST", "/api/task/v1/route/queryNearestStart"): "approved-observation-via-post",
    ("POST", "/api/task/v1/order/route/{vehicleKey}"): "approved-observation-via-post",
    ("POST", "/api/task/v1/order/command/{orderKey}"): "approved-controlled-state-change",
    ("POST", "/api/task/vehicles/updateVehicleIntegrationLevel"): "approved-controlled-state-change",
    ("POST", "/api/order/v1/add/byDefaultMissions"): "approved-controlled-state-change",
    ("GET", "/api/order/v1/orderRecord/detailByUpperId/{upperId}"): "approved-observation",
    ("GET", "/api/order/v1/orderRecord/detailByOrderId/{orderId}"): "approved-observation",
    ("GET", "/api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson"): "approved-observation",
    ("GET", "/api/imap/v1/mapInfo/stations/{mapId}"): "approved-observation",
    ("GET", "/api/version/v1/infos"): "approved-observation",
    ("POST", "/api/auth/v1/admin/login"): "conditional-human-emergency-auth-backup",
    ("PUT", "/api/auth/v1/admin/refreshToken"): "conditional-human-emergency-auth-backup",
}

SCHEMA_COPY_EXPECTATIONS = {
    "R13-23": "R13-06",
    "R13-24": "R13-09",
    "R13-25": "R13-13",
    "R13-26": "R13-16",
}


def load_sources() -> tuple[list[common.Source], list[dict[str, str]], dict[str, dict[str, str]]]:
    with SOURCE_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        batch_rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == "R13"]
    if len(batch_rows) != 26:
        raise RuntimeError(f"R13 batch boundary drift: expected=26 actual={len(batch_rows)}")
    by_id = {row["record_id"]: row for row in batch_rows}
    candidate_rows = [row for row in batch_rows if row["candidate_group_id"] == "R13"]
    ids = [row["record_id"] for row in candidate_rows]
    if ids != EXPECTED_SOURCE_IDS:
        raise RuntimeError(f"R13 candidate source drift: expected={EXPECTED_SOURCE_IDS} actual={ids}")
    if Counter(row["route_class"] for row in batch_rows) != Counter({"candidate": 16, "excluded": 10}):
        raise RuntimeError("R13 route boundary drift; expected 16 candidate and 10 excluded documents")
    expected_classes = Counter({
        "R13-PN": 1, "R13-IGN": 2, "R13-LA": 1, "R13-SS": 14,
        "R13-DS": 3, "R13-ND": 1, "R13-SD": 4,
    })
    if Counter(row["document_class"] for row in batch_rows) != expected_classes:
        raise RuntimeError("R13 document-role boundary drift")
    sources = [
        common.Source(
            row["record_id"], row["path"], row["sha256"], row["document_class"],
            row["source_type"], row["current_applicability"], row["history_or_derivation"],
        )
        for row in candidate_rows
    ]
    return sources, batch_rows, by_id


def verify_supplemental_tsl() -> dict[str, object]:
    path = REPO / TSL_PATH
    if not path.exists():
        raise RuntimeError(f"Supplemental TSL missing: {TSL_PATH}")
    if path.stat().st_size != TSL_BYTES:
        raise RuntimeError(f"Supplemental TSL byte drift: expected={TSL_BYTES} actual={path.stat().st_size}")
    actual = common.sha256_file(path)
    if actual != TSL_SHA256:
        raise RuntimeError(f"Supplemental TSL hash drift: expected={TSL_SHA256} actual={actual}")
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    profile = doc.get("profile", {})
    if profile.get("productKey") != "standard.oasis.300ul" or str(profile.get("version")) != "1":
        raise RuntimeError("Supplemental TSL identity drift")
    return {
        "path": TSL_PATH.as_posix(), "sha256": actual, "bytes": path.stat().st_size,
        "product_key": profile["productKey"], "profile_version": str(profile["version"]),
        "properties": len(doc.get("properties", [])), "events": len(doc.get("events", [])),
        "services": len(doc.get("services", [])),
        "authority_boundary": "static-content-only; source-version-environment-build-firmware-and-8005-applicability-remain-unbound",
    }


def verify_schema_copy_dedup(by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    mappings: list[dict[str, str]] = []
    for copy_id, canonical_id in SCHEMA_COPY_EXPECTATIONS.items():
        copy_row = by_id[copy_id]
        canonical_row = by_id[canonical_id]
        for row in (copy_row, canonical_row):
            actual = common.sha256_file(REPO / row["path"])
            if actual != row["sha256"]:
                raise RuntimeError(f"R13 schema copy source hash drift: {row['record_id']}")
        if copy_row["sha256"] != canonical_row["sha256"]:
            raise RuntimeError(f"R13 schema copy is no longer byte-identical: {copy_id} -> {canonical_id}")
        mappings.append({
            "excluded_copy_record_id": copy_id,
            "excluded_copy_path": copy_row["path"],
            "canonical_record_id": canonical_id,
            "canonical_path": canonical_row["path"],
            "sha256": canonical_row["sha256"],
            "disposition": "not-extracted-byte-identical-copy",
        })
    return mappings


def json_compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def schema_identity(value: Any) -> str:
    if value is None:
        return "none"
    if isinstance(value, dict):
        if "$ref" in value:
            return str(value["$ref"])
        parts: list[str] = []
        for key in ("type", "format", "title", "description"):
            if value.get(key) not in (None, ""):
                parts.append(f"{key}={common.normalize(str(value[key]))}")
        if "items" in value:
            parts.append(f"items={schema_identity(value['items'])}")
        if "allOf" in value:
            parts.append("allOf=" + "|".join(schema_identity(item) for item in value["allOf"]))
        return ";".join(parts) or json_compact(value)
    return common.normalize(str(value))


def operation_context(doc: dict[str, Any], path_item: dict[str, Any], operation: dict[str, Any]) -> str:
    parameters: list[str] = []
    for parameter in list(path_item.get("parameters", [])) + list(operation.get("parameters", [])):
        if not isinstance(parameter, dict):
            continue
        parameters.append(
            f"{parameter.get('in', '?')}:{parameter.get('name', '?')}:"
            f"required={bool(parameter.get('required', False))}:schema={schema_identity(parameter.get('schema'))}"
        )
    request = operation.get("requestBody")
    request_parts: list[str] = []
    if isinstance(request, dict):
        for media_type, media in sorted(request.get("content", {}).items()):
            request_parts.append(f"{media_type}:{schema_identity(media.get('schema'))}")
    responses: list[str] = []
    for code, response in sorted(operation.get("responses", {}).items(), key=lambda item: str(item[0])):
        content_parts: list[str] = []
        if isinstance(response, dict):
            for media_type, media in sorted(response.get("content", {}).items()):
                content_parts.append(f"{media_type}:{schema_identity(media.get('schema'))}")
        description = common.normalize(str(response.get("description", ""))) if isinstance(response, dict) else ""
        responses.append(f"{code}:{description}:{'|'.join(content_parts) or 'no-content-schema'}")
    security = operation.get("security", doc.get("security", []))
    return "; ".join([
        f"operationId={operation.get('operationId') or 'none'}",
        f"summary={common.normalize(str(operation.get('summary') or operation.get('description') or 'none'))}",
        f"tags={','.join(str(tag) for tag in operation.get('tags', [])) or 'none'}",
        f"parameters={'|'.join(parameters) or 'none'}",
        f"requestBody={'|'.join(request_parts) or 'none'}",
        f"responses={'|'.join(responses) or 'none'}",
        f"security={json_compact(security)}",
    ])


def is_privacy_or_auth_operation(source: common.Source, path: str, operation: dict[str, Any]) -> bool:
    text = f"{path} {operation.get('operationId', '')} {operation.get('summary', '')} {' '.join(operation.get('tags', []))}"
    return source.record_id == "R13-14" or bool(re.search(
        r"/auth/|login|token|user|role|permission|password|credential|secret|privacy|用户|角色|权限|密码|登录|令牌",
        text, re.I,
    ))


def operation_class_and_route(
    source: common.Source, method: str, path: str, operation: dict[str, Any]
) -> tuple[str, str, str]:
    disposition = ALLOWLIST.get((method, path), "not-authorized")
    if disposition == "approved-observation" or disposition == "approved-observation-via-post":
        return (
            "controlled-openapi-operation-allowlisted-observation-evidence",
            "evidence-for-approved-project-integration-behavior",
            disposition,
        )
    if disposition == "approved-controlled-state-change":
        return (
            "controlled-openapi-operation-allowlisted-state-change-evidence",
            "evidence-for-approved-project-integration-behavior",
            disposition,
        )
    if disposition == "approved-safety-critical-state-change":
        return (
            "controlled-openapi-operation-allowlisted-safety-critical-state-change-evidence",
            "evidence-for-approved-project-integration-behavior",
            disposition,
        )
    if disposition == "conditional-human-emergency-auth-backup":
        return (
            "controlled-openapi-operation-conditional-human-emergency-auth-evidence",
            "evidence-for-approved-conditional-auth-backup",
            disposition,
        )
    if is_privacy_or_auth_operation(source, path, operation):
        return (
            "controlled-openapi-privacy-auth-administration-operation-not-authorized-evidence",
            "evidence-only-no-project-authorization",
            disposition,
        )
    return (
        "controlled-openapi-operation-not-authorized-evidence",
        "evidence-only-no-project-authorization",
        disposition,
    )


def build_openapi_rows(source: common.Source) -> list[dict[str, str]]:
    path = REPO / source.path
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    if doc.get("openapi") != "3.0.3":
        raise RuntimeError(f"R13 OpenAPI version drift in {source.record_id}")
    if doc.get("info", {}).get("version") not in (None, ""):
        raise RuntimeError(f"R13 controlled snapshot unexpectedly acquired info.version in {source.record_id}")
    servers = [server.get("url") for server in doc.get("servers", []) if isinstance(server, dict)]
    if servers != ["http://172.19.206.222:8888"]:
        raise RuntimeError(f"R13 controlled snapshot server drift in {source.record_id}: {servers}")
    rows: list[dict[str, str]] = []
    title = common.normalize(str(doc.get("info", {}).get("title") or Path(source.path).stem))
    for api_path, path_item in doc.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for method in HTTP_METHODS:
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            upper_method = method.upper()
            candidate_class, route, disposition = operation_class_and_route(source, upper_method, api_path, operation)
            tags = ",".join(str(tag) for tag in operation.get("tags", [])) or "untagged"
            summary = common.normalize(str(operation.get("summary") or operation.get("description") or operation.get("operationId") or "undocumented operation"))
            statement = f"{upper_method} {api_path} — {summary}"
            context = operation_context(doc, path_item, operation)
            pointers = ["BOUND-R13-001", "RES-R13-ENV-001", "RES-R13-API-001"]
            if api_path == "/api/task/v1/order/command/{orderKey}":
                pointers.append("ALIAS-R13-001")
            rows.append({
                "candidate_id": "", "batch_id": "R13", "source_record_id": source.record_id,
                "source_path": source.path, "source_sha256": source.digest,
                "exact_location": f"paths.{api_path}.{method}",
                "section_path": f"OpenAPI > {title} > {tags} > {upper_method} {api_path}",
                "statement_text": statement, "source_context": context,
                "statement_fingerprint": hashlib.sha256(
                    f"{upper_method}\n{api_path}\n{json_compact(operation)}".encode("utf-8")
                ).hexdigest(),
                "candidate_class": candidate_class,
                "source_claim_status": (
                    f"controlled-static-contract-content; snapshot={SNAPSHOT_ID}; environment={SNAPSHOT_ENVIRONMENT}; "
                    f"source-build={SNAPSHOT_BUILD}; operation-authorization={disposition}; schema-presence-alone-never-authorizes-use"
                ),
                "applicable_scope": (
                    "8005-RIoT-controlled-snapshot-operation-contract-evidence; runtime-compatibility-must-be-rechecked-on-build-or-contract-change"
                ),
                "baseline_route": route,
                "duplicate_or_derivation": (
                    f"document-route:R13-candidate; unit-kind:openapi-operation; source-document-class:{source.document_class}; "
                    f"operation-identity:{upper_method} {api_path}; operation-id:{operation.get('operationId') or 'none'}; "
                    f"allowlist-disposition:{disposition}; snapshot:{SNAPSHOT_ID}; environment:{SNAPSHOT_ENVIRONMENT}; "
                    f"source-build:{SNAPSHOT_BUILD}; schema-copy-dedup:DEDUP-R13-001"
                ),
                "conflict_pointer": ",".join(pointers), "approval_state": "not-approved",
                "approval_gap": approval_gap_for(route),
            })
    if not rows:
        raise RuntimeError(f"No OpenAPI operations extracted from {source.record_id}")
    return rows


def markdown_class_and_route(source: common.Source, unit: common.Unit) -> tuple[str, str]:
    section = unit.section
    text = f"{section} {unit.statement}"
    if source.record_id == "R13-01":
        if re.search(r"本仓库相关资料", section):
            return "local-evidence-navigation-index", "evidence-only"
        if re.search(r"账号|密码|admin|bearer token|登录|HTTP请求头", text, re.I):
            return "security-credential-and-access-boundary-candidate", "needs-security-owner-bound-approved-auth-flow"
        if re.search(r"本项目如何使用", section):
            return "project-riot-integration-behavior-candidate", "needs-project-owner-and-explicit-approval"
        if re.search(r"网页端访问|API访问|获取RIoT API", section):
            return "environment-access-or-interface-discovery-note", "evidence-only-needs-controlled-environment-binding"
        if re.search(r"RCS是什么|斯坦德RCS", section):
            return "external-platform-capability-description-claim", "needs-authoritative-vendor-source-if-required"
        return "local-riot-project-note", "needs-atomic-reframing-before-approval"
    if re.search(r"问题处理结论", section):
        return "superseded-local-thing-model-handling-decision", "exclude-superseded-by-approved-resolution"
    if re.search(r"后续建议", section):
        return "local-thing-model-remediation-or-reverse-engineering-suggestion", "exclude-from-requirement-approval"
    if re.search(r"问题1|问题2|问题3", section):
        return "static-thing-model-gap-or-inconsistency-observation", "evidence-only-unresolved-external-semantics"
    if re.search(r"覆盖完整", section):
        return "static-thing-model-enum-content-observation", "evidence-only-static-content-not-authoritative-semantics"
    if re.search(r"来源文件|检查内容", text):
        return "thing-model-analysis-source-pointer", "evidence-only"
    return "local-thing-model-analysis-claim", "evidence-only-needs-authoritative-version-binding"


def markdown_pointers(source: common.Source, unit: common.Unit) -> list[str]:
    text = f"{unit.section} {unit.statement}"
    pointers = ["BOUND-R13-001"]
    if source.record_id == "R13-01":
        pointers.extend(["RES-R13-ENV-001", "RES-R13-API-001"])
        if re.search(r"admin|账号|密码|bearer|token|登录", text, re.I):
            pointers.append("SECRET-R13-001")
    else:
        pointers.extend(["RES-R13-TSL-001", "RES-R13-ENUM-001"])
        if re.search(r"建议|补充|统一|黑盒|反推|应用层禁止使用|问题处理结论|enumSpecs", text, re.I):
            pointers.append("OVERRIDE-R13-001")
    return list(dict.fromkeys(pointers))


def source_status_for(source: common.Source) -> str:
    if source.record_id == "R13-01":
        return "unapproved-project-integration-note; environment-and-api-boundaries-resolved-only-by-linked-user-decisions"
    return "local-analysis-and-provisional-handling-note; raw-tsl-static-content-bound; unresolved-semantics-and-current-handling-controlled-by-linked-user-decisions"


def build_markdown_rows(source: common.Source) -> list[dict[str, str]]:
    path = REPO / source.path
    units = common.markdown_units(source.record_id, path)
    if not units:
        raise RuntimeError(f"No Markdown atomic units extracted from {source.record_id}")
    rows: list[dict[str, str]] = []
    for unit in units:
        candidate_class, route = markdown_class_and_route(source, unit)
        supplemental = f"; supplemental-tsl:{TSL_PATH.as_posix()}@sha256:{TSL_SHA256}" if source.record_id == "R13-04" else ""
        rows.append({
            "candidate_id": "", "batch_id": "R13", "source_record_id": source.record_id,
            "source_path": source.path, "source_sha256": source.digest,
            "exact_location": unit.location, "section_path": unit.section,
            "statement_text": unit.statement, "source_context": unit.context,
            "statement_fingerprint": common.fingerprint(unit.statement),
            "candidate_class": candidate_class, "source_claim_status": source_status_for(source),
            "applicable_scope": (
                "8005-project-integration-note-needing-linked-decision-control" if source.record_id == "R13-01" else
                "standard.oasis.300ul-static-analysis; product-environment-build-firmware-and-authoritative-version-applicability-remain-unbound"
            ),
            "baseline_route": route,
            "duplicate_or_derivation": (
                f"document-route:R13-candidate; unit-kind:{unit.kind}; source-document-class:{source.document_class}; "
                f"current-applicability:{common.normalize(source.applicability)}; ledger-history:{common.normalize(source.derivation)}{supplemental}"
            ),
            "conflict_pointer": ",".join(markdown_pointers(source, unit)),
            "approval_state": "not-approved", "approval_gap": approval_gap_for(route),
        })
    return rows


def approval_gap_for(route: str) -> str:
    if route in ("evidence-only", "evidence-only-no-project-authorization") or route.startswith("evidence-only-"):
        gaps = ["evidence-only-not-an-independent-requirement-approval-unit"]
    elif route.startswith("evidence-for-approved-"):
        gaps = ["schema-operation-evidence-is-not-the-project-decision", "use-linked-resolution-as-approval-source"]
    elif route.startswith("exclude-superseded"):
        gaps = ["superseded-local-decision-not-an-approval-source", "use-linked-resolution"]
    elif route == "exclude-from-requirement-approval":
        gaps = ["authoritative-source-if-behavior-is-required", "separate-technical-or-research-plan-review"]
    elif "security-owner" in route:
        gaps = ["responsible-security-owner", "approved-credential-lifecycle-and-secret-boundary"]
    elif "project-owner" in route:
        gaps = ["authoritative-project-source", "responsible-project-owner"]
    elif "vendor-source" in route:
        gaps = ["authoritative-vendor-source", "bound-product-environment-build-and-version"]
    elif "atomic-reframing" in route:
        gaps = ["separate-project-obligation-from-platform-description-and-procedure", "responsible-owner-classification"]
    else:
        gaps = ["responsible-owner-classification", "authoritative-source"]
    return ";".join(dict.fromkeys(gaps + CORE_GAP))


def build_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    sources, _, by_id = load_sources()
    tsl = verify_supplemental_tsl()
    dedup = verify_schema_copy_dedup(by_id)
    rows: list[dict[str, str]] = []
    for source in sources:
        path = REPO / source.path
        actual = common.sha256_file(path)
        if actual != source.digest:
            raise RuntimeError(f"Source hash drift: {source.record_id} expected={source.digest} actual={actual}")
        if source.document_class == "R13-SS":
            rows.extend(build_openapi_rows(source))
        else:
            rows.extend(build_markdown_rows(source))
    for index, row in enumerate(rows, start=1):
        row["candidate_id"] = f"R13-A{index:04d}"
    counts = Counter(row["statement_fingerprint"] for row in rows)
    first_by_fingerprint: dict[str, str] = {}
    for row in rows:
        fingerprint = row["statement_fingerprint"]
        if counts[fingerprint] > 1:
            first = first_by_fingerprint.setdefault(fingerprint, row["candidate_id"])
            if first != row["candidate_id"]:
                row["duplicate_or_derivation"] += f"; exact-duplicate-of:{first}"
    return rows, dedup, tsl


def summary_for(rows: list[dict[str, str]], dedup: list[dict[str, str]], tsl: dict[str, object]) -> dict[str, object]:
    operation_rows = [row for row in rows if "unit-kind:openapi-operation" in row["duplicate_or_derivation"]]
    markdown_rows = [row for row in rows if "unit-kind:openapi-operation" not in row["duplicate_or_derivation"]]
    dispositions = Counter()
    methods = Counter()
    for row in operation_rows:
        match = re.search(r"allowlist-disposition:([^;]+)", row["duplicate_or_derivation"])
        dispositions[match.group(1) if match else "missing"] += 1
        methods[row["statement_text"].split(" ", 1)[0]] += 1
    pointers = Counter(
        pointer for row in rows for pointer in row["conflict_pointer"].split(",") if pointer and pointer != NONE
    )
    return {
        "total": len(rows),
        "source_documents": len({row["source_record_id"] for row in rows}),
        "openapi_source_documents": len({row["source_record_id"] for row in operation_rows}),
        "openapi_operations": len(operation_rows),
        "markdown_atomic_statements": len(markdown_rows),
        "excluded_batch_documents_not_extracted": 10,
        "excluded_vendor_manuals_ignored": 2,
        "excluded_local_sdk_design_or_test_documents": 3,
        "excluded_normalized_generated_inputs": 1,
        "excluded_byte_identical_schema_copies": 4,
        "schema_copy_deduplication": dedup,
        "supplemental_tsl_evidence": tsl,
        "snapshot_binding": {
            "snapshot_id": SNAPSHOT_ID, "environment": SNAPSHOT_ENVIRONMENT, "source_build": SNAPSHOT_BUILD,
            "schema_info_version": "missing-in-all-14-source-documents",
        },
        "by_source": dict(sorted(Counter(row["source_record_id"] for row in rows).items())),
        "by_class": dict(sorted(Counter(row["candidate_class"] for row in rows).items())),
        "by_route": dict(sorted(Counter(row["baseline_route"] for row in rows).items())),
        "openapi_by_method": dict(sorted(methods.items())),
        "operation_allowlist_disposition": dict(sorted(dispositions.items())),
        "pointer_counts": dict(sorted(pointers.items())),
        "pointer_definitions": POINTER_DEFINITIONS,
        "exact_duplicate_rows": sum("exact-duplicate-of:" in row["duplicate_or_derivation"] for row in rows),
        "approval_upgrades": sum(row["approval_state"] != "not-approved" for row in rows),
        "permanent_requirement_ids": sum(bool(re.search(r"\bREQ-\d{4}\b", row["candidate_id"])) for row in rows),
    }


def verify(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    if summary["source_documents"] != 16 or summary["openapi_source_documents"] != 14:
        raise RuntimeError(f"R13 source coverage mismatch: {summary['by_source']}")
    if summary["openapi_operations"] != 550:
        raise RuntimeError(f"R13 OpenAPI operation coverage drift: {summary['openapi_operations']}")
    if summary["excluded_batch_documents_not_extracted"] != 10:
        raise RuntimeError("R13 excluded document boundary mismatch")
    if len(summary["schema_copy_deduplication"]) != 4:
        raise RuntimeError("R13 schema copy deduplication mismatch")
    if summary["approval_upgrades"] != 0 or summary["permanent_requirement_ids"] != 0:
        raise RuntimeError("R13 approval isolation failed")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("R13 field schema drift")
    if [row["candidate_id"] for row in rows] != [f"R13-A{index:04d}" for index in range(1, len(rows) + 1)]:
        raise RuntimeError("R13 candidate ID sequence drift")
    if set(summary["by_source"]) != set(EXPECTED_SOURCE_IDS) or any(count <= 0 for count in summary["by_source"].values()):
        raise RuntimeError(f"R13 per-source coverage mismatch: {summary['by_source']}")
    if any(row["approval_state"] != "not-approved" for row in rows):
        raise RuntimeError("R13 contains an unauthorized approval upgrade")
    if any("version-or-sha256-binding" not in row["approval_gap"] for row in rows):
        raise RuntimeError("R13 approval gap is incomplete")
    dispositions = summary["operation_allowlist_disposition"]
    expected_dispositions = Counter(ALLOWLIST.values())
    for disposition, expected_count in expected_dispositions.items():
        if dispositions.get(disposition, 0) != expected_count:
            raise RuntimeError(
                f"R13 allowlist operation coverage mismatch for {disposition}: "
                f"expected={expected_count} actual={dispositions.get(disposition, 0)}"
            )
    if dispositions.get("not-authorized", 0) != 550 - len(ALLOWLIST):
        raise RuntimeError(f"R13 closed allowlist count mismatch: {dispositions}")
    for required in POINTER_DEFINITIONS:
        if required == "DEDUP-R13-001":
            continue
        if summary["pointer_counts"].get(required, 0) <= 0:
            raise RuntimeError(f"Required R13 pointer missing: {required}")
    for required_route in (
        "evidence-for-approved-project-integration-behavior",
        "evidence-for-approved-conditional-auth-backup",
        "evidence-only-no-project-authorization",
        "exclude-superseded-by-approved-resolution",
        "needs-project-owner-and-explicit-approval",
    ):
        if summary["by_route"].get(required_route, 0) <= 0:
            raise RuntimeError(f"Required R13 route missing: {required_route}")


def write_outputs(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_existing(expected_rows: list[dict[str, str]], expected_summary: dict[str, object]) -> None:
    if not OUTPUT.exists() or not SUMMARY.exists():
        raise RuntimeError("R13 outputs do not exist; run without --verify-only first")
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        actual_rows = list(csv.DictReader(handle, delimiter="\t"))
    actual_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if actual_rows != expected_rows:
        raise RuntimeError("R13 canonical TSV differs from a clean rebuild")
    if actual_summary != expected_summary:
        raise RuntimeError("R13 summary JSON differs from a clean rebuild")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    rows, dedup, tsl = build_rows()
    summary = summary_for(rows, dedup, tsl)
    verify(rows, summary)
    if args.verify_only:
        verify_existing(rows, summary)
    else:
        write_outputs(rows, summary)
        verify_existing(rows, summary)
    print(
        "R13 atomic candidates verified: "
        f"total={summary['total']} sources={summary['source_documents']} "
        f"openapi_operations={summary['openapi_operations']} markdown={summary['markdown_atomic_statements']} "
        f"excluded_not_extracted={summary['excluded_batch_documents_not_extracted']} "
        f"schema_copies_deduped={summary['excluded_byte_identical_schema_copies']} "
        f"allowlist={summary['operation_allowlist_disposition']} "
        f"exact_duplicate_rows={summary['exact_duplicate_rows']} approval_upgrades={summary['approval_upgrades']}"
    )


if __name__ == "__main__":
    main()
