#!/usr/bin/env python3
"""Normalize Springfox OpenAPI specs so Kiota can emit typed models.

Fixes:
- missing info.version / license.name
- schema keys with « » / Chinese characters (invalid OpenAPI component names)
- rewrites all $ref / title occurrences of renamed schemas
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


IDENT_RE = re.compile(r"^[a-zA-Z0-9.\-_]+$")


def sanitize_schema_name(name: str) -> str:
    """Convert Springfox generic / Chinese schema names to OpenAPI-safe identifiers."""
    s = name
    s = s.replace("对象", "Object")
    s = s.replace("«", "_Of_").replace("»", "")
    s = s.replace(",", "_").replace("、", "_").replace(" ", "").replace("/", "_")
    out: list[str] = []
    for ch in s:
        if re.match(r"[a-zA-Z0-9._\-]", ch):
            out.append(ch)
        else:
            out.append(f"u{ord(ch):04x}")
    result = "".join(out)
    # Collapse accidental repeats and ensure it doesn't start with a digit.
    result = re.sub(r"_+", "_", result).strip("._-")
    if not result:
        result = "AnonymousSchema"
    if result[0].isdigit():
        result = "N_" + result
    return result


def collect_schema_renames(schemas: dict[str, object]) -> dict[str, str]:
    renames: dict[str, str] = {}
    used: set[str] = set()

    # Rename longer keys first so nested generics rewrite correctly in text replace.
    for original in sorted(schemas.keys(), key=len, reverse=True):
        if IDENT_RE.fullmatch(original):
            used.add(original)
            continue
        candidate = sanitize_schema_name(original)
        base = candidate
        i = 2
        while candidate in used or (candidate in schemas and candidate != original):
            candidate = f"{base}_{i}"
            i += 1
        renames[original] = candidate
        used.add(candidate)
    return renames


def rewrite_refs(node: object, renames: dict[str, str]) -> object:
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str) and v.startswith("#/components/schemas/"):
                schema_name = v[len("#/components/schemas/") :]
                if schema_name in renames:
                    v = "#/components/schemas/" + renames[schema_name]
            out[k] = rewrite_refs(v, renames)
        return out
    if isinstance(node, list):
        return [rewrite_refs(x, renames) for x in node]
    return node


def normalize_content_types(node: object) -> object:
    """Rewrite Springfox '*/*' content keys to application/json for Kiota."""
    if isinstance(node, dict):
        if "content" in node and isinstance(node["content"], dict):
            content = node["content"]
            if "*/*" in content and "application/json" not in content:
                content = dict(content)
                content["application/json"] = content.pop("*/*")
                node = dict(node)
                node["content"] = content
        return {k: normalize_content_types(v) for k, v in node.items()}
    if isinstance(node, list):
        return [normalize_content_types(x) for x in node]
    return node


def normalize_spec(spec: dict) -> dict:
    info = spec.setdefault("info", {})
    if not info.get("version"):
        info["version"] = "1.0.0"
    license_obj = info.get("license")
    if isinstance(license_obj, dict) and not license_obj.get("name"):
        license_obj["name"] = "Proprietary"
    elif license_obj is not None and not isinstance(license_obj, dict):
        info["license"] = {"name": "Proprietary"}

    components = spec.setdefault("components", {})
    schemas = components.get("schemas") or {}
    if not isinstance(schemas, dict):
        return spec

    renames = collect_schema_renames(schemas)
    if not renames:
        return rewrite_refs(spec, {})  # type: ignore[return-value]

    new_schemas: dict[str, object] = {}
    for old_name, schema in schemas.items():
        new_name = renames.get(old_name, old_name)
        if isinstance(schema, dict):
            schema = dict(schema)
            if schema.get("title") == old_name:
                schema["title"] = new_name
            if new_name != old_name:
                schema["x-original-name"] = old_name
        new_schemas[new_name] = schema

    components["schemas"] = new_schemas
    rewritten = rewrite_refs(spec, renames)
    return normalize_content_types(rewritten)  # type: ignore[return-value]


def process_file(src: Path, dst: Path) -> dict[str, str]:
    with src.open(encoding="utf-8") as f:
        spec = json.load(f)

    schemas_before = (spec.get("components") or {}).get("schemas", {})
    renames = collect_schema_renames(schemas_before) if isinstance(schemas_before, dict) else {}
    normalized = normalize_spec(spec)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return renames


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Source OpenAPI JSON files")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for normalized specs",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for src in args.inputs:
        dst = args.output_dir / src.name
        renames = process_file(src, dst)
        print(f"[preprocess] {src.name}: renamed {len(renames)} schemas -> {dst}")
        bad = [
            k
            for k in json.loads(dst.read_text(encoding="utf-8"))
            .get("components", {})
            .get("schemas", {})
            if not IDENT_RE.fullmatch(k)
        ]
        if bad:
            print(f"[preprocess] ERROR still-invalid names in {src.name}: {bad[:5]}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
