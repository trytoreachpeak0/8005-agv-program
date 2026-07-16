# 已验证行为契约

本文件只收录能够指向证据的结论。静态 schema 描述但尚未现场观察的内容，不写入本文件。

## BC-AUTH-001 登录成败不能只看 HTTP 状态

- 结论：`POST /api/auth/v1/admin/login` 在密码错误时仍可能返回 HTTP 200；客户端必须检查响应业务 `code`。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-15
- 正例证据：[`../evidence/rounds/2026-07-15-round-1/runs/A1-login-success.json`](../evidence/rounds/2026-07-15-round-1/runs/A1-login-success.json)
- 反例证据：[`../evidence/rounds/2026-07-15-round-1/runs/A1-login-invalid-password.json`](../evidence/rounds/2026-07-15-round-1/runs/A1-login-invalid-password.json)
- 已观测结果：
  - 正确密码：HTTP 200，业务 `code=0`，返回 `tokenHead` 与 `token`。
  - 错误密码：HTTP 200，业务 `code=2009`，`message=密码不正确`，无可用 token。
- 适用范围：目前只直接证明登录接口。其他 RIoT 模块是否完全一致仍是待验证问题。
- 消费影响：`riot-sdk` 鉴权客户端应在 HTTP 成功后继续校验业务码。

## 待晋升条件

以下内容目前不能写成已验证契约：

- 所有模块都以 `code=0` 表示成功。
- `orderState=5` 必然等价于车辆已物理到站。
- `procState=IDLE` 必然表示车辆任务队列为空。
- 相同 `upperId` 重复提交不会生成重复订单。

它们必须先在 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) 中获得相应现场证据。
