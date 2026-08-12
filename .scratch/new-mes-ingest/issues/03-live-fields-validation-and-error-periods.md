# 03 — 投影实时字段、字段异常与错误期间

**What to build:** 作为运维工程师，我希望同一搬运候选的 MES 字段始终反映最新真实观测，字段变空或非法时既不回填旧值也不隐藏 Demand，并能通过正式 API 查看当前条件、错误期间及其恢复证据，以便准确解释数据如何变化以及问题何时开始和结束。

**Blocked by:** 01 — 建立新版成功轮次端到端骨架

**Status:** ready-for-agent

- [ ] 对同一唯一原始观测连续提交成功轮次时，AREA、EQP、STEP、DATES 和 PACKAGE 的有意义变化更新同一 Demand 世代的 LiveMesFieldSet，不创建新的 Series 或 Demand；MesSourceDate 保持源字段语义，不被当作 Host 观测时间或生命周期时间。
- [ ] 每次真实字段变化都产生含 before/after、PollTrace、Host UTC 时间和 ProjectionCommit 身份的事件；相同观测不追加噪声事件，SeriesSequence 始终严格单调。
- [ ] 必填字段变为 NULL 或空白时保存真实空值并形成 REQUIRED_MES_FIELD_MISSING；AREA 只有符合领域格式的值才有效，非法值形成 INVALID_MES_FIELD_FORMAT，任何场景都不得用历史值或客户端正规化掩盖错误。
- [ ] 字段异常不会阻止 Series、Demand、全部原始观测和 WatchDemandProjection 生成；正式 API 同时返回当前真实值、当前条件、稳定错误码/主分类和不可读结论，使坏数据保持可见但不能被误当作安全外读事实。
- [ ] 同一错误身份持续存在且证据值变化时只扩充同一错误期间的证据，不按轮询创建新期间；后续完整 SUCCESS 给出明确反证时以 CONDITION_CLEARED 结束该期间，并保留全部历史。
- [ ] 空库首轮已存在的字段错误以 BOOTSTRAPPED_CURRENT_CONDITION 建立最早可证明起点，不回扫或伪造旧系统中的开始时间；错误目录中的已发布代码、分类、作用域和含义在契约中稳定。
- [ ] 真实 SQL Server → 正式 API 的验收覆盖有效值、实时变化、必填字段缺失与恢复、非法 AREA 与恢复、无变化轮次及 Host 重启，证明当前投影和错误历史在同一提交中持久一致。

