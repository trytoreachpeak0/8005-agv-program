# 会话交接：2026-08-30 票 14 可用 MVP 验收

给下一个 wayfinder 会话。**决策与结论一律以 [map.md](../map.md) 和票据为准，本文件只写地图里没有的
机器状态与待办动作。**

## 怎么接上

```
/mattpocock-skills:wayfinder .scratch/wire-to-gate-ai-implementation-kit/map.md
```

前沿两张票，都未认领：

- [审阅可运行 MVP 候选并授权正式发布](../issues/12-review-the-local-kit-and-authorize-remote-publication.md)
  ——四个阻断（14／17／21／22）已全解，可以直接开跑；
- [处置生产形态下车载端 HMI 不反映 WIRE_TO_GATE 且无恢复出口](../issues/27-route-the-onboard-production-shape-hmi-defect.md)
  ——HITL，等用户指定处置方向后才动。

[发布并交接可运行 WIRE_TO_GATE MVP](../issues/15-complete-candidate-based-ai-development-start-handoff.md)
仍被票 12 阻断。

## 三仓提交位置

| 仓 | 分支 | 提交 | 状态 |
| --- | --- | --- | --- |
| `8005---AGV`（本仓，规划） | `codex/continue-wayfinder-map` | `3d2555dd` | 已推送，干净 |
| `8005-agv-control-server` | `ControlServer_MVP` | `9daeef4` | 已推送，干净 |
| `8005-agv-onboard-hmi` | — | `bbfbc52` | **只读，本会话零改动** |

本会话在服务端仓新增两个证据目录：`evidence/g3/20260830-issue14-usable-mvp-acceptance/`（干净安装
验收 + 红侧变异）与 `evidence/g3/20260830-issue14-field-closed-loop/`（四次现场运行 + 启停观测
脚本）。

## 等用户做的两件事

1. **卸掉隔离服务。** 用户以管理员装了 `8005 AGV ControlServer Ticket14`（InstallRoot
   `C:\Program Files\8005 AGV\ControlServer-Ticket14`，DataRoot
   `C:\ProgramData\8005\ControlServer-Ticket14`，端口 58505／58507），**目前仍在 Running**。
   卸载命令已给出，用户尚未回报结果。卸载脚本需要 `-ConfirmUninstall`，不加 `-RemoveDataRoot`
   即保留数据根。生产服务 `8005 AGV ControlServer`（58005／58007）全程未动。
2. **决定车载端 HMI 缺陷的去向。** 转交件在
   `C:\Users\szy\Desktop\致王昆20260830车载端生产形态HMI缺陷.md`（仓外，按跨仓路由规则不写进任何
   仓库）。票 27 等这个决定。

## 本机陷阱（会伪造绿）

- **Clash 全局模式会劫持到真实 RIoT 的连接。** 本会话开局就撞上：安全投影恒
  `UNKNOWN / RIOT_READ_TIMEOUT`，而 ICMP 8/8 通、TCP connect 对 8899／9／12345／65001 乃至根本
  不存在的 `172.19.206.99` 全部「成功」。用户切回规则模式即恢复。判定 RIoT 可达**只能**用返回
  body 的 HTTP 往返。已写进 map 的 Notes 与 `riot-path-red.json`。
- **`vEthernet (Default Switch)` 占着 `172.19.192.1/20`**，该网段包含现场 RIoT 地址
  `172.19.206.222`。Clash 正常时不影响，但它是第二层隐患。
- **车载端 `environment=Production` 拒绝回环地址**（`IsForbiddenProductionHost` 同时管
  `wireToGate.host` 与 `vehicleSafety.endpoint`）。同机验收必须绑一个非回环本地接口；本会话用
  `192.168.200.1`（vEthernet (Huawei)，主机内部交换机，不暴露到公司网）。配错的表现是车载端弹
  「软件无法启动，请联系维护人员检查程序配置」**且不产生任何日志目录**——`OnboardSettings.Load`
  在 logger 构造之前就抛。

## 现场跑闭环怎么跑

脚本在服务端仓 `evidence/g3/20260830-issue14-field-closed-loop/`：

- `Start-Ticket14FieldRun.ps1` —— 分离启动三个进程后立即返回，观察窗口由现场决定；必须显式给
  `-ConfirmRealVehicleMovement`、`-OperatorId`、`-DispatchGeneration`；
- `Watch-Ticket14FieldRun.ps1` —— 只读快照，不碰活库；
- `Stop-Ticket14FieldRun.ps1` —— 收尾、移除临时根证书、把终态读成 `run-result.json`；
- `Invoke-SimulatorLoadAssist.ps1` —— 替代操作员在仓门前放货／取货并关门。

**`dispatchGeneration` 1～7 已在 RIoT 用掉**，下次现场运行必须从 8 起，否则 `upperId` 撞上已有
终态订单而不建新单。

装卸的硬约束：`workflow.operationTimeoutMs` 只有 120 秒，模拟器 `maxOpenDoors=1` 一次只开一个仓，
所以多筐订单的全部开门-放货-关门必须挤在这 120 秒里。助手当前版本是「开门时只决定一次目标状态、
之后只重试关门」，gen7 的日志证明它能扛住连续三次响应解析失败。**不要**改回按当前货物状态每轮
重新推断意图，那正是 gen6 把 2 号仓关成 `EMPTY` 的原因。

子批录入仍需真人在 HMI 上操作，agent 替不了；`Watch` 到 `AwaitingSublot` 时从
`JourneyBacklog.TransportDemandKey` 取子批号、从 `JourneyRuntimes` 取
`ExpectedBasketCount`／`TargetSlotsJson` 报给用户。

## 桌面上的运行目录（是证据，别顺手删）

`w2g-ticket14-run2`（干净安装验收）、`w2g-ticket14-red`（红侧变异）、
`w2g-ticket14-field-gen4`～`gen7`（四次现场运行）、`w2g-ticket14-install`（安装结果 JSON 与诊断
日志）。关键文件已抄进服务端仓的证据目录并推送，桌面副本可在用户同意后清理。

发布候选本体：`C:\Users\szy\Desktop\w2g-rc-20260830-81cb9cf`（+ 一次性车载端克隆
`-onboard-src`）。票 25 那份 `w2g-rc-20260830-d243abf` 仍在，未删。
