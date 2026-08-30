# 把发布候选重建到含票 22／24 修复的 commit

Type: task
Mode: AFK
Status: resolved
Blocked by: 22, 24

## Question

票 11 交付的 RC（`C:\Users\szy\Desktop\w2g-rc-20260830`）绑 `ControlServer_MVP@2eeb6f0`，其后落了 7 个
commit，其中 `127b137` 改了产品代码 `src/.../Persistence/WireToGateStore.cs`（票 22 的 revision
跨趟修复），`1fd23ac` 给发布脚本加了 `Assert-ReleaseScanGate`（票 24）。因此现有 RC 是一份
**已知会在同一台 AGV 第二趟被车载端以 `SNAPSHOT_REVISION_REGRESSION` 拒绝**、且未经扫描闸门的
二进制。

如何从 `ControlServer_MVP@d243abf` + `OnboardHmi_MVP@304e6ad` + `protocol-v0.1.1` 重建 RC，证明
新产物确实包含票 22 的修复、确实通过了票 24 的扫描闸门，并给票 13／12 一个可部署、身份可回读的
候选？

约束：不改产品代码、不动车、不建单、不触 RIoT、不使用现场凭据；车载端仓保持只读（脚本从一次性
克隆构建）；协议身份必须从产物读回而不是复述；旧 RC 在新 RC 验证通过前不得删除。

## Answer

**新 RC 已建成并验证：`C:\Users\szy\Desktop\w2g-rc-20260830-d243abf`，272 MB，868 个文件。**
证据在 ControlServer 仓 `evidence/rc/20260830-issue25-rebuild-d243abf/`
（`SUMMARY.md` + `build-run.log` + `release-artifacts/`）。

### 身份（从产物读回，非复述）

| 项 | 值 |
| --- | --- |
| ControlServer | `d243abfc48fe7229f2f8e29374e20b930dd4c8d3` |
| OnboardHmi | `304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6` |
| 协议 | `protocol-v0.1.1` @ `1531489e…0279`，取自 `controlserver/appsettings.json:ProtocolCandidate` |
| release-manifest.json | `d680ca2adef2ec920ed5f9944591b593d3535cd9793673c8375291a64f3009d9` |
| SHA256SUMS.txt | `e195f8fd74d995447b6ea3df0e011ee88e43735fc25a44aeb92db6f0585aafc7` |

协议侧九个字段（tag／commit／releaseVersion／三个 SHA／profileId／approvalStatus／identitySource）
与 `2eeb6f0` 那份 manifest **逐字相同**——只有服务端动了。

### 本票最重要的一件事：原定判据被自己的对照证伪

第一版判据是「重建后的 `ControlServer.Infrastructure.dll` 哈希必须与 `2eeb6f0` 的不同」。它的
对照是车载端程序集——**同一个 commit `304e6ad`、同一 SDK**，理应逐字相同：

| 产物 | `2eeb6f0` vs `d243abf` |
| --- | --- |
| `ControlServer.Infrastructure.dll` | DIFF |
| `ControlServer.{Application,Domain,Host}.dll` | DIFF |
| `onboard-hmi/SQCD.Agv.Wpf.dll`（同源） | **DIFF** |
| `onboard-hmi/SQCD.Agv.Wpf.exe`（apphost） | SAME |

同源托管程序集也 DIFF ⇒ 此处托管构建**不可复现**（每次新 MVID）。所以「哈希变了」对内容
**什么都不能证明**，该判据被弃用而不是当证据报出去。apphost `.exe` 相同，说明差异确实来自
托管元数据而非环境噪声。

### 改用的真判据：修复的符号在出厂字节里

`127b137` 引入新私有方法 `SeedSnapshotRevisionsAsync`，方法名写进程序集元数据字符串堆：

| 符号 | `2eeb6f0` 产物 | `d243abf` 产物 |
| --- | --- | --- |
| `SeedSnapshotRevisionsAsync`（`127b137` 新增） | ABSENT | **PRESENT** |
| `GetNextSessionGenerationAsync`（既有） | PRESENT | PRESENT |

**红侧就是第一行左格**：同一套检索、同一文件布局，对缺修复的那份返回 ABSENT，证明检索不是
「什么都匹配」；第二行证明检索在旧产物里确实找得到符号，故那个 ABSENT 是真阴性而非坏读取。

这是**元数据级**证明，不是行为级——没有任何旅程跑在这份产物上。修复本身的行为证据仍是
`d243abf` 的 tier 1（243 passed / 0 skipped，含 `127b137` 新增且各自证过红的
`JourneyRuntimeWorkerTests` 断言）。

### 其余闸门

- **构建 0 warning**：脚本对两端 publish 的 warning 数 >0 直接 throw（257–259、290–292 行），
  退出码 0 即两端 0 warning。
- **扫描闸门实际执行且通过**：`Secret scan findings: 0; key material files: 0`，
  `Scan gate: PASS`，允许清单只有三个具名 RIoT SDK 包。票 24 已证该闸门会红。
- **868 条哈希全量回验 ALL OK**，并证明会红：对 `appsettings.json` 的**副本**追加一个字节，
  同一条校验由 GREEN 变 RED；产物本身未被修改。归档副本在提交前重新哈希，仍等于上表两个根值。

### 边界（本票不成立的部分）

- **未安装、未启动、未建会话、未跑旅程**。隔离安装验证属票 13／12。
- 车载端默认配置里的 `onboardBuildCommit` 仍过期（manifest 记为 `a6f05fbc…1821e`，非 `304e6ad`），
  归只读的车载端仓，本次重建不改变该发现。
- **旧 RC 未删**，两份并存于 `C:\Users\szy\Desktop\`。
- 一次性克隆目录 `w2g-rc-20260830-d243abf-onboard-src`（167 MB）保留未删，可复现、可安全删除。
- 车载端仓**零写入**：本地克隆仍 `bbfbc52`、工作区干净，脚本从自己的一次性克隆构建。
- 未动车、未建单、未触 RIoT、未用现场凭据、**未触产品代码**（故未跑 tier 1）。
