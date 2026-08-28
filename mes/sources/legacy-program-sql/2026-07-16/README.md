# 旧程序 SQL 访问代码快照

本目录是旧程序 SQL 的原样研究快照，不是正式查询目录，也不是客户当前批准版本。文件可能包含写操作、存储过程式语句或已失效业务假设；任何工具、应用和部署流程都不得直接加载或执行。

- `catalog.csv`：静态分类与哈希。分类仅用于确定研究优先级，不等于安全批准。
- `source-manifest.json`：迁移时间和逐文件 SHA-256。
- 当前静态分类：16 个未验证只读候选，4 个写/过程式研究文件。
- `READ_ONLY_CANDIDATE_UNVERIFIED` 仍须建立实验、确认对象和负载后才可执行。
- `WRITE_OR_PROCEDURAL_RESEARCH_ONLY` 禁止进入 MES Lab 只读 bundle。

研究结论必须进入 `mes/experiments` 与 `mes/evidence`，不能直接修改本快照；客户提供新版本时应建立新的日期快照。
