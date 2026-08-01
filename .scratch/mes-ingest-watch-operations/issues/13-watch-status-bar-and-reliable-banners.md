# 13 — 底部 Health 状态栏与不闪逝的当前横幅

**What to build:** 将顶部 Health 文本移至底部状态栏，区分 Watch 刷新与 Host MES 轮询；横幅只反映当前活动问题、至少可见 5 秒，并依靠历史事件追溯短暂故障。

**Blocked by:** 01 — 时间显示; 02 — Watch 连接状态; 10 — Alert 生命周期

**Status:** done

- [x] 底栏显示连接/陈旧状态、Host outcome、row count、duration、Host poll end、Watch last success、本机时区、活动 Alert/Paused 数
- [x] 长 BaseUrl、poll start 和错误详情放 tooltip/详情，不让状态栏布局失控
- [x] 明确区分 Watch 最近成功刷新与 Host 最近 MES 轮询完成时间
- [x] ERROR 当前条件显示红色、WARNING 显示橙色；恢复后不继续显示为活动故障
- [x] 横幅出现后最少保持 5 秒；条件持续则不消失，恢复后自动消失
- [x] 恢复在状态栏短暂显示，并确保 IngestAlert/WatchConnectionEvent 已留历史
- [x] 不以旧 Alert 历史决定当前 PausedZeroDrop；使用当前 pause/active incident 状态
- [x] 刷新局部成功不得错误清除仍失败 endpoint 的连接横幅
- [x] 状态投影以纯逻辑测试覆盖首轮未完成、timeout、poll failure、pause、恢复和 stale

## Comments

- PausedZeroDrop is ERROR severity even after its incident is resolved in history; resolved incidents do not drive current red banners.
- Implemented: `WatchStatusBarState` + `WatchBannerProjection` (5s hold / 已恢复), bottom StatusBar UI, per-endpoint partial snapshot apply, `ApplyPartialSuccess` keeps failing-endpoint banners.
