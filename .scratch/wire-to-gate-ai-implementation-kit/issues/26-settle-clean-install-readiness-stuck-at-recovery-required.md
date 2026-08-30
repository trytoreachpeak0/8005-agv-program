# 定位干净安装停在 RecoveryRequired 的那一步

Type: task
Mode: AFK
Status: open
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
