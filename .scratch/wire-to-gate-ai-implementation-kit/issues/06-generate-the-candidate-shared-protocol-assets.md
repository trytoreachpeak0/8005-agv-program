# 生成并验证完整 MVP 候选协议面

Type: task
Mode: AFK
Status: resolved
Blocked by: 01

## Question

如何依据已接受的消息面、协议治理、错误语义和契约向量要求，在第 1 天生成 W2G-IS-00～07 开发所需的完整核心协议候选：Envelope、复合身份、交付类别、错误结构、全部范围内 payload Schema、合法/非法样例、消息/轨迹向量、runner/result contract、切片索引、兼容性文件和空白的人类批准记录？

候选 manifest 必须明确全部 MVP messageType、Schema 与 IntegrationSliceId 覆盖；不得以空 Schema、宽松透传或“稍后补充”阻断核心切片开发。资产必须完整可哈希、无可用秘密、无伪造批准，并明确标记为候选而非 `ProtocolRelease`。

本票同时生成确定性 G1 校验入口并实际验证 Schema/manifest 引用、哈希、allowlist/denylist、错误码唯一性、样例、向量、八个切片覆盖和 runner/result contract。G1 成功不表示 G0、G2、G3、正式发布或现场通过。

## Answer

已在 `8005-agv-protocol/main` 生成、验证并推送完整的未批准候选包。初始资产提交为 `f18df89de1ba4fe45f0887b8c77e19246e7c1354`；票 07 首次真实运行 `dotnet test` 时发现 VSTest adapter 未登记，随后仅补充 `xunit.runner.visualstudio 3.1.5` 兼容矩阵并重建候选，当前精确提交为 `72ddde595165468520d9f3a46b25e4aa4eec0c3f`。

候选包固定为 `CANDIDATE_UNAPPROVED`，未填写两名负责人批准、未创建 tag 或 GitHub release。它包含 57 个 Schema、54 个范围内 `messageType`、54 个合法样例、1,341 个非法样例、19 条确定性轨迹向量、8 个 `IntegrationSliceId`、错误码注册表、runner/result contract、兼容性报告、实施版本矩阵和空白批准记录。开发工具锁定 Ajv `8.20.0`、ajv-formats `3.0.1` 与 pnpm lockfile；仓库以 `.gitattributes` 固定 LF，避免跨机换行改变哈希。

确定性 `pnpm g1` 对当前候选实测 `PASS`，候选 manifest SHA-256 为 `e878d89e820535fe1eb64b85681b9c2994fb98646309e6ba768219c5c8735f2e`，结果证据位于协议仓库 `evidence/g1-result.json`。G1 仅证明候选资产的结构、覆盖和哈希一致性，不表示 G0/G2/G3、负责人批准、正式协议发布、真实设备或现场资格通过。

实施时发现已接受治理存在自引用闭环：批准记录必须写入 manifest hash，但批准记录本身又被 manifest 哈希；任何填写都会再次改变 manifest hash。候选包已在 `docs/candidate-limitations.md` 明示该阻断，并新建票 16 要求真实负责人先批准非循环的外部证明方案。该问题解决前禁止正式 ProtocolRelease。
