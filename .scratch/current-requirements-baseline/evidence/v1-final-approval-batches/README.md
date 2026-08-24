# `v1.0.0` 最终批准批次

本目录记录票据《生成首版原子需求最终批准批次》的确定性产物。它只建立 HITL 审阅单位，不批准任何需求。

- `v1-final-approval-batches.tsv`：95 张最终批准票的规范清单；覆盖 `REQ-0001`～`REQ-0348`，每批至多 4 条。
- `legacy-102-batch-suggestion-review.tsv`：逐项复核旧 102 个建议批次。旧建议面向 6,449 条未批准旧来源声明，未绑定当前 `REQ`、精确规范文本、范围和验证方法，因此全部退出“最终批准单位”，只保留领域与责任角色参考价值。
- `v1-final-approval-batches-summary.json`：覆盖、唯一性、阻塞与零批准升级门禁摘要。
- `build_and_verify_v1_final_approval_batches.py`：确定性生成与 `--verify-only` 失败式核验入口。

批次身份由 `Batch`、`Approval payload SHA-256` 和候选总账 SHA-256 共同固定。批准票后续追加 `## Answer` 不改变被批准 payload；若任一候选绑定字段改变，必须重新生成 payload 并重新批准。
