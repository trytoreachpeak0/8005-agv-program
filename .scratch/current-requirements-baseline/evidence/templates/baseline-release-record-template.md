# 当前需求基线发布记录模板

> 使用规则：本文件是版本化需求文件的不可变旁置发布记录，建议与其同目录保存为 `current-requirements-v<version>.release.md`。它在最终内容已经冻结、按 SHA-256 获批并提交 Git 后生成，因而不会要求版本文件保存自身哈希，也不会形成循环引用。发布记录提交后不可修改；更正元数据需按补丁版本发布新基线。

## 发布身份

- Baseline Version: `v<major>.<minor>.<patch>`
- Versioned Requirement File: `requirements/baselines/current-requirements-v<major>.<minor>.<patch>.md`
- File SHA-256: `<64 位十六进制哈希>`
- Content Git Commit: `<包含上述精确文件内容的 40 位 commit>`
- Annotated Git Tag: `requirements-baseline-v<major>.<minor>.<patch>`
- Previous Approved Version: `<none | v<major>.<minor>.<patch>>`
- Released At: `<YYYY-MM-DDTHH:mm:ssZ>`

## 版本批准记录

- Approver: `<具名最终批准人；AI 不得填写为批准人>`
- Approved At: `<YYYY-MM-DDTHH:mm:ssZ>`
- Approved Scope: `<本版本整体适用范围>`
- Approved Version Identity: `<目标版本 + 最终文件路径 + File SHA-256>`
- Approval Evidence: `<批准所依据的票据、会议记录或等价证据链接>`
- Authority Evidence: `<若非本次默认最终批准人，链接其授权范围证据；否则写 map decision>`
- Requirement Coverage: `<本记录覆盖的 REQ ID 列表或可复核范围表达式>`

## 变化依据

- Added: `<REQ ID 与获批变更提案链接；无则写 None>`
- Modified: `<REQ ID 与获批变更提案链接；无则写 None>`
- Deprecated: `<REQ ID、替代关系与获批变更提案链接；无则写 None>`
- Version Classification Evidence: `<为什么本版本是 major/minor/patch>`

## 当前版本指针

- Pointer File: `requirements/current-baseline.md`
- Pointer Target: `requirements/baselines/current-requirements-v<major>.<minor>.<patch>.md`
- Pointer Verification: `<通过 annotated tag 所解析的 Git tree 复核本记录与唯一当前指针；不把包含本记录的 commit 哈希回填到本文件>`

## 正式发布检查

- [ ] 完整版本化需求文件存在，且内容与获批 SHA-256 完全一致。
- [ ] `Content Git Commit` 可恢复该精确文件与路径。
- [ ] 带说明 Git tag `requirements-baseline-v<version>` 存在并指向包含本发布的 commit。
- [ ] 批准记录绑定具名批准人、时间、范围、精确文件 SHA-256 和可核查证据。
- [ ] 所有条目批准记录与版本批准覆盖范围一致。
- [ ] 版本号与新增、修改、废弃及范围变化的实际性质一致。
- [ ] `requirements/current-baseline.md` 只指向本次最新批准版本，不指向候选稿。
- [ ] 上一批准版本及其发布记录仍可恢复且未被修改。
