# 最终批准 REQ-0154–REQ-0157：决定运输需求身份、对账键与取消抑制边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-041
Approval payload SHA-256: 3642de1360a5bf0eef23d7ff4cb452b3a6402d96bb0cdd818024d58a0b172417
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md](../../../.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-041` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0154 — GONE 后同键再现产生新实例。 原 TransportDemand 与原 DemandId 永久保留为 G…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0154`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** GONE 后同键再现产生新实例。 原 TransportDemand 与原 DemandId 永久保留为 GONE 历史；MesIngest 为再现候选创建新的 TransportDemand 和 DemandId，并产生“GONE 后再现”告警。新旧实例共享 TransportDemandKey，但不同时为 VISIBLE。MesIngest 不因调度抑制而隐藏或拒绝事实投影。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md](../../../.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)；`决定运输需求身份、对账键与取消抑制边界 > Answer; line 19`；来源 SHA-256 `b563317db22ad19212536cfceb43485e8f48ade782e6f2d62de89aec90380990`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **决定／旧候选指针：** issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md；R01-A0094 ／ R01-A0163 ／ R01-A0175 ／ R01-A0176 ／ R01-A0187 ／ R01-A0188 ／ R01-A0189 ／ R01-A0323 ／ R01-A0324 ／ R01-A0330 ／ R01-A0331 ／ R01-A0332 ／ R01-A0333 ／ R01-A0334 ／ R01-A0335 ／ R01-A0336 ／ R01-A0694 ／ R01-A0695 ／ R01-A2881 ／ R01-A2953 ／ R02-A0826 ／ R02-A0827 ／ R02-A0828 ／ R02-A0829 ／ R02-A0830 ／ R02-A1055 ／ R02-A1058 ／ R03-A0329 ／ R03-A0331 ／ R03-A1320 ／ R03-A1331 ／ R03-A1347 ／ R04-A0314 ／ R05-A0016 ／ R05-A0235 ／ R05-A0237 ／ R05-A0254 ／ R05-A0393 ／ R05-A0395 ／ R05-A0396 ／ R05-A0400 ／ R08-A0272 ／ R08-A0273 ／ R08-A0435 ／ R08-A0450 ／ R08-A0451 ／ R08-A0452 ／ R08-A0453 ／ R08-A0455 ／ R08-A0672 ／ R08-A0675 ／ R08-A0906 ／ R08-A0907 ／ R08-A0908 ／ R08-A0909 ／ R08-A0910 ／ R08-A0911 ／ R08-A0912 ／ R08-A0913 ／ R08-A0914 ／ R08-A0915 ／ R08-A0916 ／ R08-A0917 ／ R08-A0918 ／ R08-A0919 ／ R08-A0920 ／ R08-A0921 ／ R08-A0922 ／ R08-A0923 ／ R08-A0924 ／ R08-A0925 ／ R08-A0926 ／ R08-A0927 ／ R08-A0928 ／ R08-A0929 ／ R08-A0930 ／ R08-A0931 ／ R08-A0932 ／ R08-A0933 ／ R08-A0934 ／ R08-A0935 ／ R08-A0936 ／ R08-A0937 ／ R08-A0938 ／ R08-A0939 ／ R08-A0940 ／ R08-A0941 ／ R08-A0942 ／ R08-A0943 ／ R08-A0944 ／ R08-A0945 ／ R08-A0946 ／ R09-A0060 ／ R09-A0061 ／ R09-A0063 ／ R09-A0067 ／ R09-A0068 ／ R09-A0074 ／ R09-A0075 ／ R09-A0077 ／ R11-A0030 ／ R11-A0069 ／ R12-A0007 ／ R12-A0010 ／ R12-A0015 ／ R12-A0017 ／ R12-A0018 ／ R12-A0019 ／ R12-A0025 ／ R12-A0026 ／ R12-A0042 ／ R12-A0043 ／ R12-A0057 ／ R12-A0059 ／ R12-A0063 ／ R12-A0065 ／ R12-A0070 ／ R12-A0074 ／ R12-A0083 ／ R12-A0096 ／ R12-A0109 ／ R12-A0117 ／ R12-A0134 ／ R12-A0148 ／ R12-A0152 ／ R12-A0179 ／ R12-A0181 ／ R12-A0183 ／ R12-A0190 ／ R12-A0193 ／ R12-A0194 ／ R12-A0202 ／ R12-A0211 ／ R12-A0213 ／ R12-A0218 ／ R12-A0230 ／ R12-A0235 ／ R12-A0241 ／ R12-A0247 ／ R12-A0277 ／ R12-A0279。
- **规范文本 SHA-256：** `bd459d815b66586a4f8a13669a539aad88f67c9b62bdcdff239e35590c855891`。

### REQ-0155 — 本地取消终态挂 DemandId，禁止再次执行业务挂 TransportDemandKey。 调度以 Tra…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0155`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 本地取消终态挂 DemandId，禁止再次执行业务挂 TransportDemandKey。 调度以 TransportDemandKey 保存 TransportDemandSuppression；命中后不得创建、恢复或派发业务任务，即使 MesIngest 因持续可见或 GONE 后再现生成了新 DemandId。同一 SUBLOT 在不同时期命中其他任务类型时属于不同键，不受原抑制影响。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md](../../../.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)；`决定运输需求身份、对账键与取消抑制边界 > Answer; line 20`；来源 SHA-256 `b563317db22ad19212536cfceb43485e8f48ade782e6f2d62de89aec90380990`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **决定／旧候选指针：** issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md；R01-A0094 ／ R01-A0163 ／ R01-A0175 ／ R01-A0176 ／ R01-A0187 ／ R01-A0188 ／ R01-A0189 ／ R01-A0323 ／ R01-A0324 ／ R01-A0330 ／ R01-A0331 ／ R01-A0332 ／ R01-A0333 ／ R01-A0334 ／ R01-A0335 ／ R01-A0336 ／ R01-A0694 ／ R01-A0695 ／ R01-A2881 ／ R01-A2953 ／ R02-A0826 ／ R02-A0827 ／ R02-A0828 ／ R02-A0829 ／ R02-A0830 ／ R02-A1055 ／ R02-A1058 ／ R03-A0329 ／ R03-A0331 ／ R03-A1320 ／ R03-A1331 ／ R03-A1347 ／ R04-A0314 ／ R05-A0016 ／ R05-A0235 ／ R05-A0237 ／ R05-A0254 ／ R05-A0393 ／ R05-A0395 ／ R05-A0396 ／ R05-A0400 ／ R08-A0272 ／ R08-A0273 ／ R08-A0435 ／ R08-A0450 ／ R08-A0451 ／ R08-A0452 ／ R08-A0453 ／ R08-A0455 ／ R08-A0672 ／ R08-A0675 ／ R08-A0906 ／ R08-A0907 ／ R08-A0908 ／ R08-A0909 ／ R08-A0910 ／ R08-A0911 ／ R08-A0912 ／ R08-A0913 ／ R08-A0914 ／ R08-A0915 ／ R08-A0916 ／ R08-A0917 ／ R08-A0918 ／ R08-A0919 ／ R08-A0920 ／ R08-A0921 ／ R08-A0922 ／ R08-A0923 ／ R08-A0924 ／ R08-A0925 ／ R08-A0926 ／ R08-A0927 ／ R08-A0928 ／ R08-A0929 ／ R08-A0930 ／ R08-A0931 ／ R08-A0932 ／ R08-A0933 ／ R08-A0934 ／ R08-A0935 ／ R08-A0936 ／ R08-A0937 ／ R08-A0938 ／ R08-A0939 ／ R08-A0940 ／ R08-A0941 ／ R08-A0942 ／ R08-A0943 ／ R08-A0944 ／ R08-A0945 ／ R08-A0946 ／ R09-A0060 ／ R09-A0061 ／ R09-A0063 ／ R09-A0067 ／ R09-A0068 ／ R09-A0074 ／ R09-A0075 ／ R09-A0077 ／ R11-A0030 ／ R11-A0069 ／ R12-A0007 ／ R12-A0010 ／ R12-A0015 ／ R12-A0017 ／ R12-A0018 ／ R12-A0019 ／ R12-A0025 ／ R12-A0026 ／ R12-A0042 ／ R12-A0043 ／ R12-A0057 ／ R12-A0059 ／ R12-A0063 ／ R12-A0065 ／ R12-A0070 ／ R12-A0074 ／ R12-A0083 ／ R12-A0096 ／ R12-A0109 ／ R12-A0117 ／ R12-A0134 ／ R12-A0148 ／ R12-A0152 ／ R12-A0179 ／ R12-A0181 ／ R12-A0183 ／ R12-A0190 ／ R12-A0193 ／ R12-A0194 ／ R12-A0202 ／ R12-A0211 ／ R12-A0213 ／ R12-A0218 ／ R12-A0230 ／ R12-A0235 ／ R12-A0241 ／ R12-A0247 ／ R12-A0277 ／ R12-A0279。
- **规范文本 SHA-256：** `82533478515b45aca6b98c4b2d917143cb38fc3fd19958f69bb2ed7d37577caf`。

### REQ-0156 — 抑制只由本地取消产生。 CANCELLED_BY_OPERATOR、CANCELLED_BY_LOAD_CO…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0156`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 抑制只由本地取消产生。 CANCELLED_BY_OPERATOR、CANCELLED_BY_LOAD_COMPENSATION、CANCELLED_BY_STOP_COMPLETE 与 CANCELLED_BY_STATION_TIMEOUT 均原子写入 TransportDemandSuppression；单纯 MES_DISAPPEARED 或 GONE 不写抑制，同键以后再现时可作为新实例重新进入调度判断。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md](../../../.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)；`决定运输需求身份、对账键与取消抑制边界 > Answer; line 22`；来源 SHA-256 `b563317db22ad19212536cfceb43485e8f48ade782e6f2d62de89aec90380990`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **决定／旧候选指针：** issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md；R01-A0094 ／ R01-A0163 ／ R01-A0175 ／ R01-A0176 ／ R01-A0187 ／ R01-A0188 ／ R01-A0189 ／ R01-A0323 ／ R01-A0324 ／ R01-A0330 ／ R01-A0331 ／ R01-A0332 ／ R01-A0333 ／ R01-A0334 ／ R01-A0335 ／ R01-A0336 ／ R01-A0694 ／ R01-A0695 ／ R01-A2881 ／ R01-A2953 ／ R02-A0826 ／ R02-A0827 ／ R02-A0828 ／ R02-A0829 ／ R02-A0830 ／ R02-A1055 ／ R02-A1058 ／ R03-A0329 ／ R03-A0331 ／ R03-A1320 ／ R03-A1331 ／ R03-A1347 ／ R04-A0314 ／ R05-A0016 ／ R05-A0235 ／ R05-A0237 ／ R05-A0254 ／ R05-A0393 ／ R05-A0395 ／ R05-A0396 ／ R05-A0400 ／ R08-A0272 ／ R08-A0273 ／ R08-A0435 ／ R08-A0450 ／ R08-A0451 ／ R08-A0452 ／ R08-A0453 ／ R08-A0455 ／ R08-A0672 ／ R08-A0675 ／ R08-A0906 ／ R08-A0907 ／ R08-A0908 ／ R08-A0909 ／ R08-A0910 ／ R08-A0911 ／ R08-A0912 ／ R08-A0913 ／ R08-A0914 ／ R08-A0915 ／ R08-A0916 ／ R08-A0917 ／ R08-A0918 ／ R08-A0919 ／ R08-A0920 ／ R08-A0921 ／ R08-A0922 ／ R08-A0923 ／ R08-A0924 ／ R08-A0925 ／ R08-A0926 ／ R08-A0927 ／ R08-A0928 ／ R08-A0929 ／ R08-A0930 ／ R08-A0931 ／ R08-A0932 ／ R08-A0933 ／ R08-A0934 ／ R08-A0935 ／ R08-A0936 ／ R08-A0937 ／ R08-A0938 ／ R08-A0939 ／ R08-A0940 ／ R08-A0941 ／ R08-A0942 ／ R08-A0943 ／ R08-A0944 ／ R08-A0945 ／ R08-A0946 ／ R09-A0060 ／ R09-A0061 ／ R09-A0063 ／ R09-A0067 ／ R09-A0068 ／ R09-A0074 ／ R09-A0075 ／ R09-A0077 ／ R11-A0030 ／ R11-A0069 ／ R12-A0007 ／ R12-A0010 ／ R12-A0015 ／ R12-A0017 ／ R12-A0018 ／ R12-A0019 ／ R12-A0025 ／ R12-A0026 ／ R12-A0042 ／ R12-A0043 ／ R12-A0057 ／ R12-A0059 ／ R12-A0063 ／ R12-A0065 ／ R12-A0070 ／ R12-A0074 ／ R12-A0083 ／ R12-A0096 ／ R12-A0109 ／ R12-A0117 ／ R12-A0134 ／ R12-A0148 ／ R12-A0152 ／ R12-A0179 ／ R12-A0181 ／ R12-A0183 ／ R12-A0190 ／ R12-A0193 ／ R12-A0194 ／ R12-A0202 ／ R12-A0211 ／ R12-A0213 ／ R12-A0218 ／ R12-A0230 ／ R12-A0235 ／ R12-A0241 ／ R12-A0247 ／ R12-A0277 ／ R12-A0279。
- **规范文本 SHA-256：** `40213d8c8c759ff948beec7f30147a8871d234254ab327a0ec380b03ae2deec4`。

### REQ-0157 — 版本与范围绑定。 本结论绑定 Git 提交 420c96c2f961aaffa42a5443fa42e658…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0157`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 版本与范围绑定。 本结论绑定 Git 提交 420c96c2f961aaffa42a5443fa42e6585b1c993f 下 mes/queries/mes-task-union/ 的当前查询包；输出字段为 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE，其中 query.sql 的 SHA-256 为 54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae。它不适用于 Mock、其他项目或未来变更后的 MES 契约；若增加稳定 MES 事务 ID、改变 TASK_TYPE/SUBLOT 语义，或允许同键表达新的业务发生，必须重新审查本决定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md](../../../.scratch/current-requirements-baseline/issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)；`决定运输需求身份、对账键与取消抑制边界 > Answer; line 23`；来源 SHA-256 `b563317db22ad19212536cfceb43485e8f48ade782e6f2d62de89aec90380990`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md。
- **决定／旧候选指针：** issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md；R01-A0094 ／ R01-A0163 ／ R01-A0175 ／ R01-A0176 ／ R01-A0187 ／ R01-A0188 ／ R01-A0189 ／ R01-A0323 ／ R01-A0324 ／ R01-A0330 ／ R01-A0331 ／ R01-A0332 ／ R01-A0333 ／ R01-A0334 ／ R01-A0335 ／ R01-A0336 ／ R01-A0694 ／ R01-A0695 ／ R01-A2881 ／ R01-A2953 ／ R02-A0826 ／ R02-A0827 ／ R02-A0828 ／ R02-A0829 ／ R02-A0830 ／ R02-A1055 ／ R02-A1058 ／ R03-A0329 ／ R03-A0331 ／ R03-A1320 ／ R03-A1331 ／ R03-A1347 ／ R04-A0314 ／ R05-A0016 ／ R05-A0235 ／ R05-A0237 ／ R05-A0254 ／ R05-A0393 ／ R05-A0395 ／ R05-A0396 ／ R05-A0400 ／ R08-A0272 ／ R08-A0273 ／ R08-A0435 ／ R08-A0450 ／ R08-A0451 ／ R08-A0452 ／ R08-A0453 ／ R08-A0455 ／ R08-A0672 ／ R08-A0675 ／ R08-A0906 ／ R08-A0907 ／ R08-A0908 ／ R08-A0909 ／ R08-A0910 ／ R08-A0911 ／ R08-A0912 ／ R08-A0913 ／ R08-A0914 ／ R08-A0915 ／ R08-A0916 ／ R08-A0917 ／ R08-A0918 ／ R08-A0919 ／ R08-A0920 ／ R08-A0921 ／ R08-A0922 ／ R08-A0923 ／ R08-A0924 ／ R08-A0925 ／ R08-A0926 ／ R08-A0927 ／ R08-A0928 ／ R08-A0929 ／ R08-A0930 ／ R08-A0931 ／ R08-A0932 ／ R08-A0933 ／ R08-A0934 ／ R08-A0935 ／ R08-A0936 ／ R08-A0937 ／ R08-A0938 ／ R08-A0939 ／ R08-A0940 ／ R08-A0941 ／ R08-A0942 ／ R08-A0943 ／ R08-A0944 ／ R08-A0945 ／ R08-A0946 ／ R09-A0060 ／ R09-A0061 ／ R09-A0063 ／ R09-A0067 ／ R09-A0068 ／ R09-A0074 ／ R09-A0075 ／ R09-A0077 ／ R11-A0030 ／ R11-A0069 ／ R12-A0007 ／ R12-A0010 ／ R12-A0015 ／ R12-A0017 ／ R12-A0018 ／ R12-A0019 ／ R12-A0025 ／ R12-A0026 ／ R12-A0042 ／ R12-A0043 ／ R12-A0057 ／ R12-A0059 ／ R12-A0063 ／ R12-A0065 ／ R12-A0070 ／ R12-A0074 ／ R12-A0083 ／ R12-A0096 ／ R12-A0109 ／ R12-A0117 ／ R12-A0134 ／ R12-A0148 ／ R12-A0152 ／ R12-A0179 ／ R12-A0181 ／ R12-A0183 ／ R12-A0190 ／ R12-A0193 ／ R12-A0194 ／ R12-A0202 ／ R12-A0211 ／ R12-A0213 ／ R12-A0218 ／ R12-A0230 ／ R12-A0235 ／ R12-A0241 ／ R12-A0247 ／ R12-A0277 ／ R12-A0279。
- **规范文本 SHA-256：** `1d095c434cbe50de14c08de01090175fa28041806e40aff94ab0f2c2047804c6`。

## Required HITL resolution

- [ ] `REQ-0154`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0155`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0156`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0157`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0154`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0155`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0156`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0157`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-041`、Approval payload SHA-256 `3642de1360a5bf0eef23d7ff4cb452b3a6402d96bb0cdd818024d58a0b172417`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
