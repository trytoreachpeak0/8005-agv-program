# Round 32 执行日志 — 执行中旋钮关机是否进 HANG

## 结果

- 订单：`riot-behavior-lab-R32-Poff-20260722-101118`（多段 move，map30）
- EXECUTING 后人工拨关机 → `runtime/status=offline`（API 仍可达，5G 独立供电）
- 监视约 **900s（15min）**：一直 **`orderState=3 EXECUTING`**，`progress=11` 冻结，`proc=PROCESSING_ORDER`，`offline` 持续
- **未出现 `HANG(9)`**
- 清场：cancel → `CANCELLED(2)`（车仍 offline 时 `proc` 可短暂 `IN_CANCEL`）

## 结论

执行中旋钮关机：**关机期间**与软/硬件急停同类，保持 `EXECUTING` + 进度冻结 + `runtime=offline`，**不立刻进 HANG**（本轮约 15min）。

**补测见 Round33**：不取消、拨回开机后，订单可进入 **HANG(9)**；CONTINUE 可能 `0` 但仍挂起（伴电机错误等）。

对照：关机态**空闲建新单** → 长期 QUEUEING（Round30 P）。
