# -*- coding: utf-8 -*-
import json
import os

p = r"c:\Users\szy\Desktop\xinji\8005多仓位AGV\rcs\riot-sdk\specs\task.json"
with open(p, "r", encoding="utf-8") as f:
    spec = json.load(f)

schemas = spec["components"]["schemas"]
out = {}
for k, v in schemas.items():
    props = v.get("properties") or {}
    if (
        set(props) >= {"mapId", "stationId"}
        or set(props) >= {"mapId", "deviceKeys"}
        or "代价" in k
        or "终点" in k
        or "起点" in k
        or k == "CostUnit"
        or "RepDevice" in k
        or "Cost" in k
    ):
        out[k] = v

# also pull refs from route path request bodies
for path, item in spec["paths"].items():
    if "/route/" not in path and not path.endswith("/route/"):
        continue
    for method, op in item.items():
        rb = (op.get("requestBody") or {}).get("content") or {}
        for ctype, c in rb.items():
            ref = ((c.get("schema") or {}).get("$ref") or "").split("/")[-1]
            if ref and ref in schemas:
                out[ref] = schemas[ref]
        resp = (op.get("responses") or {}).get("200", {})
        content = resp.get("content") or {}
        for ctype, c in content.items():
            ref = ((c.get("schema") or {}).get("$ref") or "").split("/")[-1]
            if ref and ref in schemas:
                out[ref] = schemas[ref]
                # unwrap ResponseMsg generics if present as separate schema
                inner = schemas[ref]
                for prop in (inner.get("properties") or {}).values():
                    iref = (prop.get("$ref") or "").split("/")[-1]
                    if iref and iref in schemas:
                        out[iref] = schemas[iref]

op = r"c:\Users\szy\Desktop\xinji\8005多仓位AGV\rcs\riot-behavior-lab\evidence\rounds\2026-07-20-round-15\_schemas-route.json"
os.makedirs(os.path.dirname(op), exist_ok=True)
with open(op, "w", encoding="utf-8") as f:
    json.dump({"keys": list(out.keys()), "schemas": out}, f, ensure_ascii=False, indent=2)
print("wrote", len(out), "schemas to", op)
for k in out:
    print("-", k)
