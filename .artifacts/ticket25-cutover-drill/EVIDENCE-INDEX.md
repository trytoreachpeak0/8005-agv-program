# Ticket 25 — 空库切换与整体回退演练证据

**结论：PASSED**（2026-08-20 00:01:05 +08:00）

`TICKET25_CUTOVER_DRILL_PASSED`

覆盖票 25 第 4、5、6 条。演练在一次性数据库 `192.168.200.1 / MesIngest_Ticket25_Cutover`
上进行，由操作员 `LAB-WIN-01\szy` 在控制台**两次原样键入目标身份**
`LAB-WIN-01\MSSQLSERVER/MesIngest_Ticket25_Cutover` 后才执行删除与恢复。

## 两端都是真实部署，没有替身

| 端 | 来源 |
| --- | --- |
| 旧部署 | 票 13 发布包 `mes/ingest/csharp/.artifacts/ticket13-release/clean-install/MesIngest`（自带 `openapi/v1.json`），由它自己建出退役 schema 并写入真实业务行 |
| 新部署 | 票 25 打包门禁产出的发布包 `run-20260819-225413` 的 `MesIngest-win-x64.zip` |

## 逐项实测

| 步 | 检查 | 实测 |
| --- | --- | --- |
| 1 | 旧部署建立可信的退役现场 | `dbo` 下 5 张退役表，`TransportDemands` 2 行 |
| 2 | **新程序不读旧库** | 新 Host 拒绝启动，`exitCode=-532462766`，且 stderr 核对确为 schema 契约拒绝 |
| 3 | 备份、校验、记录哈希 | `RESTORE VERIFYONLY ... WITH CHECKSUM` 通过，SHA-256 `ee2456f3fa35494e…` |
| 3 | 人工确认后才删除 | `userTablesBefore=6 → userTablesAfter=0` |
| 4 | 新 Host 自建空 schema 并提交首个完整 SUCCESS | `schemaVersion=17`，`projectionCommits=2` |
| 5 | **错误当前条件用 bootstrap 起因** | `errorPeriods=1`，其中 `BOOTSTRAPPED_CURRENT_CONDITION` 1 条 |
| 5 | **不伪造更早的开始时间** | 早于本次演练起点的错误期间 `0` 条 |
| 5 | **旧记录不进新库** | 退役表 `0` 张，`dbo` 用户表总数 `0` |
| 6 | 冻结二进制被误用时的真实行为 | **记录而非断言**：旧 Host 不拒绝，反而新建 6 张 `dbo` 表并保持运行 |
| 7 | 人工确认后由独立备份恢复 | `userTablesAfterRestore=6`，`currentSchemaPresent=false` |
| 8 | **整套旧部署恢复** | 退役表 5 张、`TransportDemands` 2 行与切换前一致；`mesingest` schema 不存在；旧 Host 重新跑起来 |

`mixedModeSupported: false`：演练全程不存在新旧同时服务同一数据库的状态。

## 第 6 条的准确结论

隔离的两个方向强度**不同**，演练把这一点测了出来：

- **新程序不读旧库 —— 由代码强制。** 新 Host 校验 schema 契约后拒绝启动。
- **旧程序不读新库 —— 只能由流程保证。** 退役二进制是冻结的（本票删除的是它的源码，改不了它的行为），它不认识 `mesingest` schema，指向新库时不会拒绝，而是在旁边建自己的 `dbo` 表并正常服务。

因此这一方向的保证来自部署纪律：切换完成后卸载旧程序；回退时旧程序只指向由独立备份恢复出来的旧库。`pack/UPGRADE.md` 已按此改写（提交 `9a2f5a7`），原文把两个方向都写成有代码兜底，是不准确的。

## 演练过程中修复的缺陷

演练本身发现了 3 个真问题，均已修复并提交：

1. **`Open-CutoverConnection` 连不上任何数据库**（提交 `d5bb14a`）。
   `SqlConnectionStringBuilder` 是 `IDictionary`，PowerShell 把 `$builder.InitialCatalog`
   绑到关键字索引器而非 CLR 属性，而合法关键字是带空格的 `Initial Catalog`，于是抛
   `Keyword not supported`。**这个切换脚本此前从未成功连接过**。补了一条跑真脚本的守卫：
   把 `Open-CutoverConnection` 指向拒绝连接的地址，要求失败在网络层——只有连接串先解析成功
   才会走到那一步；把修复撤掉该测试立刻变红。
2. **破坏性确认被花在了一个无法执行的操作上**（提交 `06acb23`）。
   首次真跑时操作员键入了确认，随后备份因 SQL Server 主机上没有该目录而失败。备份是非破坏性的，
   现已移到确认之前，那次确认从此只授权 DROP；这也正是票 25 第 4 条的原文顺序。
   （曾尝试用 `xp_fileexist` 做路径预检查并**撤回**：非 sysadmin 登录下它对存在的目录返回全 0，
   会把合法切换误判为路径不存在。会误报的守卫比没有更糟。）
3. **runbook 夸大了隔离保证**（提交 `9a2f5a7`），见上一节。

另有两个只影响演练脚本自身的缺陷（不在产品内）：断言按表名过滤未限定 schema，把新契约的
`mesingest.TransportDemands` 误判为退役表；以及进程输出读取先后顺序不当，先 `ReadToEnd()`
会挂在不退出的 Host 上、先 `WaitForExit()` 又会因管道写满而死锁——改为异步抽干后两种分支都已自测通过。

## 清理

演练用的一次性资产可以随时删除，与任何生产对象无关：

- 数据库 `MesIngest_Ticket25_Cutover`（当前是回退后的旧部署状态）
- 数据库 `MesIngest_Ticket25_Smoke`（打包门禁用）
- 备份文件 `C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup\MesIngest_Ticket25_pre_cutover.bak`
