# 01 — 统一时间契约与 Watch 本机时区显示

**What to build:** 统一 MesIngest 生成/持久化/API/Watch 的时间语义；Host 时间存 UTC，MES DATES 按来源 offset 解释，Watch 按运行电脑系统时区显示，并将 DATES 明确为当前工序进入时间。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] Core/Host/Watch DTO 使用 DateTimeOffset，SQL Server 使用 DATETIMEOFFSET；禁止以无 Kind DateTime 表示业务时间点
- [ ] Host 生成的 CreatedAt、GoneAt、Alert、PollHealth 时间使用 UTC clock
- [ ] Oracle/CSV 无 offset 的 DATES 继续按工厂 UTC+08:00 解释；API 保留原时间点
- [ ] Watch 统一转换为 TimeZoneInfo.Local，格式 `yyyy-MM-dd HH:mm:ss zzz`
- [ ] DATES 列显示“当前工序进入时间 (DATES)”；STEP 只保留为下一工序原始字段
- [ ] 默认排序改为 `DATES DESC, DemandId ASC`；MesLastSeenAt 不再是默认排序
- [ ] 覆盖不同时区、夏令时/无夏令时和相同时间次排序测试

## Comments

- Confirmed domain term: MesCurrentStepEnteredAt. DATES is not the time of entering the STEP column; STEP denotes the next process.

