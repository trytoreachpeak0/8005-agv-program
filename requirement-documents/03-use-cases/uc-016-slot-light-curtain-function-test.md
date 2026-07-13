---
id: UC-016
type: use-case
title: "Slot Light Curtain Function Test 仓位光幕功能测试"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-09
primary_actor: "TBD 待定（推测为设备/电气维护人员 R-11，本次未最终确认，见 Notes）"
secondary_actor: "None 无（本 UC 只读取 IO 模块的光幕状态，不涉及 MES/RIOT）"
frequency: "TBD 待定，预期与 [[uc-015-slot-door-unlock-open-test|UC-015]] 同量级，可在同一次维护巡检中连续进行"
related_uc: ["UC-001", "UC-005", "UC-010", "UC-014", "UC-015", "UC-018"]
related_br: []
aliases: ["UC-016"]
---

# UC-016 Slot Light Curtain Function Test 仓位光幕功能测试

## Description 描述

维护人员选择目标仓位，在该仓位的门已打开的前提下（衔接 [[uc-015-slot-door-unlock-open-test|UC-015]] 的开门操作），先确认系统当前读取的光幕状态为"无遮挡"，随后在仓位内放入测试物体或用手遮挡，核对系统读取的光幕状态是否正确变为"有遮挡"；移除物体/遮挡后，再核对光幕状态是否恢复"无遮挡"。本 UC 只验证光幕传感器本身"检测有无遮挡"这一基础功能是否正常，不涉及仓门开锁/机械动作（见 UC-015）或仓门开关状态识别（见 [[uc-017-slot-door-state-detection-test|UC-017]]）。The maintenance engineer selects a target slot whose door is already open (following on from the open operation in [[uc-015-slot-door-unlock-open-test|UC-015]]), first confirms the system currently reads the light curtain status as "unobstructed", then places a test object into the slot (or blocks it by hand) and checks whether the system correctly reads the status as "obstructed"; after removing the object/obstruction, checks whether the status returns to "unobstructed". This UC only verifies the light curtain sensor's basic "obstruction detection" function, and does not cover the door lock/mechanical action (UC-015) or the door open/close state detection (UC-017).

## Trigger 触发条件

维护人员需要验证某仓位光幕传感器的检测功能是否正常，通常紧接 [[uc-015-slot-door-unlock-open-test|UC-015]] 的开门测试之后进行，也可单独针对已开启的仓门发起。The maintenance engineer needs to verify whether a slot's light curtain sensor functions correctly; this is typically performed right after the door-open test in UC-015, but may also be initiated independently on an already-open door.

## Precondition 前置条件

**Equipment & Hardware 设备与硬件**

1. 目标仓位仓门当前处于开启状态（可通过 [[uc-015-slot-door-unlock-open-test|UC-015]] 打开，或本身已处于开启状态）。The target slot's door is currently open (either opened via UC-015, or already open).

**System & Interface 系统与接口**

2. 本地服务器与 IO 模块之间通信正常，可正常读取该仓位光幕状态。The local server and the IO module communicate normally, so the slot's light curtain status can be read.

**Task & Data 任务与数据**

3. 建议测试前先通过 [[uc-014-enable-disable-slot|UC-014]] 将目标仓位标记为"已禁用"，避免测试期间该仓位被业务流程意外分配使用（非强制，见 UC-015 Assumption 第 1 条同样的处理方式）。It is recommended to first disable the target slot via [[uc-014-enable-disable-slot|UC-014]] before testing (not mandatory, same treatment as Assumption item 1 of UC-015).

**Personnel & Authorization 人员与权限**

4. 维护人员具备操作/查看该仓位光幕状态的权限（具体角色待定，见 Notes）。The maintenance engineer has permission to operate/view the slot's light curtain status (the specific role is TBD, see Notes).

## Postcondition 后置条件

**Task & Data 任务与数据**

1. 若测试正常：该仓位光幕在有/无遮挡两种物理状态下，系统读取的光幕状态均与实际一致。If the test passes: the slot's light curtain readings match the actual physical obstructed/unobstructed state in both cases.
2. 若测试异常：该仓位被标记为"异常锁定"或"测试未通过"，暂停对该仓位的后续业务分配，等待维护人员进一步排查（见 Exception Flow E3.1/E5.1）。If the test fails: the slot is marked as "Exception-locked" or "test failed", suspending further business assignment pending further troubleshooting (see Exception Flow E3.1/E5.1).
3. 本次测试结果（维护人员、仓位号、测试类型：光幕功能测试、结果：正常/异常、时间戳）被记录到本地数据库，用于追溯。This test result (engineer, slot number, test type: light-curtain function test, result: pass/fail, timestamp) is logged in the local database for traceability.

## Assumption 假设

1. 测试使用的"测试物体"由维护人员自行准备，只要能够对光幕形成有效遮挡即可（如现场随手可得的物件、或直接用手遮挡），本 UC 不规定具体物体的规格。The "test object" used is prepared by the maintenance engineer and only needs to sufficiently obstruct the light curtain (e.g. any object on hand, or simply a hand); this UC does not specify the object's exact specification.
2. 本 UC 不验证光幕的检测精度/灵敏度（如能否检测极小遮挡物），只验证"有/无明显遮挡"两种典型场景下的基础通断功能是否正常。This UC does not verify the light curtain's detection precision/sensitivity (e.g. whether it can detect very small obstructions); it only verifies the basic on/off function under two typical "clearly obstructed / clearly unobstructed" scenarios.

## Normal Flow 正常流程

### 16.0 Slot Light Curtain Function Test

1. 维护人员在维护界面中选择目标仓位（仓门已开启）
2. 系统读取并显示该仓位当前光幕状态
   2.1 维护人员核验该状态是否为"无遮挡"、与仓位当前实际为空一致（见 Exception Flow E2.1）
3. 维护人员在该仓位内放入测试物体或用手遮挡光幕
4. 系统读取该仓位光幕状态
   4.1 维护人员核验该状态是否已变为"有遮挡"（见 Exception Flow E4.1）
5. 维护人员移除测试物体/遮挡
6. 系统读取该仓位光幕状态
   6.1 维护人员核验该状态是否已恢复"无遮挡"（见 Exception Flow E6.1）
7. 系统记录本次测试结果（维护人员、仓位号、结果：正常/异常、时间戳）

## Alternative Flow 备选流程

不存在需要区分的备选流程：无论维护人员测试单个仓位还是在同一次巡检中依次测试多个仓位，均按 Normal Flow 相同的步骤逐一执行。No alternative flow is needed: whether testing a single slot or multiple slots in sequence, each slot follows the same steps described in the Normal Flow.

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤一一对应：

* E2.1 测试开始前光幕状态已显示"有遮挡"（与仓位实际为空不一致）
* E4.1 放入测试物体/遮挡后，光幕状态仍显示"无遮挡"
* E6.1 移除测试物体/遮挡后，光幕状态仍显示"有遮挡"

### E2.1 测试开始前光幕状态已显示"有遮挡"

1. 维护人员按第 2.1 步核验，发现该仓位当前实际为空，但光幕状态显示"有遮挡"
2. 维护人员检查该仓位内是否确有异物残留（如未清空的旧产品、杂物）；若确有异物，先清理后重新核验
3. 若清空后光幕状态仍显示"有遮挡"，判定该仓位光幕异常，系统将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果
4. 维护人员排查并修复光幕硬件/接线故障后，重新发起本测试，直至测试通过

### E4.1 放入测试物体/遮挡后，光幕状态仍显示"无遮挡"

1. 维护人员按第 3 步放入测试物体/遮挡光幕
2. 维护人员按第 4.1 步核验，发现光幕状态未变化，仍显示"无遮挡"
3. 判定该仓位光幕异常（检测不到遮挡），系统将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果
4. 维护人员排查并修复光幕硬件/接线故障后，重新发起本测试，直至测试通过

### E6.1 移除测试物体/遮挡后，光幕状态仍显示"有遮挡"

1. 维护人员按第 5 步移除测试物体/遮挡
2. 维护人员按第 6.1 步核验，发现光幕状态未恢复，仍显示"有遮挡"
3. 判定该仓位光幕异常（无法恢复检测为无遮挡，可能存在残留感应或硬件故障），系统将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果
4. 维护人员排查并修复光幕硬件/接线故障后，重新发起本测试，直至测试通过

## Notes 备注

* 本 UC 是用户提出的新场景"测试仓位内光幕是否正常"，与仓门机械开关（[[uc-015-slot-door-unlock-open-test|UC-015]]）、门状态识别信号（[[uc-017-slot-door-state-detection-test|UC-017]]）是三个独立的硬件测试环节，分别成文。
* 维护角色本次不做最终确定，先留 TBD，推测候选为 R-11 设备/电气维护人员，处理方式与 [[uc-015-slot-door-unlock-open-test|UC-015]] 一致。
* 待补充（TBD）事项：
  1. 维护操作角色（`primary_actor`）最终确定。
  2. 是否需要将"测试前禁用"升级为强制 Precondition，待与用户进一步确认（与 UC-015 待定事项一致）。

## Related Use Cases 关联用例

* [[uc-015-slot-door-unlock-open-test|UC-015]]：本 UC 的测试前提（仓门需处于开启状态）由该 UC 的开门操作提供。
* [[uc-017-slot-door-state-detection-test|UC-017]]：与本 UC 同属仓门相关的硬件测试系列，但验证的是门状态反馈信号而非光幕遮挡检测，两者独立进行。
* [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]：这些业务流程在装卸过程中依赖光幕核验仓位内是否确有/确无产品，本 UC 是对该硬件基础能力的独立验证，不改变、也不依赖这些 UC 的业务状态。
* [[uc-014-enable-disable-slot|UC-014]]：建议测试前后配合该 UC 完成"禁用→测试→启用"的操作闭环。
* [[uc-018-io-point-mapping-verification-test|UC-018]]：该 UC 验证的是 IO 点位映射配置本身的正确性，是本 UC 能够正常工作的更底层前提。

## Other Information 其他信息

