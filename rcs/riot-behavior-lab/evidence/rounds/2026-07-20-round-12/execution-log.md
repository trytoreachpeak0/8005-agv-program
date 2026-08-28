# Round 12 执行日志（2026-07-20）

## 来源

用户从 RIOT 网页 Network 抓包，关键写操作为：

```http
POST /api/task/vehicles/updateVehicleIntegrationLevel
Content-Type: application/json

{"deviceKeys":["BROKERX-aee2f93d717546cf9510c98c854fe83e"],"serviceId":"disable"}
{"deviceKeys":["BROKERX-aee2f93d717546cf9510c98c854fe83e"],"serviceId":"enable"}
```

网页使用 admin Bearer；本轮用 **callApiKey** 复现。

## 结果

| 步骤 | serviceId | code | 之后 enable | 之后 integrationLevel |
|---|---|---|---|---|
| 基线 | — | — | true | ON_LINE |
| 幂等 enable | `enable` | 0 | true | ON_LINE |
| disable | `disable` | 0 | **false** | **OFF_LINE** |
| enable 恢复 | `enable` | 0 | **true** | **ON_LINE** |

结论：Q-020 **解锁**。Swagger 的 `serviceId` 语义是 **`enable`/`disable`**，不是 `ON_LINE`/`OFF_LINE`。此前用错误 serviceId 导致 NPE/副作用。

证据：`runs/E1-enable-callApiKey.json`，`E2-disable.json`，`E3-enable-restore.json`，`E4-summary.json`

## 收尾

测试车已恢复 `enable=true` / `ON_LINE`，站 1，`IDLE`。
