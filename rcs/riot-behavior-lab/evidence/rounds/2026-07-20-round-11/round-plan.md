# Round 11（2026-07-20）

## 研究目标

1. 缺/假 `appointVehicleKey` 的 QUEUEING 单是否后派到其它车（短时观察 + 即时 cancel）
2. Q-020 调度上线 API 再探（有限变体；禁止把测试车长期打成 OFF_LINE 且无法恢复）
3. 多段 `move→move` 状态轨迹与可再派
4. `CMD_ORDER_REJECTED` / HANG 相关 CONTINUE/JUMP（能触发则测，不能则记）
5. 用模板动作 `actionId=129`（等待 Ns）做 act 段 interrupt

## 范围

- 仅测试车写操作；map29；观察无 key 单时若 `executeVehicleKey` 变成非测试车 → 立即 cancel 并停后续危险步骤
- act 仅用等待类 actionId=129

## 授权

- 用户批准测 README 建议 1–5
