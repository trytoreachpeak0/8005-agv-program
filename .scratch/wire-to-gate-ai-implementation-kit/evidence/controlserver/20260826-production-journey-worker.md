# 2026-08-26 ControlServer 生产 Journey Worker

## 身份与范围

- ControlServer：`ControlServer_MVP@9c0d53091618d126a8c231004b4a7560d6e8daa0`
- 协议：`protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279`
- manifest SHA-256：`a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`
- 本记录只覆盖生产 Journey Worker；没有实现或验证恢复／补偿命令与状态机，也没有启动 G3 runner。

## 实现结果

生产 `BackgroundService` 通过 Options 启动验证和 scoped DI 串联 MesIngest 完整目录轮询、确定性持久 backlog、完整静态／动态硬准入、单车租约、`JourneyIntakeCoordinator`、RIoT `TO_PICKUP`／`TO_GATE`、可靠 `OnboardJourneyPublisher` 与 SQLite journey runtime。状态只由持久事实推进：

`TO_PICKUP → 可信到站 → snapshot/worklist/Sublot → LOAD → 发车安全 → TO_GATE → 可信到站 → UNLOAD/原子完成`

可信到站同时要求精确 upperId/orderId、RIoT state 5、冻结车辆/Map/目的站、车辆 connected/enabled/IDLE/停稳/无任务占用和新鲜 Onboard 安全事实。进程重启继续原 runtime、租约、两段 movement identity、消息 ID 和操作 identity；未确认出站消息只允许在更高 session generation 下保留 messageId/payload 重新封装。旧版已有未收敛 Demand 但没有 runtime 行时拒绝猜测接管。

站点×任务类型准入按 accepted ADR 存入服务端 SQLite：具名部署以单调版本幂等导入并保留审计；同版本异内容、版本倒退、未知／重复配置均拒绝。Sublot 提交时预检，LOAD 的仓位操作、outbox 与允许决策快照在同一事务中复检并冻结版本；后续策略撤销只阻止新操作，不重解释已承诺操作。

## 验证结果

- 聚焦 Journey／准入／HTTP 边界组：32 passed，0 failed，0 skipped。
- `dotnet test .\tests\ControlServer.Tests\ControlServer.Tests.csproj -c Release`：60 passed，0 failed，0 skipped。
- `dotnet format .\ControlServer.sln --verify-no-changes --no-restore`：PASS。
- `.\scripts\build.ps1 -Configuration Release`：0 warnings，0 errors。
- 全新 SQLite 依次应用七段迁移至 `20260826093310_VersionedStationTaskAdmission`：PASS；验证数据库 SHA-256 为 `6459729875a0e2e5160d13fa4e807f0c72b2fadb7159ef5c1a7e0f5600cf5858`。
- 测试缺口验证：把 pre-departure `unknownPresent` 条件临时变异为放行时，原聚焦组曾真实存活；新增负例后同一变异被杀死并已恢复正式实现。没有残留变异。

## G2 机器证据

以下结果均为 `status=PASS`、`testExitCode=0`，绑定 ControlServer `9c0d53091618d126a8c231004b4a7560d6e8daa0` 与上述正式协议身份；目录位于产品仓库已忽略的 `artifacts/g2/`：

| Slice | tests | `gate-result.json` SHA-256 |
| --- | ---: | --- |
| W2G-IS-01 | 30/30 | `9d9957882525764b4e7b8e1f7416efeb2e2f3df8443973aeae52febbf6d779d4` |
| W2G-IS-02 | 10/10 | `d0416c78bdcc4c31be9013835ef11e0cbf3e936ef0c881d2512d21091b023f1b` |
| W2G-IS-03 | 13/13 | `ae2f1e82b282f7da911d86fece263413f47fc889015fe74801ae6f8388e4679a` |
| W2G-IS-04 | 5/5 | `96e00a186a3ef73e85e05e949cbda6969c2ef32798cdf1129c8098c5193fbcae` |
| W2G-IS-06 | 10/10 | `be9de8d300d9615ae8bebcaf9e0d1ff567ca42b16040a40447680ab1559c31c2` |

上述五条排序相对路径与文件哈希行的集合 SHA-256 为 `10062cb6e5b279477c70565e1baae37e7086e09f85778dd354a68333ccc591bb`。

## 资格边界

Worker 保持默认禁用；只有完整具名车辆/Map/站点/路线/容量/准入策略、同源新鲜 Sublot 查询以及三个外部秘密引用通过启动验证后才能启用。本轮没有使用真实凭据，没有真实 RIoT 建单或车辆动作，也没有修改 OnboardHmi 产品代码／测试。以上 Fake/本仓 G2 和迁移验证不构成完整 G3 或 Release Candidate 资格。
