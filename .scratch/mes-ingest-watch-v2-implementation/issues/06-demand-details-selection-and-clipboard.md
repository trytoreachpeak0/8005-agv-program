# 06 — 完成 TransportDemand 详情、选择与复制

**What to build:** 让操作员从 VISIBLE 或 GONE 的当前页稳定选择一条 TransportDemand，准确区分 MES 原始输入与本地投影、查看完整值并复制到其它工具，全程不提供任何业务修改入口。

**Blocked by:** 04 — 完成 VISIBLE TransportDemand 单页浏览; 05 — 完成独立 GONE TransportDemand 浏览

**Status:** done

- [x] 表格显示并允许复制规格规定的 DemandId、七个 MES 输入字段和全部本地投影字段；长值即使省略显示也能通过详情和复制取得完整内容。
- [x] 详情明确分成“MES 输入（创建时冻结）”与“本地 TransportDemand 投影”两组，并正确解释 DATES、STEP、locationRisk/locationRiskCode、createdAt 和 goneAt。
- [x] 支持双击或显式操作查看详情、复制当前单元格、复制整行、复制含列名整行和复制 DemandId；右键未选中单元格时先切换当前选择。
- [x] 当前页刷新按 DemandId 保持选择并更新详情；所选项消失时清空选择和详情并提示一次；新查询或翻页成功后默认不选中。
- [x] 详情区可调整大小，在最低主视口下持续可见且不随表格横向滚动消失。
- [x] 页面和详情不存在编辑、创建、删除、派车、装卸、确认或其它生产命令入口。

## Comments

- 2026-08-08：完成 VISIBLE/GONE 共用的只读 TransportDemand 详情投影、稳定选择刷新、单元格/整行/含列名整行/DemandId 复制，以及独立可调详情区。
- 双轴代码审查：Standards 无硬性违规；已消除重复详情模板、测试专用生产查找方法和重复选择同步。Spec 发现的普通单元格双击/复制 DemandId 选择缺口已用 CurrentCell/SelectedCells 路径修复并补回归测试。
- 验证：票据相关 Core/Watch 测试 30/30，通过正式 fake Host 旅程；`MesIngest.Watch.UiTests` 21/21。完整 `MesIngest.Tests` 在沙箱内 444 通过、19 个 SQL Server 环境测试跳过，2 个 HttpListener 用例受沙箱限制；同 3 个契约测试在沙箱外诊断重跑 3/3 通过。
