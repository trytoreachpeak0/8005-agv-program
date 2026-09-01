# 补齐 standard.oasis.300ul 物模型枚举证据

Type: task
Status: resolved
Blocked by: 25

## Question

项目方需要提供哪一份可核查、带版本的 `standard.oasis.300ul` 原始 TSL 或等价权威来源，以及对应产品、固件、环境、枚举值、错误码、捕获时间与适用范围，才能裁定当前物模型问题清单中的缺号、不一致和无说明 code；若无法取得，哪些字段必须继续标记为未知而不能进入当前基线？

## Answer

已建立 [`standard.oasis.300ul` 物模型证据边界](../evidence/riot-interface/standard-oasis-300ul-thing-model-evidence.md)。仓库实际保存了 53,458 字节的原始形态 TSL（SHA-256 `3b93756ad18896c278cffc1c13711b289aa8236bc79a35e178180581c9faee36`，Git blob `1500fa1b882306fe36107021ed1177c71aab550e`），内嵌 productKey `standard.oasis.300ul` 和 profile 版本 `1`；此前候选文档清单只登记了派生的问题清单，未登记 `.tsl` 本体，本次已把本体作为补充原始证据接入后续 R13 分类而不改写初始快照。

该文件没有可核查的导出来源、捕获人/时间、源环境、RIoT build、控制器固件、厂商确认或 8005 适用性绑定，所以只能证明静态内容，不能裁定缺号、`pathType` 差异或错误码语义。证据记录已固定以后关闭未知边界所需的八类最低字段，并明确在此之前必须保持未知：三个跳号区间的含义与可达性、两处 `pathType` 的正确归并方式、`multiLoadState`、三个错误/故障字段、36 个服务 `result.code` 的全部语义，以及现存 TSL 的真实版本来源和生效范围。这些均不得以 Git/文件时间、本地分析、生成代码或黑盒观察代填，也不得作为已知需求进入当前基线。
