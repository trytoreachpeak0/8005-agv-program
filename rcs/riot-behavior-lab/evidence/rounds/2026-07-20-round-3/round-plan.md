# Round 3（2026-07-20）

## 1. 研究目标

- 关联问题：`Q-016`、`Q-017`
- 本轮要回答：
  1. 系统里有哪些可调度车辆；设备列表如何混入非车设备。
  2. 能否用车辆名解析到 `deviceKey`（下单前置）。
- 明确不回答：建单、到站、取消、写设备、`deviceKey`↔`vehicleKey` 是否恒等（富对象里另有 `vehicleTaskInfo.key`，本轮只确认 simpleInfo 的 `deviceKey` 可用于标识车辆）。

## 2. 环境元数据

- RIoT 基址：现场别名 `lab-primary`（`environment.local.json`）
- 鉴权：`callApiKey`（A2 / BC-AUTH-002），本轮不登录
- RIoT 平台版本：`v2.2.0.30`（沿用既有记录；本轮未重新核对）
- 本机时间与时区：`Asia/Shanghai`（UTC+8）

## 3. 范围与授权

- 只读实验：`B1`（设备全量、task 车辆清单、名称解析正反例）
- 已批准写实验：无
- 明确跳过：一切写接口、建单、A1 重跑
- 授权时间与原始表述：2026-07-20，用户要求获取系统车辆、关注非车设备混入，并验证通过车辆名读取 `deviceKey`（下单前置，非下单本身）

## 4. 前置状态

- Q-015 / A2 已通过
- 已知测试车 key（环境配置）：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 本轮无写操作，不依赖车空闲

## 5. 执行顺序

1. 设备全量列表（含非车）
2. task 车辆 key / simpleInfo / taskVehicles 对照
3. 车辆 vs 非车差分
4. 名称→deviceKey 正例与反例
5. 更新 open-questions / knowledge / fixtures

## 6. 本轮状态表

| 类别 | 编号 | 测试项 | 只读/写 | 状态 |
|---|---|---|---|---|
| B 车辆发现 | B1 | devices 全量（含非车） | 只读 | 通过 |
| B 车辆发现 | B1 | getAllVehicleKeys | 只读 | 通过 |
| B 车辆发现 | B1 | getAllVehicleSimpleInfo | 只读 | 通过 |
| B 车辆发现 | B1 | getAllTaskVehicles（结构探查） | 只读 | 通过 |
| B 车辆发现 | B1 | 车辆 vs 非车差分 | 只读 | 通过 |
| B 车辆发现 | B1 | 名称→deviceKey 正例/反例 | 只读 | 通过 |

## 7. 收尾确认

- 测试车可用：本轮未触碰写操作
- 无遗留订单：本轮未建单
- 无其他车辆受影响：仅只读
- 凭据已脱敏：是
- 未解决异常已登记：devices 的 `current+size` 翻页本现场不可靠，已记入契约旁证
