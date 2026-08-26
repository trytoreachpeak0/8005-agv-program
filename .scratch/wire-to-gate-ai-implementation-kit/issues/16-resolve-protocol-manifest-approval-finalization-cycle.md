# 解决协议清单与批准记录的发布闭环

Type: grilling
Mode: HITL
Status: resolved
Blocked by: 06

## Question

两名真实协议负责人是否接受把“内容 manifest”和“发布批准证明”分离，消除当前治理中的自引用闭环？当前规则同时要求批准记录填写精确 `manifestSha256`，又要求 manifest 哈希批准记录自身；填写批准会改变 manifest，因而不存在稳定终值。

建议方案：内容 manifest 继续覆盖所有协议内容，但明确排除外部批准证明；批准证明作为 GitHub release asset 或独立 `attestations/release-approval.json`，绑定不可变候选 commit、内容 manifest SHA-256、两名负责人身份/时间/结论及证明自身哈希。正式 tag/release 元数据同时登记内容 manifest 与批准证明哈希。任何方案都必须由两名真实负责人明确接受并同步修改治理 Schema、G1 和发布说明；AI 不得代替批准，也不得在闭环未解除时创建正式 ProtocolRelease。

## Comments

### 2026-08-25T19:16:41+08:00 — 第一位负责人确认

- 审批身份：`trytoreachpeak0`
- 结论：明确接受“内容 manifest + 独立批准证明”的分离方案，并接受独立 `slots-simulator`、OnboardHmi 通过正式 `ModbusSlotIoProvider` 连接模拟器、HTTP 仅承担环境/故障注入且不提供业务开锁命令的配套架构方案。
- 批准的候选协议提交：`72ddde595165468520d9f3a46b25e4aa4eec0c3`
- 指定的第二位协议审批人：`SocialKKKK`
- 当前状态：等待 `SocialKKKK` 本人明确接受分离方案并批准精确候选提交；仅指定其身份不构成其批准。收到第二份本人确认前，不修改正式批准状态、不创建 tag/release，也不关闭本票。

### 2026-08-25 — 第二位负责人确认

- 审批身份：`SocialKKKK`
- 结论：本人明确接受“内容 manifest 与独立批准证明分离”的发布治理方案。
- 批准的候选协议提交：`72ddde595165468520d9f3a46b25e4aa4eec0c3`

## Answer

两名真实协议负责人 `trytoreachpeak0` 与 `SocialKKKK` 均接受消除自引用闭环的治理修订，并批准以候选提交 `72ddde595165468520d9f3a46b25e4aa4eec0c3` 为修改起点。最终决定如下：

- `manifest/release.json` 是审批中立的 `CONTENT_SNAPSHOT`，排除自身、整个 `attestations/`、Git/依赖目录和生成证据；内容 hash 不随审批证明变化。
- 仓库只跟踪 Schema 和空白 `attestations/release-approval.template.json`。最终 `release-approval.json` 不提交到 Git，而作为 GitHub Release Asset，绑定冻结的内容 commit、内容 manifest SHA-256、两名不同负责人身份/时间/明确结论。
- G1 独立校验内容 manifest 和审批证明；正式运行通过 `PROTOCOL_APPROVAL_ATTESTATION` 指向外部 asset，并输出 manifest 与 attestation 两个 SHA-256。attestation 不包含自身 hash；annotated tag 和 GitHub release 元数据外部登记两个 hash。
- 固定发布顺序为：冻结并推送内容 commit → 两人批准该精确 commit/hash → 生成并以 G1 校验外部 attestation → 创建指向内容 commit 的 annotated `protocol-v<SemVer>` tag 并登记两个 hash → 发布同一 attestation asset。

治理修改已推送协议仓库 `main@3ad309ffd5f9a48a6cf390b51a81da2f47c814dd`。重复生成得到稳定 manifest `92c19e74affe876902e1c64aa5cdbca845f5dbc93a8c82014a16627a26deb8d3`；候选 G1 PASS（59 Schema、54 消息、54 正例、1,341 反例、19 轨迹、8 切片），外部双审批合成夹具路径也已单独 PASS 后删除。真实 attestation 保持 `PENDING`，因为治理修改产生了新 commit；正式 `protocol-v0.1.0` 必须由两人再批准这个新精确 commit/hash，由后续票据处理。
