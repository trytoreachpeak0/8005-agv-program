# 收口票 21 记录的五项脚本／证据层偏差

Type: task
Mode: AFK
Status: open
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
