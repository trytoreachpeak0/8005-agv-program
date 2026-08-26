# WIRE_TO_GATE MVP 最终需求适用性清单

- Baseline: `current-requirements-v1.0.0.md` / SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`
- Final TSV: [final-requirement-applicability-profile.tsv](final-requirement-applicability-profile.tsv) / SHA-256 `0678fddb8cb0dc4b1df620257ac7076fc8658e3bda828f0de5c6e9f0fe0461de`
- Coverage: `REQ-0001`～`REQ-0348`，348 条，零遗漏、零重复、每条恰好一个最终分类。
- Approval basis: 依据用户对本 Wayfinder 后续各票采用推荐值的明确授权；只批准 MVP 实施适用性，不修改 v1.0.0 Lifecycle。

## 四类精确清单

### MVP 直接必须（85 条）

REQ-0001、REQ-0026、REQ-0028～REQ-0031、REQ-0040、REQ-0074、REQ-0079、REQ-0146～REQ-0147、REQ-0150～REQ-0164、REQ-0169、REQ-0183～REQ-0184、REQ-0186～REQ-0187、REQ-0190～REQ-0193、REQ-0200～REQ-0201、REQ-0204、REQ-0207～REQ-0210、REQ-0213、REQ-0221～REQ-0224、REQ-0231、REQ-0243～REQ-0250、REQ-0252～REQ-0253、REQ-0267、REQ-0269～REQ-0270、REQ-0281、REQ-0298、REQ-0302～REQ-0303、REQ-0305、REQ-0308、REQ-0312～REQ-0313、REQ-0319、REQ-0321～REQ-0322、REQ-0324～REQ-0325、REQ-0327、REQ-0329～REQ-0335、REQ-0343～REQ-0345

### MVP 交互／安全依赖（101 条）

REQ-0002～REQ-0025、REQ-0027、REQ-0047、REQ-0051、REQ-0053～REQ-0054、REQ-0056、REQ-0069～REQ-0071、REQ-0073、REQ-0078、REQ-0089、REQ-0148～REQ-0149、REQ-0165～REQ-0168、REQ-0181～REQ-0182、REQ-0188、REQ-0194、REQ-0199、REQ-0205、REQ-0211、REQ-0216、REQ-0218、REQ-0225～REQ-0230、REQ-0232～REQ-0235、REQ-0237～REQ-0242、REQ-0251、REQ-0255、REQ-0257～REQ-0259、REQ-0262～REQ-0265、REQ-0271～REQ-0272、REQ-0276、REQ-0278～REQ-0279、REQ-0282、REQ-0290、REQ-0299～REQ-0301、REQ-0304、REQ-0306～REQ-0307、REQ-0309、REQ-0314～REQ-0315、REQ-0323、REQ-0336～REQ-0338、REQ-0340～REQ-0342、REQ-0347～REQ-0348

### 首期延后（31 条）

REQ-0037、REQ-0052、REQ-0055、REQ-0072、REQ-0075～REQ-0077、REQ-0080～REQ-0088、REQ-0203、REQ-0212、REQ-0215、REQ-0256、REQ-0260～REQ-0261、REQ-0266、REQ-0268、REQ-0273～REQ-0275、REQ-0277、REQ-0280、REQ-0339、REQ-0346

### 本场景不适用（131 条）

REQ-0032～REQ-0036、REQ-0038～REQ-0039、REQ-0041～REQ-0046、REQ-0048～REQ-0050、REQ-0057～REQ-0068、REQ-0090～REQ-0145、REQ-0170～REQ-0180、REQ-0185、REQ-0189、REQ-0195～REQ-0198、REQ-0202、REQ-0206、REQ-0214、REQ-0217、REQ-0219～REQ-0220、REQ-0236、REQ-0254、REQ-0283～REQ-0289、REQ-0291～REQ-0297、REQ-0310～REQ-0311、REQ-0316～REQ-0318、REQ-0320、REQ-0326、REQ-0328

## 相对 01 票候选矩阵的分类调整

| Requirement | 候选 | 最终 | 理由 |
| --- | --- | --- | --- |
| REQ-0069 | 首期延后 | MVP 交互／安全依赖 | MesIngest 数据卷低空间门禁决定目录是否仍可作为当前执行来源；MVP 不建设该监控面，但不得绕过其暂停结果。 |
| REQ-0070 | 首期延后 | MVP 交互／安全依赖 | StoragePressurePause 时执行承诺读取必须以 503 fail-closed；ControlServer 不得沿用旧目录受理 Demand。 |
| REQ-0071 | 首期延后 | MVP 交互／安全依赖 | 暂停恢复与 HistoryResetAcknowledgement 属 MesIngest 本地管理边界；MVP 只消费其受审计结果，不实现远程恢复旁路。 |
| REQ-0073 | 首期延后 | MVP 交互／安全依赖 | 重建产生新 HistoryEpoch 且未确认时禁止外部当前读取，是最终重读和跨纪元防重成立的上游门禁。 |
| REQ-0074 | 首期延后 | MVP 直接必须 | Demand 发现、最终重读、AcceptedDemandSnapshot 与重启对账都必须绑定 HistoryEpoch，旧纪元缓存和快照不得复用。 |
| REQ-0190 | 首期延后 | MVP 直接必须 | 指定 AGV 必须具有显式 (agvId, WIRE_TO_GATE) VehicleTaskTypeAdmission；未配置即拒绝，首期用受控预置配置。 |
| REQ-0194 | 首期延后 | MVP 交互／安全依赖 | DispatchZoneVehicleAdmission 硬集合直接保留；多车软偏好、回退次序和跨车策略不进入首期。 |
| REQ-0199 | 首期延后 | MVP 交互／安全依赖 | MVP 消费 Map→DispatchZone→AREA、任务类型白名单和分区硬准入的受控配置身份；评分、拓扑设计和配置 UI 延后。 |
| REQ-0205 | MVP 直接必须 | MVP 交互／安全依赖 | 多车及在途追加竞争不适用，但不预绑忙车、共享 UnassignedDemandBacklog、持续老化和事实变化后重选必须保留。 |
| REQ-0236 | MVP 交互／安全依赖 | 本场景不适用 | 本条按 R-09/R-11/R-13 或逐人附加权限授权的模型不用于 MVP；REQ-0253 与票据 05 已改用两个管理员角色，现场资质仍单独强制。 |
| REQ-0251 | 首期延后 | MVP 交互／安全依赖 | SystemAdministrator 的角色身份、异常恢复资格和不得覆盖安全事实的边界适用；完整账号、配置、版本维护产品面首期延后。 |
| REQ-0252 | 首期延后 | MVP 直接必须 | 试运行和最小异常恢复至少需要一个不共享的个人管理员账号；一人一号、单活动会话和替换审计直接适用。 |
| REQ-0253 | MVP 交互／安全依赖 | MVP 直接必须 | 最小 ExceptionRecoverySession 明确由 MaintenanceAdministrator 或 SystemAdministrator 以个人账号独立操作，普通操作员无权恢复。 |
| REQ-0254 | 首期延后 | 本场景不适用 | 充不上现场确认、人工清桩和充电桩恢复属于自动充电/充电桩产品面；MVP 仅保留人工充电 Hold 与重新投运。 |
| REQ-0258 | MVP 直接必须 | MVP 交互／安全依赖 | MVP 必须消费服务端发布的仓位模型/配置身份并禁止车载平行改业务模型；ConfigurationMaintenanceConsole 编辑、复制、提交和激活 UI 不进入首期。 |
| REQ-0276 | 首期延后 | MVP 交互／安全依赖 | 预建个人管理员账号仍须遵守已批准的基础密码有效性；可配置增强、找回和完整账号生命周期产品面延后。 |
| REQ-0278 | 首期延后 | MVP 交互／安全依赖 | 目标硬件操作和异常处置使用真实管理员登录，会话只能沿已批准明确边界结束；首期不另造自动超时语义。 |
| REQ-0279 | 首期延后 | MVP 交互／安全依赖 | 最小 ExceptionRecoverySession 必须跨短暂断线保留原人员、事件与范围并继续对账，不能因空闲超时释放安全阻断。 |
| REQ-0307 | 首期延后 | MVP 交互／安全依赖 | FactoryPilotConfigurationSnapshot、运行证据和活动 Demand 引用的 MapStationCatalogSnapshot 修订必须可追溯；完整长期清理管理面延后。 |

## 分类语义与限界

- `MVP 直接必须`：精确条目直接约束本场景实现或验收，不能以其它能力替代。
- `MVP 交互／安全依赖`：不要求首期重建条目全部产品面，但其中的来源事实、门禁、安全、恢复、身份或审计语义必须被消费或保留。
- `首期延后`：本场景首期不实现；原条目仍为 v1.0.0 active，不代表永久废弃。
- `本场景不适用`：对单车、单图、单 Demand、WIRE_TO_GATE 旅程不适用；不从已发布基线删除。
- 车载端开发同事对原型票的豁免不延伸到生产实现、ProtocolReleaseIdentity、G0～G3、现场试运行或最终交接批准。
- 本清单没有发布协议、运行门禁、取得真实凭证/物料/现场证据，也没有代替另一名开发者或第三方确认。
