# 01 — 跨仓桌面锁接进 control-server，mes-ingest 那把锁改带超时等待

**做什么：** 让两个仓库里任何会驱动交互式桌面的脚本，在 `win11-01` 上真正互斥。
`8005-agv-control-server` 拿到与 `8005-mes-ingest` 同名的机器级互斥体
`Global\W2G-InteractiveDesktop`；`8005-mes-ingest` 那把锁从快速失败（超时 0、exit 3）
改为带超时的等待，使 CI 作业在撞上另一个仓的调度时排队而不是变红。

来源是完整产品规格第 14 节实施图待办第 2 项，标注「批次 2 前」。它必须先于任何会起
WPF 窗口、抓像素或驱动 UI Automation 的批次 2 工作落地——否则 L2 真装置场景与
`golden-renderer` 会在跨仓调度上互相打断。

**名字才是契约，代码不是。** 两个仓是独立克隆、没有共享包，第二个仓自己拷一份 helper
是预期做法，不要为此建共享包。

**前置：** 无，可立即开工。

**状态：** resolved（2026-09-08）—— 决议见 [01-answer.md](01-answer.md)。grep 出第四个入口
（`Invoke-AuthorizedAbsentObservationShadow.ps1`，票据只点名三个）；control-server 侧用 `.psm1`
而非拷一份包装脚本，理由见决议。最后一条「CI 不出现因互斥导致的红」需要推分支才能验，未做

- [x] `8005-agv-control-server` 有一份自己的桌面锁 helper，互斥体名字与 `8005-mes-ingest`
      的 `Invoke-WithDesktopLock.ps1` 逐字符相同
- [x] 该仓所有驱动交互式桌面的脚本（L2 真装置场景入口）都经这把锁，没有绕过的路径
- [x] `8005-mes-ingest` 的锁改为带超时等待，超时值可传参，超时后才失败
- [x] 两个仓各有一条测试或脚本自检，证明第二个持有者会等待而不是立即失败
- [~] 在两个仓同时发起桌面作业，实测第二个排队后成功（本机三层实测通过）；**CI 上未实跑**，需推分支
- [x] 改动不触碰 `8005-mes-ingest` 的任何需求条目与既有 workflow 语义（范围外判定排除的
      是它的 100 条需求，不是它作为 CI 基础设施的部分）
