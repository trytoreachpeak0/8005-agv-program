# `v1.0.0` 剩余最终批准批次集中审批记录

## 批准身份

- Approver: 用户本人（本地图默认且唯一最终批准人；见 [`issues/03-final-baseline-approver.md`](../../issues/03-final-baseline-approver.md)）
- Approved At: `2026-08-24T15:16:06Z`
- Approval Evidence: 本次 Codex 任务中，用户先明确要求采用“并行只读核对、集中审批、单一写入”的压缩流程，随后在完整汇总结论和异常处置方案展示后明确回复“同意”。
- Candidate Ledger: [`v1-canonical-requirement-candidates.tsv`](../v1-canonical-candidates/v1-canonical-requirement-candidates.tsv)，SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`
- Approval Batch Manifest: [`v1-final-approval-batches.tsv`](v1-final-approval-batches.tsv)，SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`
- Covered Tickets: `93`–`183`
- Covered Requirements: `REQ-0017`–`REQ-0348`（332 条）
- Approved Scope: 各票据所列精确规范文本、适用范围、验证方法、来源身份、冲突处置及当前 approval payload；不扩大到票据明确保留为投运前或现场验证的事实边界。

## 并行只读核对

三个隔离工作树分别核对票据 `93`–`123`、`124`–`153`、`154`–`183`。核对范围包括候选总账、批次 manifest、每票 payload、REQ 成员、规范文本及其 SHA-256、验证方法、来源身份、已解决决定和仍需人工判断的例外。

- A：31 张票、119 条 REQ；31 张可集中批准，0 例外，0 未解决证据缺口。
- B：30 张票、107 条 REQ；29 张可集中批准；票据 127 的 `REQ-0149` 存在显示文本与总账文本/hash 的机械漂移；0 业务语义例外，0 未解决证据缺口。
- C：30 张票、106 条 REQ；30 张可集中批准，0 例外，0 未解决证据缺口。

## 机械异常处置

票据 127 的生成器曾把 `REQ-0149` 规范文本中的字面量 `serviceId=enable|disable` 渲染为 `serviceId=enable／disable`，而记录的规范文本 SHA-256 与 payload 始终绑定候选总账中的原始精确文本。

用户明确授权按候选总账机械修复、重新生成身份后随其余推荐一并批准。修复结果：

- `REQ-0149` 精确文本恢复为候选总账中的 `serviceId=enable|disable`；没有业务含义变更。
- Ticket 127 Approval Payload SHA-256 保持 `54e87924094ecb63c19c7a445320a16043c5122917ab79df9382cabad57d224e`。
- Ticket 127 corrected initial ticket SHA-256 为 `ed2ca2bb5cf19464f11e0fbe8e92d884817eac1bbfa02c2f2b44f953b9d9c2a6`。
- 修正后的 manifest SHA-256 为 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`。
- 批次生成器 `--verify-only` 已对 95 批、348 条 REQ、零重复、零遗漏通过确定性核验。

## 最终批准结论

用户批准票据 `93`–`183` 中所有 `REQ-0017`–`REQ-0348` 的推荐结论，即逐项批准各票所展示并由当前候选总账、当前 manifest、各票 Batch 与 Approval Payload SHA-256 共同绑定的精确规范文本、范围和验证方法进入 `v1.0.0`。

本批准不复用旧候选总账下的 `Superseded Answer`。每张票仍须分别记录本集中批准证据、自己的 Batch、payload、REQ 列表和逐项批准结论后才能设为 `resolved`。

用户同时明确授权本次集中落盘覆盖 Wayfinder 默认的“每个会话只解决一票”限制；单一协调者串行写入每张票和地图，避免并发覆盖。
