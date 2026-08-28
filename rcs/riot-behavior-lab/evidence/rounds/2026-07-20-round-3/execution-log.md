# Round 3 执行日志

## 记录规则

- 鉴权：`Authorization: Bearer <callApiKey>`，未调用 `admin/login`。
- 本轮无写接口。
- 超大富对象（`getAllTaskVehicles`）只保留结构样本与标识字段结论。

## B1 设备全量（含非车）

- 时间：`2026-07-20T10:09:11+08:00`
- 请求：`GET /api/device/v1/devices?current=1&pageSize=100`
- 证据：[`runs/B1-devices-all.json`](./runs/B1-devices-all.json)
- 观察事实：
  - HTTP 200，`code=0`，`total=32`，一次拉回 32 条。
  - 旁证：`current+size` 翻页本现场会重复返回第 1 页；`pageSize=100` 可拉全量。
  - 列表同时包含 AGV 与门/电梯/风淋门等非车设备。
- 与假设关系：为 Q-016 提供“devices ≠ 车辆列表”的直接证据
- 是否足以晋升 knowledge：是（并入 BC-VEH-001）

## B1 task 车辆清单

- 时间：`2026-07-20T10:09:11+08:00`～`10:09:12+08:00`
- 证据：
  - [`runs/B1-getAllVehicleKeys.json`](./runs/B1-getAllVehicleKeys.json) — 18 个 key
  - [`runs/B1-getAllVehicleSimpleInfo.json`](./runs/B1-getAllVehicleSimpleInfo.json) — 18 条 `{deviceKey, deviceName}`
  - [`runs/B1-getAllTaskVehicles.json`](./runs/B1-getAllTaskVehicles.json) — 18 条富对象；标识在 `vehicleTaskInfo.key` / `vehicleTaskInfo.name`
- 观察事实：三条 task 车辆接口车辆数一致为 **18**；均为 `code=0`。
- 与假设关系：`SUPPORTED`（Q-016 可调度车辆集合）

## B1 车辆 vs 非车差分

- 证据：[`runs/B1-vehicle-vs-device-diff.json`](./runs/B1-vehicle-vs-device-diff.json)、[`runs/_inventory-summary.txt`](./runs/_inventory-summary.txt)
- 观察事实：
  - devices **32**，task 车辆 key **18**，交集 **18**，仅在 devices 中 **14**。
  - 仅在 devices 中的 14 台均为非车：风淋门、自动门、电梯等；`deviceType=3`，`productKey` 为 `standardrobots.autodoor.v1p03` / `weichuang.lift.00001` / `1234.2233.3444` 等。
  - 18 台可调度车均为 `deviceType=1` 且 `productKey=standard.oasis.300ul`（本现场观测，不升格为全平台规则）。
- 与假设关系：`SUPPORTED`（Q-016）

## B1 名称 → deviceKey

- 时间：`2026-07-20T10:09:55+08:00`
- 证据：[`runs/B1-name-to-deviceKey.json`](./runs/B1-name-to-deviceKey.json)
- 观察事实：
  - **推荐接口**：`GET /api/task/vehicles/getAllVehicleSimpleInfo`
  - 正例：车名 `新基测试300c协作1` → 唯一命中 `BROKERX-aee2f93d717546cf9510c98c854fe83e`，与环境 `testVehicleKey` 一致。
  - 反例：`不存在的车辆名-riot-behavior-lab` → 0 命中。
  - 本轮 18 个车辆名全部唯一（无重名）。
- 与假设关系：`SUPPORTED`（Q-017）
- 是否足以晋升 knowledge / fixtures：是

## 本轮结论

- 已回答：`Q-016`、`Q-017` → **`SUPPORTED`**
- 推荐默认路径：用 `getAllVehicleSimpleInfo` 做车辆清单与名称解析；不要用裸 `devices` 当车辆列表。
- 仍开放：`deviceKey` 与 `vehicleTaskInfo.key` / 建单 `appointVehicleKey` 是否在写路径上恒等（下单轮次再证）。
- 建议下一实验：在用户确认测试车名/key 后，进入站点摸底或建单相关问题重开。

## 时间轴摘要

| 时间（约） | 场景 | 结果 | 证据 |
|---|---|---|---|
| 10:09 | devices 全量 | 通过 | `B1-devices-all.json`（32，含非车） |
| 10:09 | task 车辆三接口 | 通过 | `B1-getAllVehicle*.json`（18） |
| 10:09 | 差分 | 通过 | `B1-vehicle-vs-device-diff.json` |
| 10:09 | 名称解析 | 通过 | `B1-name-to-deviceKey.json` |
