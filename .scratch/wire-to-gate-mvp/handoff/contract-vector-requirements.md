# 契约测试向量要求

## 运行器契约

每个语言无关向量都必须声明：规范化输入与输出、有序步骤、虚拟单调时间、初始持久事实、确定性故障动作、预期消息、持久化检查点、禁止副作用、最终状态，以及在预期失败时恰好一个稳定错误码。允许的动作包括 `advance`、`drop`、`delay`、`duplicate`、`disconnect`、`reconnect`、`crash`、`restart` 和脚本化的外部适配器结果。判定不得依赖墙钟等待、线程调度或未记录的随机性。

运行前必须重新计算完整的 ProtocolReleaseIdentity 和向量集哈希。身份缺失或不匹配时判定为 FAIL。规范化只能移除运行器契约明确声明为非语义的字段；不得移除 MessageId、业务键、修订号、哈希、顺序、错误、检查点或虚拟时间步骤。

## 每种消息的覆盖要求

- 每个允许的 messageType 至少提供一个完整合法 envelope：`V-<messageType>-MIN-001`。
- 每条 required、类型、枚举、可空性、唯一性、排序、关联和跨字段规则，均提供一个只破坏该约束的最小非法向量：`I-<messageType>-<constraint>-NNN`，并声明一个预期错误码和 JSON Pointer。
- 每个历史或禁用名称均提供一个禁止剖面向量；未知 messageType、错误 ProtocolVersion、过期 sessionGeneration，以及 release／哈希不匹配必须分别提供向量。
- 秘密字段只能使用明确无效的占位值，绝不能包含可用秘密。

## 必须覆盖的轨迹

`CV-SESSION-RECOVERY-HAPPY`、`CV-SESSION-RECONNECT-DURING-RECOVERY`、`CV-RELIABLE-RETRY-SAME-CONTENT`、`CV-RELIABLE-RETRY-DIFFERENT-CONTENT`、`CV-REQUEST-FIRST-RESULT-REPLAY`、`CV-SNAPSHOT-REPLACE-AND-ACK`、`CV-SNAPSHOT-SAME-REVISION-CONFLICT`、`CV-PICKUP-SUBLOT-LOAD`、`CV-LOAD-CORRECTION`、`CV-LOAD-CANCELLATION-ALL-EMPTY`、`CV-PREDEPARTURE-SAFETY-EXPIRES`、`CV-GATE-UNLOAD-ALL-EMPTY`、`CV-CONNECTION-LOSS-SAFE-FINISH`、`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`、`CV-EXCEPTION-RESUME`、`CV-EXCEPTION-COMPENSATE`、`CV-FAULT-CARGO-HANDOFF`、`CV-FORCED-MECHANICAL-RECOVERY`、`CV-MANUAL-CHARGING-RETURN`。

每条轨迹都必须固定逐步消息、持久事实、明确禁止的副作用、最终 readiness／业务／物理状态及稳定错误码。[联调切片索引](integration-slices.tsv)给出机器可消费的最小映射；每个切片还必须运行所有相关的合法与非法消息向量。

## 结果与证据

每次运行都必须产生不可修改的 ConformanceRunIdentity，其中包含：runId、切片、运行类型、适用时两端产品的完整 commit／build digest、复合协议身份、两个适用的 FakePeerIdentity、runner／harness 身份、向量集及其哈希、虚拟时间脚本哈希、不含秘密的环境／配置摘要、时间戳，以及 `PASS|FAIL|INCONCLUSIVE`。

每个向量必须比较：envelope／payload／方向／关联／错误；交付、去重、修订与持久化；消息顺序及消息缺失；发送、ACK、不可逆动作和结果重放前的持久化；禁止的 RIoT／业务／开锁／READY／重复副作用；以及最终车辆 readiness、Demand、移动、业务仓位和可证明物理状态。

FAIL／INCONCLUSIVE 证据不可修改，必须包含首个分歧步骤、规范化后的预期／实际差异、稳定错误码、日志／审计指针、持久事实哈希、禁止副作用断言和修复运行的 runId。重跑不得覆盖红色证据。
