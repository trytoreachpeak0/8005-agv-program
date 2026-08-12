# 15 — 正式单语句 Oracle Round source

**What to build:** 把客户批准的六类 `MES_TASK_UNION` 查询接入生产轮询入口，确保每个 `MesTaskUnionRound` 只执行一条只读 Oracle 语句并取得语句级一致的完整候选集合。开发、构建和部署只承认一份正式查询原稿，Oracle Thin 为默认模式、Thick 与 Instant Client 作为配置切换的现场兜底；驱动、映射或结构契约失败形成可追踪的 FAILURE/INCOMPLETE，而字段值异常仍作为 SUCCESS 原始证据进入新版轮次骨架。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架

**Status:** ready-for-agent

- [ ] 轮询执行证据证明六个 `UNION ALL` 分支由一次命令、一次结果集完成，不按分支发起六次查询，也不通过后续拼接冒充同一语句级快照。
- [ ] 正式查询在开发原稿、构建输入和部署产物之间可用内容摘要核对为同一份来源；生产程序不存在第二份可独立漂移的嵌入 SQL，发布包缺少或篡改查询时明确拒绝轮询。
- [ ] 查询保持只读，不修改客户 SQL 语义，不执行 DDL，也不尝试创建或调整客户索引、视图；命令超时和取消产生可定位、可脱敏的轮次失败证据。
- [ ] 结果列与类型完整时，即使 AREA、EQP、STEP、DATES、PACKAGE 为空、非法或同键重复，轮次仍为 SUCCESS 并原样保留证据；执行失败或所需列/类型使结构契约不能成立时才产生 FAILURE 或 INCOMPLETE，且不能进入业务投影事务。
- [ ] fake executor 验证每轮只调用一次、命令超时、取消、列/类型映射、返回顺序不影响规范化摘要，以及失败日志不包含凭据或未经允许的原始敏感值。
- [ ] Oracle 模式默认使用 Thin；切换 Thick 与 Instant Client 只需部署配置，不改领域行为或查询文本，配置错误得到可诊断失败而不会静默退回不同查询。
- [ ] 可重复的工厂探针说明如何分别记录 Thin 连通结果和必要时的 Thick 复验；未连接真实 Oracle 11g 时证据明确标记未执行，不把 fake 或 CI 结果宣称为现场通过。
- [ ] 从正式 source 读取的成功结果可沿生产轮询入口形成带 PollTrace、查询版本、规范化内容摘要和行数证据的 `MesTaskUnionRound`，关闭 Watch 不会中止 Service 轮询。
