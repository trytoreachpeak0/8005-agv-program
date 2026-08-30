# 在车载端只读仓创建对应的版本 tag

Type: task
Mode: HITL
Status: open
Blocked by:

## Question

服务端仓已发布 `w2g-mvp-rc-0.1.0`（绑 `9daeef4`），协议仓 `protocol-v0.1.1` 早已发布。三个版本绑定
仓库中只剩车载端 `8005-agv-onboard-hmi` 没有对应的 tag：本次 MVP 使用的
`OnboardHmi_MVP@304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6` 在该仓没有任何不可变引用，
该仓当前**零 tag、零 release**。

精确 commit 已经记录在服务端 release 资产的 `release-manifest.json` 里，因此版本可追溯性不缺；
缺的是该仓自身的不可变引用，以及「谁在什么时候创建它」这个决定。

该仓对 agent 只读，agent 不得在其中创建 tag、release、分支或提交。本票只承载用户侧的决定与执行
确认，不在该仓写入任何内容。

需要用户决定：由本人还是王昆创建、用什么 tag 名（服务端用 `w2g-mvp-rc-0.1.0`，协议仓用
`protocol-v0.1.1`）、是否同时建 GitHub Release，以及是否要等票 27 的 HMI 缺陷落定后再打。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-onboard-hmi

Routing status: read-only for agents；需用户或王昆执行

Impact on this ticket: 不影响已发布的服务端 release 可用性与版本可追溯性；影响的是车载端仓自身是否
有不可变引用。
