# Round 28 执行日志 — 硬件急停长订单是否进 HANG

## 状态

**完成**：长监视（约 15 min）**未**进入 HANG

## 条件

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：**api测试2**（mapId=30）
- 订单：`riot-behavior-lab-R28-Ahw-20260722-081939`（7 段 move 长单）
- 人工：硬件急停（约 08:21:15 起 `emergencyState=CAN_NOT_RECOVER`）

## 时序事实

| 时间 | 现象 |
|------|------|
| 08:19:43 | `orderState=3 EXECUTING` |
| 08:21:15 | `emergencyState=CAN_NOT_RECOVER`（急停生效） |
| → 08:35:03 | 持续约 **14 min**：仍为 `orderState=3`，`progress=14` 冻结，`proc=PROCESSING_ORDER`，`m0_resultCode=0` |
| 监视结束 | **`hitHang=false`** |

证据：`S1-create.json` / `S2-hang-hit.json` / `S2-hang-samples.json`（520 采样点）

## 结论

在本现场、map30 长订单 + 硬件急停保持按下的条件下：

- **硬件急停不会把订单打进 `orderState=9 HANG`**（至少 14+ 分钟窗口内）
- 订单可长期停在 **EXECUTING**，进度冻结；判别靠 `emergencyState`（本轮为 `CAN_NOT_RECOVER`）
- 与 Round27 短监视及「默认永不单独进 HANG」现场约定一致；本轮用更长事实复核

## 清场

需物理松开急停后 `cancelEmergency`；订单 `CMD_ORDER_CANCEL`。
