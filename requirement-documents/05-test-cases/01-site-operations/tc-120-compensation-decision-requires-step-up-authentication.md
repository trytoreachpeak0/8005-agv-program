---
id: TC-120
type: test-case
title: "整批清空决定必须使用单次强绑定的即时二次认证"
status: draft
created: 2026-07-31
updated: 2026-07-31
related_fr: ["FR-002"]
related_uc: ["UC-001"]
aliases: ["TC-120"]
---

# TC-120 整批清空决定必须使用单次强绑定的即时二次认证

## Preconditions 前置条件

一个 LoadBatch 因目标仓位关键硬件反馈故障处于 VehicleRecoveryRequired；当前登录人具有 R-09 或等效生产管理权限，但只有既有登录会话，尚未为本次 LoadCompensationDecision 完成有效的即时二次认证。

## Test Steps 测试步骤

1. 当前登录人仅凭已有会话尝试提交 LoadCompensationDecision。
2. 模拟再次刷卡或认证失败，再次提交。
3. 使二次认证成功，形成绑定确认人、DemandId A、SlotOperationAttemptId A 和完整决定内容的认证证据，提交决定。
4. 模拟首次响应丢失，使用相同 MessageId 和相同内容重发步骤 3。
5. 尝试把步骤 3 的认证证据用于 DemandId B、不同 SlotOperationAttemptId，或修改原因码/备注后提交。
6. 另形成一次认证证据，但使首次提交因业务状态校验失败而被拒绝；随后业务状态恢复，再次使用原证据提交。

## Expected Result 预期结果

步骤 1 和步骤 2 均被拒绝，不生成 LoadCompensationDecision，不进入 LoadCompensationRequired，也不下发任何开锁指令。步骤 3 允许服务端接受决定；接受决定本身仍不得自动开锁，后续必须另行取得补偿执行授权。步骤 4 返回步骤 3 已持久化的同一结果，不再次消费认证、不生成第二个决定。步骤 5 均因绑定不匹配被拒绝。步骤 6 的首次拒绝结果被可靠记录，原证据不得在状态恢复后再次使用，必须重新认证后形成新的提交。

## Verifies 验证对象

[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] AC-4.6、AC-4.6.1
