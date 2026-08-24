# 补齐 RIoT 目标环境与受控接口快照证据

Type: task
Status: resolved
Blocked by: 25

## Question

项目方需要提供怎样的受控接口快照 manifest 与环境映射，才能把 RIoT schema 绑定到可核查的目标环境：捕获人和时间、RIoT build、环境用途与所有者、脱敏 base URL 标识、各 schema 哈希、捕获方式、适用项目范围和确认记录；现有 `172.19.206.222` 与 `172.10.1.72` 分别属于什么环境、有效期和用途，且如何在不记录秘密的前提下补齐证据？

## Answer

用户本人作为本次当前需求基线默认且唯一的最终批准人，于 2026-08-03 直接确认并关闭了环境与快照来源缺口；结构化原始上下文见 [RIoT 环境与接口快照用户确认](../evidence/riot-interface/riot-environment-and-snapshot-user-confirmation-2026-08-03.md)，完整环境映射、manifest、逐文件哈希和秘密边界见 [RIoT 目标环境与受控接口快照补证记录](../evidence/riot-interface/riot-controlled-snapshot-evidence-request.md)。

`172.19.206.222:8888` 被固定为 `RIOT-8005-RUNTIME`：它是 8005 项目真实运行时必须访问的 RIoT 实例，由软件人员和实施人员共同所有，永久有效但只可从现场网络访问，版本为 `v2.2.0.14`。`172.10.1.72:8888` 被固定为 `RIOT-CROSS-PROJECT-TEST`：它是另一项目、另一现场的独立 RIoT 实例，曾作为 8005 API 测试环境，由软件人员和实施人员共同所有，永久有效但须通过对应网络、VPN 或 5G 模块访问，build 为 `2.2.0.30`。用户初次答复中的 `172.19.1.72` / `v2.2.014` 已由其明确修正，保留修正链但不再作为环境事实。

现存 `rcs/riot_swagger/` 下 14 份 OpenAPI 3.0.3 JSON 已登记为 `RIOT-OPENAPI-8005-202607-EARLY-01`：由用户本人于 2026 年 7 月初手动从 `RIOT-8005-RUNTIME` 导出，源 build 为 `v2.2.0.14`，适用于 8005；同一套 OpenAPI 客户端后来用于 `2.2.0.30` 环境的 riot-lab 行为测试。补证记录固定了 14/14 文件的路径、字节数和 SHA-256；精确导出日、逐接口 URL 和工具步骤未保存，已显式记为未知而未由 Git 时间代填。

该证据只绑定环境、build、快照身份和适用范围，不授权任何 API，也不证明权限、副作用或错误语义。manifest 禁止保存用户名、密码、token、CallApiKey、cookie 或私钥；后续 API 白名单、鉴权和调用安全继续由“决定 RIoT 项目 API 白名单与调用安全边界”独立裁决。本票不改变业务领域词汇，因此不修改根 `CONTEXT.md`。

## Comments

### 2026-08-03 — 已建立补证记录，等待项目方确认环境映射

已建立 [RIoT 目标环境与受控接口快照补证记录](../evidence/riot-interface/riot-controlled-snapshot-evidence-request.md)，固定现存 14 份 OpenAPI 原始文件的逐文件 SHA-256、schema 中记录的 server，以及不含秘密的受控 manifest 最低字段和捕获规则。

仓库只能证明：14 份 schema 指向 `172.19.206.222:8888` 且缺失 `info.version`；行为实验和 SDK 文档常用 `172.10.1.72:8888`；Round 1 的 `v2.2.0.30` 是事后补记。现有材料不能证明两个地址的实例关系，也不能把 schema 绑定到该 build。

本票继续保持 `claimed`。等待用户本人或其明确授权的具名项目责任人确认两个环境的用途、所有者、有效期、build、相互关系，以及现存 schema 的捕获人/时间/方法和当前 8005 适用范围；不得用 Git 作者、文件时间或实验成功代填。

### 2026-08-03 — 用户已绑定 8005 环境与现存 Swagger，保留一项地址/build 歧义

用户本人确认 `172.19.206.222` 是 8005 项目真实运行时 RIoT，版本 `v2.2.0.14`，由软件人员和实施人员共同所有，永久有效但只可从现场网络访问；另一项目的 RIoT 曾作为本项目 API 测试环境，和 8005 实例属于不同现场、不同实例。

用户同时确认现存 14 份 Swagger 由其本人于 2026 年 7 月初手动从 `172.19.206.222` 导出，适用于 8005。已在[补证记录](../evidence/riot-interface/riot-controlled-snapshot-evidence-request.md)中建立 `RIOT-8005-RUNTIME` 与 `RIOT-OPENAPI-8005-202607-EARLY-01` 的绑定，并以[用户确认记录](../evidence/riot-interface/riot-environment-and-snapshot-user-confirmation-2026-08-03.md)保留来源。

本票暂不解决：用户本次把测试环境写为 `172.19.1.72` / `v2.2.014`，而仓库反复记录 `172.10.1.72`，Round 1 又事后补记 `v2.2.0.30`。在用户明确消歧前不把它们当作笔误或静默改写。

### 2026-08-03 — 用户关闭测试环境地址、build 与所有者歧义

用户明确修正测试环境的准确地址为 `172.10.1.72`、准确 build 为 `2.2.0.30`，并确认所有者角色为软件人员和实施人员。补证记录与用户确认记录已保留初次答复和最终修正链；所有补证缺口关闭，本票解决。

### 2026-08-03 — 用户修正现存 OpenAPI 的源 build

用户在后续“决定 RIoT 项目 API 白名单与调用安全边界”对话中明确确认：现存 14 份 OpenAPI 的源 build 是 `2.2.0.30`，不是先前记录的 `v2.2.0.14`。环境来源仍为 `RIOT-8005-RUNTIME`，快照仍适用于 8005；`v2.2.0.14` 继续作为 8005 运行环境版本事实保留。用户确认记录、受控 manifest 和本票 Answer 已同步追加修正链。

### 2026-08-03 — 用户最终澄清 OpenAPI 与测试环境 build 的关系

用户明确纠正上一条：OpenAPI 本身来自 `v2.2.0.14`，只是同一套 OpenAPI 客户端后来被放到 `2.2.0.30` 环境下运行 riot-lab 行为测试。受控 manifest 和本票 Answer 已恢复快照源 build `v2.2.0.14`，并保留中间误解作为修正链。
