# Round 7 执行日志（续：人工上线后）

## 人工干预结果

- 用户回复：已上线。
- 复查：`integrationLevel=ON_LINE`，`enable=true`，`procState=IDLE`，仍在 map `api测试`；`fleetMode` 仍可能显示 `FLEET_MODE_OFFLINE`（与调度 ON_LINE 可并存，勿单靠 fleetMode 判断能否接单）。
- 证据：`runs/E0-baseline-after-human-online.json`

## E1 主路径更正

| API | 结果 |
|---|---|
| `POST /api/task/v1/order` | 上线后仍 `code=00002` NPE，未落库 |
| `POST /api/order/v1/add/byDefaultMissions` | **成功** |

## 成功订单 1（探测单）

- `upperId=riot-lab-I-20260720-120949`
- `orderId=order-2079056586101358592`
- 目的站 2；终态 `orderState=5 SUCCESS`
- `appointVehicleKey` = `executeVehicleKey` = 测试车
- 完成后车在 **站点2**（坐标约 y=-1522）
- 证据：`E1-retry-I-bdm-lock0.json`，`E1-bdm-I-detailByUpperId.json`

## 成功订单 2（完整轨迹：站2→站1）

- `upperId=riot-behavior-lab-E1b-2to1-*`（见 `E1b-create-2to1.json`）
- 发单前：station=2，IDLE
- 轨迹摘要：
  - `orderState`：1 → 3 → 5
  - 执行中：`procState=PROCESSING_ORDER`，`movementState=MT_RUNNING`，`currentStation=0`（离站）
  - 完成：车 `station=1`，`procState=IDLE`，坐标约 (158,-479)
- `executeVehicleKey` 全程测试车
- 证据：`E1b-create-2to1.json`，`E2-poll-samples-2to1.json`，`E2-post-move-2to1.json`

## 结论

- Q-001 / BC-ORDER-001：建单用 `byDefaultMissions`
- Q-011 / BC-ORDER-002：`appointVehicleKey` 绑本车
- Q-020 API 仍 BLOCKED；人工网页上线可用
- 无误派他车；测试车最终停在 **站点1**
