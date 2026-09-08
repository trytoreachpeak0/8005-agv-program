# 票 01 决议：跨仓桌面锁接通，两个仓在同一把互斥体上真的互等

Resolved: 2026-09-08
Resolves: `01-cross-repo-desktop-lock.md`

## 结论一句话

**`Global\W2G-InteractiveDesktop` 现在有两个持有方，撞上时排队而不是变红。**
`8005-agv-control-server` 拿到自己的一份实现（`scripts/DesktopLock.psm1`），四个会起 WPF 的入口
全部在脚本内部取锁；`8005-mes-ingest` 那把锁的默认超时从 0 改成 1800 秒。

验收证据是三层，不是一层：

| 层 | 做了什么 | 结果 |
| --- | --- | --- |
| 各仓自检 | 两个 `Test-DesktopLockQueueing.ps1` 各起真的竞争进程 | 各 6 条断言全 PASS |
| 跨仓实测 | 两个仓**各自独立的实现**双向互等 | 两个方向都排队 7.9s 后接手 |
| 端到端 | mes-ingest 持锁时跑 L2 `real-onboard-normal-load` | 报 `DESKTOP_LOCK_WAITING`，放手后接手，场景 PASS |

## 落在哪

### `8005-agv-control-server`（worktree `8005-fp/`，分支 `fp/v2-impl`）

| 文件 | 改动 |
| --- | --- |
| `scripts/DesktopLock.psm1` | **新增**。`Get-DesktopLockName` / `Enter-DesktopLock` / `Exit-DesktopLock` |
| `scripts/Test-DesktopLockQueueing.ps1` | **新增**。自检，6 条断言 |
| `scripts/l2/Invoke-L2Scenario.ps1` | 仅 `Onboard = 'Real'` 的场景取锁 |
| `scripts/run-staged-g3.ps1` | 取锁 |
| `scripts/run-staged-g3-restart.ps1` | 取锁 |
| `scripts/Invoke-AuthorizedAbsentObservationShadow.ps1` | 取锁 |
| `.github/workflows/l2.yml` | 「跨仓桌面互斥未解决」那段注释作废 |
| `CLAUDE.md` | L2 真装置那节加一条「会取锁、可能排 30 分钟」 |

### `8005-mes-ingest`（worktree `8005-fp/`，分支 `fp/batch-2`）

| 文件 | 改动 |
| --- | --- |
| `Invoke-WithDesktopLock.ps1` | `-TimeoutSeconds` 默认 `0` → `1800`；先零等待再带超时等，中间打 `DESKTOP_LOCK_WAITING` |
| `Invoke-WatchUiTests.ps1` | 新增 `-DesktopLockTimeoutSeconds`（默认 1800），`WaitOne(0)` 硬编码去掉 |
| `Test-DesktopLockQueueing.ps1` | **新增**。自检，6 条断言 |
| `.github/workflows/desktop-tests.yml` | `timeout-minutes` 30 → 60 |
| `.github/workflows/golden-renderer.yml` | `vm-tests` 30 → 60；`render` 保持 180（理由见下） |
| `CLAUDE.md` | 「Acquisition is fail-fast」整段替换 |

## 自行定案的六件事

### 一、control-server 用 `.psm1`，不是拷一份 `Invoke-WithDesktopLock.ps1`

规格第 14 节写的是「拷一份 `Invoke-WithDesktopLock.ps1`」，同时明说「名字才是契约，代码不是」。
我按后半句做，形态换了：

那边的调用方是 **workflow step**，所以「用 `-Command { }` 包住一段命令」是自然形状。这边的四个
持有者都是**长脚本自己内部**要占桌面，而且它们**手动跑的次数不比 CI 少**——包装器保护不了裸调用，
而裸调用正是这些脚本的主要用法。所以接口是围着「占桌面的那一段」的 Enter/Exit。

**没有建共享包**，票据和规格都不要它，两个仓的发布周期也不该为三十行代码绑在一起。

### 二、超时值 1800 秒

单次持锁的实测上界约 8 分钟（`watch-window-visual` 一次迭代 ~7.3 分钟、`desktop-tests` 那 163 个
测试几分钟、L2 真装置场景 ~25 秒）。30 分钟是三倍余量，同时**仍是有限值**——真出异常时以
`DESKTOP_LOCK_BUSY` 说明原因，比挂到 job 的 `timeout-minutes` 上只留一行「已超过最大执行时间」强。

无限等待被否掉的理由就是这一条：诊断信息会消失。

### 三、超时后仍是 exit 3 / `DESKTOP_LOCK_BUSY`

票据问「超时后该退什么码」。答案是**不改**。`Invoke-WatchUiTests.ps1` 的
`WATCH_UI_SERIALIZATION_BUSY` 契约与 exit 3 都保持原样——**改的是等多久才失败，不是失败长什么
样**。`-TimeoutSeconds 0` 仍然可用，自检的第 2 条断言就守着它。

control-server 侧不同：`Enter-DesktopLock` **抛异常**而不是 exit。它的调用方是长脚本中间的一行，
那里 `exit` 会跳过 `finally` 里的进程清理与证据落盘。异常走 `catch`，L2 编排器照常写 FAIL 证据。

### 四、四个入口，票据点名三个

票据说「动手前自己 grep 确认，别照抄这行」。grep 的结果多一个：
**`scripts/Invoke-AuthorizedAbsentObservationShadow.ps1`** 也起 `SQCD.Agv.Wpf.exe`（而且是
`WindowStyle Normal`，故意可见）与 `SQCD_8005AGV_Simulator.exe`。已一并接上。

排除掉的两个，理由记下来省下次再查：`run-demand-bearing-g3-vectors.ps1` 只起
`ControlServer.Host.dll`（无窗口），`test-wire-to-gate.ps1` 一个进程都不起。

**`-WindowStyle Hidden` 不代表不占桌面。**staged G3 的三处 `Start-Process` 都带这个参数，但它隐藏
的是这些进程根本没有的控制台窗口，WPF 窗口照样创建。判断依据只能是「起的是不是 WPF 程序」。

### 五、取锁点尽量靠后

四处都取在「第一个 WPF 进程启动之前」，而不是脚本开头。clone、protocol G1、build、publish、
无头 ControlServer、TLS 探测这些都不碰桌面，**排队期间不该占着任何东西**。L2 那处还多一层：
只有 `Onboard = 'Real'` 的场景取锁，四条合成场景一如既往不碰它。

释放都在 `finally` **最后一行**，在对端进程停掉之后。早放会把桌面交给另一个仓，而这边的 WPF 窗口
还在关。

### 六、`golden-renderer.yml` 的 `render` job 不加超时预算

它是 180 分钟，看起来最该加。但 `Test-WatchWindowBaselineStability.ps1` 是**每次迭代**调一次
`Invoke-WatchUiTests.ps1`，所以锁是**逐次取放**的，不是跨整个循环持有。三连跑最坏
3 × (30 分钟等 + 7.3 分钟跑) = 112 分钟，180 够。

这个性质是好事而不是巧合：一次三连跑若整段持锁 22 分钟，对面仓的排队就没意义了。已写进注释，
免得有人「优化」成取一次锁跑三轮。

## 撞到的三个坑

### `AbandonedMutexException` 那段以前是死代码，现在不是了

helper 的注释自己写了原因：`-TimeoutSeconds 0` 时没有等待者，被杀的持有者的互斥体**直接不存在**，
下一个 `WaitOne(0)` 返回 `$true`，异常根本不会抛。改成真等待之后，等待者自己持着句柄让对象活了
下来，于是它才第一次可达。

两个仓的自检各有一条断言专门覆盖它：起持有者 → 让等待者阻塞上去 → 杀掉持有者 → 断言等待者接手
并报 `DESKTOP_LOCK_ABANDONED`。**两边都实测走到了那一行。**

### `$using:` 在普通 scriptblock 调用里无效

写跨仓实测脚本时用了 `& $helper -Command { ... $using:ReadyFile ... }`，持锁者静默地什么都没写。
`$using:` 是 `Invoke-Command`／`Start-Job` 的远程作用域语法；`& $Command` 是同 runspace 执行，
scriptblock 沿作用域链就能看见调用方的变量，直接写 `$ReadyFile` 即可。

### 自检不能用 `Start-Sleep` 猜时机

第一版用「持锁者睡 5 秒」加「等待者应该等到 ≥2.5 秒」。这在 pwsh 冷启动慢的机器上会假红——等待者
的计时从它自己进程内开始，pwsh 启动那 1～3 秒不在里面，于是实际等待可能短于下界。

现在每一步都由**信号文件**驱动：持锁者持到主进程放行为止，主进程等到等待者的日志真的出现
`DESKTOP_LOCK_WAITING` 才动手。**一个偶发红的自检比没有自检更糟**，这条值得多写二十行。

顺带：`| Out-File` 要等整条管道结束才写盘，于是「等待者已阻塞」与「等待者已退出」会同时到达，主进程
永远抓不到阻塞窗口。改成 `ForEach-Object { ... Out-File -Append }` 逐行落盘。

## 验收对账

| 票据条目 | 结果 |
| --- | --- |
| control-server 有自己的 helper，互斥体名字逐字符相同 | ✅ `scripts/DesktopLock.psm1`；两仓自检各有一条断言守着字面量 |
| 该仓所有驱动交互式桌面的脚本都经这把锁，没有绕过的路径 | ✅ 四个入口（票据点名三个，grep 出第四个），锁在脚本内部不是包装器 |
| mes-ingest 的锁改为带超时等待，超时值可传参 | ✅ 默认 1800，两条获取路径都可传参 |
| 两个仓各有一条测试或脚本自检，证明第二个持有者会等待 | ✅ 各 6 条断言全 PASS，含时间下界与弃锁接手 |
| 在两个仓同时发起桌面作业，实测第二个排队后成功 | ✅ 跨仓双向 7.9s；端到端 L2 真装置排队后 PASS |
| CI 不出现因互斥导致的红 | ⚠️ **见下，未在 CI 上实跑** |
| 不触碰 mes-ingest 的需求条目与既有 workflow 语义 | ✅ 只改超时预算与注释，触发条件、runner 标签、`concurrency`、`cancel-in-progress` 一律没动 |

## 未做的一件事：CI 上的实跑

最后那条验收要在 `win11-01` 上真的让两个仓的 workflow 撞一次，而那需要把两个分支推上去触发。
**推不推由用户定，本会话没推过任何东西**，所以这条停在这里。

需要时的做法：推 `fp/batch-2`（mes-ingest）与 `fp/v2-impl`（control-server），手动 dispatch
`desktop-tests.yml`，同时在客户机上手动跑一次 L2 真装置场景，看两边日志里的
`DESKTOP_LOCK_WAITING` / `DESKTOP_LOCK_ACQUIRED` 配对。锁语义本身已经在本机验证过三层，CI 那次
验证的是**调度层面**：`timeout-minutes` 的新预算够不够，以及排队会不会撞上 job 超时。

另外注意 control-server 现在**没有任何 workflow 会取这把锁**——`l2.yml` 跑在 `headless` runner
上、只跑四条合成场景。所以「CI 撞车」目前只可能发生在「人手动跑 real-onboard/staged G3」与
「mes-ingest 的桌面 workflow」之间。`l2.yml` 那段过时注释已经改成「排他性不再是阻塞点，要不要把
真装置场景挪到 `golden-renderer` runner 是调度与容量决定」——**那是票 17／18 的事，本票不做**。

## 给下游票的指针

- **票 17／18**：真装置场景挪 CI 的机制障碍已清。剩下的是容量与调度：`golden-renderer` runner 是
  mes-ingest 独占的（它是那个仓注册的 runner），control-server 要用得先在那台机器上装第四个
  runner 实例并打 `golden-renderer` 标签——工作区 CLAUDE.md 记着「一个 runner 只能绑一个仓库」。
  **加了 runner 记得回去改工作区 CLAUDE.md 的 runner 表**，它漏记过两个 runner。
- **任何新增会起 WPF 的脚本**：`Import-Module scripts/DesktopLock.psm1` 后 Enter/Exit，取锁点放在
  第一个 WPF 进程之前，释放放 `finally` 最后。control-server 的 `CLAUDE.md` 已写进这条。
- **改名字的那天**：两个仓一起改，两个自检里的字面量一起改。名字漂移没有任何症状，只表现为两套
  桌面测试偶尔一起跑。

## 证据

| 什么 | 在哪 |
| --- | --- |
| L2 合成回归 | `evidence/l2/20260908-ticket01-normal-load-01`（PASS） |
| L2 真装置，无争抢 | `evidence/l2/20260908-ticket01-real-onboard-normal-load-01`（PASS，`timeline.jsonl` 有 `Interactive desktop lock acquired.`） |
| L2 真装置，排在 mes-ingest 后面 | `evidence/l2/20260908-ticket01-real-onboard-normal-load-queued-02`（PASS） |

自检随时可复跑，各约 15 秒：

```
pwsh -NoProfile -File 8005-mes-ingest/Test-DesktopLockQueueing.ps1
pwsh -NoProfile -File 8005-agv-control-server/scripts/Test-DesktopLockQueueing.ps1
```
