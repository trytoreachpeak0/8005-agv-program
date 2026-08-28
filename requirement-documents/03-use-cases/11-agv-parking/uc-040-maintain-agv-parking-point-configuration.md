---
id: UC-040
type: use-case
title: "Maintain AGV Parking Point Configuration 维护 AGV 停靠点配置"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-13
updated: 2026-07-13
primary_actor: "AGV 运维/调度管理员（R-13）"
secondary_actor: "RIOT"
frequency: "低频；停靠点布局调整或新车接入后执行"
related_uc: ["UC-019", "UC-020", "UC-024", "UC-037", "UC-041"]
related_br: ["BR-009"]
aliases: ["UC-040"]
---

# UC-040 维护 AGV 停靠点配置

## 描述

AGV 运维/调度管理员为每台多仓位 AGV（或按车型/分组）维护"空闲返回停靠点"的候选停靠点集合——即该车空闲时可以被自动派去停靠等待的候选站点范围。本 UC 只负责"配置"本身：候选停靠点的选择范围、保存与审计。具体"系统何时判定某车需要返回停靠、如何从候选集合中选出一个空闲停靠点、多车竞争同一批停靠点时如何排队"等运行时行为，由 [[br-009-parking-point-allocation-and-queueing|BR-009]] 统一定义规则，供 [[uc-041-return-idle-agv-to-parking-point|UC-041]] 遵守；本 UC 不重复定义该算法本身。

> 本 UC 与 [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]] 的结构基本对称（候选站点集合的配置类 UC），区别在于停靠点配置不涉及电量阈值，只涉及候选站点范围本身，因为触发时机已确定为"AGV 一空闲即立即判断"（见 [[uc-041-return-idle-agv-to-parking-point|UC-041]] Trigger），不需要额外的阈值参数。

## 触发条件

管理员需要新增、修改某台 AGV（或某个车型/分组）的候选停靠点配置，或在停靠点布局调整、新车接入后需要补充配置。

## 前置条件

**系统与接口**

1. RIOT 接口在线可用，且本系统已能取得 RIOT 当前地图站点列表（含站点类型标记，用于识别哪些站点可作为"停靠点"）。

**任务与数据**

2. 目标 AGV 已通过 [[uc-019-register-agv-from-rcs|UC-019]] 接入且未归档。
3. 候选停靠点必须来自 RIOT 当前同步的地图站点列表，不允许管理员手工录入任意站点编号（做法与 [[uc-024-maintain-area-station-mapping|UC-024]]、[[uc-037-maintain-agv-charging-strategy-configuration|UC-037]] 对站点来源的约束一致）；候选停靠点是否要求站点类型标记为专门的"停靠点"类型，还是可以复用其他业务站点，TBD 见 Notes。

**人员与权限**

4. 管理员具备停靠点配置维护权限。

## 后置条件

**任务与数据**

1. 该 AGV（或分组）的候选停靠点集合被保存，供 [[br-009-parking-point-allocation-and-queueing|BR-009]] 后续选点/排队决策及 [[uc-041-return-idle-agv-to-parking-point|UC-041]] 引用。
2. 修改只影响保存后新发生的返回停靠判断，不影响已经在停靠中的车辆。
3. 操作人、目标 AGV/分组、修改前后值及时间戳被记录到审计日志。

## 假设

1. 停靠点本身是 RIOT 地图站点的一种（可能是专门划定的站点，也可能复用其他空闲区域站点），其列表、有效性及当前占用/空闲状态均由 RIOT 同步提供；本 UC 不维护停靠点本身的主数据，只从已同步的站点中选择候选集合。
2. 一台 AGV 可以配置多个候选停靠点，实际每次具体分到哪一个，由 [[br-009-parking-point-allocation-and-queueing|BR-009]] 在运行时决定，不在本 UC 中固定为唯一绑定。

## 正常流程

### 40.0

1. 管理员进入停靠点配置页面，选择目标 AGV（或车型/分组）
2. 系统展示当前配置（候选停靠点集合）及最近修改记录
   2.1 系统同步 RIOT 当前地图站点列表，标记其中可作为停靠点的站点及其有效状态（见 Exception Flow E2.1）
3. 管理员从已同步且有效的站点中勾选候选停靠点集合
   3.1 系统校验候选停靠点集合不能为空（见 Exception Flow E3.1）
4. 系统展示修改前后差异，管理员确认保存
5. 系统保存新配置，记录审计日志

## 备选流程

不存在需要区分的备选流程：无论按单台 AGV 还是按车型/分组维护，均按 Normal Flow 相同的选点范围、校验和保存步骤处理。

## 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤（或子步骤）一一对应：

* E2.1 RIOT 站点同步失败，无法确认可用停靠点列表
* E3.1 候选停靠点集合为空

### E2.1 RIOT 站点同步失败

1. 系统按第 2.1 步同步 RIOT 地图站点列表，发现通信异常、超时或结果不完整
2. 系统采用 fail-closed：允许只读查看已有配置，禁止新增、修改候选停靠点集合
3. 系统显示最后一次成功同步时间，并记录接口异常
4. IT/软件维护人员（R-12）或管理员排查并修复 RIOT 接口/网络异常后，管理员重新进入本 UC 进行配置

### E3.1 候选停靠点集合为空

1. 管理员未勾选任何候选停靠点即尝试保存
2. 系统提示"候选停靠点集合不能为空"，拒绝保存
3. 管理员至少选择一个候选停靠点后重新提交

## 备注

* 本 UC 是为填补需求缺口而新增：`vision-and-scope.md` 原功能树中提到的"系统辅助任务：……返回驻点……"此前没有任何 UC 落地，经与用户确认需要补充，拆分为本 UC（配置候选停靠点）与 [[uc-041-return-idle-agv-to-parking-point|UC-041]]（自动返回执行流程）+ [[br-009-parking-point-allocation-and-queueing|BR-009]]（选点与排队规则），拆分方式参照 [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]] / [[br-007-charging-pile-allocation-and-queueing|BR-007]] 的既有先例。
* 待补充（TBD）事项：
  1. 候选停靠点是否要求 RIOT 侧有专门的"停靠点"站点类型标记，还是可以复用任意非业务占用的站点。
  2. 候选停靠点集合是按单台 AGV 维护，还是也支持按车型/分组批量维护，界面细节待补充。
  3. 保存配置前是否要求目标车辆已禁用（类比 [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]] 的同类 TBD），待与用户确认。

## 关联用例

* [[uc-041-return-idle-agv-to-parking-point|UC-041]]：消费本 UC 配置的候选停靠点集合，结合 [[br-009-parking-point-allocation-and-queueing|BR-009]] 完成实际选点与排队。
* [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]]：结构对称的另一类"空闲窗口配置类" UC，两者共同服务于同一个"AGV 空闲"触发窗口的不同消费者。
* [[uc-024-maintain-area-station-mapping|UC-024]]：本 UC 中"候选停靠点必须来自 RIOT 已同步且有效的站点列表"这一约束方式，与该 UC 对站点来源的约束方式一致。
* [[br-009-parking-point-allocation-and-queueing|BR-009]]：定义本 UC 配置数据在运行时如何被用于选点及排队决策，本 UC 不重复定义该算法。

## 其他信息
