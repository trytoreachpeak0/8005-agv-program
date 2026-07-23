# Round 7（2026-07-20）

## 1. 研究目标

- Q-001：`POST /api/task/v1/order` 能否为指定测试车创建 NORMAL 短距移动订单。
- Q-011（部分）：`appointVehicleKey` 是否真正绑到本车（`executeVehicleKey` 是否回写为本车）。
- Q-002 / Q-005（部分）：订单执行期间与到站后，订单态与车侧态如何变化。
- 前置发现：测试车当前 `integrationLevel=OFF_LINE` / `vehicleTaskInfo.enable=false`，而多数产线车为 `ON_LINE`/`enable=true`。需先单车切到可调度态，再建单。

## 2. 范围

- **只允许操作测试车**：`新基测试300c协作1` / `BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：`mapId=29`（`api测试`）
- 起点：站点1（用户已放车）
- 目的：站点2（同图仅另一站，短距）
- **不用车辆组**
- 不测：充电、interrupt、幂等、取消主路径（本轮若卡死才用 cancel 善后）

## 3. 授权

- 时间：2026-07-20
- 原始表述：用户确认车在 mapId=29 / stationId=1，授权对「新基测试300c协作1」下订单，可先不用车辆组。

## 4. 执行序列

| 步骤 | 实验卡 | 风险 | 状态 |
|---|---|---|---|
| 0 | 基线采样（B2） | 只读 | 通过（曾 OFF_LINE；人工上线后 ON_LINE） |
| 1 | 单车切 `ON_LINE`（API） | 写-可逆 | API 失败；**人工网页上线成功** |
| D1 | 路径代价 站2 | 只读 | 通过（costs=1040） |
| 2a | `task/v1/order` | 写 | 失败（NPE，未落库） |
| 2b | E1 `byDefaultMissions` 目的站2 | 写 | **通过** → SUCCESS |
| 3 | E1b+E2 站2→站1 全程监控 | 写+只读 | **通过** → SUCCESS，车回站1 |
| 4 | cancel 善后 | 写 | 无需 |

## 5. 安全约束

- 写操作必须显式带测试车 key；`updateVehicleIntegrationLevel` 虽为批量形接口，本轮 `deviceKeys` **只放本车一把 key**。
- 禁止系统随便派车；禁止车辆组；禁止动其它车。
- 发现误派他车立即停测并升级人工。

## 6. 建单最小 body（SCHEMA + 现场 SUCCESS 订单旁证）

```json
{
  "appointVehicleKey": "<testVehicleKey>",
  "appointMapId": 29,
  "orderType": "NORMAL",
  "orderName": "riot-behavior-lab-E1-<ts>",
  "upperId": "riot-behavior-lab-E1-<ts>",
  "mission": [
    { "type": "move", "mapId": 29, "destination": 2 }
  ]
}
```

现场 SUCCESS 订单 mission 旁证：`type=move` + `mapId` + `destination`。
