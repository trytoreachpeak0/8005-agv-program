# OnboardHmi 实施交接

## 建设职责

OnboardHmi 负责目标车辆 UI、经过身份认证且受 session 隔离的连接、本地 IO 与硬件安全、OnboardExecutionJournal、物理执行与恢复、抽象能力／安全状态发布、可靠结果重放、Fake ControlServer 对端，以及目标硬件技术证据。

## 必须交付的工作包

| 切片 | OnboardHmi 交付内容 |
| --- | --- |
| W2G-IS-00 | 精确 release／session 握手；完整能力／安全／恢复报告；拒绝旧代次；在 READY 且投影新鲜前禁用业务动作。 |
| W2G-IS-01 | 只读显示唯一已承诺 Demand 的旅程与计划；不得从 MesIngest 发现、排序或绑定任务。 |
| W2G-IS-02 | 扫码／键盘单次提交入口；批量命令持久接受；完整有序仓位集；装货／纠错／取消 UI 与物理闭环。 |
| W2G-IS-03 | 实时 PreDepartureSafetyCheck 与可靠安全撤销；绝不调用 RIoT 或选择移动。 |
| W2G-IS-04 | 自动关卡卸货展示；批量物理执行；逐仓 EMPTY／锁闭／复位证明；不得要求第二次业务输入。 |
| W2G-IS-05 | ActiveUnlockSet 收敛与安全收尾；断联后不启动新模块组；只依据 journal 与实时 IO 完成重连／重启恢复。 |
| W2G-IS-06 | 消息／请求／结果去重及稳定冲突响应；重放不得重复执行仓门动作。 |
| W2G-IS-07 | 在 journal 检查点崩溃恢复；四条固定恢复路径；ForcedRecoveryGeneration 隔离；人工充电复投运请求及不可修改的技术证据。 |

## 物理不变量

- 物理仓位 1～8 的身份稳定，每个仓位最多一个花篮。仓位不得因配置或硬件不可用而从模型中消失。
- 实时 SlotPhysicalState 始终是车载端权威。锁反馈、光幕有效性／占用、输出复位和 IO 在线状态必须逐仓计算。UNKNOWN 必须阻断。
- 在不可逆输出前，必须持久化完整命令和 PREPARED 检查点。相同 SlotOperationAttemptId／相同内容返回已保存状态或结果；相同 ID／不同内容必须拒绝且不得操作 IO。
- 批量开锁遵循已配置的模块分组。断联时，ActiveUnlockSet 只能包含已发送或发送结果未知的组；尚未发送的组保持关闭。
- 装货以 OCCUPIED 闭环；卸货／取消／补偿以 EMPTY 闭环；全部都要求锁闭且开锁输出已复位。已知但相反的占用状态继续执行相同目标闭环；UNKNOWN 进入恢复。
- 重启后必须重读实时 IO，历史观测不得覆盖实时事实。只有结果和下一步都能唯一解释时才允许继续。

## UI 映射

以 A 方案“旅程导引台”作为结构权威，而不是仅作为截图主题。必须制作并评审 prototype-to-production 映射，覆盖窗口层级、固定三区布局、尺寸／间距、控件、四个状态维度、八仓状态、旅程步骤、扫码／键盘焦点，以及每个允许／禁用／恢复动作。不得把原型假数据或原型专用词汇带入生产。

真实车载端开发者必须本人确认此映射及其可实现性。P6 前，必须在实际目标硬件上，以真实分辨率、缩放、触摸、扫码枪、键盘及代表性的观看距离／光照进行验证。如适用，Golden WPF tier 2/3 仍须用户另行批准。

## Fake ControlServer 与测试

本仓库必须维护带完整 FakePeerIdentity 的 Fake ControlServer。它消费固定的共享 release，只模拟协议可观察的服务端状态、精确投影／命令、确定性故障脚本和首个结果重放。它不得成为第二个任务引擎，也不能声称 MesIngest／RIoT 正确性已经验证。

必须提供具有相同语义接口的非交互命令：

```text
test-wire-to-gate --gate G2 --slice <W2G-IS-00..07|affected> \
  --protocol-manifest <immutable-path> --output <new-run-directory>
```

该命令先以真实 OnboardHmi 逻辑对接 Fake ControlServer，再把 Fake ControlServer 作为被测组件，输出共享结果 Schema 和 ConformanceRunIdentity；判定不得依赖墙钟 sleep 或随机调度。本交接包不声称当前已有可执行命令。

## 人工门禁与禁止捷径

不得仅凭 tag 名、分支或 ProtocolVersion 接受 release。不得把离线缓存投影作为新动作权威。不得新增第二套 UI 架构、把原始 IO 字段放进协议、调用 RIoT、选择任务、提供“人工安全／空仓／完成”覆盖，或执行未批准的恢复动作。Fake／G2 证据不能替代目标硬件或 G3 证据。
