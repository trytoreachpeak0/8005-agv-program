# 09 — 可调 Demand/Alert 高度与本地布局偏好

**What to build:** 用 Grid + GridSplitter 替换 Alerts 固定 140 高度，让两表共同填满空间、可拖动并在下次启动恢复比例。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] TransportDemands/Alerts 使用 star row + 垂直 GridSplitter，共同填满状态栏/筛选区外空间
- [ ] 默认比例 70/30；两表最小高度防止被拖到不可见
- [ ] 关闭时保存比例到 Watch 本地用户偏好，启动恢复
- [ ] 偏好损坏、越界或版本不兼容时回到 70/30
- [ ] 双击 splitter 恢复默认比例
- [ ] 窗口 resize/maximize 后比例和填充行为正确
- [ ] 不把 UI 偏好写入 Host、SQL Server 或共享 appsettings

## Comments

- This preference is per Watch machine/user, like local connection-event logs.

