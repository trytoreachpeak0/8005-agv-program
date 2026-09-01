# 最终批准并发布不可变协议版本

Type: grilling
Mode: HITL
Status: resolved
Blocked by: 16

## Question

协议负责人 `trytoreachpeak0` 与 `SocialKKKK` 是否分别批准治理修订后的精确内容提交 `3ad309ffd5f9a48a6cf390b51a81da2f47c814dd` 和内容 manifest SHA-256 `92c19e74affe876902e1c64aa5cdbca845f5dbc93a8c82014a16627a26deb8d3`，并授权依照已冻结的外部 attestation 流程创建 annotated tag / GitHub Release `protocol-v0.1.0`？

只有收到两名负责人对上述新 commit/hash 的本人明确批准后，才可生成外部 `release-approval.json`，以 `PROTOCOL_APPROVAL_ATTESTATION` 运行 G1，计算审批 asset hash，创建指向该内容 commit 的 annotated tag 并在 release 元数据登记 manifest/attestation 两个 hash。AI 不得代签；任一身份、hash、G1 或远程 tag 冲突都必须保持阻断。

## Comments

### 2026-08-25 — 两名负责人最终批准

- `trytoreachpeak0` 在本 HITL 会话中批准精确 commit `3ad309ffd5f9a48a6cf390b51a81da2f47c814dd`、内容 manifest SHA-256 `92c19e74affe876902e1c64aa5cdbca845f5dbc93a8c82014a16627a26deb8d3`，并授权发布 `protocol-v0.1.0`。
- `SocialKKKK` 本人明确回复并批准同一精确 commit/hash，授权发布 `protocol-v0.1.0`。
- 用户在 GitHub 最终提交前再次确认公开发布及上传包含两名负责人身份、批准时间和批准声明的外部 `release-approval.json`。

## Answer

两名真实负责人批准齐全后，已严格按冻结顺序完成不可变协议发布：

- 生成 Git 外部批准证明 `release-approval.json`，绑定精确内容 commit 与 manifest；
- 以 `PROTOCOL_APPROVAL_ATTESTATION` 运行正式 G1，结果 `PASS`：59 个 Schema、54 种消息、54 个正例、1,341 个反例、19 条轨迹和 8 个集成切片；
- 外部批准证明 SHA-256 为 `1ba217142b02614923bdc88a7fef0c3266ba3e954bc0d2b74ba509579c465f35`；
- 创建并推送 annotated tag `protocol-v0.1.0`，tag object `27ae39074911fdb2aa50518fe7da1341ffccfc02` 已由远程 peeled ref 回读确认指向获批 commit `3ad309ffd5f9a48a6cf390b51a81da2f47c814dd`；
- 已发布 [GitHub Release `protocol-v0.1.0`](https://github.com/trytoreachpeak0/8005-agv-protocol/releases/tag/protocol-v0.1.0)，release 元数据登记内容 manifest、批准证明、Schema bundle 与 vectors 的完整哈希；
- 已上传同一份 `release-approval.json`，GitHub 页面摘要与独立重新下载计算均得到 `1ba217142b02614923bdc88a7fef0c3266ba3e954bc0d2b74ba509579c465f35`；
- 协议仓库 `main` 仍干净并与 `origin/main` 一致，没有为生成证据增加未批准的新内容 commit。

本票解除票据“完成双端联合测试并修复跨仓缺陷”的协议发布阻断；G2/G3、真实 IO、目标硬件和工厂资格没有被本次发布扩大或暗示通过。
