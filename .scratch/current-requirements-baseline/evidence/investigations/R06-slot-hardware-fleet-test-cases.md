# R06 仓位、硬件、车队及其余测试案例调查

## 调查范围与结论

本报告只调查无损清单 `batch_id=R06` 的 65 个文件。清单连续位于 `.scratch/current-requirements-baseline/evidence/material-inventory/material-inventory.tsv:1675-1739`：56 个 `TC-042`～`TC-097`、8 个“暂无测试用例”目录占位 README、1 个测试案例总索引。逐文件重算 SHA-256 后与清单 65/65 一致；这些路径在调查时均为 `tracked-clean`。88 个 Wiki 链接逐一按仓库 Markdown 文件名解析，未发现缺失或歧义。

文档级结论如下：

- **52 个可进入后续原子验收分类的候选，但仍全部是草稿、未批准。** 范围是 `TC-042`～`TC-043`、`TC-048`～`TC-097`。它们逐一指向现存 FR/UC，并在当前文本下与所标 FR AC 保持直接语义对应；例如根索引明确规定 `Given/When/Then` 对应 `Preconditions/Test Steps/Expected Result`、一条 AC 对应一条 TC（`requirement-documents/05-test-cases/README.md:5-12`）。这里的“候选”只允许后续拆分、去重、追源和批准，不表示本报告批准这些条目。
- **4 个发生上游漂移的旧草稿：`TC-044`～`TC-047`。** 它们仍写“占用/异常仓位禁用失败并跳过”“启用即恢复 Idle”等旧规则（各文件 `:15-29`），而当前 `FR-016` 已改为有业务内容时进入 `Disable Pending`、人工启用不覆盖车载硬件不可操作、批量返回独立结果（`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-016-slot-enable-disable-batch-eligibility-and-state-update.md:21-47`）。其 `Verifies AC-1..4` 指针已不再对应当前 AC 语义，不能直接作为当前验收候选；应先重写或明确冻结到旧版 FR 哈希。
- **8 个占位。** `04`～`11` 域 README 都明确写“暂无测试用例”“尚无 FR”“待补充”（各文件 `:1-5`），不含原子验收条件。
- **1 个索引。** 根 `README.md` 是规范、批次和覆盖范围说明，不是独立验收条目；其 `:8` 自己定义 TC/AC 的组织规则，`:11-12` 只是第四、第五批索引，`:13-15` 还索引了不在 R06 的后续批次。
- **0 个现状测试执行证据。** 56 个 TC 只有前置条件、步骤、预期结果和 `Verifies`，没有实际结果、执行人、执行时间、环境、构建/版本、Pass/Fail 或附件。即使正文写“记录测试结果”，那也是预期行为，不是一次已经执行的测试。故本批不能证明实现现状或通过状态。

## 来源身份、形成历史与批准证据

### 来源身份与形成

这些材料的可核查一手来源是仓库内 Markdown 和 Git 对象：

1. 根 `requirement-documents/05-test-cases/README.md` 最早由提交 `96eb2035a6d0a7c692bbfe99c42985de872d68f3` 于 2026-07-13 加入；它在 `ecd0fd89c51c6602eda13f37b7c2e9fe181e5aad` 和 `493ac5a89cb89daf1f8c090ef6091b8d006180be` 又被修改。
2. 其余 64 个 R06 文件均由提交 `ecd0fd89c51c6602eda13f37b7c2e9fe181e5aad` 于 2026-07-15 一次加入，提交作者为 Zhengyu Shao。提交主题描述的是一个包含 RCS Insight、环境验证文档和 SDK 示例的大批次，不能据此推定这 64 个需求材料已被业务方批准。
3. 提交 `493ac5a89cb89daf1f8c090ef6091b8d006180be` 于 2026-07-31 修改了 R06 中 8 个仓位硬件 TC（`TC-048/049/050/055/056/057/061/063`）和根索引；其余 48 个 TC 与 8 个占位 README 自 2026-07-15 加入后未再形成 Git 版本。该提交同时重写了部分上游 FR，但遗漏 `TC-044`～`TC-047`，由此形成上述漂移。
4. 56 个 TC 的 front matter 均为 `status: draft`（每个文件 `:5`）。TC 没有 `created_by`/`updated_by` 字段；上游 `FR-015`～`FR-030`、关联 UC 和 `BR-002` 同样是 `status: draft`，FR 中的 `created_by/updated_by: ZhengyuShao 邵正宇` 只证明文档作者元数据，不是批准。

### 批准证据与适用范围

R06 内没有 `approved_by`、审批人、签字/签名、批准日期、授权角色、批准对象版本或批准范围字段；也没有能把 Git 提交作者转化为需求批准人的治理记录。因此 **65/65 均无具名批准证据，批准范围为空，不能批准当前基线**。

部分上游 UC 的 Notes 自称“经与用户确认”，例如 UC-013 的禁用语义及仍待确认的 Actor（`requirement-documents/03-use-cases/03-agv-fleet-management/uc-013-enable-disable-agv.md:96-103`）、UC-038 的型号维护结论（`requirement-documents/03-use-cases/03-agv-fleet-management/uc-038-maintain-agv-slot-model.md:137-144`）和 UC-011 的看板角色/范围（`requirement-documents/03-use-cases/02-slot-and-hardware/uc-011-view-slot-monitoring-dashboard.md:87-90`）。这些文本没有给出具名确认人、原始会议/邮件、日期、授权范围和被确认版本哈希；只能作为待追溯来源声明，不能给下游 TC 继承批准。

当前适用性只能作以下有限判断：案例内容与仓位/硬件/车队领域和当前仓库模型高度相关；52 个对齐案例可作为后续分类输入，4 个漂移案例须先修复，8 个占位和 1 个索引不进入原子验收。所有判断都受上游 FR/UC/BR 仍为草稿且无外部批准原件限制。

## 派生关系、覆盖与重复

### 可核查派生链

- `TC-042`～`TC-043` → `FR-015 AC-1..2` → `UC-011`。`FR-015` 明示 Origin 为 UC-011 的流程、后置条件和异常流程（`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-015-slot-monitoring-dashboard-display-and-refresh.md:29-40`）。
- `TC-044`～`TC-047` 名义上 → `FR-016 AC-1..4` → `UC-014`，但 TC 仍保留 2026-07-14 的旧 AC 文本；当前 FR 的 `updated: 2026-07-30` 和 AC 已改变（`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-016-slot-enable-disable-batch-eligibility-and-state-update.md:5-10,21-47`）。这是已证实的派生漂移，不是待猜测冲突。
- `TC-048`～`TC-063` → `FR-017`～`FR-021` → `UC-015/016/017/018/039`；对应 FR 均在 Origin 段明确指向 UC 流程（例如 `requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-017-slot-door-unlock-open-test-and-result-recording.md:29-38`、`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-018-slot-light-curtain-function-test.md:29-38`、`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-020-bidirectional-io-point-mapping-verification.md:29-38`、`requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-021-slot-to-io-point-mapping-create-modify-validation.md:29-38`）。
- `TC-064`～`TC-075` → `FR-022`～`FR-024` → `UC-038` 与 `BR-008`；FR 的 Origin 明确列出 UC 流程和 BR 条款（`requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-022-slot-model-draft-field-and-layout-validation.md:29-39`、`requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning.md:29-39`、`requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation.md:29-39`）。
- `TC-076`～`TC-081` → `FR-025/026` → `UC-019`（以及 `FR-026` 对 `BR-008` 的派生）；见 `requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-025-agv-registration-eligibility-and-slot-model-version-validation.md:29-38`、`requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging.md:29-39`。
- `TC-082`～`TC-097` → `FR-027`～`FR-030` → `UC-013/020/021/022`，部分同时依赖 `BR-002/BR-008`；见各 FR `:29-38`。所有这些上游仍是 draft。

这些链证明“仓库内由哪个草稿派生”，不证明链首内容正确、获批或当前对客户适用。

### 后续原子分类注意点

1. `TC-048` 与 `TC-055` 都覆盖一次完整开锁—弹门—关门—锁 DI 恢复链；`TC-050` 与 `TC-056` 都覆盖开锁后未弹门/反馈未变化。它们分别验证 FR-017 与 FR-019，视角不同但操作与预期高度重叠。后续应按“开锁命令/结果记录”与“锁反馈/机构状态机”拆原子事实并去重，不能仅因 TC 编号不同就批准两份重复义务。
2. `TC-064`～`TC-075` 的二次认证、不可变版本、回滚和历史引用保留不仅是测试步骤，还承载高风险业务/审计政策；分类时必须回到 UC-038/BR-008 的批准证据，不得由测试案例反向创设规则。
3. `TC-076`～`TC-097` 引用了 RCS/RIOT、队列、外部状态和安全状态。当前只有预期行为，没有接口版本、环境或执行证据；外部约束仍需与对应接口材料分别核实。
4. 8 个占位目录仅保留分类结构；不能把“暂无 FR/TC”解释成该领域不需要需求或已经验收。

## 逐文件固定身份与分类台账

分类代码：`A` = 与当前上游 AC 对齐的**未批准草稿验收候选**；`D` = **上游漂移的旧草稿**；`P` = **占位**；`I` = **索引/规范**。所有 SHA-256 均为完整值，均已重算匹配清单。

### 02-slot-and-hardware（22 个）

| 文件证据 | 固定 SHA-256 | 名义上游 | 分类与当前适用性 |
| --- | --- | --- | --- |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-042-dashboard-normal-display.md:2-10,23-29` | `8a85621b35c8e6c3da1aa338147f0417b9c89326780a0d2982ee1b80d8cd8961` | FR-015 AC-1 / UC-011 | A；看板正常展示候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-043-dashboard-refresh-failure-retain-old-data.md:2-10,23-29` | `ce5bd7e5c0b0b24c4b84e65b5291d85b5fe4c35d356998ec80eb44e0d584a4a3` | FR-015 AC-2 / UC-011 | A；刷新失败保留旧值候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-044-slot-disable-eligible-success.md:2-10,15-29` | `64afb7b39fdfee16d38ee4b5c3ffdfe3be752b8ca3e9b9e0ec4da8331be3479e` | FR-016 AC-1 / UC-014 | D；只覆盖旧版 Idle→Disabled |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-045-slot-disable-not-idle-skip.md:2-10,15-29` | `5a26cd58e51f66ff5ebc6920ff6a4e6b8a7562f2d2abf114e6ebf121218af19b` | FR-016 AC-2 / UC-014 | D；“占用即跳过”与当前待禁用冲突 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-046-slot-enable-eligible-success.md:2-10,15-29` | `3746325fc49a3b2429c9649dc6b8a5e1edb3000f368921724c35db1c69e58d79` | FR-016 AC-3 / UC-014 | D；遗漏硬件不可操作不得覆盖 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-047-slot-enable-not-disabled-skip.md:2-10,15-29` | `9f6dcbf3c0d90ea71a818a2a1c4070e581b757c48c115297e80c67887425e28d` | FR-016 AC-4 / UC-014 | D；当前 AC-4 已是批量独立结果 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-048-unlock-test-pass-record-normal.md:2-10,23-29` | `1a6d1192220b267cbc857b9e93ab9d50d166a194996c58e3e67cf3b9f79abe17` | FR-017 AC-1 / UC-015 | A；开锁完整成功候选；与 TC-055 重叠审查 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-049-unlock-command-dispatch-failure.md:2-10,23-29` | `2e65d50cbdd8131f6be5997eeeeb4e72ce6a8f9320d8bbc0c641e515c7e5f608` | FR-017 AC-2 / UC-015 | A；指令下发失败候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-050-door-not-opened-mark-abnormal.md:2-10,23-29` | `2bfbd081b377aeadf6a0a5f0b9e7c3b56fb043fd1a8b0e6a9f34b4a6fa45393f` | FR-017 AC-3 / UC-015 | A；未弹门候选；与 TC-056 重叠审查 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-051-light-curtain-precheck-abnormal.md:2-10,23-29` | `601df5366aaf0095ef15e0887e9141986d5326db123ca96479b55e037575f6a8` | FR-018 AC-1 / UC-016 | A；光幕初态异常候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-052-light-curtain-all-stages-pass.md:2-10,23-29` | `69f0834a93fcc8c04fb08ab00ee3abe3b154c6afc4c85b410270ea9e756edec6` | FR-018 AC-2 / UC-016 | A；三阶段成功候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-053-light-curtain-occlusion-not-detected.md:2-10,23-29` | `71cf4fcc3a0b27c7ff8c3bf971bf3db5a0d375e1bfb7e3e9d79cbf1973269518` | FR-018 AC-3 / UC-016 | A；遮挡未检出候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-054-light-curtain-clear-not-restored.md:2-10,23-29` | `a159b1fc496dc46c8e4b05277754af9d418493184f84dba53166c807709eb3c4` | FR-018 AC-4 / UC-016 | A；移除后未恢复候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-055-door-state-both-directions-pass.md:2-10,23-29` | `9b184369ac8c8615e7f00e62df3cc2a43459db7dfccc25b517ec4189ce0312b6` | FR-019 AC-1 / UC-017 | A；锁反馈完整成功；与 TC-048 重叠审查 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-056-door-opened-signal-still-closed.md:2-10,23-29` | `7ffc39543ab7d1ea1e3c5e58d9e8b1df66b3f118e95ff9d20e306e792a65e4c5` | FR-019 AC-2 / UC-017 | A；未弹门/锁 DI 未变；与 TC-050 重叠审查 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-057-door-closed-signal-still-opened.md:2-10,23-29` | `6e662d5570a96dfb7ac03170cf7b79126914a9252a2d5f8c749d954bd8c80d7d` | FR-019 AC-3 / UC-017 | A；关门后未锁闭候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-058-mapping-both-directions-pass.md:2-10,23-29` | `88ab1d5ce3b391f44da5edeb1607e0d9c0d77cbc70d394d39c4004df47732bac` | FR-020 AC-1 / UC-018 | A；双向映射成功候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-059-mapping-direction-one-mismatch.md:2-10,23-29` | `95a091e4b4439e536e176e3bc0a04aeb311647c7b95793b7cbb13d31b387f25e` | FR-020 AC-2 / UC-018 | A；DO→物理仓不符候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-060-mapping-direction-two-mismatch.md:2-10,23-29` | `3cdc0adb555791a8d4b28e554be900beaf00b001e832c6b90e5df4651b4101e9` | FR-020 AC-3 / UC-018 | A；物理仓→DI 不符候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-061-mapping-save-pass-pending-verification.md:2-10,23-29` | `0edea73b9b08d8ee0197ae6f3f8d99ac1f0c32590c5b9d964a15e776703a15a3` | FR-021 AC-1 / UC-039 | A；保存为待核对候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-062-mapping-channel-conflict-reject.md:2-10,23-29` | `a38be5e5384b8fd0bea1172df4de571f658d4019bf4e0dd041f10f14160bd89e` | FR-021 AC-2 / UC-039 | A；通道冲突拒绝候选 |
| `requirement-documents/05-test-cases/02-slot-and-hardware/tc-063-mapping-required-point-missing-reject.md:2-10,23-29` | `2878a731d09abb95a9ff6a90e8ad6af0aa9520be0913ffe4cb251ff8e06a0da2` | FR-021 AC-3 / UC-039 | A；必填点位缺失候选 |

### 03-agv-fleet-management（34 个）

| 文件证据 | 固定 SHA-256 | 名义上游 | 分类与当前适用性 |
| --- | --- | --- | --- |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-064-draft-validation-pass-and-publishable.md:2-10,23-29` | `21f0ffae2eb8fc9270c7141f9c38a9b12510394d16d2b2791ec5d793d788506a` | FR-022 AC-1 / UC-038 | A；模型草稿完整可发布候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-065-draft-duplicate-face-or-slot-id-reject.md:2-10,23-29` | `10ca1554ce4ae36707abb1e41ee77d0deb2762c55d0c2bf2a98045afdbaaf8eb` | FR-022 AC-2 / UC-038 | A；重复 ID 拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-066-draft-out-of-bounds-reject.md:2-10,23-29` | `365075780ba09f1cb79d04897200a5bfea97cf5f618f74f98139950a61573669` | FR-022 AC-3 / UC-038 | A；越界拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-067-draft-overlap-reject.md:2-10,23-29` | `10ce26b97714ec2b0bb96390f7c2eb80cb9f5b59e02bd23baf901e6eb2b87577` | FR-022 AC-4 / UC-038 | A；重叠拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-068-draft-incomplete-spec-save-not-publishable.md:2-10,23-29` | `0b5cebcb12520e8d84a28bff55460ce8422384bf1874c27f50dab4082f2092f8` | FR-022 AC-5 / UC-038 | A；不完整草稿暂存候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-069-publish-success-immutable-version.md:2-10,23-29` | `b2f942b4a4a1fb087aad038f34d53ca29b68c5ba65216a552df2493ca3c21cd2` | FR-023 AC-1 / UC-038 | A；二次认证发布候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-070-publish-incomplete-spec-reject.md:2-10,23-29` | `b67edd4735ef956fe0a8c3fc41d1ca594c70e1cd2c521e26ca18a9fb6afd5cd9` | FR-023 AC-2 / UC-038 | A；规格不完整拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-071-publish-dual-auth-fail-reject.md:2-10,23-29` | `3ba3b08a0e527b02988de62d08db5b91725173c18441814775aef2357f5ad94e` | FR-023 AC-3 / UC-038 | A；二次认证失败候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-072-publish-transaction-fail-rollback.md:2-10,23-29` | `7115a1e3da25f22e9ecd44295a33183f730346c32cf728d5f2abe40c9bb7eba2` | FR-023 AC-4 / UC-038 | A；发布回滚候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-073-retire-success-historical-refs-unaffected.md:2-10,23-29` | `ae658cee476c19cd2e7104cee6d00674356d6b3781763cb38aa04c24030423ab` | FR-024 AC-1 / UC-038 | A；停用且保留历史候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-074-retire-dual-auth-fail-reject.md:2-10,23-29` | `b86deaebf7190be1502170dc91af71f6759da4c921a996db2619b2ab750b9d90` | FR-024 AC-2 / UC-038 | A；停用认证失败候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-075-retire-transaction-fail-rollback.md:2-10,23-29` | `4709365d3fc0fa043019e87f0700fe80b5739de670cf9e6b4876452ba09b2cd5` | FR-024 AC-3 / UC-038 | A；停用回滚候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-076-registration-validation-pass.md:2-10,23-29` | `746b738028fb574ffcadcf0f9ba758cb39d6ac9859959c26080d32a6745f3f0f` | FR-025 AC-1 / UC-019 | A；接入校验成功候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-077-registration-model-version-not-published-reject.md:2-10,23-29` | `da811366d1adbade2e1f33d12ce84d8107589cbe4128b5ca5e0216e7b66dddf3` | FR-025 AC-2 / UC-019 | A；非 Published 拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-078-registration-duplicate-vehicle-id-reject.md:2-10,23-29` | `e5e79cf7b8318736d4176f5ea4d0500fce4e90a04ff5246e20ce7af9ab6fc8ec` | FR-025 AC-3 / UC-019 | A；车辆 ID 重复候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-079-registration-incomplete-config-reject.md:2-10,23-29` | `b2cca20f6f40b4054de29405ce22786f3d0c31ba1d9fb2bfc68f82394b1dbfa0` | FR-025 AC-4 / UC-019 | A；配置不完整候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-080-registration-atomic-creation-success.md:2-10,23-29` | `d2b9664b7404fd95e2ec03701b82cfb731c8db1ad554f4cc07a8fbf5451d47c0` | FR-026 AC-1 / UC-019 | A；原子创建候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-081-registration-rcs-query-fail-reject.md:2-10,23-29` | `a102487a63e11b82c9a9e07b264d2f3ce299107b1a91d35193f5746d3778ab42` | FR-026 AC-2 / UC-019 | A；RCS 查询失败候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-082-enable-disable-immediate-disable-empty-queue.md:2-10,23-29` | `adb0d36146f4985d5a2f44321355dfaf744a3d701e4834dc72543aa9c2b21fe3` | FR-027 AC-1 / UC-013 | A；空队列立即禁用候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-083-enable-disable-pending-then-auto-disable.md:2-10,23-29` | `f033fa8f0babe384eed036f75cb9b2fdc7aca5aeaa9762a370a16c12ec1996e7` | FR-027 AC-2 / UC-013 | A；待生效后自动禁用候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-084-enable-disable-enable-restore-normal.md:2-10,23-29` | `683e0d0d916fd193438685efcf8b838591064897161da0399206c365573af5a1` | FR-027 AC-3 / UC-013 | A；启用恢复候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-085-enable-disable-repeat-disable-ignore.md:2-10,23-29` | `789b5ddaa768752e998e1f8e8c3daa64c1079a3363f4ea9248b5484cb26124fd` | FR-027 AC-4 / UC-013 | A；重复禁用忽略候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-086-enable-disable-invalid-enable-ignore.md:2-10,23-29` | `cc28039c452009b2c9b59dbabaf524878ae83c6562a241e9b235917bf7f39246` | FR-027 AC-5 / UC-013 | A；无效启用忽略候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-087-dispatch-profile-update-pass.md:2-10,23-29` | `f4d997034bfbe2bc8db17511a3cdafef1cc1863bdf4eaa7e7471662a1709bc3b` | FR-028 AC-1 / UC-020 | A；调度配置保存候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-088-dispatch-profile-not-fully-stopped-reject.md:2-10,23-29` | `715551a312a263306b6307b07b1b0806dbdc38266699cfa8cc964b8959e2ca21` | FR-028 AC-2 / UC-020 | A；车辆未停用拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-089-dispatch-profile-door-safety-fail-closed-reject.md:2-10,23-29` | `5ef2f3d46a6a5cec87ec40ace778b7d867ce9f3babca3592121e9f5a5af09944` | FR-028 AC-3 / UC-020 | A；安全状态 fail-closed 候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-090-dispatch-profile-config-conflict-reject.md:2-10,23-29` | `6ce1f21516df3e55b5907440de12516ce05c927826e36640b19ee8538654d4fe` | FR-028 AC-4 / UC-020 | A；配置冲突拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-091-archive-eligible-success.md:2-10,23-29` | `555341f71531a324b45db849c3fbdaf7193b42cb828a90a863bd16ef05d3d71f` | FR-029 AC-1 / UC-021 | A；归档成功候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-092-archive-not-disabled-reject.md:2-10,23-29` | `6f2690e9ae7fc66d3783aaaf3181536f5be97b9723ad4068df4e68ffcadaa06c` | FR-029 AC-2 / UC-021 | A；未禁用拒绝归档候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-093-archive-unfinished-business-reject.md:2-10,23-29` | `1f735080d9b0dcf89cd0eede67fdddd1b38e68796811cc73d635603f14d59d0c` | FR-029 AC-3 / UC-021 | A；未结束业务拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-094-archive-external-safety-fail-closed-reject.md:2-10,23-29` | `e7a01016267fad39c09464657f5fc80b3a6500fede342d8831843b3a4a7d8694` | FR-029 AC-4 / UC-021 | A；外部/安全状态拒绝候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-095-fleet-dashboard-normal-display.md:2-10,23-29` | `52e962bede21aab659c516c46291703eeed0bf20b935e831e5588cade57c0856` | FR-030 AC-1 / UC-022 | A；车队看板正常展示候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-096-fleet-dashboard-rcs-status-fail-stale.md:2-10,23-29` | `dde18ee6291fc84fc5f31ea8519cd09481fa7fcda593023a256a874abd84272e` | FR-030 AC-2 / UC-022 | A；外部状态过期/未知候选 |
| `requirement-documents/05-test-cases/03-agv-fleet-management/tc-097-fleet-dashboard-io-safety-status-fail-unknown.md:2-10,23-29` | `c231ce3548ff3696ac8f5dc2cd46eef4801c6acaaa042702acf55b95388bb44c` | FR-030 AC-3 / UC-022 | A；IO/安全未知候选 |

### 其余目录占位与总索引（9 个）

| 文件证据 | 固定 SHA-256 | 分类与当前适用性 |
| --- | --- | --- |
| `requirement-documents/05-test-cases/04-transport-task-dispatch/README.md:1-5` | `9442e09e92d04f4e25e719e60e49f039bf9b79c7131a17160bccc30322e1659b` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/05-agv-charging/README.md:1-5` | `9a629e7103a51c57c8ba8a3e19f44d6b1f9595c9b08ce505c454c5b5e014aafe` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/06-area-station-mapping/README.md:1-5` | `642ba45e2f2394e4327963ca5b0cd10b0c25ea968d3e1c9fa5828888549b9a8d` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/07-workflow-engine/README.md:1-5` | `9110537983578aa24fd15d1cf3a3369538ff517d7605a6c81d0ac50fd90b3cfd` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/08-user-and-access/README.md:1-5` | `3266d7e620cd930201eb29501b075678466c0382354d747365dddfcbedf25acb` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/09-logs-and-audit/README.md:1-5` | `3ee2efc19521e7f411d9e1ba648135ea55711756b2b6e1772472d0bb71396a8a` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/10-safety-and-interlock/README.md:1-5` | `9f56e1f3c2dd2b41a4b3ded116b0db9bdfd74132fae9c54d8cca878b86bb73cc` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/11-agv-parking/README.md:1-5` | `7bc32cd2196cf0d04434309554384996750e6c5839c64084833a36fb14d0de74` | P；无 FR/TC 的结构占位 |
| `requirement-documents/05-test-cases/README.md:1-16` | `43c3c0dd4dffd28ea1ea8d655ebab3df2632c290b1fa0e8f696476d7d265f41a` | I；测试目录规范与批次索引，不形成验收义务 |

## 后续证据请求

1. 为 52 个对齐候选提供逐原子条目的具名批准人、授权角色、批准日期、适用项目/站点/车辆/版本、被批准 FR/UC/BR 与 TC 的不可变哈希；不能仅引用 Git 作者或“经用户确认”字样。
2. 决定 `FR-016` 当前语义后重写 `TC-044`～`TC-047`，或明确它们仅绑定旧版 `FR-016` 的提交/Blob 哈希；必须补齐待禁用、业务结束自动生效、启用不覆盖硬件不可操作和批量独立结果的当前验收覆盖。
3. 对 `TC-048`/`TC-055`、`TC-050`/`TC-056` 做原子去重，明确命令下发、机械弹门、锁 DI、DO 复位、人工目视与结果记录分别由哪个条目负责。
4. 若要把任何 TC 当作现状测试证据，应另提供测试执行记录：系统/构建版本、配置与环境、执行人和时间、实际结果、Pass/Fail、日志/截图/数据附件及其哈希。
5. 为 UC-038/FR-023/024 的二次认证与不可变版本政策、UC-019/FR-025/026 的 RCS/RIOT 接入约束，以及 FR-028～030 的 fail-closed 规则补齐上游业务与外部接口批准证据；测试案例不能反向批准这些规则。
