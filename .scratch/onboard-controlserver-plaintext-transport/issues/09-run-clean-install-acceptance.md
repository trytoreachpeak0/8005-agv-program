# 在新候选上完成干净安装验收

Type: task
Mode: HITL
Status: resolved
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

## Answer

三次运行，全部证据在服务端仓 `evidence/g3/20260901-issue09-clean-install-acceptance/`
（提交 `a0f1b3f`），SUMMARY.md 逐条对应。本票同时答掉了票 03 留下的两条。

| 运行 | 结果 |
| --- | --- |
| 干净安装验收（第三轮，最终） | **35 PASS / 0 FAIL / 4 INCONCLUSIVE** |
| §4.5 升级路径排练 | **18 PASS / 0 FAIL** |
| 红侧单字段变异 | **7 PASS / 0 FAIL** |
| 第一轮（保留为 harness 缺陷红证据） | 30 PASS / 5 FAIL |

### 0. 先决动作：候选作废并重建（本票发现的缺口）

手册 §4.5 让站点跑 `.\scripts\Update-ControlServerLocal.ps1`，用的是与 §4.2 安装命令相同的包内
相对路径，但发布脚本的复制清单只有 Install／Uninstall／Publish 三个。**票 08 冻结的候选里跑不了
它自己文档化的升级路径。** §4.5 是本轮票 04 新写的，缺口是这一轮引入的。

修法必然改到被哈希覆盖的文件，故候选在 `19ce7db` 重建（`w2g-rc-20260901b-19ce7db`，SHA256SUMS
868→869 条，manifest 新增 `operatorEntryPoints.upgrade`）。更正已写进票 08 与票 11。

重建换的是身份标签不是产品，这是可证的：`git diff --name-only 56d4b1c..19ce7db -- src tests
Directory.Build.props Directory.Packages.props global.json` 列出 **0 个文件**；两版服务端包 383 个
文件里 373 个哈希未变（变的十个是四个自有程序集的 dll/pdb、apphost、记录哈希的 manifest）；两个
apphost 各 152064 字节，差异恰好 38 字节且全在连续窗口 `0x24D6C–0x24DBB` 内，解码即
`ProductVersion 1.0.0+56d4b1cc…` → `1.0.0+19ce7db7…`，窗口之外逐字节相同。

据此**未重跑 G3**：`run-staged-g3.ps1` 的 `$ControlServerCommit` 移到 `19ce7db`（单行），但
**最后一次真实 G3 执行仍是票 13 那次、在 `56d4b1c` 上**——据实记录，不假装重跑过。

### 1. 票 03 第 1 条：`Update-ControlServerLocal.ps1` 参数化（用户 2026-09-01 选定）

补了五个参数：`-ServiceName` / `-InstallRoot` / `-DataRoot` / `-BackupRoot` /
`-CertificatePasswordVariable`，默认值全部等于它们替换掉的硬写值，**生产调用形态逐字未变**；
`$stagingPath` 由硬写的生产同级路径改为从 `-InstallRoot` 派生。手册 §4.5 那句「不可参数化」一并
改掉，并写明五个参数的唯一用途是先在隔离实例上排练再动生产。

第五个参数不是凑数：不参数化机器级变量名，排练就会清掉**正在运行的生产服务**依赖的那条
`CONTROL_SERVER_ONBOARD_CERTIFICATE_PASSWORD`。排练用探针名
`CONTROL_SERVER_TICKET09_PROBE_CERT_PASSWORD`，执行的代码路径完全相同，只有名字不同。

于是票 03 那三段零证据的路径**全部有了真实执行证据**，在老 TLS 期候选
`w2g-rc-20260831-31263b1`（服务端 `9daeef4`）装出的隔离实例上跑：

- **回滚**（先跑，用一个 manifest 自洽但 `appsettings.json` 非法 JSON 的包，让失败落在备份**之后**
  ——这是唯一能走到回滚的方式）：诊断日志逐步记为
  `preflight-complete > service-stopped > backup-complete > staging-complete removedKeys=4
  healthUrlRewritten=True > certificate-cleanup-complete directory=True password=True >
  replacement-installed > failure: … cannot be started … > rollback-complete`。回滚后安装树与升级前
  **0 差异**、探针口令原值恢复、服务 Running、`certs\` 带 3 个文件回来。
- **证书目录删除**：`certificateDirectoryRemoved: true` **且**回读 `certs\` 不存在（只信报告字段就是
  脚本自说自话）。对照是 `LEGACY-INSTALL` 记录的升级前 3 个文件。
- **机器级口令清除**：探针变量消失 **且**生产那条原值未变。两半都要——只清「看起来像证书口令的
  一切」也能满足前一半。
- 另外：迁移后四个键全消失、`Health:url` 重写为 `http://localhost:58607`、升级后实例
  `/health/live` 200 明文、安装与数据根零密钥材料（同一检测器在备份根仍找得到回滚依赖的老证书）、
  `currentUserRootCertificateRemoved: false` / `…IsManual: true` 如实保留。
- `REHEARSAL-CERT-STORES-UNCHANGED`：整轮排练四个存储指纹摘要零变动，**包括**老安装器自己那次证书
  生成（它在 `CurrentUser\My` 建根与叶、导出后各自删掉；`-InstallCurrentUserRoot` 有意不传）。
- `REHEARSAL-PRODUCTION-UNAFFECTED`：零漂移、口令未变。**这条断言正是参数化的意义所在**——用生产
  变量名排练它就会红。

### 2. 票 03 第 2 条：安装不碰证书，在真实安装里证到

隔离实例 `8005 AGV ControlServer Ticket09`，58505/58507，绑 `192.168.200.1`（车载端
`environment=Production` 拒 loopback），用候选**自带**的脚本装与卸。

- `INSTALL-CERT-STORES-UNCHANGED` / `LIFECYCLE-CERT-STORES-UNCHANGED`：四个存储（`CurrentUser\Root`
  44、`LocalMachine\Root` 42、两个 `My` 各 1）的**排序指纹集合摘要**在安装期与「安装到卸载」全程
  各零变动。是摘要不是计数——换掉一张证书计数不变而摘要会变。
- `INSTALL-NO-CERTS-DIRECTORY` / `INSTALL-NO-KEY-MATERIAL`：无 `certs\`，安装／数据／备份三个根零
  密钥材料文件。
- `INSTALL-MACHINE-CERT-PASSWORD-UNTOUCHED`：机器级证书口令既没写也没清，只记存在性与相等判定，
  不打印值。
- `INSTALL-NON-INTERACTIVE`：整轮安装在 `-NonInteractive` 宿主里跑完并返回；信任确认对话框会在此
  永久阻塞。
- **独立佐证**（沿用票 13「硬编码的 `tls=$false` 不是证据」那条）：全程 install → 会话 → 受理 →
  重启 → 卸载的服务端日志 30461 行，搜
  `Schannel|SslStream|AuthenticationException|X509|certificate|https://` 命中 **0**。

### 3. 票 14 规格的改写与保留

改写掉的两条：`SAFETY-PROJECTION-HTTP-AUTH` 明文 HTTP 200、无凭据 **401**（票 14 是 HTTPS 加钉扎
根）；`HEALTH-LIVE-HTTP` 直连 http `{"status":"live"}` 200。`INSTALL-CONFIG-PLAINTEXT` 与
`CFG-ONBOARD-PRODUCTION` 另外证了两端配置面都没有把 TLS 键带回来。

票 14 记为 INCONCLUSIVE 的两条**本票关掉**：`INSTALL-AS-SERVICE`（result PASS、
`sourceCommit=19ce7db7…`、服务 Running）与 `PERSISTENT-LOGS`（数据根下
`controlserver-20260901.ndjson`，30461 行）。

保留的方向全绿：全量文件哈希 869 条零失配（红侧翻一字节即报出该文件）、真实 RIoT
`motionState=STOPPED`（`source=RIOT_BEHAVIOR_LAB_R41`）、`readiness=Ready`、`/health/ready`
503 `RECOVERY_HANDSHAKE_REQUIRED` → 200、`Restart-Service`（文档化的 §5 操作，不是杀进程）后
generation 1→2 且回到 Ready、`ProtocolInbox` 34→49 且日志不重建、服务卸载 result PASS 且两个根
都删净。生产服务全程 PID 8632、三个监听地址不变、机器级口令值不变（**按 PID 取监听，不按进程名**
——票 03 那个口径伪影已修）。

### 4. 需求受理：本轮能证与不能证的

安装器**按设计**写 `JourneyRuntime.enabled=false`（手册 §11：不建单、不动车）。本票在隔离实例上
显式翻开它并把这一偏离写成断言，`RiotCreateDispatch` 与 absent-observation 两个建单闸门保持包内
默认 `false`。翻开生效的运行期回读在日志里：三条
`Journey runtime is disabled; MesIngest polling and movement dispatch are fail-closed.` 全部出现在
02:23:45–49（安装器自己的生命周期检查阶段），翻开并重启**之后一条都没有**。

- `DEMAND-DECISION-REACHED` **PASS**：12 条 `WIRE_TO_GATE` 需求逐条走到具名判定
  （`OUT_OF_SCOPE_AREA=10`、`AREA_STATION_NOT_FOUND=1`、`BATTERY_POLICY_NOT_SATISFIED=1`），
  264 行 backlog 零行缺 ReasonCode。对照是全部非 `WIRE_TO_GATE` 需求都归到
  `OUT_OF_SCOPE_WORK_TYPE`——分类器在按作业类型区分，不是给所有行盖同一个章。
- `DEMAND-ACCEPTED` **INCONCLUSIVE 而非 FAIL**：`AcceptedDemands=0`，运行时刻 MES 里没有一条需求
  满足现场条件。MES 此刻装着什么不是候选的属性。第二轮快照见过 43 条 `WIRE_TO_GATE`、同样逐条
  按名拒绝；票 14 那次恰好碰上一条合格的。硬凑成绿就得**造一条需求**。

另外三条 INCONCLUSIVE 沿用票 14 的具名外部资格：`MOVEMENT-CLOSED-LOOP`（票 10，建单闸门关闭且无
逐次安全 GO；`SAFETY-NO-CREATE` 的 `RiotDispatchAuditEvents=0` 是「本轮没动车」的正面证据）、
`HW-ONBOARD-TARGET`、`HW-REAL-IO`（仅模拟器）。

### 5. 红侧：检测器抽成模块，红侧改的是同一份代码

`Ticket09Detectors.psm1` 收了两个 harness 依赖的全部检测器，红侧脚本 `Import-Module` 的是**同一个
模块**而不是复刻。七个检测器各在未改输入上绿、在**单字段**变异上红：指纹集合换一张（计数不变，
计数式检测器看不见）、配置加一个 `requireHttps`、车载端配置加一个 `useTls`、目录多一个 `.pfx`、
文件多一个字节、候选文件翻一个字节、服务 PID 加一。

### 6. 红侧当场抓到的两个检测器缺陷，以及第一轮抓到的三个

红侧第一次执行 7 条里红了 2 条，都是本 map Notes 已有那一族的新变体：

1. `@(<空管道>.FullName)` 是 `@($null)`，`Count` 为 **1**——`Get-KeyMaterialFiles` 在无命中时报出
   一条无名发现。修法是让投影留在管道里（`| ForEach-Object { $_.FullName }`）。
2. `$list.Add('{0}…{4}' -f $a, $b, $c, $d, $e)`——**方法调用参数表里的逗号绑给调用而不是 `-f`**，
   格式化只拿到一个参数、在 `{1}` 上抛异常，`Add` 从未执行，于是 `Compare-StoreDigests`
   **永远报不出差异**。修法是先把字符串算进变量。

验收第一轮 5 红里另有 3 条也是 harness 缺陷（红证据保留在 `round1-harness-defects/`）：密钥材料扫描
指向了整个 run root 因而扫到 harness 自己种的对照 `.pfx`；`@(@(Select-String …).Matches).Count`
——同一个 `@($null)` 坑的第三次——在零 `REPLACE_` 残留的文件上报出 1，是**假红**；`Add-Type -Path`
指向安装根锁住了 `e_sqlite3.dll`，导致收尾卸载删不掉刚清空的目录。剩下 2 条是 MesIngest 缺前置。

### 7. 前置与环境

第一轮时 MesIngest 服务是 Stopped、另有一个不持端口的 `MesIngest.Host.exe` 残留，服务端**按设计
fail-closed**：`MesIngest catalog polling failed closed; no journey was accepted.`。用户 2026-09-01
授权清掉残留进程并启动服务，`preconditions/mesingest-precondition.json` 记了前后状态与一次**看返回
body**的 contract 探测（本机全局代理会让裸 connect 对不存在的主机也成功）。MesIngest 现仍在运行
（启动类型本就是 Auto）。

车载端仓写入仍为零：用的是候选里打好的车载端包，身份取自 `release-manifest.json`。
