# 在车载端只读仓创建对应的版本 tag

Type: task
Mode: HITL
Status: resolved
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

2026-08-30 更新（票 27 会话只读 fetch 所得）：`OnboardHmi_MVP` 的 tip **已不再是 `304e6ad`**，
owner 于当日 20:06 推送 `31263b1`（`Fix production W2G HMI status and recovery visibility`）。因此
「给本轮 MVP 打 tag」必须显式指向 `304e6ad`，不能用 `HEAD` 或分支名——那会把一个**不在本 RC 二进制
内**的修复错标成本轮版本。票 27 的答案已确认该修复不在本资产内。该仓仍为零 tag、零 release。

Impact on this ticket: 不影响已发布的服务端 release 可用性与版本可追溯性；影响的是车载端仓自身是否
有不可变引用。

## Answer

**tag 已创建，由用户执行，agent 对该仓全程零写入。** 三个待决问题的答案：由**用户本人**（仓 owner）创建、
tag 名与服务端一致取 **`w2g-mvp-rc-0.1.0`**、**只建 annotated tag 不建 GitHub Release**。第四问「是否等
票 27」已由票 27 结案自行答掉：不等——可见性修复在 `31263b1`，本资产建自 `304e6ad`，二者本就不该同 tag。

三个决定各自的理由，都不是风格偏好：

- **执行方**。本票唯一的真实风险是**打错目标**：owner 于 08-30 20:06 推了 `31263b1`，谁顺手用 `HEAD`
  或分支名，谁就把一个不在 RC 二进制内的修复标成本轮版本。用户是仓 owner，权限确定且执行时点在手，
  agent 给出的命令把 40 位完整 SHA 写死，风险被消掉而不是被转达。
- **tag 名**。跨仓版本绑定的身份就是这一个 RC，三仓同名最容易对上。协议仓的 `protocol-v0.1.1` 是
  独立演进的资产版本、不是同一序列，不构成反例。
- **不建 Release**。缺的是「该仓自身的不可变引用」，annotated tag 已经足够；二进制资产已随服务端
  release 分发过一次，车载端再建一个空 Release 只是多一份要维护、且会与服务端说明漂移的正文——
  票 27 刚为「已知限制第 1 项」在包外改过一次说明，两头各写正是要避免的形态。

annotation 正文按服务端那条 tag 的格式写，并显式记下 **`31263b1` 不在此 tag 内**，让后来者从 tag 本身
就能看到这条边界，而不必回溯票据。

### 四条判据（全部回读取证，不是执行返回码）

| 判据 | 结果 |
| --- | --- |
| 远程 ref 类型与 peel | `refs/tags/w2g-mvp-rc-0.1.0` 是 tag 对象 `bee6224fba069af325bc33a39711c99f9bf212dd`，peel 出 commit `304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6`，与 `release-manifest.json` 的 `components.onboardHmi.commit` 逐字一致；tagger `Zhengyu Shao`，`2026-08-30T14:17:49Z` |
| 没有误指 tip | `merge-base --is-ancestor 31263b1 304e6ad` 返回非零 → `31263b1` **不在** tag 内 |
| annotation 逐字 | 去掉 GitHub API `.message` 侧那个多余尾空行后，本地正文与远程 sha256 同为 `0eb3bba868b6ec265f772b71164984e90a64851e583ebc1e2a4d693f2a2f91fe`，VERBATIM MATCH |
| 未越界 | 该仓 `releases` 仍 `[]`；`OnboardHmi_MVP@31263b1`、`main@bc56fa9` 与推 tag 前一致；本地克隆工作树干净；服务端 tag 对象仍 `0c4d11031afac203902c638dfe3fa9f3e57a05be`、三资产仍 `uploaded` 且尺寸不变（171,955 / 98,898 / 123,976,762）；协议仓两 tag 未动 |

**红侧证明绿不是空的**：在与绿侧**同一条**归一化（只去尾部空行）下，把本地正文首行的 `0.1.0` 改成
`0.1.9`，比对器立刻 DIFFERS。归一化没有被放松到让红侧也变绿。

### 具名残留

该 tag 只是不可变引用，**不携带二进制**。车载端产物的可复现性仍受票 25 那条已留档的事实约束——
托管构建每次新 MVID，从 `304e6ad` 重新构建**不会**得到与包内逐字节相同的程序集。要复核本轮车载端
二进制，权威来源是服务端 release 资产内那 868 条 SHA-256，不是从此 tag 重建。
