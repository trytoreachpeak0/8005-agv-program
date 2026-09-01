# Round 39（2026-08-04）— QUEUEING 原因诊断只读探针

## 问题

- Q-040：`queryVehicleNotAssignOrder` 的真实 `orderKey` 口径、鉴权、响应、错误与新鲜度契约是什么？
- 现有历史 QUEUEING 样本能否复用于诊断，还是接口只能反映当前状态？

## 环境绑定

- 目标：`RIOT-CROSS-PROJECT-TEST`，`http://172.10.1.72:8888`。
- RIoT build：`2.2.0.30`（用户于 2026-08-03 确认；不是 8005 OpenAPI 快照的源 build `v2.2.0.14`）。
- 测试车与 CallApiKey：只从 `environment.local.json` 读取；证据中不落可复用凭据。
- SCHEMA：Round 7 `swagger-task.json` 与 8005 `riot_swagger/task.json` 均声明同一路径；返回 `reason: string`、`suggestList: string[]`，无受控枚举。

## 批准范围

- 只允许 GET：车辆快照、订单列表、`queryVehicleNotAssignOrder`。
- 不调用任何建单、取消、禁用/启用、急停/解除或其它写接口。
- 不为了制造原因样本改变车辆、订单、定位、地图或现场状态。

## 步骤

1. 保存环境绑定、前置车辆快照与当前 QUEUEING 列表。
2. 若当前测试车有 QUEUEING 单，优先用其字符串 `orderId` 探测。
3. 对已有 Round 13/29/30 的历史测试车样本探测字符串 `orderId`、数值 id 与 `upperId`。
4. 探测未知订单、未知车辆、无鉴权和假鉴权。
5. 若找到成功且 result 非空的组合，重复三次检查文本稳定性与新鲜度字段。
6. 保存后置快照与前后差异；只记录实际覆盖，不把历史场景标签当成本次原因证据。

## 停止条件

- 任一请求不是 GET、目标不再是测试环境、前后出现不可解释的订单/车辆变化，立即停止。
- 当前没有能覆盖所需原因的样本时，保留缺口，不升级为写实验。
