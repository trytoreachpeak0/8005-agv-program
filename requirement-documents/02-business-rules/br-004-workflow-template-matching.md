---
id: BR-004
type: business-rule
title: "Workflow Template Matching 流程模板匹配规则"
status: draft
created: 2026-07-13
updated: 2026-07-13
related_uc: ["UC-025", "UC-026", "UC-027", "UC-028", "UC-029"]
related_br: ["BR-003", "BR-005", "BR-006"]
aliases: ["BR-004"]
---

# BR-004 Workflow Template Matching 流程模板匹配规则

## Rule Statement 规则内容

### 1. 匹配输入与候选范围

创建业务任务或流程实例时，系统必须使用创建时已经冻结的业务上下文匹配流程模板。匹配输入至少包括：

- `moveType`：搬运类型。
- `taskSource`：任务来源，例如 `MES`、`MANUAL`、`MOCK` 或其他经开发预置的枚举。
- `materialType`：物料类型。
- `sourceStation`、`targetStation`：已按 [[br-003-area-station-mapping|BR-003]] 解析的起点、终点站点。
- `sourceStationType`、`targetStationType`：起点、终点的站点类型。

只有满足以下全部条件的模板版本才进入候选集合：

1. 状态为 `Published`，且在实例创建时刻已经生效、尚未 `Retired`。
2. 模板声明的每个匹配维度等于输入值，或该维度明确声明为通配 `ANY`。
3. 模板引用的步骤类型均存在于 [[workflow-step-catalog|预置步骤目录]]，且模板结构符合 [[br-006-workflow-step-execution|BR-006]]。
4. 起终点已成功解析；站点、站点类型、物料类型或任务来源任一关键输入缺失、无效或无法确定时，不得把未知值当作 `ANY`。

`ANY` 只能由模板显式声明。空值、读取失败和未知枚举不等于 `ANY`，也不得通过默认值补齐后继续匹配。

### 2. 具体匹配优先级

系统先过滤不匹配候选，再对剩余候选按下列优先级逐项比较；只有前一项相同时才比较后一项：

1. `moveType` 精确匹配优先于 `ANY`。
2. `taskSource` 精确匹配优先于 `ANY`。
3. `materialType` 精确匹配优先于 `ANY`。
4. 起点和终点的站点编号均精确匹配。
5. 仅起点站点编号精确匹配。
6. 仅终点站点编号精确匹配。
7. 起点和终点的站点类型均精确匹配。
8. 仅起点站点类型精确匹配。
9. 仅终点站点类型精确匹配。

实现时应将上述规则表示为以下按顺序比较的优先级向量，不得自行改成可产生不同结果的加权总分：

```text
(moveTypeExact,
 taskSourceExact,
 materialTypeExact,
 bothStationIdsExact,
 sourceStationIdExact,
 targetStationIdExact,
 bothStationTypesExact,
 sourceStationTypeExact,
 targetStationTypeExact)
```

每一项取 `1` 或 `0`，按从左到右的字典序降序比较。站点编号精确匹配后，站点类型仍必须与实际站点类型一致或为 `ANY`；精确站点配置不能借此绕过站点类型约束。

模板名称、创建时间、数据库主键、版本号及配置顺序不得作为运行时消除并列的隐含排序条件。发布校验应尽量阻止可导致同一上下文并列的规则同时生效，但运行时仍必须执行唯一性检查。

### 3. 唯一结果与 fail-closed

- 候选集合为空时，匹配结果为“无匹配”，任务/流程实例不得进入自动执行或下发。
- 最高优先级存在两个或以上候选时，匹配结果为“多匹配”，系统不得自动任选一个。
- 只有最高优先级候选恰好一个时，匹配成功，并按 [[br-005-workflow-template-versioning|BR-005]] 绑定该已发布版本的不可变快照。
- 无匹配、多匹配、输入不完整、模板读取失败或匹配服务异常均采用 fail-closed：任务进入明确的“模板匹配异常/等待授权处理”状态，不得开锁、派车、调用任意外部写接口或推进业务任务状态。

每次匹配必须记录输入快照、候选版本 ID、各候选优先级向量、最终结果、失败原因和时间。

### 4. 授权手动覆盖

仅 R-12（IT/软件维护人员）或 R-13（AGV 运维/调度管理员）具有专门的“流程模板匹配覆盖”权限时，可以对“无匹配”或“多匹配”结果手动选择一个当前有效的 `Published` 模板版本。

手动覆盖必须同时满足：

1. 使用个人账号完成再次认证，不得使用共享账号。
2. 填写非空、可追溯的覆盖原因；只填写空白、默认占位文字或无意义内容不得提交。
3. 明确展示原匹配输入、原结果、候选列表、所选模板及其版本，操作人确认后方可生效。
4. 审计记录操作人、角色、认证时间、任务/流程实例、原匹配结果、覆盖原因、所选版本、执行结果和关联告警。
5. 覆盖只作用于指定任务/流程实例，不修改匹配规则，不影响其他实例。
6. 不得选择 `Draft`、`Retired`、结构无效或包含未知步骤类型的模板，不得绕过 [[br-006-workflow-step-execution|BR-006]] 的强制安全步骤与安全联锁。

R-12/R-13 不得通过手动覆盖创建脚本步骤、任意 API 调用或修改已发布模板。若当前不存在可安全执行的已发布模板，覆盖必须被拒绝并保持阻断。

## Rationale 制定原因

同一搬运业务可能因任务来源、物料类型和站点组合采用不同的认证、扫码、硬件及异常处理流程。具体、稳定且可解释的优先级可避免配置顺序或版本时间影响运行结果；唯一性检查和 fail-closed 可防止错误模板导致误派车、误开门或未经校验的物料流转。

## Source 来源

2026-07-13 流程模板需求确认：

- 按 `moveType`、任务来源、物料类型、起终点/站点类型匹配已发布模板。
- 匹配结果必须唯一；无匹配或多匹配时 fail-closed。
- R-12/R-13 可在授权、填写原因并完整审计的前提下进行单实例手动覆盖。

## Related Use Cases 关联用例

- [[uc-025-maintain-workflow-template|UC-025]]：维护模板匹配条件、校验结构，并在发布前检查冲突和管理可参与匹配的版本。
- [[uc-026-select-template-and-create-workflow-instance|UC-026]]：按本规则完成候选过滤、优先级比较和唯一性判定，匹配成功后绑定不可变快照并创建实例。
- [[uc-027-execute-workflow-steps|UC-027]]：仅执行已唯一绑定且结构有效的模板快照。
- [[uc-028-handle-workflow-step-exception|UC-028]]：处理匹配异常后的授权人工覆盖，不得绕过本规则。
- [[uc-029-view-workflow-instance-progress|UC-029]]：只读展示匹配证据和覆盖审计。
- [[br-003-area-station-mapping|BR-003]]：提供匹配所需的冻结起终点及站点类型。
- [[br-005-workflow-template-versioning|BR-005]]：定义已发布版本和实例快照。
- [[br-006-workflow-step-execution|BR-006]]：约束匹配后可执行的流程结构和安全边界。
