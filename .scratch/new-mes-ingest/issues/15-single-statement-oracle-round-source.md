# 15 — 正式单语句 Oracle Round source

**What to build:** 把客户批准的六类 `MES_TASK_UNION` 查询接入生产轮询入口，确保每个 `MesTaskUnionRound` 只执行一条只读 Oracle 语句并取得语句级一致的完整候选集合。开发、构建和部署只承认一份正式查询原稿，Oracle Thin 为默认模式、Thick 与 Instant Client 作为配置切换的现场兜底；驱动、映射或结构契约失败形成可追踪的 FAILURE/INCOMPLETE，而字段值异常仍作为 SUCCESS 原始证据进入新版轮次骨架。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架

**Status:** ready-for-human

- [x] 轮询执行证据证明六个 `UNION ALL` 分支由一次命令、一次结果集完成，不按分支发起六次查询，也不通过后续拼接冒充同一语句级快照。
- [x] 正式查询在开发原稿、构建输入和部署产物之间可用内容摘要核对为同一份来源；生产程序不存在第二份可独立漂移的嵌入 SQL，发布包缺少或篡改查询时明确拒绝轮询。
- [x] 查询保持只读，不修改客户 SQL 语义，不执行 DDL，也不尝试创建或调整客户索引、视图；命令超时和取消产生可定位、可脱敏的轮次失败证据。
- [x] 结果列与类型完整时，即使 AREA、EQP、STEP、DATES、PACKAGE 为空、非法或同键重复，轮次仍为 SUCCESS 并原样保留证据；执行失败或所需列/类型使结构契约不能成立时才产生 FAILURE 或 INCOMPLETE，且不能进入业务投影事务。
- [x] fake executor 验证每轮只调用一次、命令超时、取消、列/类型映射、返回顺序不影响规范化摘要，以及失败日志不包含凭据或未经允许的原始敏感值。
- [x] Oracle 模式默认使用 Thin；切换 Thick 与 Instant Client 只需部署配置，不改领域行为或查询文本，配置错误得到可诊断失败而不会静默退回不同查询。
- [x] 可重复的工厂探针说明如何分别记录 Thin 连通结果和必要时的 Thick 复验；未连接真实 Oracle 11g 时证据明确标记未执行，不把 fake 或 CI 结果宣称为现场通过。
- [x] 从正式 source 读取的成功结果可沿生产轮询入口形成带 PollTrace、查询版本、规范化内容摘要和行数证据的 `MesTaskUnionRound`，关闭 Watch 不会中止 Service 轮询。

## Comments

- 2026-08-14：实现完成。生产 V2 已接入单语句 Oracle round source、Thin/Thick
  独立 provider、因果 PollTrace 投影、Service-owned hosted poll 与严格发布/工厂证据链。
- 正式查询按原始字节锁定 SHA-256
  `54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae`；发布包只保留
  一份查询及邻接 manifest，缺失、空文件、篡改或镜像分叉均拒绝。
- 验证证据：Release build 0 warning / 0 error；Ticket 15 聚焦测试 84/84；
  SQL Server 16、兼容级别 160 的正式生产入口门禁 5/5 且 0 skipped；自包含
  `win-x64` 发布与严格包校验通过。
- 独立 Spec review 无缺口。Standards review 发现的 Production V2 空跑和模拟 probe
  伪造现场通过风险均已修复并加入回归测试。
- 未提供获批的真实 Oracle 11g 端点，因此没有声称现场连通通过；工厂 probe 会如实记录
  `NOT_EXECUTED`。完整验证记录见 `.testagent/status.md`。
