# 17 — `FP-IS-00`～`07` 在 v2 下重证

**做什么：** 把八个批次 0 切片在协议 v2 下重新证一遍，三道门禁全 PASS：
`CONTROL_SERVER_G2`、`ONBOARD_HMI_G2`、`G3`。这是**批次 2 轨 A 的出口**。

八个切片与 `W2G-IS-00`～`07` 一一对应，关系是「**v2 下的重证**」而不是「可以沿用的通过
结论」——`ConformanceRunIdentity` 已规定任一绑定分量变化都必须建立新运行。

**而且根本没有通过结论可以沿用**：`RELEASE-CANDIDATE.md` 第 12 节末原文写着
`W2G-IS-00`～`07` 与 RC 目前仍为 `INCONCLUSIVE`，八类 G3 向量各有证据不等于八个切片通过。
**证据与说明里都不得暗示存在可沿用的通过结论。**

`ONBOARD_HMI_G2` 自 2026-09-04 起由我方跑、我方填那一列，不再等 Kun Wang。**但这不改变
谁签发布**——release attestation 仍要两名不同产品负责人。

**排期提示（不是硬依赖）**：G2 与 G3 证据绑定精确 commit。轨 B 的能力票会持续改服务端，
建议把这八个切片的重证放在一个**连续窗口**内跑完，窗口内轨 B 暂缓合并；或等轨 B 的票
09～13 合完再跑。两种都行，别边跑边合。

**前置：** 票 14（服务端 v2）、票 15（车载端 v2）、票 16（`vectorId` 绑定守卫）。

**票 16 于 2026-09-08 完成，这一条前置解除**（见 [16-answer.md](16-answer.md)）。守卫落在
控制端 `562544e`，CI 绿（run
[34227325616](https://github.com/trytoreachpeak0/8005-agv-control-server/actions/runs/34227325616)，
`569 passed / 0 failed / 0 skipped`）。**票 14、15 仍未完成，本票尚不可开工。**

票 16 转交本票一件事：`CV-LOAD-CANCELLATION-ALL-EMPTY` 是它 20 条绑定里最薄的一条——服务端
取消面（`OnboardRecoveryCoordinator.AuthorizeLoadCancellationAsync`）只有
`FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 一条测试覆盖，
且走的是 `REJECTED` 分支，只证了 `AUTHORIZE_CANCELLATION_EXPLICITLY` 那一半；
`RECONCILE_EMPTY_FINAL_STATE` 那一半在实现里（同文件 `safeEmpty` 判据）但没有独立测试。
**`FP-IS-02` 重证时应当补上。**

**状态：** ready-for-agent

- [ ] 八个切片各跑一遍 `CONTROL_SERVER_G2`，八份 `gate-result.json` 全 PASS
- [ ] 八个切片各跑一遍 `ONBOARD_HMI_G2`，八份 `gate-result.json` 全 PASS
- [ ] 八个切片各跑一遍 `G3`，全 PASS
- [ ] 每份 `gate-result.json` 绑定精确的 `ProtocolReleaseIdentity`（v2 三元组）
- [ ] 证据落在 `evidence/g2/<日期>-<描述>/<FP-IS-NN>/` 与 `evidence/g3/<日期>-<描述>/`
- [ ] `-EvidenceRoot` 是不存在的目录；红的证据不被绿的重跑覆盖；失败时 stage root 不删
- [ ] 证据目录只增不改——若需纠正，写新目录并在 `SUMMARY.md` 里指向被纠正的那份
- [ ] 车载端侧的门禁跑在我方 `w2g/*` 分支上，commit 绑定如实记录
- [ ] 证据与说明中不出现「沿用已通过结论」这类表述
