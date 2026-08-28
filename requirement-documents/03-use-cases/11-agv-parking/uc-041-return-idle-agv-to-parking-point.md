---
id: UC-041
type: use-case
title: "Return Idle AGV to Parking Point 空闲AGV自动返回停靠点"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-13
updated: 2026-07-13
primary_actor: "本地服务器（系统内部过程，非人工角色）"
secondary_actor: "RIOT"
frequency: "与 AGV 变为空闲的频率一致：每次 AGV 的 RIOT 任务队列变为空，本 UC 都会被触发判断一次"
related_uc: ["UC-008", "UC-009", "UC-012", "UC-040"]
related_br: ["BR-009"]
aliases: ["UC-041"]
---

# UC-041 空闲AGV自动返回停靠点

## 描述

某台多仓位 AGV 的 RIOT 任务队列变为空（即"空闲"）后，本地服务器立即判断该 AGV 是否需要自动返回停靠点：若该 AGV 未被 [[uc-008-dispatch-move-order-to-riot|UC-008]] 抢先分配新的搬运任务、也未被 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 抢先派去充电，且该 AGV 当前不在任何一个已配置的候选停靠点上，系统按 [[br-009-parking-point-allocation-and-queueing|BR-009]] 从 [[uc-040-maintain-agv-parking-point-configuration|UC-040]] 配置的候选停靠点集合中选定一个具体停靠点，调用 RIOT 接口下发移动任务，AGV 随即前往该停靠点等待。

> 本 UC 与 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] 是对"该 AGV 当前 RIOT 任务队列变为空"这一同一触发窗口的三个竞争消费者，本 UC 优先级最低：AGV 一旦空闲，UC-008 会尝试自动派发本地待处理的搬运任务，UC-012 由 R-13 主动争取该窗口派发充电任务，本 UC 只在前两者均未抢先处理时才生效；三者不做互相抢占的设计，谁先完成谁获胜（详见 Exception Flow E1.1、[[br-009-parking-point-allocation-and-queueing|BR-009]] 第4节）。

## 触发条件

某台多仓位 AGV 的 RIOT 任务队列由非空变为空（无正在执行的移动任务）。

## 前置条件

**系统与接口**

1. RIOT 接口在线可用。
2. 该 AGV 在 [[uc-040-maintain-agv-parking-point-configuration|UC-040]] 中已配置至少一个候选停靠点。

**任务与数据**

3. 该 AGV 当前不处于"已禁用"或"禁用待生效"状态（见 [[uc-013-enable-disable-agv|UC-013]]）。
4. 该 AGV 当前不在任何一个已配置的候选停靠点上（若已经在候选停靠点上，判定为无需移动，见 Alternative Flow A1.1）。

## 后置条件

**系统与接口**

1. 该 AGV 在 RIOT 侧新增一个移动到所选停靠点的移动任务；AGV 随即按 RIOT 规划路径移动至该停靠点并停靠等待，直至被 UC-008 或 UC-012 重新派出。

**任务与数据**

2. 本次自动返回停靠下发记录（AGV、停靠点、时间戳）被记录到本地数据库，用于追溯。
3. 若当前所有候选停靠点均不可用（被占用/预占），该 AGV 按 [[br-009-parking-point-allocation-and-queueing|BR-009]] 加入"待返回停靠"排队集合，保持原地不动，等待后续停靠点释放或被 UC-008/UC-012 带离排队集合。

## 假设

1. "AGV 空闲"的判定只依据该 AGV 当前 RIOT 任务队列是否为空，不要求其仓位也全部空闲；即使仓位中仍有在运产品，也可能触发返回停靠点判断（与 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 对"空闲"的定义方式一致）。
2. 本 UC 假定"该 AGV 是否已被 UC-008/UC-012 抢先处理"这一判断可以在同一次空闲事件的处理窗口内可靠完成；三者之间具体的执行时序/锁机制（如谁先拿到该 AGV 的处理权）TBD，见 Notes。

## 正常流程

### 41.0

1. 系统检测到某 AGV 的 RIOT 任务队列变为空，触发本 UC 判断
   1.1 系统核验该 AGV 是否已被 [[uc-008-dispatch-move-order-to-riot|UC-008]] 或 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 抢先处理（见 Exception Flow E1.1）
   1.2 系统核验该 AGV 当前是否处于"已禁用"或"禁用待生效"状态（见 Exception Flow E1.2）
   1.3 系统核验该 AGV 当前是否已在某个候选停靠点上（见 Alternative Flow A1.1）
2. 系统按 [[br-009-parking-point-allocation-and-queueing|BR-009]] 从该 AGV 在 [[uc-040-maintain-agv-parking-point-configuration|UC-040]] 中配置的候选停靠点集合内选定一个当前空闲的停靠点
   2.1 系统核验是否存在当前空闲的候选停靠点（见 Exception Flow E2.1）
3. 系统调用 RIOT 接口，为该 AGV 创建一个移动到所选停靠点的移动任务
   3.1 系统核验 RIOT 是否正常接收本次下发请求（见 Exception Flow E3.1）
4. 系统记录本次自动返回停靠下发日志（AGV、停靠点、时间戳）
5. AGV 按 RIOT 规划路径移动至该停靠点并停靠等待（导航过程本身由 RIOT 自主管理，是否复用 [[uc-009-monitor-move-order-until-arrival|UC-009]] 的轮询监听逻辑，TBD 见 Notes）

## 备选流程

### A1.1 该 AGV 已在候选停靠点上

1. 系统按第 1.3 步核验，发现该 AGV 当前已经停靠在某个候选停靠点上
2. 系统判定无需移动，本次触发不产生任何 RIOT 下发动作，直接结束本轮判断

## 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤（或子步骤）一一对应：

* E1.1 该 AGV 已被 UC-008 或 UC-012 抢先处理
* E1.2 该 AGV 当前已被禁用
* E2.1 当前没有任何候选停靠点空闲
* E3.1 停靠移动指令下发失败/超时

### E1.1 该 AGV 已被 UC-008 或 UC-012 抢先处理

1. 系统按第 1.1 步核验该 AGV 是否已被抢先处理，发现其 RIOT 任务队列已因 [[uc-008-dispatch-move-order-to-riot|UC-008]] 或 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 重新变为非空
2. 系统放弃本次返回停靠点判断，不下发任何指令，不排队、不重试
3. 待该 AGV 下一次变为空闲时，重新触发本 UC 判断

### E1.2 该 AGV 当前已被禁用

1. 系统按第 1.2 步核验，发现该 AGV 当前处于"已禁用"或"禁用待生效"状态
2. 系统放弃本次返回停靠点判断，不下发任何指令
3. 该 AGV 启用后，若仍处于空闲状态，需等待下一次空闲事件触发（或由管理员通过其他方式手动移动，具体是否需要单独提供手动移动入口 TBD）

### E2.1 当前没有任何候选停靠点空闲

1. 系统按第 2.1 步核验，发现该 AGV 的候选停靠点集合内所有站点均处于占用或预占状态
2. 系统按 [[br-009-parking-point-allocation-and-queueing|BR-009]] 将该 AGV 加入"待返回停靠"排队集合，本轮不下发任何指令，该 AGV 保持原地不动
3. 后续有候选停靠点释放，或该 AGV 被 UC-008/UC-012 带离排队集合时，排队状态相应更新

### E3.1 停靠移动指令下发失败/超时

1. 系统按第 3 步向 RIOT 发起创建停靠移动任务的请求
2. 系统按第 3.1 步核验，发现本次请求通信异常、超时，或 RIOT 返回下发失败
3. 系统自动重试（具体重试次数/间隔 TBD）
4. 若重试仍失败且达到预设阈值，系统触发告警提示（如界面告警、上报 IT/软件维护人员 R-12 或 AGV 运维/调度管理员 R-13），本次返回停靠下发暂停，该 AGV 保持原空闲状态，可被后续重新尝试或被 UC-008/UC-012 正常派车/派充电
5. IT/软件维护人员或 AGV 运维/调度管理员排查并修复 RIOT 接口/网络异常后，可等待下一次空闲事件重新触发，或视需要提供人工重试入口（TBD）

## 备注

* 本 UC 是为填补需求缺口而新增：`vision-and-scope.md` 原功能树中提到的"系统辅助任务：……返回驻点……"此前没有任何 UC 落地；经与用户确认，触发时机为"AGV 一空闲即立即判断"（不设等待窗口），停靠点选择方式参照 [[uc-037-maintain-agv-charging-strategy-configuration|UC-037]]/[[br-007-charging-pile-allocation-and-queueing|BR-007]] 的候选集合+排队模型（见 [[br-009-parking-point-allocation-and-queueing|BR-009]]），且本 UC 相对 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] 优先级最低，不做抢占设计，处理方式与 UC-012 对 UC-008 的既有竞争关系一致（三者两两之间均为"谁先完成谁获胜"，不排队等待抢占窗口）。
* 待补充（TBD）事项：
  1. 三个"AGV 空闲窗口"消费者（UC-008/UC-012/本 UC）之间具体的执行时序/锁机制，确保同一次空闲事件不会被两个消费者同时处理产生冲突指令。
  2. AGV 前往停靠点途中的导航过程是否复用 [[uc-009-monitor-move-order-until-arrival|UC-009]] 的轮询监听逻辑。
  3. 停靠移动下发失败达到重试阈值后，是否需要提供人工手动重试入口，还是仅等待下一次自然空闲事件。
  4. 该 AGV 启用后（若之前因禁用放弃过返回停靠判断）是否需要立即补一次判断，还是必须等待下一次真正的空闲事件。

## 关联用例

* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 与该 UC 竞争同一个"AGV 空闲"触发窗口，优先级低于该 UC；若该 UC 先完成派车，本 UC 放弃本次判断（见 Exception Flow E1.1）。
* [[uc-012-manually-dispatch-agv-to-charge|UC-012]]：本 UC 与该 UC 同样竞争"AGV 空闲"触发窗口，优先级低于该 UC；两者的竞争处理方式相同，互不排队抢占。
* [[uc-009-monitor-move-order-until-arrival|UC-009]]：本 UC 下发停靠移动任务后，AGV 移动至停靠点的导航过程是否需要复用该 UC 的轮询监听逻辑，TBD 待补充。
* [[uc-013-enable-disable-agv|UC-013]]：本 UC 的 Precondition 依赖该 UC 维护的"已禁用"/"禁用待生效"状态——处于该状态的 AGV 不会被本 UC 自动派发返回停靠指令。
* [[uc-040-maintain-agv-parking-point-configuration|UC-040]]：提供本 UC 选点所需的候选停靠点集合配置。
* [[br-009-parking-point-allocation-and-queueing|BR-009]]：定义本 UC 第2步"选定具体停靠点"的选点算法及多车竞争同一批停靠点时的排队规则，本 UC 不重复定义该算法本身。

## 其他信息
