# 把 G3 runner 对齐到明文车载端 238b46e

Type: task
Mode: AFK（改脚本与静态取证）；若决定实跑 staged G3，该次运行另议成本
Status: open
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
