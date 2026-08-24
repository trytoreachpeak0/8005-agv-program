# 生成首版原子需求最终批准批次

Type: task
Status: resolved
Blocked by: 87

## Question

基于已经完成来源层叠、冲突处置和规范化的 `v1.0.0` 候选总账，如何按责任边界与可独立判断粒度重新核对既有 102 个批次建议，并生成覆盖全部候选且零重复、零漏项的最终 HITL 批准票据？

每张批准票必须展示推荐结论、取舍、证据边界、永久需求身份、规范文本和精确来源指针；批次创建本身不得替用户批准任何条目。创建后须以原生 blocking 关系使首版发布任务等待全部批准票关闭。

## Evidence

- [建立首版规范需求候选与来源层叠总账](87-build-v1-canonical-requirement-candidate-ledger.md)
- [确定需求确认的条目粒度](04-atomic-requirement-approval-granularity.md)
- [决定基线版本的存储与变更治理形式](09-baseline-release-storage-and-change-governance.md)

## Answer

已基于 SHA-256 固定的 `v1.0.0` 候选总账建立最终 HITL 批次体系，且没有替用户批准任何条目。

### 旧建议复核与最终分批

- 旧 102 个建议批次已逐项复核；它们覆盖的是 R01–R13 中 6,449 条未批准旧来源声明，未绑定当前 348 个 `REQ` 的精确规范文本、范围、验证方法或候选总账身份，因此 **0 个**原样继承为最终批准单位。其领域和责任角色仍保留为分批参考，逐项处置见复核账。
- 当前 348 条候选按同一 `primary_source` 与同一责任边界分组，再按连续 `REQ` 顺序切成每批最多 4 条，共形成 **95 张**最终批准票。覆盖为 348/348，唯一覆盖为 348/348，零重复、零漏项。
- 每张票逐条展示推荐结论、批准／拒绝／修订的取舍、候选永久身份、精确规范文本、适用范围、验证方法、来源路径与位置、来源 SHA-256、来源批准边界、AI/形成边界、替代与冲突处置、决定/旧候选指针及规范文本 SHA-256。
- 推荐默认值是逐条“批准”，但只作为 HITL 建议；所有票均保持 `Status: open`，候选总账仍保持 `candidate-awaiting-final-item-approval`，批准升级为 0。用户必须对每条明确批准、拒绝或修订；完整展示且无例外时，“采用推荐值”才解释为逐条采用该票全部推荐项。

### 身份、阻塞与发布边界

- 每个批次由 `V1-APP-NNN`、`Approval payload SHA-256` 与候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646` 共同固定。任何绑定字段变化都要求重新生成并重新批准。
- 批准票为《最终批准 REQ-0001–REQ-0004：新版 MesIngest 当前规范》至《最终批准 REQ-0346–REQ-0348：决定公共业务点绑定的维护与生效治理》，编号 89–183；它们原生 `Blocked by: 88`，本票关闭后共同进入可执行前沿。
- 已从地图雾区毕业并新建《生成并发布首个当前需求基线 v1.0.0》（编号 184）。该发布任务原生阻塞于全部 95 张批准票；任一条目拒绝、待修订、缺失批准或 payload 身份漂移都会阻止发布。

### 失败式核验

- 上游候选总账先以 `--verify-only` 复核通过：348 个连续唯一候选、12,452 条旧来源、363 条可追指针、来源身份漂移 0、旧来源批准升级 0。
- 本批次生成器随后以 `--verify-only` 独立复核通过：95 个批次、348/348 唯一覆盖、旧 102 个建议及其 6,449 条计数均固定、发布阻塞数 95、批准升级 0；全部生成票据与清单字节身份无漂移。

### Assets

- [最终批准批次清单](../evidence/v1-final-approval-batches/v1-final-approval-batches.tsv) — 95 批，SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`
- [旧 102 批建议逐项复核账](../evidence/v1-final-approval-batches/legacy-102-batch-suggestion-review.tsv) — SHA-256 `45dff3c54861ec75005b6760aa587761539ac3147358d6da8124638d43161cd8`
- [可重建摘要](../evidence/v1-final-approval-batches/v1-final-approval-batches-summary.json)
- [形成与核验说明](../evidence/v1-final-approval-batches/README.md)
- [确定性生成／失败式核验脚本](../evidence/v1-final-approval-batches/build_and_verify_v1_final_approval_batches.py)

本票只新增治理票据与证据资产，不修改产品代码或原始需求材料，也未形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`，也不触发产品测试。
