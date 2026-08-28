# Round 12（2026-07-20）

## 目标
用网页 Network 抓包确认的 body 验证 Q-020：
`POST /api/task/vehicles/updateVehicleIntegrationLevel`
`{"deviceKeys":["<testKey>"],"serviceId":"enable"|"disable"}`

## 来源
用户从浏览器复制的网页请求（admin Bearer）；本轮用 callApiKey 复现。
