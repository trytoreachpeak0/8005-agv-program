---
id: DR-001
type: decision-record
title: "技术栈"
status: decided
created: 2026-07-08
updated: 2026-07-10
related_fr: ["FR-001", "FR-007", "FR-011", "FR-013", "FR-014"]
related_uc: []
aliases: ["DR-001"]
---

# DR-001 技术栈

## Decision 决策

.NET 8 + WPF（GUI）。

WPF 不只展示运行状态，还应提供完整配置编辑能力，覆盖模块模板/实例、仓位与 IO 映射、版面布局、默认 DO 工作模式与脉冲宽度等 JSON 配置。保存前必须按 JSON Schema 和应用层语义规则完整校验；保存成功后支持热重载，无需重启进程。

热重载必须按"校验全部新配置→原子切换"执行；失败时继续使用旧配置并明确报告错误，不允许部分生效。涉及监听端口、模块端点等无法安全原地切换的资源时，技术设计可采用受控重建对应服务，但对外仍保持一次配置变更的原子结果。

## Rationale 理由

与根目录 `requirement-documents/00-vision/vision-and-scope.md` 第 3.3 节"服务器软件只能部署在 Windows Server、工控机软件只能部署在 Windows"的部署约束一致。

开发自测需要频繁调整模块、通道和布局；由 WPF 提供与 Schema 共用的完整编辑入口，可避免手改 JSON 造成引用或边界错误。热重载缩短联调反馈周期，但不能以牺牲运行配置一致性为代价。

## Alternatives Considered 备选方案

曾考虑只提供只读面板、配置完全依赖手工编辑 JSON；因多模块和映射配置交叉引用较多、容易出错，未采纳。曾考虑保存后要求重启；因联调迭代频繁，选择校验后热重载。

## Related 关联

[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]、[[fr-007-wpf-visualization-panel|FR-007]]、[[fr-011-configurable-slot-layout|FR-011]]、[[fr-013-configurable-register-table-template|FR-013]]、[[fr-014-multi-io-module-simulation|FR-014]]
