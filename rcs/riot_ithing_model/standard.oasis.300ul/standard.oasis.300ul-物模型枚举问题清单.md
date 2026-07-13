# standard.oasis.300ul 物模型枚举问题清单

> 来源文件：`standard.oasis.300ul.tsl`（productKey = `standard.oasis.300ul`）
> 检查内容：物模型中所有 `dataType.type = "enum"` 的属性/服务字段，枚举取值是否连续、是否都有说明；以及"看起来该是枚举但未声明为枚举"的字段。

## 一、覆盖完整、有清晰解释的枚举（无问题）

以下属性 `specs` 数值连续、每个值都配了英文标识符，视为文档完整：

| 属性 identifier | 中文名 | 取值范围 |
|---|---|---|
| `emergencyState` | 急停状态 | 0~3，连续 |
| `breakSwState` | 解抱闸状态 | 0~2，连续 |
| `sysState` | 系统状态 | 0~24，连续（25个值全） |
| `locationState` | 定位状态 | 0~5，连续 |
| `operationState` | 操作状态 | 0~2，连续 |
| `fleetMode` | 当前的调度模式 | 0~2，连续 |
| `newMovementTaskState` | 新移动任务标记 | 0~2，连续 |
| `freshState` | 新开启状态 | 0~2，连续 |
| `powerState` | 电源状态 | 0~2，连续 |
| `hstate` | 硬件状态 | 0~3，连续 |
| `movementState.paths[].type`（TaskType） | 移动任务子字段 | 0~4，连续 |
| `movementState.paths[].taskResult` | 移动任务子字段 | 0~3，连续 |
| `movementState.paths[].dstStationType` | 移动任务子字段 | 0~1，连续 |
| `playLight` 服务入参 `lightType` | 灯光类型 | 0~2，连续 |
| `playLight` 服务入参 `lightColor` | 灯光颜色 | 0~7，连续 |

说明：这些值虽然只有英文标识符（如 `SYS_STATE_TASK_NAV_NO_WAY`），没有中文注释，但命名基本可以望文生义，属于"有解释"。

## 二、问题1：枚举数值跳号（中间值缺失）

| 属性 identifier | 中文名 | 已定义的值 | 缺失的值 | 备注 |
|---|---|---|---|---|
| `batteryState` | 电池状态 | 0(NA), 2(CHARGING), 3(NO_CHARGING) | **1** | 不清楚1是否会实际出现、代表什么 |
| `movementState.state`（TaskState） | 移动子任务状态 | 0,2,3,4,5,6,7,8 | **1** | 同上 |
| `movementState.paths[].avoidPolicy` | 避障策略 | 0(AT_ZERO),1(WAIT),2(REPLAN),16(NONE) | **3~15（共13个值）** | 跳号幅度很大，很可能是预留位段，需厂商确认 |

**风险**：如果设备实际运行中上报了这些缺失的数值，接口消费方无法知道其含义，需要向设备厂商/RCS平台维护方确认这些空号是否会出现、代表什么状态。

## 三、问题2：同一字段在物模型内两处定义不一致

`pathType` 枚举在文件中出现两次，定义不同步：

- **属性定义**（`movementState.paths[].pathType`）：
  `{"0":"PATH_ZERO","1":"PATH_LINE","2":"PATH_CIRCLE","3":"PATH_BEZIER","4":"PATH_ROTATE"}`
  （不含 -1）
- **服务入参定义**（`moveFollowPath` 服务 `paths[].pathType`）：
  `{"0":"PATH_ZERO","1":"PATH_LINE","2":"PATH_CIRCLE","3":"PATH_BEZIER","4":"PATH_ROTATE","-1":"UNRECOGNIZED"}`
  （多了 -1:UNRECOGNIZED）

**建议**：统一两处定义，属性侧也补上 `-1:UNRECOGNIZED`，避免消费方按不同接口读到的枚举定义不一致。

## 四、问题3：明显该是枚举/离散状态，但完全没有取值说明的字段

以下字段数据类型是裸 `int`（或 `int` 数组），没有配置 `enumSpecs`，无法知道具体数值代表什么含义：

| 字段 identifier | 中文名 | 所在位置 | 说明 |
|---|---|---|---|
| `multiLoadState` | 多位顶升状态标记 | 顶层属性 | 命名明显是状态标记，但只给了 `min:0`，无任何取值列表 |
| `lastErrorCode` | 系统最新错误码 | 顶层属性 | 无枚举/对照表 |
| `hardwareErrorCode` | 硬件错误码 | 顶层属性 | 无枚举/对照表 |
| `faultCodesList` | 故障码集 | 顶层属性（int数组） | 无枚举/对照表 |
| 全部 30+ 个 service 返回结构中的 `code` | 状态码 | 每个 service 的 `outputData.result.code` | **几乎所有服务**（login、moveToStation、triggerEmergency、chargeActionCmd 等）返回的成功/失败状态码，全部是裸 int，无任何取值说明，无法判断调用是否成功、失败原因是什么 |

**这是本次检查中最大的空白点**：错误码/故障码，以及服务调用统一返回的 `code` 状态码，在这份物模型里完全没有文档化，且是全局性的问题（不是个别服务遗漏）。

## 五、后续建议

1. 找设备厂商（斯坦德机器人）要《故障码/错误码对照表》和《服务调用返回码说明》，补齐 `lastErrorCode`、`hardwareErrorCode`、`faultCodesList`、以及各 service `code` 字段的含义。
2. 向厂商确认 `batteryState`、`movementState.state`、`avoidPolicy` 中缺失的数值（1、3~15）是否会实际出现、代表什么状态。
3. 统一 `pathType` 枚举在属性定义与服务入参定义之间的差异（建议在物模型管理后台补充 `-1:UNRECOGNIZED` 到属性侧）。
4. 如果厂商无法提供文档，可通过黑盒试验（连续拉取属性、观察实际工况）或查看设备管理后台前端源码里的映射表，反推缺失枚举值/错误码的含义，并将结果补录回物模型的 `enumSpecs` 中，形成闭环文档。

## 六、问题处理结论（当前阶段决策）

| 问题 | 处理方式 |
|---|---|
| 问题1：枚举数值跳号（`batteryState`、`movementState.state`、`avoidPolicy` 缺失值） | **暂不处理，尊重原值**。跳号处不做任何猜测或补充，实际运行中如遇到未定义数值，按"未知值"原样透传/记录，不在业务逻辑中做隐含假设。后续如设备商可提供确认信息再补充文档。 |
| 问题2：`pathType` 枚举在属性定义与服务入参定义不一致 | **按建议统一执行**：在属性侧（`movementState.paths[].pathType`）补充 `-1:UNRECOGNIZED`，与服务入参定义（`moveFollowPath` 服务）保持一致，消除两处定义的差异。 |
| 问题3：`multiLoadState`、`lastErrorCode`、`hardwareErrorCode`、`faultCodesList` 及各 service 返回的 `code` 无取值说明 | **应用层禁止使用，直接搁置**：由于这些字段没有官方或已验证的取值含义说明，应用中不得直接或间接依赖这些字段的具体数值做业务判断（包括但不限于分支逻辑、报警文案映射、统计分析）。仅允许原样记录/透传，供人工排查参考。待后续通过厂商文档或黑盒试验补齐 `enumSpecs` 并验证准确后，再评估是否放开给业务逻辑使用。 |
