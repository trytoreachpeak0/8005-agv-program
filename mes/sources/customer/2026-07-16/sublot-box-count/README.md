# SUBLOT 料盒数量查询来源

## 来源状态

当前可追溯来源是客户提供并已写入《宿迁长电 AGV 项目 MES 数据接口需求确认》的查询定义（该文档第 6 节）以及仓库旧路径中的 SQL。`query.sql` 是 2026-07-16 按当时最新正式 SQL 保存的来源快照，不代表另一个正式版本。

对应正式查询为 [`../../../../queries/sublot-box-count/query.sql`](../../../../queries/sublot-box-count/query.sql)，`QUERY_ID` 为 `SUBLOT_BOX_COUNT`。

## 使用边界

本目录仅用于客户来源追溯和差异研究，不得作为应用、测试工具或部署流程的运行时依赖。正式执行只能从 `SUBLOT_BOX_COUNT` 查询包解析。后续客户变更应建立新的日期快照，不覆盖本目录。
