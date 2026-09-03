# 一次冻结协议 v2 消息面、错误码与向量范围

Type: grilling
Status: open
Blocked by: 03, 04, 05, 12, 13

## Question

以票 03～05 输出的「必须由协议承载的业务能力」清单为输入，一次性冻结 `8005-agv-protocol` v2 的完整设计面。

这一票必须一次做完。逐条加需求逐次发 release 会反复作废两端已有的 G2 证据——协议是 Kun Wang 那侧构建的契约，一次补丁发布同时作废两端受影响的 G1/G2/G3 证据。当前状态是 `ProtocolVersion` 1、`WireToGateMvpProtocolProfile` allowlist、明文期、两端无协商无降级。

须回答：

1. **消息面**：v2 的完整 `messageType` allowlist。哪些 v1 消息沿用、哪些扩展字段、哪些新增、哪些废弃。多车并发、Worklist 选任务入口、自动充电周期、充电失败与清桩、治理面（若票 05 判定需要）各自需要哪些消息。
2. **错误码与交付类别**：v2 的完整错误码表，以及每个消息的交付类别归属。MVP 用的是五类交付 + 通用 ACK + 业务幂等 + 五步恢复对账，v2 是沿用这套还是需要扩展。
3. **测试向量范围**：v2 的一致性测试向量覆盖哪些场景，`vectorId` 命名与编号规则，以及向量与切片（票 07）的绑定方式。合法与非法消息样例的覆盖标准是什么。
4. **v1 与 v2 的版本关系**：并存、替换还是版本协商。当前明文期两端无协商无降级、版本错配的表现是连接被拒而不是一条说明原因的错误——v2 是否引入协商能力，若不引入，两端升级的切换方式是什么（同时替换？CD 的 WIRE_TO_GATE 两端打进一个包这一现有约束在 v2 下是否仍然成立）。
5. **冻结的强度**：本票的产出是「v2 设计面已冻结、可据以实施」还是「v2 已可发布」。二者的区别在于是否需要写出 Schema、样例与向量文件本身——那属于实施，不属于本图。本票须明确交付物的边界，以及实施图拿到本票产出后还需补什么才能切一个 `ProtocolRelease`。
6. **发布与通知**：v2 的正式 release 仍受 `docs/release-governance.md` 约束，须两名产品负责人签名，AI 与 CI 不能批准。本票须写明：本图不产生 release，本票的结论推送后按 notify-after-change 规则开 issue @`SocialKKKK`，说明改了什么、触及哪些 `W2G-IS-*` 切片、以及他的 `ONBOARD_HMI_G2` 证据是否作废。

### 票 03 定下的协议清单（本票的输入，不要重新推导）

[票 03 决议](03-answer.md)输出了 B3 与 B5 必须由协议承载的能力，并**纠正了票 02 的两处判断**。

`UpcomingStopPlanSnapshot`：

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 1 | `legs.maxItems` 2 → **9** | `schemas/messages/UpcomingStopPlanSnapshot.schema.json:116` |
| 2 | `sequence.maximum` 2 → **9** | 同文件 `:82-86` |
| 3 | **顶层 `demandId`（单数）语义失效**，须下移到每个 leg 或去掉 | 同文件 payload 顶层 |
| 4 | `businessDedupKeys` 由 `["demandId"]` 变更（dedup 键变更是 breaking） | `manifest/release.json:234-248` |

`CurrentStopWorklistSnapshot`：

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 5 | `items.maxItems` 1 → **8** | `schemas/messages/CurrentStopWorklistSnapshot.schema.json:115` |
| 6 | 顶层 `operationSessionId` **下移到 `items[]`** | 同文件 payload 顶层 |
| 7 | `workType` 的 `const` 由 `WIRE_TO_GATE` **解除为六类 enum** | 同文件 `:87-91`；来自票 13 |

B5 新增：

| # | 改动 |
| --- | --- |
| 8 | 新增车载 → 服务端的选任务请求消息，载 `demandId` + `worklistRevision` + **五字段回显**（完整 SUBLOT、任务类型、起点、终点、`ExpectedBasketCount`） |
| 9 | 新增服务端裁决消息（接受或拒绝 + 拒绝原因码） |
| 10 | `W2G-IS-01` 的 `ownerResponsibilities.onboardHmi` 里 `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` **字面必须改** |
| 11 | 向量 `CV-DEMAND-ACCEPT-TO-PICKUP` 的 `forbiddenSideEffects` 里 `onboard-demand-selection` 须改 |

上限 9 与 8 的推导：一车至多 8 个仓位（`SlotNo` 的 `maximum: 8`，
`schemas/common/types.schema.json:55`），一个 Demand 至少占 1 个花篮，故至多 8 个待装条目、
8 个取货停靠加 1 个关卡停靠。

**票 02 的两处判断已被纠正，本票不要照旧执行：**

1. **`legType` 的 enum 不因 B3 而改。**档 2 下每一段仍是「去某个取货点」或「去关卡」。
   给它加值的是**票 12（等待点）与票 04（充电）**，两票不要与本节相互推诿。
2. **`stopRole` 的 enum 不因 B3 而改**，理由同上。

**B2 不进协议 v2**（票 02 已定，票 03 复核确认）：信封的 `agvId` 必填且**无 `const`、`enum`、
`pattern`**，对 54 条消息 schema 逐个筛查这三个关键字**零命中**，从未限制车辆总数为 1，
三车三会话即可。

### 一条本票必须先知道的工程量事实

**54 条消息 schema 各自内联复制了一份信封，没有任何一条 `$ref` 引用 `envelope.schema.json`**
（对 `schemas/messages/` 的 grep 零命中），且各自按需收紧（两个快照消息把 `correlationId`
收成 `"type": "null"`、`sessionGeneration` 去掉 null 分支、`messageType` 加 `const`）。
**本票若要动信封，等于改 54 个文件。**`profileId` 当前 `const` 为 `WIRE_TO_GATE_MVP`，
完整产品是否随之改名同样牵动这 54 份副本。

另：`CurrentStopWorklistSnapshot` 的 `items` 当前**没有 `minItems`**，只有 `maxItems: 1`，
空数组本来就合法——多 Demand 化不需要为「空清单」另做处理。

### 已知边界

- 本票不写 Schema、样例或向量文件，不改 `8005-agv-protocol` 仓库内容，不打 tag，不切 release。
- 本票不代 Kun Wang 批准跨端契约。单人批准的是本图的设计决定；正式 release 的双人签名门禁不变。
- 本票不决定批次归属与顺序，那是票 09；不决定切片编号，那是票 07。
- 冻结范围以票 03～05 的业务决定为准。若发现某项业务能力在票 03～05 中未决定而协议无法冻结，应回到对应票补齐，不在本票替它做业务决定。
