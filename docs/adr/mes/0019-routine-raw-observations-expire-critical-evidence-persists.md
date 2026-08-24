# 普通原始观测有限保留，关键边界原始证据永久保留

完整成功轮次的原始行当前随每次轮询重复增长，但永久错误历史只要求关键事实仍可被原文解释。决定普通 DemandRawObservation 提供 30 天 RawObservationAvailabilityWindow，窗口外可不可恢复地清理；与错误、冲突、字段变化及 Demand 创建、GONE、重现、归档边界直接关联的完整原始行提升为 DurableRawEvidence 并永久保留，以有限在线原文换取可控存储，同时不牺牲关键业务历史的可解释性。

**Status**: superseded by ADR-mes-0022

**Consequences**:
- DemandSeriesEvent、DemandSeriesErrorPeriod 与其结构化证据继续永久保留，不因普通原始观测清理而缩短。
- 清理必须先证明一组原始行不属于 DurableRawEvidence；无法证明时不得删除。
- 所有原始行永久在线与关键证据有限提升两种语义不能混用，Host 与 Watch 必须公开实际可用边界。
