# 在新候选上完成干净安装验收

Type: task
Mode: HITL
Status: open
Blocked by: 08

## Question

对票 08 的候选跑干净安装验收，规格对齐上一轮票 14 那次（23 PASS／0 FAIL），并针对本轮改动增删
断言。

必须保留的断言方向：全量文件哈希、真实 RIoT 返回 `STOPPED`、`readiness=Ready`、
`/health/ready` 从 503 转 200、需求受理、重启后 generation 推进并回到 Ready、服务安装与卸载。

本轮**必须改写**的断言：

- 原「HTTPS 安全投影 200 且无凭据 401」改为**HTTP** 安全投影 200 且无凭据 401；
- 原健康检查钉扎根证书的部分改为直接 HTTP；
- **新增**：安装全过程不生成、不导入、不移除任何证书，且不弹出任何信任确认对话框，可在非交互
  环境完整跑完（这是票 03 的目标，必须在真实安装里证到，不能只在脚本层面看代码）；
- **新增**：数据根下不再出现 `certs\`（若票 01 决定保留该目录另作他用，则按其决定调整）。

验收要求：

- 断言必须是**机器可读的实际发射**，不是事后把结果转写成表格——票 21 第 2 项与票 24 拒绝过后者，
  票 13 是第一次真实发射，本轮沿用；
- 至少两条单字段变异各自证红，证明这套断言不是恒绿；
- 用户以管理员身份跑服务安装那一段（沿用票 14 做法），生产服务全程不受影响，使用隔离实例与
  独立端口。

Mode 为 HITL：服务安装需要管理员权限，由用户执行。可沿用票 03 的做法——agent 用
`Start-Process -Verb RunAs` 发起，用户在 UAC 上点确认，agent 再读回报告，无须把整轮交给用户手工跑。

## 票 03 留给本票的两条

1. **是否给 `Update-ControlServerLocal.ps1` 补参数化，由本票决定。** 该脚本把服务名
   （`8005 AGV ControlServer`）与安装／数据／备份根硬写成生产值，没有对应参数，因此**升级流程无法在
   隔离实例上排练**：唯一执行对象就是生产服务。票 03 只以红绿对照覆盖了配置迁移逻辑，证书目录删除、
   机器级 `CONTROL_SERVER_ONBOARD_CERTIFICATE_PASSWORD` 清除、备份／回滚这三段的**真实执行至今零
   证据**。本票要么补参数化后把升级路径也纳入验收，要么明确记录这三段仍未取证并说明为何可接受。
2. **本票「安装不生成／不导入／不移除证书」那条新增断言，票 03 已在隔离实例上取过一次**，见
   `evidence/g2/20260831-plaintext-transport-ticket03/lifecycle-report.json` 与
   `Invoke-IsolatedLifecycle.ps1`（已参数化为 `-Root` / `-PackagePath`）。本票是在**票 08 的正式候选包**
   上重跑，取证形态可直接复用那份脚本的四个回读点：`currentUserRootUnchangedAcrossInstall` /
   `...AcrossUninstall`、`certsDirectoryPresentAfterInstall`、`keyMaterialFilesUnderInstall`、
   `machineCertificatePasswordUntouched`。注意其 `Get-ProductionSnapshot` 按进程名取端口，隔离探针与
   生产进程同名会混入探针端口，本票若沿用须按 PID 过滤修掉这个口径伪影。
