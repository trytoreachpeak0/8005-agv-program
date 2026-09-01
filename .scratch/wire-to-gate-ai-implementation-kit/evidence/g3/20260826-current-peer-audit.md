# 2026-08-26 当前双端提交联合审计

## 绑定身份

- ControlServer：`ControlServer_MVP@3ceeee6dd243015b3f5fb94e9fea1d144dc4babf`，已推送远程。
- OnboardHmi：王昆本人提交 `OnboardHmi_MVP@045514770da9858a8a49196dede276192e4f2a1b`。
- slots-simulator：王昆本人提交 `main@fb5f7c593742bf98bc3957b8729a38aad5321f28`。
- 协议：`protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279`；manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`。
- GitHub Release 的外部批准证明重新下载 SHA-256 为 `89f67c82bb0741fb3959d314a6ae0130690fa16c96f9acceaac0f691b01390cb`，内容含 `trytoreachpeak0` 与 `SocialKKKK` 对上述精确 commit/manifest 的本人批准。

## 本地门禁

- OnboardHmi 在 `core.autocrlf=false` 的干净验证 clone 中完成协议 G1、Release build、全部测试、format、W2G/Legacy 边界审计和 UI 静态布局审计：全部 PASS；Unit `62/62`、W2G G2 `13/13`、0 skip。`summary.json` SHA-256 为 `ebec97487a39db9150d8f546a77c8cc23e3ab46fedcf9275caad61867cde154a`。
- slots-simulator 核心 `18/18`、HTTP/Modbus 自动化 `14/14` PASS。
- ControlServer Release 非增量构建 0 warning / 0 error，完整测试 `18/18`、0 skip，format PASS；W2G-IS-00～07 八份 G2 全部 PASS。八份 `gate-result.json` 的排序路径/文件哈希集合 SHA-256 为 `6e80f9e9599a922b8e1e4329a2cf8a6e4008f7f20b15c28b8237b6b91ca42c24`。
- OnboardHmi 仓库的一键入口 `scripts/run-local-validation.ps1 -ProtocolRoot ... -SimulatorRoot ...` 会把参数名误传为位置参数；默认 Windows CRLF checkout 还会让 format 门禁报大量换行错误。本轮未修改王昆仓库，而是按其清单逐项执行并在无 CRLF 转换的干净 clone 中取得上述绿色证据。

## 真实双进程 smoke 与修复

使用真实 ControlServer Host、真实 OnboardHmi WPF 进程和独立 slots-simulator，绑定上述精确版本，在 loopback 非 TLS 开发配置中执行恢复 smoke；未下发业务动作，未连接或模拟 RIoT。

首次运行发现两项 ControlServer 跨仓偏差：

1. ControlServer 对收到的 JSON 先排序属性再计算确认哈希，OnboardHmi 则对实际持久化和发送的 UTF-8 wire line 计算哈希，导致 `CONTENT_HASH_MISMATCH`；
2. ControlServer 对 Safety 快照返回 `snapshotKind=SAFETY`，正式 Schema 和 OnboardHmi 要求 `SAFETY_STATE`。

两项均已在 ControlServer 提交 `3ceeee6dd243015b3f5fb94e9fea1d144dc4babf` 修复并推送；回归测试 `SnapshotAppliedAcksUseExactWireContentHashAndProtocolKinds` 同时锁定精确 wire hash、原 snapshot messageId、`CAPABILITY` 和 `SAFETY_STATE`。

修复后的真实双进程结果：

- OnboardHmi 成功连接 IO simulator；
- 双方完成正式 release 身份接受、Capability、Safety、RecoveryStateReport 和 SessionReadiness；
- OnboardHmi 日志记录 `上层会话已建立：generation=1，readiness=RecoveryRequired`；
- ControlServer 持久状态为 `CapabilityRevision=1`、`SafetyRevision=1`、`RecoveryReportId` 非空、`Readiness=RecoveryRequired`、`ReasonCode=DEPARTURE_SAFETY_NOT_READY`；
- 1502、58005、58006、58007 均在测试后回收。

该 `RecoveryRequired` 是正确的 fail-closed 结果：当前 OnboardHmi 生产组合根使用 `UnavailableVehicleSafetySignalProvider`，未接入真实停稳/驻车信号时固定报告 UNKNOWN。不得通过测试注入或伪信号把它改写成 READY/G3 PASS。

## 仍阻断正式 G3

- 王昆需在 OnboardHmi 提供并本人确认真实车辆停稳/驻车信号 provider 与目标接线/时效配置；AI 仍无权修改车载产品代码。
- ControlServer 生产 `OnboardMessageProcessor` / `OnboardTcpServer` 仍只覆盖恢复握手和 Heartbeat 的请求—响应；Demand/worklist/旅程、Sublot、SlotOperation、DurableAck/result reconciliation 和异常恢复命令尚未形成真实双向业务分发闭环。
- 当前没有可用的 MesIngest `58004` 服务与 shared secret，也没有 RIoT call API key、具名 `vehicleKey`/生命周期、`mapId`、机台和关卡 `stationId`；路线图禁止用 RIoT 模拟器或猜测身份代替。
- 因此 W2G-IS-00～07 G3 继续为 `INCONCLUSIVE`，本证据只能证明两端本地 G2 和真实恢复 smoke 的收口进展。
