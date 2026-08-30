# 收口票 21 记录的五项脚本／证据层偏差

Type: task
Mode: AFK
Status: resolved
Blocked by: 21

## Question

票 21 的复核除两个产品代码缺陷（已由票 22 收口）外，另记录了五项**脚本与证据层**偏差。它们不触及
产品代码、不需 tier 1，票 21 与票 22 都明确要求另开一票处理，以免一次 tier 1 同时承载产品与脚本
两类改动。完整判据见 [票 21 的 `## Answer`](21-review-the-unreviewed-server-and-runner-changes.md)，
此处只列条目：

1. **票 20 留了一个等价的漂移口**：`run-staged-g3-restart.ps1` 的 `param()` 保留
   `$CommitBindingSource`，指向一份带旧 commit 的脚本副本即可让整轮证据宣称错误绑定而不报错。
   现有缓解只有 `configuration.json` 里记的源路径 + SHA-256。
2. **票 11 的「二十六条断言」只是 markdown 表格**：`install-result.json` 只有 9 条 `checks`
   字符串，第 1–6、19–26 条无机器可读落点；与 18／19／20 三票的 `assertions` 数组做法不一致。
3. **票 11 的证据目录缺关键产物**：`evidence/rc/` 下没有 `release-manifest.json`、
   `SHA256SUMS.txt`、`inventory/dependencies-*.json`、`secret-scan.json`。
4. **`New-WireToGateReleaseCandidate.ps1` 的扫描结果不设闸**：`secretScan.totalFindingCount` 与
   `unresolvedLicenseCount` 只写进 JSON，源码含 `"apiKey": "…"` 时脚本仍 PASS 出包；
   另 `Get-PackageLicense` 硬编码 `$env:USERPROFILE\.nuget\packages`，设了 `NUGET_PACKAGES` 的
   机器上许可清单会全 UNRESOLVED。
5. **三个 runner 逐字复制公共函数**，而 `run-demand-bearing-g3-vectors.ps1` 改用 AST 抓另一脚本的
   函数体与 here-string——重命名函数或把 here-string 从 `@'…'@` 改成 `@"…"@` 会让它启动即抛错。

**要决定的是：哪几项在本轮截止前值得做，各自的最小修法是什么。** 第 4 项直接关系发布物可信度，
优先级最高；第 1、5 项关系证据可信度与脚本脆性；第 2、3 项是补记录。

### 完成判据

- 逐项给出「做／不做」与理由，不做的写明风险由谁承担；
- 做的部分：改动归 ControlServer 仓，本票只留路由指针；
- 脚本改动须有可证伪的验证（例如第 4 项：植入一条假秘密，证明改前 PASS、改后 FAIL）；
- **不触及产品代码**。若发现必须改产品代码，停下另开票，不要并进本票。

### 注意

- 本票是否应挡住票 12（授权发布）由用户决定。第 4 项若不修，则发布脚本的秘密扫描与许可证清单
  不构成闸门，这一点须在放行时明确写下。

## Answer

逐项决定：**做 1、3、4，不做 2、5。**第 4 项是本票的主体。未触及产品代码，未跑 tier 1。

### 第 4 项（做）：扫描结果现在是闸门

`New-WireToGateReleaseCandidate.ps1` 新增 `Assert-ReleaseScanGate`，在 `inventory/` 落盘之后、
生成 manifest 之前调用。命中以下任一条即中止：任何扫描 finding、任何密钥材料文件、任何**不在
具名允许清单内**的包解析不出许可证。

允许清单只有 `RIoT.Sdk.Core`／`Facade`／`Generated` 三个本项目自建包——就是票 11 finding #3 已
报告的那三个，**逐个具名而不是给一个计数上限**，所以新出现的无许可证依赖会让发布失败而不是悄悄
并进计数。位置选在 manifest 之前是有意的：失败时 `inventory/` 已落盘可供定位，但绝不产出
manifest、`SHA256SUMS.txt` 或任何能宣称通过的包。失败信息只给「路径:行号:规则名」——扫描自己写着
`matchedValuesDisclosed = false`，把命中内容打进报错等于把秘密打进每一条控制台和 CI 日志。

`Get-PackageLicense` 的 `$env:USERPROFILE\.nuget\packages` 硬编码换成 `Get-NuGetGlobalPackagesRoot`，
先看 `NUGET_PACKAGES`。这两条本来是**互相掩护**的：设了 `NUGET_PACKAGES` 的机器上全部许可证读成
UNRESOLVED，而没有闸门时照常出包，谁也不会发现。

### 第 1 项（做）：漂移口拆掉

`run-staged-g3-restart.ps1` 的 `$CommitBindingSource` 从 `param()` 移除，改成 `$PSScriptRoot`
相对的固定常量。票 20 的自述（「留了覆盖口就等于留了漂移口」）现在与代码一致。读回的四个 commit
一字未变——这次改的是「谁能指定路径」，不是「绑定到哪个 commit」。

### 第 3 项（做）：产物归档

`release-manifest.json`、`SHA256SUMS.txt`、`inventory/` 三份 JSON 已抄进
`evidence/rc/20260830-isolated-install-2eeb6f0/release-artifacts/`。**归档前先验证它们仍然哈希到
票 11 SUMMARY 记的那两个值**（`97468cae…5aec1`、`221ea67c…6e3ec`），所以这是那一次运行自己的产物，
不是重新构建的。SUMMARY 的 Files 表已补，并明写「当时第 26 条只是计数不是闸门」。

归档时撞到一件本身就是证据完整性问题的事：本仓 `.gitattributes` 默认 `* text=auto eol=lf`，
第一次提交把 `release-manifest.json` 存成 162,774 字节而不是 171,544，**checkout 出来的哈希不再是
证据宣称的那个值**。已加 `evidence/rc/*/release-artifacts/** -text`，并从对象库回读验证两份文件
确实哈希回 `97468cae…` 与 `221ea67c…`。

### 第 2 项（不做）：不事后补造机器可读记录

票 11 那 26 条是对一次**已经发生**的安装运行的观测。现在把 markdown 表格转写成 `assertions` 数组，
产出的不是观测记录而是转写，却长得像 harness 输出——**比诚实的 markdown 表格更坏**，因为它会被后来
的人当成机器产出来引用。真正的修法是下一次安装验证自己发射这个数组，那需要重跑隔离安装，属票 13／12
的范围。

风险由用户在授权发布时承担：票 11 的第 1–6、19–26 条只能靠重跑复核，不能靠读 JSON 复核。本轮的部分
缓解是第 3、4 两项——第 6、26 条背后的产物现在仓内可查，第 26 条从计数升成闸门。

### 第 5 项（不做）：三个 runner 的重复函数不在本轮抽公共模块

失败形态是**启动即抛异常**，响亮且立刻，不是静默污染证据。而抽公共模块要同时动三个 runner
（166 KB + 42 KB + 38 KB），它们零测试覆盖，且本地图其它票的证据全部绑在它们的输出上——那里的回归
只会在下一次证据运行时才暴露。截止前三小时做这个，风险大于收益。

风险由改名 `Get-SharedCommitBinding` 或改动 harness here-string 引号形式的人承担：他们会立刻拿到
崩溃，而不是错误的证据。建议 RC 之后另开一票处理。

### 可证伪验证

两个 harness 都用 **AST 从提交进仓的脚本里把规则、扫描和闸门原地取出**，跑的是要发布的代码而不是
副本，并与 `0e4d471` 基线的同名函数并排对比。绿断言在证明能变红之前不算证据，红侧是**直接断言**
出来的，不是推定的：

| Harness | 结果 |
| --- | --- |
| `Test-ReleaseScanGate.ps1` → `scan-gate-result.json` | **PASS 12/12** |
| `Test-CommitBindingPort.ps1` → `commit-binding-port-result.json` | **PASS 5/5** |

- 植入 `"apiKey"` 字面量被检出并**抛错**（3、4、11），基线被证明**根本没有闸门**（8）；
- `.pfx` 抛错（6）；未列入清单的 UNRESOLVED 抛错、三个允许的不抛（7）；
- 断言报错信息**不含**植入值、只含 `路径:行号`（5）；
- `Get-PackageLicense` 现在能经 `NUGET_PACKAGES` 解析（9），基线对同一个包返回 `UNRESOLVED`（10）；
- 重启 runner 的覆盖参数在基线存在（1）、现在不再可绑定（2、3），读回的四个 commit 不变（4）；
  并且**证明了 reader 会毫无怨言地接受一份带假 commit 的副本**（5）——这正是那个路径不能由调用方
  指定的理由。

闸门**不追溯**已经存在的那份包，所以第 12 条改用它自己的归档 inventory 来回答「它会不会被拦」：
`2eeb6f0` 那份 RC **通过**——0 findings、0 密钥材料文件、3 个 UNRESOLVED 恰好就是允许清单里的
RIoT SDK。它不会被拦。

两个 harness 都不构建、不安装、不运行 RC；`Get-Command -Syntax` 只解析 param 块，重启 runner 一条
语句都没执行。

### 对票 12 的影响

第 4 项已修，所以「放行时须明确写下发布脚本的扫描不构成闸门」这句**不再需要写**——它现在构成闸门，
并已写进 `docs/RELEASE-CANDIDATE.md` §10。剩下的第 2、5 两项不足以挡住授权发布：一个是证据格式，
一个是响亮失败。**建议本票不阻断票 12**，但是否阻断仍由用户决定。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server
Owner artifact: `evidence/rc/20260830-issue24-scan-gate/`（README + 两份 harness + 两份结果 JSON）、
`evidence/rc/20260830-isolated-install-2eeb6f0/release-artifacts/`
Impact on this ticket: 已解决。改动与证据归 ControlServer 仓，本票只留决策记录与路由指针。
