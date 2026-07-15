# Mock Fixtures

现场只有一台测试车，不该为了补测试反复连真实环境。这个目录存放**当前对外承诺、跨轮次持续有效**的 mock 素材——每条 fixture 是一次真实调用的脱敏留档，供 `riot-sdk` 的 C#/Python 单测直接消费（stub `HttpMessageHandler` / `responses` 库等）。

## 1. 这个目录和 `rounds/<round>/runs/` 的区别

- `rounds/<round>/runs/*.json`：**每一轮**的原始抓取产物，按轮次归档，是审计留痕——回答"这一轮到底跑了什么"。历史不会被覆盖，方便对比"RIoT 升级前后行为是否一致"。
- `mock-fixtures/*.json`（本目录）：**不带轮次日期**，代表"当前确认稳定、可以放心让 SDK 单测依赖"的版本。`riot-sdk` 的测试代码只应该引用这里，不需要关心这个 fixture 是哪一轮抓的。

### 晋升流程

1. 某一轮跑完一个场景，产物先落在该轮的 `rounds/<round>/runs/<编号>-<scenario>.json`。
2. 确认返回结构稳定可信（不是偶发的现场异常）后，把它**复制**一份到本目录，去掉轮次归属，作为"当前对外承诺"的版本。
3. 如果本目录已存在同名 fixture（同编号+场景），且新一轮的结果与旧版本**结构不一致**（字段增删、语义变化），说明 RIoT 行为变了：更新本目录里的版本为最新的，同时在 `test-catalog.md` §3 的"已核实状态枚举"里补充说明这一变化，不要静默覆盖了事。
4. 两处都保留：`rounds/` 留历史证据，`mock-fixtures/` 留当前版本——不是二选一。

## 2. 命名约定

`<编号>-<scenario>.json`，`scenario` 用能一眼看出触发条件的英文短横线短语：

- 正例固定叫 `success`（如 `A1-login-success.json`）。
- 反例用触发条件命名（如 `A1-login-invalid-password.json`、`E1-order-unknown-vehicle-key.json`、`H1-disable-unknown-device-key.json`）。

## 3. 文件 schema

```json
{
  "at": "yyyy-MM-dd HH:mm:ss",
  "scenario": "success | invalid-password | unknown-vehicle-key | ...",
  "method": "POST | GET | ...",
  "url": "完整 URL",
  "requestBody": { "...": "敏感字段（密码/token）必须打码为 ***" },
  "httpStatus": 200,
  "elapsedMs": 438,
  "response": { "code": "...", "message": "...", "...": "..." },
  "forMock": {
    "sdkModel": "对应的 SDK 类型/方法，例如 RiotAuthClient.LoginAsync → AuthTokens",
    "clientMethod": "…",
    "notes": "mock 时应模拟出的行为：正常返回什么形状，还是应驱动客户端抛哪种异常"
  }
}
```

`forMock` 是固定字段，任何新产物都要填，不能只留原始 request/response——目的是让以后写单测的人（或 AI）不用重新读懂业务语义，直接照着 `forMock.notes` 写 stub 断言。

## 4. 跨项目引用路径

从 `rcs/riot-sdk/` 视角，相对路径是 `../rcs-insight/mock-fixtures/`。例如 C# 测试项目里：

```csharp
var fixturePath = Path.Combine("..", "..", "rcs-insight", "mock-fixtures", "A1-login-success.json");
```

具体怎么读取 fixture 并驱动 stub（helper 代码），留给以后接入单测工程时再写；本目录目前只负责把素材和约定放好位置。

## 5. Mock 对照表

编号 + 场景 → 接口 → SDK 模型/方法 → fixture 文件 → 状态。这是**跨轮次持续累积**的表，不属于单一轮次，每跑完一个场景就补一行，不要等全部测完再补。

| 编号 | 场景 | 接口 | SDK 模型/方法 | fixture 文件 | 状态 |
|---|---|---|---|---|---|
| A1 | success | `POST /api/auth/v1/admin/login` | `RiotAuthClient.LoginAsync` → `AuthTokens` | [`A1-login-success.json`](./A1-login-success.json) | 已晋升 |
| A1 | invalid-password | 同上 | `LoginAsync` 抛 `RiotApiException`（code=2009） | [`A1-login-invalid-password.json`](./A1-login-invalid-password.json) | 已晋升 |
| B1 | success | `GET /api/device/v1/devices` | `DeviceClient` 设备列表 | — | 待执行 |
| B1 | unknown-device-key | 同上（过滤不存在 key） | 同上（空结果路径） | — | 待执行 |
| B2 | success | `GET /api/task/v1/task/getVehicleInfo/{deviceKey}` | `VehicleTaskInfo` | — | 待执行 |
| B2 | unknown-device-key | 同上 | 同上（失败路径） | — | 待执行 |
| C1 | success | `GET /api/imap/v1/mapInfo/all` | 地图列表 DTO | — | 待执行 |
| C1 | no-auth | 同上（去掉 token） | 401 路径 | — | 待执行 |
| C2 | success / invalid-mapid | `GET /api/imap/v1/mapInfo/stations/{mapId}` | 站点列表 DTO | — | 待执行 |
| E1 | success | `POST /api/task/v1/order` | `OrderDTO` → 订单创建 | — | 待执行 |
| E1 | unknown-vehicle-key | 同上 | 创建失败路径（安全边界） | — | 待执行 |
| E3 | interrupt-executing | `POST /api/task/v1/order/interrupt` | `InterruptOrderDtoObject` | — | 待执行 |
| E3 | interrupt-terminal-order | 同上 | 失败路径 | — | 待执行 |
| H1 | success / unknown-device-key | `POST /api/device/v1/devices/disable/{deviceKey}` | disable 路径 | — | 待执行 |
| H2 | success / unknown-device-key | `POST /api/device/v1/devices/enable/{deviceKey}` | enable 路径 | — | 待执行 |

**已有一条可验证的结论（来自 A1 invalid-password）**：RIoT 登录失败**不体现在 HTTP 状态码上**（仍是 200），必须读业务 `code`。这与 [`RiotAuthClient.SendAuthAsync`](../../riot-sdk/csharp/RIoT.Sdk.Core/RiotAuthClient.cs) 现有实现里 `IsSuccessCode(businessCode)` 的判断方式一致——说明这条 SDK 逻辑已经是对的，也说明**任何时候都不能只用 `resp.IsSuccessStatusCode` 判断 RIoT 接口成败**，这条经验对所有后续卡片同样适用。

## 6. 使用方式（约定，暂不新增测试工程代码）

- C# 侧：以后写 `RIoT.Sdk.Tests` 单测时，可以写一个小 helper 读本目录下的 `*.json`，把 `response` 部分序列化成 stub `HttpResponseMessage` 内容，驱动 `RiotAuthClient` / 各 Facade 客户端，断言其解析结果或抛出的异常类型与 `forMock` 描述一致。
- Python 侧：同理用 `responses` / `httpx` 的 mock transport 消费同一批文件。
- 两侧共用同一份 fixture，不必各自再造一套假数据——现场返回的真实结构（字段名、命名风格、错误码含义）比拍脑袋编的 mock 更可信。

## 7. 重要限制

- 反例产物**不代表**已经把所有异常路径穷尽；只覆盖实测触发过的场景。
- 即便脱敏，也不要把 fixture 当成「回放真实系统」的替代——只用于契约/结构层面的 mock，不代表实时状态（比如车辆当前电量、位置这类会变的字段，mock 时应视为快照，不是实时值）。
- 反例设计优先服务于**安全边界验证**（E1/H1/H2 这类），而不是单纯为了把 mock 覆盖率做高；如果某条反例执行后发现系统行为不符合预期（例如 E1 反例真把订单派给了别的车），按 [`../safety-boundaries.md`](../safety-boundaries.md) 立刻走人工升级，不要只当成"一条失败的测试"记完就过。
