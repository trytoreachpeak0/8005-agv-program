# 07 — Watch 分页 Demand 浏览、组合筛选与列头排序

**What to build:** 让 MesIngest.Watch 成功对接新的分页 `/api/demands`，默认浏览所有 VISIBLE，按需分页查看 GONE，并将所有列排序下推到服务端完整结果集。

**Blocked by:** 01 — 时间契约; 02 — HTTP 可靠性; 05 — 分页 Demand API

**Status:** ready-for-agent

- [ ] 启动默认请求 VISIBLE + DATES DESC，滚动/下一页按 cursor 继续，不下载全部历史
- [ ] GONE 历史默认 GoneAt 最近 24 小时，允许用户显式扩大时间范围
- [ ] 增加 DemandId 输入：完整精确或至少 6 位十六进制前缀，约 300ms 防抖
- [ ] TASK_TYPE、SUBLOT、status、DemandId、时间范围可组合，任何筛选变化清页并重查
- [ ] 两表列头第一次升序、第二次降序、显示箭头；刷新保持列和方向
- [ ] 移除 sort ComboBox/asc CheckBox；排序参数发送到 Host，不只排序当前页
- [ ] 相同值以 DemandId 稳定次排序；错误 cursor 后安全重载第一页
- [ ] 明确显示已加载数量/是否还有更多，不把一页行数冒充全库总数
- [ ] 真实 HTTP 契约集成测试证明 Watch 与升级后的 envelope 对接成功

## Comments

- STEP remains displayable but is not a priority filter/sort design driver.

