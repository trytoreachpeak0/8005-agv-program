# 定位干净安装停在 RecoveryRequired 的那一步

Type: task
Mode: AFK
Status: resolved
Blocked by:

## Question

在票 25 重建的 RC（`w2g-rc-20260830-d243abf`）上，干净 SQLite + 全新 journal 的部署会话建立后
恒停在 `readiness=RecoveryRequired`，`/health/ready` 恒 503，282 条 MesIngest backlog 一条都
不被受理，因此 RIoT 读路径与整个移动闭环在这份部署上不可达（票 13 的 `SESSION-READINESS`、
`DEPLOY-HEALTH`、`ADAPTER-RIOT-READONLY`）。

`OnboardMessageProcessor.cs:56` 在 SessionHello 时无条件置 `RecoveryRequired`，只有车载端发出
`RecoveryStateReport`、服务端走 `DecideReadinessAsync`（同文件 229 行）才转 `Ready`。

那份 `RecoveryStateReport` 为什么没发出？它是产品缺陷，还是缺一步应当写进公开操作步骤的动作？

判据必须先证红再报：拿到一次 `readiness=Ready` 的对照运行，并说明它与失败运行的**唯一**差异。
已知的候选差异是车载端 publish 形态——票 13 用的是 RC 自带的 `onboard-hmi`，而历史上跑通完整
闭环的是 stage 构建的 `C:\Users\szy\w2g-stage\onboard\...\bin\Release\...`，两者同 commit
`304e6ad`。不要只试一个点就下结论。

若定位到车载端产品代码，归 `8005-agv-onboard-hmi`（对 agent 只读），本仓只留路由指针，
并给用户一份可直接转给王昆的通知。若定位到服务端或操作步骤，在 `8005-agv-control-server` 修复
并按硬规矩收尾（Release 0 warning、`dotnet format`、tier 1 0 skip、八片 G2 绑精确 commit）。

不得为了让 readiness 变绿而放宽 `/health/ready` 闸门或跳过 `RecoveryStateReport`——那是掩盖，
不是修复。

## Answer

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server

Owner issue/artifact: `docs/RELEASE-CANDIDATE.md` and
`evidence/g3/20260830-issue26-clean-install-readiness/`

Published branch/commit: `ControlServer_MVP@81cb9cf60a7990a7a7fb1b235042df5d0a9afd99`
（操作步骤与红绿 harness 在 `264615abb5ba87bcc3bc725160729ffba8d247df`，八片 G2 证据在后续提交）

Impact on this ticket: 阻断是部署资格步骤漏掉可信车辆停稳投影，不是恢复报告漏发或 publish 形态缺陷；
按生产模板启用 `vehicleSafety`、信任 ControlServer HTTPS 证书链，并取得新鲜且车辆身份匹配的
`STOPPED` 投影后，干净会话可进入 `Ready`。

票 13 的真实 SQLite 回读显示 `RecoveryStateReport=1`，最终原因是
`DEPARTURE_SAFETY_NOT_READY`。同一捕获握手在两个全新库上重放：原安全事实得到
`RECOVERY_REQUIRED`；只把 `vehicleStopped/departureSafe` 改为 `true` 并清空旧原因码，即得到
`READY`，两侧都收到该恢复报告的 `DurableAck`。因此票面「报告没发出」假设被证伪。

公开 RC 手册已补齐同机／异机证书信任、`vehicleSafety.endpoint`、`expectedVehicleKey`、新鲜
`STOPPED` 预检和 reasonCode 分诊。未改产品代码；未动车、未建单、RIoT mutation 为 0。Release
构建 0 warning / 0 error，`dotnet format` 通过，全仓 243 passed / 0 skipped；W2G-IS-00～07
八片 G2 全 PASS，绑定 `264615abb5ba87bcc3bc725160729ffba8d247df`。
