# ControlServer 实施交接

## 建设职责

ControlServer 负责业务状态机、持久化 inbox／outbox、MesIngest 只读边界、确定性选择、RIoT 移动与对账、发往 OnboardHmi 的投影、业务审计、Fake Onboard 对端，以及跨仓库 G3 验收索引。

## 必须交付的工作包

| 切片 | ControlServer 交付内容 |
| --- | --- |
| W2G-IS-00 | 精确 release／session 隔离；五步恢复；能力／安全／结果对账；只有唯一一致后才能 READY。 |
| W2G-IS-01 | 目录发现与最终重读；硬准入与稳定排序；AcceptedDemandSnapshot 原子受理与去重；`TO_PICKUP` intent／outbox；Fake RIoT 对账。 |
| W2G-IS-02 | 到站门禁；Sublot 最终校验；容量计算；预留／Guard／命令原子建立；LoadBatch／纠错／取消提交。 |
| W2G-IS-03 | 新鲜的 PreDepartureSafetyCheck；`TO_GATE` intent；保持／继续／未知订单对账；关卡精确到站。 |
| W2G-IS-04 | 自动完整卸货；消费逐仓物理证据；本地成功与 TransportDemandCompletion 原子提交；证明不依赖 PDA／MES。 |
| W2G-IS-05 | 断联状态、禁止新命令的收敛措施、RecoveryHandshake 授权及进入需要恢复的路由。 |
| W2G-IS-06 | 持久 inbox／outbox、请求首个结果重放、业务键内容冲突、RIoT 与 OperationResult 未知结果对账。 |
| W2G-IS-07 | 每个持久边界的崩溃检查点；ExceptionRecoverySession 业务决策；人工充电保持／复投运；不得产生重复副作用。 |

## 持久化不变量

必须为以下对象持久化明确身份与唯一约束：DemandId、TransportDemandKey 完成／抑制事实、AGV 活动执行、MovementLegId／DispatchGeneration／upperId、OperationSession、StationOperationGuard、SublotReservation、SlotOperationAttemptId／内容哈希、全部协议 MessageId、请求首个结果、带修订的投影、恢复动作／会话，以及 ForcedRecoveryGeneration。未知外部结果必须保留原绑定；重启后不得仅依据内存阶段推进业务状态。

正常完成必须在一个事务中写入 UnloadBatch、StopClosureCommit、Demand 成功和 TransportDemandCompletion。取消、补偿与交接分别使用各自已批准的终态和抑制语义。MesIngest 始终保持只读。

## 适配器边界

- MesIngest：消费完整当前目录和精确 HistoryEpoch；无条件执行最终重读；绝不写入、隐藏或篡改来源事实。
- RIoT：只有 ControlServer 可以调用。先持久化 OrderIntent，使用稳定 upperId，独立查询结果，绝不依据单一遥测字段推断到站或停止。
- OnboardHmi：只发送业务级命令。绝不传输原始 IO 映射，也不得覆盖车载端的安全拒绝。

## Fake Onboard 与测试

本仓库必须维护带完整 FakePeerIdentity 的 Fake Onboard。它消费固定的共享向量，只能模拟协议可观察的车载事实、确定性时间、断联／崩溃／重启及脚本化物理结果。它不能声称真实 IO 或 HMI 已验证。

仓库必须提供具有以下语义接口的非交互命令；具体脚本语言可以遵循仓库技术栈：

```text
test-wire-to-gate --gate G2 --slice <W2G-IS-00..07|affected> \
  --protocol-manifest <immutable-path> --output <new-run-directory>
```

测试必须先校验复合 release 身份，使用虚拟时间，运行全部映射到的合法／非法／轨迹向量及服务端专属断言，并输出公共结果 Schema 和 ConformanceRunIdentity。`affected` 必须来自机器可读的影响范围选择，不能是人工跳过清单。本规划包不声称上述命令目前已经存在。

## 人工门禁与禁止捷径

G0～G2 未通过时，不得合并依赖协议的行为。没有精确构建的 G3，不得宣称切片完成。不得虚构协议批准、车辆凭证、MesIngest／RIoT 环境身份、工厂证据或生产 release。本范围内不得实施多车、其他 WorkType 或自动充电功能。
