# WIRE_TO_GATE MVP 规格与双仓库实施交接包

- 交接包状态：`FINAL_ACCEPTED`
- 交接包版本：`1.0.0`
- 汇编日期：`2026-08-25`
- 范围：仅包含规划与规格；本交接包不创建生产仓库、协议发布、构建、部署、测试运行或实际批准记录。

## 阅读入口

两个实施团队及其 AI 助手必须按以下顺序阅读：

1. [MVP 范围与验收规格](mvp-specification.md)
2. 对应仓库的实施交接：[ControlServer](controlserver-handoff.md) 或 [OnboardHmi](onboard-handoff.md)
3. [共享协议仓库初始化交接](protocol-repository-handoff.md)
4. [IntegrationSliceId 索引](integration-slices.tsv)
5. [契约测试向量要求](contract-vector-requirements.md)
6. [受控工厂试运行清单](factory-pilot-checklist.md)
7. [资产身份清单](asset-manifest.tsv)

下列仓库资产也是交接包的一部分，必须与本目录一同交付：

- `requirements/baselines/current-requirements-v1.0.0.md`，SHA-256 为 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`；
- `.scratch/wire-to-gate-mvp/evidence/final-requirement-applicability-profile.tsv`，SHA-256 为 `0678fddb8cb0dc4b1df620257ac7076fc8658e3bda828f0de5c6e9f0fe0461de`；
- `.scratch/wire-to-gate-mvp/issues/` 下已解决的第 02～12 项决策；
- 根目录 `CONTEXT.md`、`docs/adr/cross/` 下状态为 accepted 的 ADR，以及选定的 A 方案“旅程导引台”源文件 `.scratch/wire-to-gate-mvp/prototype/onboard-single-scenario/onboard-single-scenario-prototype.html?variant=A`。

如果上述任一固定 SHA-256 不一致，必须停止：本交接包不再适用于当前资产。

## 不可妥协的阅读规则

- 348 行最终 TSV 是唯一的需求适用性权威：85 条 `MVP 直接必须`、101 条 `MVP 交互／安全依赖`、31 条 `首期延后`、131 条 `本场景不适用`，零遗漏、零重复。
- `首期延后` 和 `本场景不适用` 不改变 v1.0.0 中的 Lifecycle，也不代表永久删除。
- 当本交接包摘要引用已解决决策时，详细内容以对应决策文件为权威。团队不得重新解释摘要，从而放宽安全、身份、持久化、恢复、协议或试运行门禁。
- 原型评审豁免仅适用于已解决的原型评审票。它不批准生产 UI 映射、协议发布、跨仓库行为、目标硬件或工厂使用。
- 缺少真实身份、凭证、构建、批准或证据时必须阻断。占位符、AI 声明和沉默都不构成批准。

## 交接边界

本交接包在最终规格已接受后，授权团队进行工作拆分和实施规划。它不授权创建远程仓库、发布协议 tag、合并依赖协议的实现、部署到车辆、运行 Golden WPF tier 2/3，或启动 P0～P7。上述动作仍须满足各自的批准与证据门禁。
