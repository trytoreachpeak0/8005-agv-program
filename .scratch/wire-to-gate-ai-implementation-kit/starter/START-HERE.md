# WIRE_TO_GATE MVP 实施入口

## 本轮目标

最迟于 2026-08-28 17:00（Asia/Taipei）交付三个远程仓库共同组成的可运行 MVP Release Candidate。完成判定见 [MVP Definition of Done](definition-of-done.md)；文档、骨架、Fake、单端测试或录屏均不能单独构成交付。

## 权威顺序

发生冲突时按以下顺序停止并上报，不得自行选择较宽松解释：

1. 已接受的需求基线及 [348 行最终适用性表](../../wire-to-gate-mvp/evidence/final-requirement-applicability-profile.tsv)；
2. 根 `CONTEXT.md` 与 `docs/adr/cross/` 中 accepted ADR；
3. [MVP 范围与验收规格](../../wire-to-gate-mvp/handoff/mvp-specification.md)及已解决决策 02～12；
4. [共享协议交接](../../wire-to-gate-mvp/handoff/protocol-repository-handoff.md)、机器 Schema/manifest/错误码/向量；机器资产与解释性 Markdown 冲突时，以同一已批准 release 的机器资产为准；
5. [ControlServer 交接](../../wire-to-gate-mvp/handoff/controlserver-handoff.md)、[OnboardHmi 交接](../../wire-to-gate-mvp/handoff/onboard-handoff.md)和 [W2G-IS-00～07 索引](../../wire-to-gate-mvp/handoff/integration-slices.tsv)；
6. 本目录中的薄实施输入和仓库内实施票。

原型 A `../../wire-to-gate-mvp/prototype/onboard-single-scenario/onboard-single-scenario-prototype.html?variant=A` 是 OnboardHmi 生产布局和交互权威；原型工程、假数据和原型词汇不得成为生产依赖。

## 三个仓库

| 仓库 | 开发分支 | 负责人 | 本轮输出 |
|---|---|---|---|
| `https://github.com/trytoreachpeak0/8005-agv-control-server` | `ControlServer_MVP` | szy | 可运行服务端、持久化、MesIngest/RIoT 适配器、Fake Onboard、G2、安装物 |
| `https://github.com/trytoreachpeak0/8005-agv-onboard-hmi` | `OnboardHmi_MVP` | 王昆 | 可运行 HMI、原型 A 映射、journal、IO 模拟器、Fake ControlServer、G2、安装物 |
| `https://github.com/trytoreachpeak0/8005-agv-protocol` | 候选分支后发布不可变 tag | szy＋王昆 | Schema、manifest、错误码、样例、向量、runner、批准记录、ProtocolRelease |

产品代码不强制 PR。两个产品只能锁定同一个精确 ProtocolReleaseIdentity，不跟踪协议 `main`，不用 Git submodule，不在产品仓库平行改写协议。

## 已知实施环境

- ControlServer：Windows 11 开发电脑；技术栈由快速研究票冻结。
- OnboardHmi：Windows 10/11 虚拟工控机，1024×768、100%，鼠标，扫码结束符 Enter，普通键盘；技术栈由王昆冻结。
- IO：本轮交付八仓模拟器；真实 IO 资格不在本周范围。
- MesIngest：现有 V2，与 ControlServer 同机，包含 WIRE_TO_GATE 测试数据。
- RIoT：`http://172.19.206.222:8888`，Map `25`，车辆显示名“老厂前线新多仓位1”；CallApiKey 已准备。技术车辆 ID、取货站和关卡站必须先只读查询并由用户确认。
- 秘密不得进入仓库、聊天、发布物或证据；只通过环境变量或受 ACL 保护的部署配置注入。

## 每次开工

1. 记录当前仓库 commit、协议候选 commit/manifest hash 和 IntegrationSliceId。
2. 读取 [逐切片工作包](slice-work-packages.tsv)，只实现当前未通过切片的最小生产闭环。
3. 先增加失败测试，再实现；每个持久化、不可逆副作用和恢复点都必须可验证。
4. 本端 G2 与 Fake 对端通过后立即做候选联合运行；失败先修复，不进入依赖切片。
5. 保存不可改写 PASS/FAIL/INCONCLUSIVE 证据；任何身份或有影响配置变化都会使旧证据对新候选失效。

双方可以使用任意 AI、IDE、skill 或任务工具；AI 只能决定不改变业务、安全、协议和副作用语义的内部实现细节。

