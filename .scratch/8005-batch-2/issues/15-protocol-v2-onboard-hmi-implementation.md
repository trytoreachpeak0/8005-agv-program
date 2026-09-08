# 15 — 车载端实现协议 v2（`w2g/*` 分支 → PR）

**做什么：** 让车载 HMI 说 v2，与票 14 的服务端对上。身份三元组、消息面、错误码、schema
URI 段跟上批次 1 冻结的面，车载端侧的 `IntegrationSlice` trait 同步重打为 `FP-IS-NN`。

**交付形态是 PR，不是合并。** `8005-agv-onboard-hmi` 的开发工作在我方，但仓库写权限仍在
Kun Wang：只在 `w2g/*` 分支上工作，改动以 pull request 交给 `OnboardHmi_MVP`，**我们不
合并**。已有先例并跑通（PR #5，2026-09-04 同日一小时内评审合并）。

**绝不推 `OnboardHmi_MVP`，绝不 force-push，绝不动不是我们的分支或 tag。**

两件容易忘的事：

- **该仓工作树脏会中断 L2**——`Get-L2PeerPublish` 从本地仓库的一次性克隆发布两端，拒绝
  脏源。跑 L2 前先把改动提交到 `w2g/*` 分支。
- **该仓的 `CLAUDE.md` 与 `docs/` 仍是他们的文档**——改仓库怎么描述自己，与修它的代码是
  两件事，不要顺手改。

**冲突边界：** 与票 14 并行（不同仓）。两端必须对齐同一份冻结面——协议仓的 v2 候选是唯一
真相，两端各自照它实现，不互相抄。

**前置：** 批次 1 完成（协议 v2 候选生成 ＋ G1 通过）。

**2026-09-08 已满足，前置解除。**协议仓 `fp/v2-candidate`（HEAD `f6ee75d`，已推送）即 v2
候选，G1 于 2026-09-08 在协议仓 self-hosted runner 上实跑通过（run
[34212719223](https://github.com/trytoreachpeak0/8005-agv-protocol/actions/runs/34212719223)）：
`status PASS`、`failures []`、69 schema／63 消息／31 向量／16 切片。详见票 14 的前置节。

## 票 14 于 2026-09-08 完成，转交本票五件事

服务端侧已落地（见 [14-answer.md](14-answer.md)），控制端 L1 `583 passed / 0 failed / 0 skipped`。
**两端不互相抄实现，但身份的九个值必须逐字节相同**，所以下面四条是事实通报，不是抄作业。

1. **九个身份常量的值**（服务端 `ProtocolCandidateIdentity`，全部取自协议仓
   `f6ee75defe6e2d18f63f4082bee445dbb678ab1b`）：`ProtocolVersion 2`、
   `ProfileId AGV_FULL_PRODUCT`、`ReleaseVersion 1.0.0`、`Tag protocol-v1.0.0`、
   `ManifestSha256 84f984ea…`、`SchemaBundleSha256 71146c88…`、`VectorsSha256 51c5aaca…`、
   `ApprovalStatus SUPERSEDING_CANDIDATE`。
2. **`tag` 必须填 `protocol-v1.0.0`，不能留空。** 这个 tag 在协议仓**还没打**（规格 6.6 第 6
   条要两名产品负责人 attestation），但 v2 的 `$defs/ProtocolReleaseIdentity` 对 `tag` 的约束是
   `required` ＋ `minLength: 1` ＋ `^protocol-v` ＋ `additionalProperties: false`，留空会让
   `SessionHello`／`SessionAccepted`／`SessionRejected` 三条消息 schema 非法。**两端都不做运行期
   schema 校验，没有门禁会报**——「这个 tag 还没打」这件事由旁边的 `ApprovalStatus` 承担。
3. **服务端校验对端身份的四项是 `commit`／`manifestSha256`／`profileId`／`protocolVersion`**
   （`OnboardMessageProcessor.cs:556-559`），**不校验 `tag`**。别因为服务端不查就填错。
4. **身份切了不等于报文切了。** 服务端这边七处 v1 形状的 payload 是收尾双轴复审才查出来的：
   `UpcomingStopPlanSnapshot` 顶层多发 `demandId`、leg 缺 `stopPurposeCategory`／`demandId`／
   `publicStationFunction`、`legType` 发 `TO_GATE`；`CurrentStopWorklistSnapshot` 的 `stopRole`
   发 `GATE`；`VehicleBusinessStateSnapshot` 完全不发必填的 `activePurpose`。**改完身份之后 L1
   仍全绿，一条测试都没察觉。**车载端发的 O_TO_C 消息要逐条比对 v2 schema，尤其
   `CapabilitySnapshot` 新增的 `activeSlotConfigurationFingerprint`（规格 6.2，`FP-C7`）。
   本仓的 `ProtocolPayloadShapeArchitectureTests` 是可以照抄的形状。
5. **车载端 `tests/` 零处 `IntegrationSlice` trait**（票 16 实测，186 处全在控制端）。所以下面
   那条「车载端侧 trait 重打为 `FP-IS-NN`」的前提不成立，**要么改写该条验收，要么理解成「从零
   建 trait」**——这是本票开工时第一件要裁定的事。

**状态：** 2026-09-09 完成，见 [15-answer.md](15-answer.md)

- [x] 车载端三项身份全部切到 v2
      —— 实测是**三份副本**：`WireToGateProtocol.cs`、`scripts/run-w2g-g2.ps1` 的 `$expected`
      表、`ReasonCodeRegistryArchitectureTests` 的 vendor 路径。三份都切了，前两份之间由
      `ProtocolIdentityArchitectureTests.TheGateScriptExpectsTheSameIdentityAsTheAssembly` 钉住
- [x] 63 条消息、**54** 个错误码中属于车载端的那部分全部实现
      —— 落成 `ProtocolMessageSurfaceArchitectureTests`：52 条具名、11 条钉住（9 条 v2 新增排在
      批次 3～8，2 条 v1 就没实现）。**控制端那三条钉不适用车载端**，实测车载端都具名了。
      错误码 43 → 54 已同步进 `IsProtocolErrorCode`，vendor 注册表整份换成 v2
- [x] ~~车载端侧 `IntegrationSlice` trait 重打为 `FP-IS-NN`，并逐条复核测试~~
      —— **用户 2026-09-09 裁定：改写为空真，从零建 trait 归票 20。** 车载端零处 trait，
      没有东西可重打；本票只把两个门禁脚本里的 `W2G-IS-NN` 字面量改成 `FP-IS-NN`
- [x] 车载端测试全绿 —— `168 passed / 0 failed / 0 skipped`（原基线 151 ＋ 17 条新守卫）
- [x] 全部工作在 `w2g/*` 分支上，`OnboardHmi_MVP` 零推送
- [x] ~~PR 已开，标题与正文用中文，说明这次变更会作废对方全部 `ONBOARD_HMI_G2` 证据~~
      —— **前提在 2026-09-09 失效，用户当日裁定：只推长期分支，不开 PR。**
      `OnboardHmi_MVP` 已于 2026-09-09 合并 PR #19，钉到**已发布的** `protocol-v0.3.0`
      （`ProtocolVersion 3`／`WIRE_TO_GATE_MVP`）。本票钉的是**未发布的** v2 候选，PR 进去等于
      把已签发布覆盖掉，而那条提交自己写着「两端必须同版本才能出包」。做法对齐控制端：
      全产品线活在长期分支 `origin/fp/v2-impl` 上，从未 PR 进 `ControlServer_MVP`。详见
      [15-answer.md](15-answer.md) 第十三节
- [x] 该仓 `CLAUDE.md` 与 `docs/` 未被本票改动
      —— **该仓根本没有 `CLAUDE.md`**（票据这句是从别的仓抄来的）；`docs/` 与 `README.md` 零改动
- [x] 工作树干净，`w2g/*` 分支已推送，L2 可从它发布车载端
      —— `w2g/fp-v2-impl` = `f0b4e0d`，fast-forward（`641292e..f0b4e0d`），未 force-push
