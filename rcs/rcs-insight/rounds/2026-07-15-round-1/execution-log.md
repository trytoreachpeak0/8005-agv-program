# Round 1 执行日志

按 [`test-catalog.md`](../../test-catalog.md) 的编号记录本轮实际执行结果。未执行的卡片先留空占位，不要提前瞎填。

---

## A1 登录拿 token

- **2026-07-15 ~10:30** — 正例 **通过**
  - 调用：`POST http://172.10.1.72:8888/api/auth/v1/admin/login`，body `{ username: admin, password: *** }`
  - HTTP `200`，耗时约 `438ms`；业务 `code=0`，`message=成功`
  - `result` 字段：`tokenHead`, `token`；access token 非空（JWT，`len=191`，预览 `eyJhbGciOiJIUzUx...`）；未见独立 refreshToken
  - 产物（脱敏）：[`runs/A1-login-success.json`](./runs/A1-login-success.json)
- **2026-07-15 ~10:44** — 反例1（错误密码） **通过**（行为符合预期）
  - 调用同上接口，密码替换为错误值
  - **关键发现**：HTTP 仍是 `200`，业务 `code=2009`，`message=密码不正确`，`result` 为空 —— **鉴权失败不是靠 HTTP 状态码区分的，必须读业务 `code`**
  - 与现有 SDK 实现交叉核对：[`RiotAuthClient.SendAuthAsync`](../../../riot-sdk/csharp/RIoT.Sdk.Core/RiotAuthClient.cs) 里 `IsSuccessCode(businessCode)` 判空后抛 `RiotApiException`，逻辑与本次真实返回一致 —— 该反例同时验证了 SDK 现有实现是对的
  - 产物（脱敏）：[`runs/A1-login-invalid-password.json`](./runs/A1-login-invalid-password.json)
- 人工干预：未触发

---

## B1 设备列表查到测试车 + 在线状态

（留空）

---

## B2 getVehicleInfo：位置 / 电量 / 任务状态

（留空）

---

## C1 地图列表 mapInfo/all

（留空）

---

## C2 有效站点 stations/{mapId}

（留空）

---

## C3 边 / 路网 edges/{mapId}

（留空）

---

## C4 地图关系 Map Relation

（留空）

---

## D1 路径成本 getRouteCostsBy

（留空）

---

## E1 创建一个移动订单

（留空）

---

## E2 监控订单直到到站

（留空）

---

## E3 对进行中订单做 interrupt

（留空；务必记 interrupt 前后 `orderState`/`procState` 对照表）

---

## F1 指定该车充电

本轮未执行（本轮跳过）。

---

## G1 空闲返停靠点

本轮未执行（本轮跳过）。

---

## H1 disable 测试车

（留空）

---

## H2 enable 测试车（收尾）

（留空）

---

## 执行日志索引（可选汇总）

| 时间 | 编号/场景 | 结论 | 备注 |
|---|---|---|---|
| 2026-07-15 ~10:30 | A1 / success | 通过 | `runs/A1-login-success.json`；token len=191，无独立 refresh |
| 2026-07-15 ~10:44 | A1 / invalid-password | 通过（反例） | `runs/A1-login-invalid-password.json`；HTTP 200 + code=2009，非 HTTP 层报错 |

结论可选：`通过` / `失败` / `等待人工` / `本轮跳过`。
