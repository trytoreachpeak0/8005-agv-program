# Round 25 执行日志 — 充电成功路径（借用车，仅本轮）

## 状态

**完成**：订单 SUCCESS 已采到

## 范围约束

- 车：`BROKERX-52501bcbe60f4723bc815f24fc763c1e`（电镀顶升AGV1）— **仅本轮允许，此后禁止再用**
- 地图：华士老厂 `mapId=11`
- 充电站：站点 **16**（名称「充电点」，`type=2`，`enter_exit=26`）

## 建单

- `move(16) + act(78, param1=1, param2=0)` → `code=0`
- 自动展开：`move(26) → move(16) → act(78)`
- upperId：`riot-behavior-lab-R25-ok-20260721-162057`

## 时序

| 时间 | 现象 |
|------|------|
| 16:20:57 | 建单；车在站 31，电量 ~60 |
| ~16:22:18 | 进入第二段 move（充电站） |
| 16:22:24 | `idx=2` act(78) `AT_RUNNING`，站 16 |
| 16:22:45 | `batteryState=CHARGING`，`AT_FINISHED` |
| 16:22:46 | **`orderState=5 SUCCESS`**，`progress=100`，`proc=IDLE` |

## 结论（Q-033 成功）

- 接充电器后：`batteryState` `NO_CHARGE` → `CHARGING`，act 结束，订单 **SUCCESS**
- act `resultCode=0`；文案字段仍可能带「挂起」字样（本轮 `resultStr` 含编码 0），以 **orderState / resultCode** 为准
- 证据：`S1-create.json` / `S1-act-hit.json` / `S2-after-charge-samples.json` / `S2-final.json` / `E9-final.json`

## MES/现场业务约定（用户口述，未再测）

- 离桩：再下订单即可；系统在队首自动插入 `act(78,2,0)` 结束充电，再执行业务任务
- act 78：`param1=1` 开始充电；`param1=2` 结束充电（param2 均为 0）
- 充满阈值：100%
- 充电 HANG：仅人工排查
- 电量 ≤10% 本体自动关机 → 下单前电量须 >10%
- RIoT 自动充电未启用；充电由 MES 订单触发
- `multiLoadState` 不用（多仓位不直连 RCS）→ 见 Q-008 `NA`
