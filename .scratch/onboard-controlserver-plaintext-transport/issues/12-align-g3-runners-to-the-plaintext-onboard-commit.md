# 把 G3 runner 对齐到明文车载端 238b46e

Type: task
Mode: AFK（改脚本与静态取证）；若决定实跑 staged G3，该次运行另议成本
Status: resolved
Blocked by: 06

## Question

票 06 把车载端身份固定为 `OnboardHmi_MVP@238b46e` 之后，`8005-agv-control-server`（可写）的三个
G3 runner 仍指向 TLS 期车载端，且其中一个在明文车载端上会直接失败。本票让它们与新车载端对齐。

### 已具名的两处，来自票 06 的只读核验

**(1) `scripts/run-staged-g3-restart.ps1:508` 无条件赋值一个已被删除的键。**

```powershell
$settings = Get-Content -LiteralPath $onboardConfig -Raw | ConvertFrom-Json
...
$settings.wireToGate.useTls = $false          # 第 508 行
```

票 03 的提交 `991cb8e` 已把另两处改成「属性存在才碰」的条件式（`run-staged-g3.ps1:2167`、
`Invoke-AuthorizedAbsentObservationShadow.ps1:558`），唯独漏了这一处——那两处原本写 `$true`，
改值时被看到；restart runner 本来就写 `$false`，值不用改，整行被跳过。

失效形态已由票 06 在 pwsh 7 上实测：`ConvertFrom-Json` 得到的是 `PSCustomObject`，给不存在的属性赋值
抛 `SetValueInvocationException: The property 'useTls' cannot be found on this object.`，脚本在
`publish` 之后、配置写回之前中断。**不是**票 05 §5.4 描述的「静默写回错键」。即便赋值通过，
车载端 `238b46e` 新增的 `RejectRemovedTransportKeys` 也会因该键存在而拒绝启动，是第二道。

目标形态：与另两个 runner 一致的条件式，并顺带核对是否也需要处理 `serverCertificateSha256`
（restart runner 用的是车载端 dev `appsettings.json`，该文件本就无此键，但要读代码确认而不是假定）。

**(2) `scripts/run-staged-g3.ps1:12` 的默认 `$OnboardCommit` 是 `304e6ad9952a…`。**

那是 `31263b1` 的**父提交**，比票 27 的可见性修复还早，更不含明文改造。改锁到
`238b46eb2c9ae90584e4288a782176f66b7de942`。

注意杠杆：`run-staged-g3-restart.ps1` 的 `Get-SharedCommitBinding`（第 27 行）与
`run-demand-bearing-g3-vectors.ps1`（第 75–81 行，`$CommitBindingFunctionSource` 指回 restart runner）
都是从 `run-staged-g3.ps1` **解析**这四个默认值，不各自持有副本。因此这一处改动会同时改变三个 runner
的绑定——这既是省事，也意味着改错会同时打穿三个。`run-demand-bearing-g3-vectors.ps1:84` 还对
函数源文件取 SHA256 写进证据，改动会改变该哈希，属预期。

### 本票要回答的第三件事：改完之后跑不跑

三个 runner 的**实际可运行性至今未证**（这是地图「Not yet specified」第一条的剩余部分）。票 03 只证了
安装链，票 02 只证了服务端单侧。选项：

- 只做静态改动 + 静态取证，把实跑推给票 07 的跨机联调；
- 或在本票就跑一次 staged G3，把 runner 可运行性与明文两端联通性一并证掉。

staged G3 要 publish 三个仓、起代理与服务，成本不低。**本票先给出建议与成本，由用户定**，不要
自行开跑。

## 判据设计要求

- 改动判据必须是回读取证：改后重读该行，并用与票 06 相同的 pwsh 语义验证——同构 JSON 输入下
  条件式写法不抛异常且写回不含该键；
- 红侧：把条件保护删掉（或在无 `useTls` 的输入上跑原写法）必须重现
  `SetValueInvocationException`，证明这条判据会响；
- commit 锁定判据：改后 `Get-SharedCommitBinding` 解析出的 `OnboardCommit` 必须等于 `238b46e…` 全长值，
  且三个 runner 读到的是同一个值；红侧是在改前解析应得到 `304e6ad…`；
- 若决定实跑，按仓内既有 G3 证据惯例落证据目录，并显式记录本轮与上一轮的差异（无 TLS 代理、
  无临时信任根）。

## 不在本票范围

- `docs/RELEASE-CANDIDATE.md` 里仍在讲 `serverCertificateSha256` 的三处（第 217／227／296 行）——归票 04。
- 车载端仓的任何写入。`238b46e` 已由票 06 核验，其自身的 `run-staged-g3-recovery-ack-drop.ps1`
  王昆已删掉对应行，不需要也不允许我们碰。

## Answer

两处具名改动均已完成并提交推送：`8005-agv-control-server@65841df`（分支 `ControlServer_MVP`，
`c80d2d3..65841df`）。工作树干净。车载端仓全程只做 `git cat-file`／`git show`／`rev-parse`，
写入为零，工作树 `git status --porcelain` 行数 = 0。

### 1. `run-staged-g3-restart.ps1` 的无条件赋值（原第 508 行）

改成与另两处一致的条件式，位置为改后第 515–517 行：

```powershell
if ($settings.wireToGate.PSObject.Properties.Name -contains 'useTls') {
    $settings.wireToGate.useTls = $false
}
```

**红侧（改前，实测）**：把 `238b46e` 的 `src/SQCD.Agv.Wpf/appsettings.json`（`ConvertFrom-Json` 后
`wireToGate` 无 `useTls`）喂给原写法，抛
`SetValueInvocationException: Exception setting "useTls": "The property 'useTls' cannot be found on
this object."`。检测器会响，与票 06 的机理一致。

**绿侧（改后，回读取证）**：从改后源文件按行抽出上面那三行原文并执行，同一输入不抛异常，
`ConvertTo-Json` 写回不含 `"useTls"`。全文再无未加保护的 `$settings.wireToGate.useTls = $false`。

**对照（证明这条保护不是恒假的空壳）**：同一段保护施加在 TLS 期车载端 `304e6ad` 的
`appsettings.json`（该文件确有 `"useTls": false`）上，先把值置为 `$true` 再执行，出来是 `False`
——分支确实进得去，赋值确实生效。

**`serverCertificateSha256`：核实为不需要处理，不是假定。** 回读两侧的 `src/SQCD.Agv.Wpf/appsettings.json`：
`238b46e` 与 `304e6ad` 都不含该键（Development 环境本就不设指纹）。restart runner 改写的正是这个文件，
所以对它加删除保护是死代码。理由已写进代码注释。`run-staged-g3.ps1:2170` 那处对称保护保持原样不动
（它同样改写这个文件，同样用不上，但那是票 03 的既成事实，不在本票范围）。

### 2. 共享 commit 绑定移到 `238b46e`

`run-staged-g3.ps1:12` 的 `$OnboardCommit` 改为 `238b46eb2c9ae90584e4288a782176f66b7de942`。
三个 reader 各按自己的真实解析链读，结果一致：

| reader | 解析路径 | 读到的 `OnboardCommit` |
| --- | --- | --- |
| A `run-staged-g3.ps1` | 自身 param block 默认值 | `238b46eb…de942` |
| B `run-staged-g3-restart.ps1` | 自身 `Get-SharedCommitBinding`（AST 提取后执行）解析 A | `238b46eb…de942` |
| C `run-demand-bearing-g3-vectors.ps1` | 自身 `Get-ScriptFunction` 从 B 取函数，再解析 A | `238b46eb…de942` |

C 的两个默认参数回读确认仍是 `(Join-Path $PSScriptRoot 'run-staged-g3.ps1')` 与
`(Join-Path $PSScriptRoot 'run-staged-g3-restart.ps1')`，即杠杆链未被绕开。
其余三个 commit（`3d8b00c7…`／`fb5f7c59…`／`1531489e…`）逐字未变。
**红侧**：同一套解析在改前跑，三处都得到 `304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6`。

`run-demand-bearing-g3-vectors.ps1:84` 对 `run-staged-g3-restart.ps1` 取 SHA256 写进证据，本次改动
改变了该哈希，属预期。三个 runner 改后 `Parser::ParseFile` 均 `parseErrors=0`。

远端一致性：`origin/OnboardHmi_MVP` 当前 tip 就是 `238b46e`，两个 runner 的
`New-ExactClone -RemoteRef 'origin/OnboardHmi_MVP'` 会硬校验 tip 等于绑定值。**副作用要记住**：
王昆一旦再往该分支推一个提交，三个 runner 立刻以 `onboard-hmi remote ref mismatch` 失败，
这是设计意图（逐字身份），不是回归。

### 3. 改完之后跑不跑 staged G3——建议：**不在本票跑**，等票 08 之后

先说一件本票发现、改绑定时才浮出来的阻塞：

> **`$ControlServerCommit` 仍锁 `3d8b00c7…`，那是 TLS 期的服务端**（`fix: publish each stop's
> worklist under its own revision`），既不含票 02 的 `ae4a17d`，也不含票 03 的 `c7874f0`。
> 只改 `OnboardCommit` 的结果是「TLS 期服务端 ＋ 明文车载端」，必然握不上手。
> **任何一次 staged G3 实跑之前，必须先把 `ControlServerCommit` 也移到含明文改造的服务端提交。**

本票没有顺手改它，因为它锁哪个值取决于实跑当刻的服务端身份，而服务端身份要到**票 08 重建发布候选**
才定下来；现在锁一个中间提交（比如本票的 `65841df`），票 08 一落地就作废，等于多一次自指的绑定更新。

**成本（本机实测口径的估算，未跑）**：三个仓 exact clone ＋ 协议仓 G1 的 node/pnpm 依赖安装 ＋
三个 .NET 项目 Release publish（冷构建）＋ simulator／ControlServer／WPF 车载端／代理起停 ＋
多阶段稳定窗口采样，单次 **20–40 分钟**；`run-staged-g3.ps1` 要在交互桌面上起 WPF 车载端，会占住
前台（restart runner 与 vectors runner 声称可无人值守）。vectors runner 还额外需要一份授权现场
run 的 `controlserver.db` 作为 `-FieldRunRoot`。

**为什么建议推后而不是现在跑**：

1. 前置条件未满足（上面那条），现在跑要先做一次注定作废的绑定更新；
2. staged G3 是**同机 loopback**，证不了 Destination 要的「异机明文」形态——那是票 07；
3. 现在跑的增量信息只有「runner 本身还能跑」，而 runner 真正要服务的场合在票 08／09 附近，
   到那时服务端身份已定，一次跑同时兑现「runner 可运行」与「候选身份可 staged 验证」两件事。

**给用户的三个选项**（本票只出建议，决定权在用户）：

- **A（推荐）**：推到票 08 之后。届时把 `ControlServerCommit` 锁到发布候选提交，一次跑掉。
- **B**：现在就跑一次冒烟。先把 `ControlServerCommit` 临时锁到 `65841df`，跑 `run-staged-g3-restart.ps1`
  （最便宜、可无人值守、且它正是本票修掉那处失败的 runner），只为证明 runner 链路还活着；
  票 08 之后再更新绑定。成本 20–40 分钟。
- **C**：并进票 07。跨机联调那次顺带在同机先跑一遍作前置烟测。

### 不在本票范围（复核后仍成立）

- `docs/RELEASE-CANDIDATE.md` 第 217／227／296 行的 `serverCertificateSha256`——归票 04；
- 车载端仓任何写入——零写入已取证。

### 本票另发现（未改，供后续票取用）

`run-staged-g3.ps1` 里仍有 TLS 期**命名与叙述**残留，均不影响行为：合成对端类名
`StagedG3TlsHarness`（第 226 行定义，被三个 runner 引用）、第 2045 行讲历史的注释。证据字段
`tls = $false`／`certificatesGenerated = $false`／`temporaryTrustRootInstalled = $false` 是有意
记录本轮无 TLS 的，应保留。改类名会同时改动三个 runner 与 vectors runner 第 65 行的 here-string
匹配串，是一次纯改名但打击面等于本票的杠杆面，不该混在本票里。
（本票只顺手改掉了 restart runner 头部一条**已经失真**的注释：它声称自己是唯一不需要交互确认的
runner，票 03 拆完证书后 `run-staged-g3.ps1` 同样不装信任根。）

### 第 3 节的决定（用户 2026-08-31）

用户选 **A：推到票 08 之后**。实跑连同 `ControlServerCommit` 的更新已落为
[`在明文绑定上实跑 staged G3`](13-run-staged-g3-on-the-plaintext-binding.md)（`Blocked by: 08`）。
本票不再持有该待决项。
