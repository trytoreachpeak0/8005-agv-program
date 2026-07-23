# Round 2 执行日志

## 记录规则

- 未执行步骤保持未执行，不提前填写结果。
- 时间使用带时区的 ISO 8601 格式（本机 `Asia/Shanghai`）。
- 每个结论必须链接到 `runs/` 中的证据。
- 摘要之外保留脱敏请求和响应；超大 `mapJson`/设备明细已按证据文件内 `_note` 裁剪。
- 本轮**未调用** `POST /api/auth/v1/admin/login`，也未执行任何写接口。

## A2 调用密钥 → 地图列表（正例）

- 开始时间：`2026-07-20T10:01:17+08:00`
- 结束时间：`2026-07-20T10:01:21+08:00`
- 前置条件：`callApiKey` 已写入本地 `environment.local.json`（gitignored）；本机可达现场基址。
- 请求证据：[`runs/A2-map-success.json`](./runs/A2-map-success.json)
- 状态轨迹：不适用（单次只读）
- 人工事件：无
- 观察事实：
  - `Authorization: Bearer <callApiKey>`，**未登录**。
  - `GET /api/imap/v1/mapInfo/all` → HTTP `200`，业务 `code=0`，`message=成功`。
  - `result` 为地图数组，本轮观测到 **18** 张地图（证据中已剥离 `mapJson`）。
- 与假设关系：`SUPPORTED`（对 Q-015 的地图探针正例）
- 异常与善后：无
- 结论候选：调用密钥可作为长期 Bearer，无需每次 `admin/login`。
- 是否足以晋升 `knowledge`：是（与其余 A2 场景合并为 BC-AUTH-002）
- 是否足以晋升 `fixtures`：是

## A2 调用密钥 → 设备列表（对照）

- 开始时间：`2026-07-20T10:01:21+08:00`
- 结束时间：`2026-07-20T10:01:21+08:00`
- 前置条件：同上
- 请求证据：[`runs/A2-devices-success.json`](./runs/A2-devices-success.json)
- 观察事实：
  - 同一 `callApiKey`，`GET /api/device/v1/devices` → HTTP `200`，业务 `code=0`。
  - 分页 `result.records` 本轮返回 **10** 条（证据已裁剪明细）。
- 与假设关系：`SUPPORTED`（跨模块旁证：不止 imap）
- 异常与善后：无
- 是否足以晋升 `knowledge`：并入 BC-AUTH-002
- 是否足以晋升 `fixtures`：是

## A2 无 Authorization（反例）

- 开始时间：`2026-07-20T10:01:12+08:00`
- 结束时间：`2026-07-20T10:01:12+08:00`
- 请求证据：[`runs/A2-map-no-auth.json`](./runs/A2-map-no-auth.json)
- 观察事实：
  - 同一地图探针，无 `Authorization` → HTTP **`401`**。
  - 响应体：`code=401`，`message=暂未登录或token已经过期`；无业务 `result`。
- 与假设关系：`SUPPORTED`（缺失密钥应失败）
- 说明：与 A1 登录密码错误（HTTP 200 + 业务码）不同，**业务接口缺 token 走 HTTP 401**。
- 是否足以晋升 `knowledge` / `fixtures`：是

## A2 伪造密钥（反例）

- 开始时间：`2026-07-20T10:01:12+08:00`
- 结束时间：`2026-07-20T10:01:12+08:00`
- 请求证据：[`runs/A2-map-invalid-key.json`](./runs/A2-map-invalid-key.json)
- 观察事实：
  - `Authorization: Bearer invalid-call-key-riot-behavior-lab` → HTTP **`401`**。
  - 响应体与无鉴权相同：`code=401`，`message=暂未登录或token已经过期`。
- 与假设关系：`SUPPORTED`（伪造密钥应失败）
- 是否足以晋升 `knowledge` / `fixtures`：是

## 本轮结论

- 已回答问题：`Q-015` → **`SUPPORTED`**
- 仍未回答问题：调用密钥的权限范围边界、轮换/刷新、过期行为；写接口是否同等接受该密钥（本轮未测写）。
- 与历史轮次差异：Round 1 只验证了 `admin/login`；本轮证明长期调用密钥可替代每次登录换 token（至少覆盖 imap/device 只读）。
- 新增风险：无（只读）。注意：业务接口鉴权失败是 HTTP 401，不要套用 A1「只看业务 code」的登录特例。
- 建议下一实验：在确认调用密钥为默认鉴权路径后，按用户新的 P0 规划重开后续业务问题，并用同一 `callApiKey` 跑只读摸底（B1/C1 等）。

## 时间轴摘要

| 时间（约） | 编号 / 场景 | 结果 | 证据 |
|---|---|---|---|
| 2026-07-20 10:01 | A2 / map-no-auth | 通过（反例） | `runs/A2-map-no-auth.json`；HTTP 401 + code=401 |
| 2026-07-20 10:01 | A2 / map-invalid-key | 通过（反例） | `runs/A2-map-invalid-key.json`；HTTP 401 + code=401 |
| 2026-07-20 10:01 | A2 / map-success | 通过 | `runs/A2-map-success.json`；HTTP 200 + code=0，18 张地图 |
| 2026-07-20 10:01 | A2 / devices-success | 通过 | `runs/A2-devices-success.json`；HTTP 200 + code=0，records=10 |
