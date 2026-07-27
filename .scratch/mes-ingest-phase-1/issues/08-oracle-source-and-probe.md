# 08 — Oracle 生产快照源与诊断探针

**What to build:** 生产 MesSnapshotSource 读取正式 MES_TASK_UNION；默认 Thin，可配置切 Thick+Instant Client；正式 SQL 从仓库原稿发布到安装目录旁 queries/；提供一次性连通/查询诊断探针。本票交付“可拿去工厂验证的能力”，不宣称现场已验证成功。

**Blocked by:** 07 — Windows Service 持续单飞轮询

**Status:** ready-for-agent

- [ ] Oracle adapter 执行正式 MES_TASK_UNION，期望列含 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE
- [ ] 默认 Thin；Thick+Instant Client 可由配置切换，无需改业务代码
- [ ] 构建/发布将仓库正式 query 原稿拷入安装旁 queries/，无漂移的第二份生产 SQL 叉
- [ ] MES 凭证与连接仅本地配置，永不进仓库
- [ ] 提供一次性连通/查询诊断（探针）路径，便于工厂首启
- [ ] Oracle 失败/超时/不完整结果按既有规则不污染投影并告警
- [ ] 连接池、超时等数值可配置；模式切换不依赖重编
