# 双仓协作契约

## 固定协作面

双方可以使用不同 AI、IDE、skill、分支提交习惯和任务工具，但必须共享以下身份：协议候选/Release 的完整 commit 与 manifest hash、IntegrationSliceId、双方产品 commit/build digest、标准 G1/G2/G3 命令、runner/result Schema 和证据目录。

每天至少在开始、候选变化和结束时交换一行状态：

```text
time | slice | protocolCommit/manifestSha256 | controlCommit/build | onboardCommit/build | G1 | controlG2 | onboardG2 | G3 | blocker | next
```

秘密、证书私钥和 CallApiKey 不进入状态行。

## 协议与切片状态机

1. `DRAFT`：协议资产可改，不允许产品端宣称锁定。
2. `CANDIDATE_FROZEN`：记录完整协议 commit/manifest/hash；双方只对这一候选实现当前切片。
3. `G1_PASS`：机器契约自洽；允许双方运行本端 G2，不构成正式发布。
4. `CONTROL_G2_PASS` / `ONBOARD_G2_PASS`：真实本端＋本仓 Fake 通过；任一端 FAIL 先在责任仓修复。
5. `CANDIDATE_G3_PASS`：精确两端构建真实对真实通过当前切片；允许进入依赖切片。
6. `HUMAN_APPROVED`：szy 与王昆本人确认精确协议 commit/manifest 和差异。
7. `PROTOCOL_RELEASED`：创建不可变 annotated tag/release；两端改为锁定完整 ProtocolReleaseIdentity。
8. `MVP_RC_ACCEPTED`：全部八个切片和发布 Definition of Done 通过，由用户接受软件候选。

G1、G2、G3 的执行顺序不替代 G0：依赖协议的生产合并和部署仍要求内容完整、身份精确且具有真实批准的不可变 ProtocolRelease。

## 每个切片的节奏

1. 双方确认同一候选身份与工作包。
2. 各自先写失败测试，再实现最小生产路径。
3. 任一端本地 G2 PASS 后立即发布绑定 commit/build 的结果，不等待整个端完成。
4. 两端均可运行时立即执行本切片 G3；失败由首个规范分歧定位责任端。
5. 修复只重跑受影响门禁和依赖切片；红色证据永久保留。
6. 当前切片 G3 PASS 后才能进入依赖切片；无依赖的切片可并行。

## 协议变更

任何字段 required/类型/枚举/含义、方向、交付类别、关联、去重、持久承诺、恢复顺序、错误语义或副作用变化都先停止产品实现并创建 ProtocolChangeProposal。Proposal 必须绑定 base/target 候选、兼容性、两端迁移和受影响向量；Schema、样例、错误码、向量、兼容性和 manifest 同步变化并重新 G1。两名开发者本人批准后形成新候选或 release。

以下内部变化无需协议提案：不改变可观察语义的重构、局部命名、日志文案、私有算法或性能优化；但仍须运行受影响本仓测试。

## 证据失效

协议身份、任一产品 commit/build digest、Fake、runner、向量集合、虚拟时间脚本或影响判定的配置发生变化，旧 PASS 对新候选失效。新运行使用新 runId；旧 PASS/FAIL/INCONCLUSIVE 不覆盖、不删除。

共同 G3 索引保存在 ControlServer 仓库建议路径 `requirements/acceptance/wire-to-gate/integration-slices/<IntegrationSliceId>/<runId>/`，并以哈希指向两端各自原始证据。

