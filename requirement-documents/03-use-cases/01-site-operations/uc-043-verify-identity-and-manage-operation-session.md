---
id: UC-043
type: use-case
title: "现场人员身份核验与操作会话管理 Verify Site Personnel Identity and Manage Operation Session"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
primary_actor: "生产操作员/终点站操作员（按场景引用 R-01~R-08，见 [[stakeholders-and-user-classes|干系人与用户角色清单]]）"
secondary_actor: "MES（返回人员身份及岗位权限）"
frequency: "与 UC-001/UC-002/UC-006/UC-010 同量级，每次 AGV 到站至少触发一次身份核验"
related_uc: ["UC-001", "UC-002", "UC-003", "UC-005", "UC-006", "UC-010", "UC-044"]
related_br: []
aliases: ["UC-043"]
---

# UC-043 现场人员身份核验与操作会话管理

## 描述

多仓位 AGV 到达站点（见 [[uc-003-agv-arrives-at-designated-station|UC-003]]）后，操作员扫描工牌上的一维码或手动输入工号，系统提交 MES 核验人员身份及岗位权限，核验通过后建立与本次到站绑定的操作会话。会话建立后，操作员在该会话内执行 [[uc-001-load-completed-lot-into-slot|UC-001]]（装载）、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]（取出纠错）、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]（终点站取料）或 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]（取料残留重新打开）等仓门操作时，不需要针对每次操作重复验证身份，但每次操作仍记录关联当前会话的操作人身份，保证可追溯到具体个人。

会话分为两个阶段：**未开始仓门操作**与**仓门操作已锁定**。会话建立后、任何仓门尚未被打开之前，操作员可以主动提前结束会话，便于换人重新核验身份；一旦会话内发生了第一次仓门打开动作，会话即进入锁定阶段，此后只能通过完成 [[uc-002-confirm-task-completion|UC-002]]（确认完成）结束会话，不再允许手动结束——因为同一次到站的装卸操作被认为应由同一个人完成始终，不支持中途换人。[[uc-006-cancel-transport-task-upon-arrival|UC-006]]（取消运送）无论在哪个阶段执行，都不会结束或影响会话状态。

## 触发条件

1. [[uc-003-agv-arrives-at-designated-station|UC-003]] 完成到站、装卸操作界面跳转后，当前站点/终端不存在有效会话，操作员准备执行本次到站的任一操作（装载、取出、取消或重新打开）之前。
2. 未开始仓门操作阶段的会话被操作员主动结束后，需要重新核验身份才能继续操作。

## 前置条件

**系统与接口**

1. MES 在线，可返回扫码/工号对应的人员身份及岗位权限。

**设备与硬件**

2. 现场终端具备一维码扫描能力或手动输入通道。

**任务与数据**

3. [[uc-003-agv-arrives-at-designated-station|UC-003]] 已完成，当前站点已进入装卸操作界面。

**人员与权限**

4. 当前站点/终端不存在其他仍处于活动状态（未开始或已锁定阶段均算）的会话；若存在，须先结束该会话才能发起新的核验。

## 后置条件

**任务与数据**

1. 核验通过后，系统建立与本次到站绑定的操作会话，记录操作人身份（工号/姓名，来自 MES）、AGV、站点及会话开始时间，初始处于"未开始仓门操作"阶段。
2. 会话有效期内，操作员执行 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]]/[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 不需要重复验证身份，但各操作记录均关联当前会话的操作人身份。
3. 会话内首次发生仓门打开动作后，会话进入"仓门操作已锁定"阶段；此后执行 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 不改变会话阶段，也不结束会话。
4. 会话仅在下列方式下结束：
   4.1 未锁定阶段，操作员主动提前结束会话。
   4.2 锁定阶段，操作员完成 [[uc-002-confirm-task-completion|UC-002]] 确认完成——这是锁定阶段唯一的正常结束方式。
5. 验证失败时不建立会话，不允许任何后续装载、取出、取消或重新打开操作。
6. 验证成功/失败、会话开始、阶段切换及结束均记录审计。

## 假设

1. 不设置独立的空闲超时机制；会话只通过后置条件第 4 条列出的方式结束，操作员长时间不操作也不会被系统自动登出（TBD：若现场需要空闲超时保护，待后续补充）。
2. 同一站点/终端在同一时刻只允许一个有效会话；不支持在已有有效会话时由另一人直接顶替，需先结束当前会话。"结束会话"（限未锁定阶段，见 A6.1）本身不要求核验身份，终端前任何人均可执行，因此换人/顶替场景无需单独的强制顶替入口，通过"他人先结束会话、再扫码核验新身份"两步即可实现事实上的顶替。
3. 本 UC 建立的操作会话与 [[uc-033-login-and-session-management|UC-033]] 的管理配置端会话彼此独立，不共用账号体系，呼应 [[uc-030-maintain-user-account|UC-030]]、[[uc-031-maintain-role-and-permission|UC-031]]、[[uc-032-assign-user-roles|UC-032]] 中"现场工牌与本地管理账号彼此独立"的既有说明。

## 正常流程

### 43.0

1. 操作员在 AGV 到站后的装卸操作界面扫描工牌上的一维码
2. 系统将扫描内容提交 MES 核验人员身份及岗位权限
   2.1 系统核验 MES 是否返回有效的人员身份（见 Exception Flow E2.1）
   2.2 系统核验该人员岗位权限是否满足当前站点/场景所需的操作权限（见 Exception Flow E2.2）
3. 核验通过后，系统建立本次到站绑定的操作会话，记录操作人身份、AGV、站点及开始时间，会话进入"未开始仓门操作"阶段
4. 系统在界面上显示当前已验证的操作人身份，允许后续操作
5. 操作员在会话内执行一次或多次 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]]/[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]，均复用当前会话、不再重复验证身份
   5.1 首次发生仓门打开动作后，系统将会话状态更新为"仓门操作已锁定"
6. 操作员可在会话内穿插执行 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 取消运送，不影响会话阶段或有效性
7. 操作员完成本次到站所需的全部操作后，执行 [[uc-002-confirm-task-completion|UC-002]] 确认完成
8. 系统结束当前会话，记录结束时间及结束方式（"UC-002 确认完成"），界面恢复为"未验证"状态

## 备选流程

### A1.1 手动输入工号

1. 操作员手动输入工号，替代扫描一维码
2. 其余步骤与 Normal Flow 第 2～8 步一致

### A6.1 未开始仓门操作阶段主动提前结束会话

1. 操作员在会话仍处于"未开始仓门操作"阶段时（如本次到站只需要执行 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 取消所有任务、不涉及任何装卸，或需要更换操作员），点击"结束会话"——该操作不要求核验身份，终端前任何人均可执行，不要求必须是当前会话绑定的操作人本人
2. 系统结束当前会话，记录结束时间及结束方式（"操作员主动提前结束"），界面恢复为"未验证"状态
3. 下一位操作员可重新执行 Normal Flow 第 1 步核验身份，建立新会话（若是由他人代为结束会话后顶替，效果等同于换人，无需额外的强制顶替机制）

## 异常流程

以下异常与 Normal/Alternative Flow 中的对应步骤关联：

- E2.1 人员身份不存在或 MES 返回异常
- E2.2 岗位权限不满足当前场景
- EA6.2 会话已进入锁定阶段时尝试手动结束

### E2.1 人员身份不存在或 MES 返回异常

1. 系统提交扫码/工号至 MES 核验
2. MES 返回"人员不存在"，或因网络/接口异常无法返回结果
3. 系统不建立会话，提示"身份核验失败，请重新扫码或联系管理员"，不泄露具体失败原因是否为账号不存在
4. 操作员重新扫码/输入，或联系管理员核实工号是否正确

### E2.2 岗位权限不满足当前场景

1. MES 返回有效人员身份，但其岗位权限不满足当前站点/场景所需的操作权限
2. 系统不建立会话，提示"当前人员权限不足，无法在本站点操作"
3. 操作员联系班组长或具备对应权限的人员处理

### EA6.2 会话已进入锁定阶段时尝试手动结束

1. 操作员在会话已处于"仓门操作已锁定"阶段时，尝试点击"结束会话"
2. 系统拒绝该请求，提示"本次到站操作已开始，必须先完成 UC-002 确认完成才能结束会话"
3. 操作员继续完成剩余装卸操作后，通过 [[uc-002-confirm-task-completion|UC-002]] 结束会话

## 备注

- 本 UC 补充了此前 UC-001/UC-002/UC-005/UC-006/UC-010 中笼统的"操作员具备扫码/装料操作权限"前置条件，具体化"身份如何验证、验证后是否需要重复验证"这一此前未明确定义的机制。
- 经与用户确认：会话粒度按每次 AGV 到站建立，不是操作员班次级别的会话；每次到站都需要重新核验身份建立新会话。
- 经与用户确认：会话覆盖 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]、[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 这几类仓门操作，均不需要重复验证身份。
- 经与用户确认：会话结束方式分两个阶段——仓门操作开始前可手动提前结束（换人场景）；仓门操作一旦开始，会话锁定给当前操作员，唯一的正常结束方式是完成 [[uc-002-confirm-task-completion|UC-002]]。
- 经与用户确认：[[uc-006-cancel-transport-task-upon-arrival|UC-006]] 不再作为会话结束条件（不论会话处于哪个阶段），因为取消运送本身不代表操作员已经完成本次到站的全部工作。
- 经与用户确认：不再为"强制顶替"单独设计入口。未锁定阶段的"结束会话"（A6.1）本身不要求核验身份，终端前任何人都可以点击结束，因此顶替场景通过"他人先结束会话、再扫码核验新身份"两步即可完成，不需要额外的一步式强制顶替机制；锁定阶段维持 EA6.2 的既有限制，不允许手动结束或顶替，必须完成 [[uc-002-confirm-task-completion|UC-002]]。

## 关联用例

- [[uc-003-agv-arrives-at-designated-station|UC-003]]：本 UC 的触发依赖该 UC 完成到站、界面跳转后进入。
- [[uc-001-load-completed-lot-into-slot|UC-001]]：会话内的装载操作复用本 UC 建立的会话，不重复验证身份；首次执行即触发会话进入锁定阶段。
- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：会话内的取出纠错操作复用本 UC 建立的会话。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：会话内的终点站取料操作复用本 UC 建立的会话。
- [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]：会话内的取料残留重新打开操作复用本 UC 建立的会话。
- [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：可在会话内任意阶段执行，不影响会话状态或结束会话。
- [[uc-002-confirm-task-completion|UC-002]]：完成本 UC 建立的锁定阶段会话的唯一正常结束方式。
- [[uc-030-maintain-user-account|UC-030]]、[[uc-031-maintain-role-and-permission|UC-031]]、[[uc-032-assign-user-roles|UC-032]]、[[uc-033-login-and-session-management|UC-033]]：本 UC 建立的现场操作会话与这些 UC 定义的管理配置端本地账号/角色/会话体系彼此独立，不共用账号或会话机制。

## 其他信息
