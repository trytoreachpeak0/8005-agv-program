# Round 27 执行日志 — 执行中异常与 CONTINUE 判别

## 状态

**完成**（A/B/E/F 均已采；结论有修订）

## 环境

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`，map29
- 订单形态：三段 move 往返（拉长 EXECUTING 窗口）

## A — 硬件急停（现场约定）

- 订单：`riot-behavior-lab-R27-A-20260721-190942`
- 急停后：`emergencyState=CAN_NOT_RECOVER`，`speed=0`
- **本轮监视期内未进 `orderState=9`**（长期 `EXECUTING(3)`）
- **现场约定（2026-07-21）**：硬件急停本身**默认视为永远不会单独把订单打进 HANG**；调用方用急停车态判人工介入即可
- 补充：软/硬件急停期间，车也可能进入**其它故障态**，从而间接导致订单挂起——那是故障路径，不是「急停⇒HANG」的必然
- 非 HANG 时 CONTINUE → `100021`
- 清场：cancel → `CANCELLED(2)`；需**物理松开**急停后 `cancelEmergency` 才回 `OK`
- 证据：`A-*` / `A2-hang-*` / `A-cont-*`

## B — 软件急停（**已由 Round31 修订**：不会单独进 HANG）

- 订单：`riot-behavior-lab-R27-B-20260721-191842`
- ~~本轮曾记：可先长时间 EXECUTING，后进 HANG~~ → **作废**；以 Round31 为准：**软件急停不会单独进 HANG**
- Round31：`triggerEmergency` → `CAN_RECOVER`，约 **15min** 仍 `EXECUTING` / `progress` 冻结
- 恢复：`cancelEmergency`（不必等 HANG / CONTINUE）
- 证据：本轮 `B-*`（历史）；修订 [`../2026-07-22-round-31/`](../2026-07-22-round-31/)

## E — 单机取消移动（SUPPORTED，可恢复）

- 订单：`riot-behavior-lab-R27-E-20260721-192457`
- 较快 **`HANG(9)`**；`resultCode=901`；文案「订单被取消,导致订单挂起」；`emergencyState=OK`
- `CONTINUE_FROM_HANG` → **`code=0`** → 最终 **`SUCCESS(5)`**
- 证据：`E-hang-*` / `E-cont-*`

## F — 解抱闸（SUPPORTED，需先人工拨回）

- 订单：`riot-behavior-lab-R27-F-20260721-193043`
- 进 HANG：`breakSwitchState=UNMOVABLE`，`controlState=CONTROL_STATE_ERR`；文案同 E（901），靠车态区分
- 仍解抱闸时 CONTINUE → **`14013` 车辆状态异常**
- **拨回开机**（`break=MOVABLE`）后再 CONTINUE → **`code=0`** → **`SUCCESS(5)`**
- 证据：`F-hang-*` / `F-cont-*` / `Fok-cont-*`

## 调用方判别（修订后；含 Round31）

1. 以 **`orderState=9`** 为 HANG 门槛；**软/硬件急停**期间可能长时间停在 EXECUTING，勿过早试 CONTINUE。
2. HANG 后试 `CMD_ORDER_CONTINUE_FROM_HANG`：
   - **`code=0`** → 可恢复类（本轮：**E**；以及拨回开机后的 **F**）
   - **`14013`** → 车态异常（本轮：**F 解抱闸未拨回**）→ 读 `breakSwitchState`
   - **`100021`** → 仍因车辆原因不可继续（常见于急停未清 / 非 HANG）
3. 车态辅助：`emergencyState`（A/B）、`breakSwitchState`（F）；E 无急停/抱闸异常。
4. **A/B 急停默认永不单独进 HANG**（B 由 Round31 约15min 复核）；用急停车态识别：A 物理松开，B `cancelEmergency`。若另有故障态可间接挂起（故障路径，非急停必然）。
