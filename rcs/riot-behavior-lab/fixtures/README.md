# 稳定 Fixtures

现场只有一台测试车，不该为了补客户端测试反复连接真实环境。这个目录存放从现场证据中晋升、当前确认稳定的脱敏样例，供 `riot-sdk` 的 C#/Python 单测消费。

Fixture 是证据的派生资产，不是原始证据，也不能证明当前现场状态。

## 1. 这个目录和 `evidence/rounds/<round>/runs/` 的区别

- `evidence/rounds/<round>/runs/*.json`：每一轮的原始脱敏抓取，回答“这一轮到底发生了什么”，历史不得覆盖。
- `fixtures/*.json`：不带轮次日期，代表当前可供客户端契约测试依赖的派生版本。

### 晋升流程

1. 某一轮跑完一个场景，产物先落在该轮的 `evidence/rounds/<round>/runs/<编号>-<scenario>.json`。
2. 确认返回结构稳定可信（不是偶发的现场异常）后，把它**复制**一份到本目录，去掉轮次归属，作为"当前对外承诺"的版本。
3. 每个 fixture 必须通过 `sourceEvidence` 指回产生它的轮次证据。
4. 如果新一轮与当前 fixture 结构不一致，先登记行为差异并判断适用版本，再更新 fixture；禁止静默覆盖。
5. 两处都保留：`evidence/` 留历史事实，`fixtures/` 留当前派生版本。

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
  "responseRaw": { "code": "...", "message": "...", "result": {} },
  "responseSummary": { "code": "...", "message": "..." },
  "sourceEvidence": "evidence/rounds/<round>/runs/<file>.json",
  "forMock": {
    "sdkModel": "对应的 SDK 类型/方法，例如 RiotAuthClient.LoginAsync → AuthTokens",
    "clientMethod": "…",
    "notes": "mock 时应模拟出的行为：正常返回什么形状，还是应驱动客户端抛哪种异常"
  }
}
```

`responseRaw` 保留完整脱敏响应结构；`responseSummary` 只用于阅读，不能替代原始响应。`sourceEvidence` 和 `forMock` 都是必填字段。

现有两个 A1 fixture 是重构前产生的摘要格式，只能支持已记录字段的测试，不能当作完整登录响应回放。下次重跑 A1 时应按新 schema 重新晋升。

## 4. 跨项目引用路径

仓库内固定位置是 `rcs/riot-behavior-lab/fixtures/`。SDK 测试应通过测试配置或仓库根目录定位该目录，不在生成代码中硬编码工作目录层级。

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

**已有一条可验证的结论（来自 A1 invalid-password）**：RIoT 登录失败**不体现在 HTTP 状态码上**（仍是 200），必须读业务 `code`。这与 [`RiotAuthClient.SendAuthAsync`](../../riot-sdk/csharp/RIoT.Sdk.Core/RiotAuthClient.cs) 现有实现一致。该结论目前只直接覆盖登录接口；其他模块应分别验证，不能未经实验推广成全平台规则。

## 6. 使用方式（约定，暂不新增测试工程代码）

- C# 侧：以后写 `RIoT.Sdk.Tests` 单测时，可以写一个小 helper 读本目录下的 `*.json`，把 `response` 部分序列化成 stub `HttpResponseMessage` 内容，驱动 `RiotAuthClient` / 各 Facade 客户端，断言其解析结果或抛出的异常类型与 `forMock` 描述一致。
- Python 侧：同理用 `responses` / `httpx` 的 mock transport 消费同一批文件。
- 两侧共用同一份 fixture，不必各自再造一套假数据——现场返回的真实结构（字段名、命名风格、错误码含义）比拍脑袋编的 mock 更可信。

## 7. 重要限制

- 反例产物**不代表**已经把所有异常路径穷尽；只覆盖实测触发过的场景。
- 即便脱敏，也不要把 fixture 当成「回放真实系统」的替代——只用于契约/结构层面的 mock，不代表实时状态（比如车辆当前电量、位置这类会变的字段，mock 时应视为快照，不是实时值）。
- 反例设计优先服务于**安全边界验证**（E1/H1/H2 这类），而不是单纯为了把 mock 覆盖率做高；如果某条反例执行后发现系统行为不符合预期（例如 E1 反例真把订单派给了别的车），按 [`../governance/safety-boundaries.md`](../governance/safety-boundaries.md) 立刻走人工升级，不要只当成“一条失败的测试”记完就过。
