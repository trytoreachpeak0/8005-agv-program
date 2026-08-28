# Round 19 执行日志（2026-07-20）— 急停检测与解除

## 环境

- 测试车：`新基测试300c协作1`，map30 / 站5（后到站2）
- 急停由用户主动下发；解除 body 形态来自用户网页 Network 抓包

## 1) 检测（SUPPORTED）

基线 → 急停后字段变化：

| 字段 | 正常 | 急停中 |
|---|---|---|
| `vehicle.emergencyState` | `OK` | **`CAN_RECOVER`** |
| `vehicle.controlState` | `CONTROL_STATE_OK` | **`CONTROL_STATE_ERR`** |
| runtime `emergencyState` | `1`（NONE） | **`3`（RECOVERABLE）** |

- MES 判定急停：读 `getVehicleInfo` → `emergencyState != OK`（可恢复为 `CAN_RECOVER`）
- 证据：`E0-baseline.json`、`S1-watch-samples.json`、`S1-hit.json`

## 2) 解除（契约已对齐 UI）

正确调用（网页抓包 + Round19 S2d 用 callApiKey 复验）：

```http
POST /api/device/v1/command/sync/service/{deviceKey}/cancelEmergency
Content-Type: application/json

{
  "messageId": 880815,
  "mqCallback": { "tag": "string", "topic": "string" },
  "thingsProperties": {}
}
```

**S2d 纯净往返（callApiKey）**：

- 急停中：`emergencyState=CAN_RECOVER`，`controlState=CONTROL_STATE_ERR`，属性 `3`
- 调用上述 body → 业务 **`code=0` / 成功**
- ~1s 后：`emergencyState=OK`
- 证据：`S2d-before.json`、`S2d-cancel-call.json`、`S2d-after-samples.json`、`S2d-summary.json`

反例（本轮早先尝试）：

- body `{}` / 缺字段 → sync 侧 **NPE `00002`**
- async `cancelEmergency` 可返回业务 `code=0`，但**不能**据此认定已解除（当时状态仍 `CAN_RECOVER`）

S2c 曾出现 `05007` 超时并与网页解除时序重叠；**以 S2d 为准**。

## 4) 软件下急停 triggerEmergency（SUPPORTED）

正确调用（网页抓包 + Round19 S4 用 callApiKey 复验）：

```http
POST /api/device/v1/command/sync/service/{deviceKey}/triggerEmergency
Content-Type: application/json

{
  "messageId": 848312,
  "mqCallback": { "tag": "string", "topic": "string" },
  "thingsProperties": {}
}
```

**S4 往返（callApiKey）**：

1. 基线 `OK` → `triggerEmergency` → **`code=0`**
2. ~1s：`emergencyState=CAN_RECOVER`，属性 `3`，`controlState=CONTROL_STATE_ERR`
3. `cancelEmergency` → **`code=0`** → `OK` + `CONTROL_STATE_OK`

证据：`S4-baseline.json`、`S4-trigger-call.json`、`S4-after-trigger-samples.json`、`S4-cancel-call.json`、`S4-summary.json`  
fixture：`fixtures/R19-triggerEmergency-ui-body.json`（不含 JWT）

## 3) 解除后可再派（SUPPORTED）

- 急停恢复后短距建单：`SUCCESS`，车到站2，全程 `emergencyState=OK`
- 证据：`S3-create.json`、`S3-samples.json`、`E9-final.json`

## MES 建议

1. **检测**：轮询/订阅 `getVehicleInfo.emergencyState`；`CAN_RECOVER` = 可软件解除  
2. **下急停**：`POST .../triggerEmergency`，body 同解除（`messageId` + `mqCallback` + `thingsProperties`）  
3. **解除**：`POST .../cancelEmergency`，同一 body 形态  
4. **校验**：以车态回 `OK`（及随后 `CONTROL_STATE_OK`）为准，不要只看 HTTP/`code=0`  
5. 鉴权：`callApiKey` 可用
