# 处置生产形态下车载端 HMI 不反映 WIRE_TO_GATE 且无恢复出口

Type: grilling
Mode: HITL
Status: open
Blocked by:

## Question

票 14 的现场闭环在 RC 的生产形态下走通了业务，同一轮暴露出车载端 HMI 的一个可用性缺陷：站点操作
一旦落进 `RecoveryRequired`，现场操作员在随包 HMI 上没有任何前进或撤销的手段，且整个 WIRE_TO_GATE
业务过程不进 HMI 的状态横幅与操作记录。

缺陷归车载端仓，该仓对 agent 只读，因此本仓不保存缺陷正文、复现步骤、修复或测试。

需要用户决定走哪条路：转交王昆在车载端仓修复、指定一个明确可写的跟踪目的地、还是判定为本轮 MVP
可接受的已知限制并写进发布说明。决定之前不在任何仓库写入缺陷记录或修复。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-onboard-hmi

Routing status: read-only for agents；尚未指定可写跟踪目的地

Impact on this ticket: 不阻断票 14 的闭环结论（generation 7 已 `Completed`），但阻断「随包 HMI
对现场操作员可用」这一条资格结论。

转交件（仓外）：`C:\Users\szy\Desktop\致王昆20260830车载端生产形态HMI缺陷.md`

现场证据（服务端仓，本项目自有）：`8005-agv-control-server@9daeef4` 的
`evidence/g3/20260830-issue14-field-closed-loop/SUMMARY.md`。
