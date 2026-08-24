# 最终批准 REQ-0158–REQ-0161：决定当前 MES 只读与卸货、完工回写边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-042
Approval payload SHA-256: 191394d79ebd998e010645785c39012d241a6c9428b70d6ad036508cd387bd31
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md](../../../.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-042` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0158 — 当前 8005 范围内所有组成部分严格只读访问 MES；不得执行完工、卸货、过站、入库或其它 MES 写操作…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0158`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 当前 8005 范围内所有组成部分严格只读访问 MES；不得执行完工、卸货、过站、入库或其它 MES 写操作，也不得通过工作流或外部调用代替现场流程推动 MES 状态变化。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md](../../../.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md)；`决定当前 MES 只读与卸货、完工回写边界 > Answer; line 15`；来源 SHA-256 `9d9603b2f50e0721de9f91b881b04cb79434907ad3164a9866909699f3096c9f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **决定／旧候选指针：** issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md；R01-A0279 ／ R01-A0700 ／ R01-A0701 ／ R01-A0702 ／ R01-A0714 ／ R01-A0760 ／ R01-A0761 ／ R01-A0762 ／ R01-A0819 ／ R01-A0820 ／ R01-A0849 ／ R01-A0850 ／ R01-A1094 ／ R01-A1095 ／ R01-A1190 ／ R01-A1191 ／ R01-A1192 ／ R01-A1193 ／ R01-A1194 ／ R01-A1195 ／ R01-A1196 ／ R01-A1197 ／ R01-A1332 ／ R01-A1547 ／ R01-A1930 ／ R01-A1931 ／ R01-A1943 ／ R01-A1944 ／ R01-A1945 ／ R01-A1946 ／ R01-A2038 ／ R01-A2039 ／ R01-A2122 ／ R01-A2123 ／ R01-A2124 ／ R01-A2125 ／ R01-A2126 ／ R01-A2127 ／ R01-A2128 ／ R01-A2129 ／ R01-A2174 ／ R01-A2220 ／ R01-A2221 ／ R01-A2241 ／ R01-A2452 ／ R01-A2809 ／ R01-A2810 ／ R01-A2844 ／ R01-A2889 ／ R01-A2901 ／ R01-A2912 ／ R01-A2928 ／ R01-A2936 ／ R01-A2945 ／ R01-A2974 ／ R01-A2987 ／ R01-A3004 ／ R01-A3005 ／ R01-A3008 ／ R02-A0008 ／ R02-A0009 ／ R02-A0050 ／ R02-A0113 ／ R02-A0114 ／ R02-A0878 ／ R02-A0879 ／ R02-A0880 ／ R02-A0881 ／ R02-A0882 ／ R02-A0883 ／ R02-A0884 ／ R02-A0885 ／ R02-A1065 ／ R02-A1066 ／ R02-A1067 ／ R02-A1068 ／ R02-A1069 ／ R02-A1070 ／ R03-A0456 ／ R03-A1325 ／ R03-A1621 ／ R08-A0434 ／ R08-A0909 ／ R08-A1114 ／ R08-A1137 ／ R09-A0058 ／ R09-A0063 ／ R09-A0079 ／ R09-A0101 ／ R09-A0111 ／ R11-A0064 ／ R11-A0070 ／ R11-A0072 ／ R11-A0080 ／ R11-A0085 ／ R11-A0090 ／ R11-A0096 ／ R12-A0002 ／ R12-A0007 ／ R12-A0008 ／ R12-A0042 ／ R12-A0045 ／ R12-A0062 ／ R12-A0068 ／ R12-A0081 ／ R12-A0082 ／ R12-A0083 ／ R12-A0084 ／ R12-A0085 ／ R12-A0086 ／ R12-A0087 ／ R12-A0088 ／ R12-A0110 ／ R12-A0132 ／ R12-A0139 ／ R12-A0258 ／ R12-A0260 ／ R12-A0288。
- **规范文本 SHA-256：** `2351a9a724c1158945c9ca87895807c158bc2a7373b0c2564fe7ed8ee60de682`。

### REQ-0159 — 8005 的物理卸货与搬运结果只形成其本地业务终态和正常审计事实；本地完成不等同于 MES 完成，也不以任何…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0159`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 8005 的物理卸货与搬运结果只形成其本地业务终态和正常审计事实；本地完成不等同于 MES 完成，也不以任何 MES 写回或状态变化作为完成条件。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md](../../../.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md)；`决定当前 MES 只读与卸货、完工回写边界 > Answer; line 16`；来源 SHA-256 `9d9603b2f50e0721de9f91b881b04cb79434907ad3164a9866909699f3096c9f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **决定／旧候选指针：** issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md；R01-A0279 ／ R01-A0700 ／ R01-A0701 ／ R01-A0702 ／ R01-A0714 ／ R01-A0760 ／ R01-A0761 ／ R01-A0762 ／ R01-A0819 ／ R01-A0820 ／ R01-A0849 ／ R01-A0850 ／ R01-A1094 ／ R01-A1095 ／ R01-A1190 ／ R01-A1191 ／ R01-A1192 ／ R01-A1193 ／ R01-A1194 ／ R01-A1195 ／ R01-A1196 ／ R01-A1197 ／ R01-A1332 ／ R01-A1547 ／ R01-A1930 ／ R01-A1931 ／ R01-A1943 ／ R01-A1944 ／ R01-A1945 ／ R01-A1946 ／ R01-A2038 ／ R01-A2039 ／ R01-A2122 ／ R01-A2123 ／ R01-A2124 ／ R01-A2125 ／ R01-A2126 ／ R01-A2127 ／ R01-A2128 ／ R01-A2129 ／ R01-A2174 ／ R01-A2220 ／ R01-A2221 ／ R01-A2241 ／ R01-A2452 ／ R01-A2809 ／ R01-A2810 ／ R01-A2844 ／ R01-A2889 ／ R01-A2901 ／ R01-A2912 ／ R01-A2928 ／ R01-A2936 ／ R01-A2945 ／ R01-A2974 ／ R01-A2987 ／ R01-A3004 ／ R01-A3005 ／ R01-A3008 ／ R02-A0008 ／ R02-A0009 ／ R02-A0050 ／ R02-A0113 ／ R02-A0114 ／ R02-A0878 ／ R02-A0879 ／ R02-A0880 ／ R02-A0881 ／ R02-A0882 ／ R02-A0883 ／ R02-A0884 ／ R02-A0885 ／ R02-A1065 ／ R02-A1066 ／ R02-A1067 ／ R02-A1068 ／ R02-A1069 ／ R02-A1070 ／ R03-A0456 ／ R03-A1325 ／ R03-A1621 ／ R08-A0434 ／ R08-A0909 ／ R08-A1114 ／ R08-A1137 ／ R09-A0058 ／ R09-A0063 ／ R09-A0079 ／ R09-A0101 ／ R09-A0111 ／ R11-A0064 ／ R11-A0070 ／ R11-A0072 ／ R11-A0080 ／ R11-A0085 ／ R11-A0090 ／ R11-A0096 ／ R12-A0002 ／ R12-A0007 ／ R12-A0008 ／ R12-A0042 ／ R12-A0045 ／ R12-A0062 ／ R12-A0068 ／ R12-A0081 ／ R12-A0082 ／ R12-A0083 ／ R12-A0084 ／ R12-A0085 ／ R12-A0086 ／ R12-A0087 ／ R12-A0088 ／ R12-A0110 ／ R12-A0132 ／ R12-A0139 ／ R12-A0258 ／ R12-A0260 ／ R12-A0288。
- **规范文本 SHA-256：** `0d3eb1210817610e518fa761e2c989560d084d3d1ef4a95eb1bad495ed91aebc`。

### REQ-0160 — 正常卸货后所需的 MES 入站、过站、接收或其它状态变化，由目的站对应的现场责任人通过既有 PDA/MES …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0160`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 正常卸货后所需的 MES 入站、过站、接收或其它状态变化，由目的站对应的现场责任人通过既有 PDA/MES 流程承担；责任随目的站业务角色确定，不固定归属于 AGV 装货操作员，8005 不代办或接管。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md](../../../.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md)；`决定当前 MES 只读与卸货、完工回写边界 > Answer; line 17`；来源 SHA-256 `9d9603b2f50e0721de9f91b881b04cb79434907ad3164a9866909699f3096c9f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **决定／旧候选指针：** issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md；R01-A0279 ／ R01-A0700 ／ R01-A0701 ／ R01-A0702 ／ R01-A0714 ／ R01-A0760 ／ R01-A0761 ／ R01-A0762 ／ R01-A0819 ／ R01-A0820 ／ R01-A0849 ／ R01-A0850 ／ R01-A1094 ／ R01-A1095 ／ R01-A1190 ／ R01-A1191 ／ R01-A1192 ／ R01-A1193 ／ R01-A1194 ／ R01-A1195 ／ R01-A1196 ／ R01-A1197 ／ R01-A1332 ／ R01-A1547 ／ R01-A1930 ／ R01-A1931 ／ R01-A1943 ／ R01-A1944 ／ R01-A1945 ／ R01-A1946 ／ R01-A2038 ／ R01-A2039 ／ R01-A2122 ／ R01-A2123 ／ R01-A2124 ／ R01-A2125 ／ R01-A2126 ／ R01-A2127 ／ R01-A2128 ／ R01-A2129 ／ R01-A2174 ／ R01-A2220 ／ R01-A2221 ／ R01-A2241 ／ R01-A2452 ／ R01-A2809 ／ R01-A2810 ／ R01-A2844 ／ R01-A2889 ／ R01-A2901 ／ R01-A2912 ／ R01-A2928 ／ R01-A2936 ／ R01-A2945 ／ R01-A2974 ／ R01-A2987 ／ R01-A3004 ／ R01-A3005 ／ R01-A3008 ／ R02-A0008 ／ R02-A0009 ／ R02-A0050 ／ R02-A0113 ／ R02-A0114 ／ R02-A0878 ／ R02-A0879 ／ R02-A0880 ／ R02-A0881 ／ R02-A0882 ／ R02-A0883 ／ R02-A0884 ／ R02-A0885 ／ R02-A1065 ／ R02-A1066 ／ R02-A1067 ／ R02-A1068 ／ R02-A1069 ／ R02-A1070 ／ R03-A0456 ／ R03-A1325 ／ R03-A1621 ／ R08-A0434 ／ R08-A0909 ／ R08-A1114 ／ R08-A1137 ／ R09-A0058 ／ R09-A0063 ／ R09-A0079 ／ R09-A0101 ／ R09-A0111 ／ R11-A0064 ／ R11-A0070 ／ R11-A0072 ／ R11-A0080 ／ R11-A0085 ／ R11-A0090 ／ R11-A0096 ／ R12-A0002 ／ R12-A0007 ／ R12-A0008 ／ R12-A0042 ／ R12-A0045 ／ R12-A0062 ／ R12-A0068 ／ R12-A0081 ／ R12-A0082 ／ R12-A0083 ／ R12-A0084 ／ R12-A0085 ／ R12-A0086 ／ R12-A0087 ／ R12-A0088 ／ R12-A0110 ／ R12-A0132 ／ R12-A0139 ／ R12-A0258 ／ R12-A0260 ／ R12-A0288。
- **规范文本 SHA-256：** `ef6423c6619e619c846352f342c612a88113256ba9599127ff479bd0a7438d0a`。

### REQ-0161 — 物理卸货完成并满足安全结束条件后，8005 立即结束本地任务并释放车辆；不等待现场 PDA/MES 操作，不…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0161`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 物理卸货完成并满足安全结束条件后，8005 立即结束本地任务并释放车辆；不等待现场 PDA/MES 操作，不等待、轮询或验证 MES 状态变化，也不以之后只读观察到的 MES 变化回溯改变本地卸货终态。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md](../../../.scratch/current-requirements-baseline/issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md)；`决定当前 MES 只读与卸货、完工回写边界 > Answer; line 18`；来源 SHA-256 `9d9603b2f50e0721de9f91b881b04cb79434907ad3164a9866909699f3096c9f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md。
- **决定／旧候选指针：** issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md；R01-A0279 ／ R01-A0700 ／ R01-A0701 ／ R01-A0702 ／ R01-A0714 ／ R01-A0760 ／ R01-A0761 ／ R01-A0762 ／ R01-A0819 ／ R01-A0820 ／ R01-A0849 ／ R01-A0850 ／ R01-A1094 ／ R01-A1095 ／ R01-A1190 ／ R01-A1191 ／ R01-A1192 ／ R01-A1193 ／ R01-A1194 ／ R01-A1195 ／ R01-A1196 ／ R01-A1197 ／ R01-A1332 ／ R01-A1547 ／ R01-A1930 ／ R01-A1931 ／ R01-A1943 ／ R01-A1944 ／ R01-A1945 ／ R01-A1946 ／ R01-A2038 ／ R01-A2039 ／ R01-A2122 ／ R01-A2123 ／ R01-A2124 ／ R01-A2125 ／ R01-A2126 ／ R01-A2127 ／ R01-A2128 ／ R01-A2129 ／ R01-A2174 ／ R01-A2220 ／ R01-A2221 ／ R01-A2241 ／ R01-A2452 ／ R01-A2809 ／ R01-A2810 ／ R01-A2844 ／ R01-A2889 ／ R01-A2901 ／ R01-A2912 ／ R01-A2928 ／ R01-A2936 ／ R01-A2945 ／ R01-A2974 ／ R01-A2987 ／ R01-A3004 ／ R01-A3005 ／ R01-A3008 ／ R02-A0008 ／ R02-A0009 ／ R02-A0050 ／ R02-A0113 ／ R02-A0114 ／ R02-A0878 ／ R02-A0879 ／ R02-A0880 ／ R02-A0881 ／ R02-A0882 ／ R02-A0883 ／ R02-A0884 ／ R02-A0885 ／ R02-A1065 ／ R02-A1066 ／ R02-A1067 ／ R02-A1068 ／ R02-A1069 ／ R02-A1070 ／ R03-A0456 ／ R03-A1325 ／ R03-A1621 ／ R08-A0434 ／ R08-A0909 ／ R08-A1114 ／ R08-A1137 ／ R09-A0058 ／ R09-A0063 ／ R09-A0079 ／ R09-A0101 ／ R09-A0111 ／ R11-A0064 ／ R11-A0070 ／ R11-A0072 ／ R11-A0080 ／ R11-A0085 ／ R11-A0090 ／ R11-A0096 ／ R12-A0002 ／ R12-A0007 ／ R12-A0008 ／ R12-A0042 ／ R12-A0045 ／ R12-A0062 ／ R12-A0068 ／ R12-A0081 ／ R12-A0082 ／ R12-A0083 ／ R12-A0084 ／ R12-A0085 ／ R12-A0086 ／ R12-A0087 ／ R12-A0088 ／ R12-A0110 ／ R12-A0132 ／ R12-A0139 ／ R12-A0258 ／ R12-A0260 ／ R12-A0288。
- **规范文本 SHA-256：** `4a51befe0089aa723fb76074607f1b87d78c55dfced7405d47150914e0afb317`。

## Required HITL resolution

- [ ] `REQ-0158`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0159`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0160`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0161`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0158`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0159`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0160`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0161`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-042`、Approval payload SHA-256 `191394d79ebd998e010645785c39012d241a6c9428b70d6ad036508cd387bd31`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
