# OnboardHmi↔ControlServer 明文传输改造路线图

Label: wayfinder:map

## Destination

把 OnboardHmi 与 ControlServer 之间的两条链路从 TLS/HTTPS 改为明文 TCP/HTTP，并拆掉安装与发布
链路里的整套证书机制，使工厂内网部署不再需要生成、分发、导入或续期任何证书。

改造覆盖两条独立链路：

- **链路 A**：业务协议 NDJSON over TCP（默认端口 58005），`OnboardTcpServer` ↔
  `WireToGateSessionClient`；
- **链路 B**：车辆安全投影 REST（`/api/onboard/v1/vehicle-safety`），Kestrel HTTPS ↔
  车载端 `HttpClient`。

到达终点要求：服务端产品代码、部署脚本与发布手册中的证书机制已移除；车载端三处硬校验由该仓
owner 王昆改完并推送；两端在**异机明文**形态下建立会话并通过安全投影；重建的发布候选完成干净
安装验收与**真车闭环**现场验收，并发布为服务端仓的不可变 tag/release，「凭据明文过网」作为已知
限制原样写入发布说明。

## Notes

- 本地图承接已走完的 [`WIRE_TO_GATE 一周可运行 MVP 交付路线图`](../wire-to-gate-ai-implementation-kit/map.md)
  及其已发布的 `w2g-mvp-rc-0.1.0`／`0.1.1`；不重新扩展产品范围，只改传输层安全形态。
- **本地图携带执行**（用户 2026-08-31 明确选择）：不止于决策，要一路做到重建候选、现场验收与发布。
  各仓仍须遵守自身 AGENTS/CONTEXT 与测试门禁。
- **动机是部署复杂度，不是故障排除**。用户明确：链路本身走得通，只是工厂内网、两端都是自有应用，
  为此维护证书信任链累赘且抬高部署成本。因此本轮不接受「换一种证书方案」作为等价交付。
- **agent 已提出并被用户重申否决的替代方案**：把链路 B 从系统信任存储改为指纹钉扎（与链路 A 现有
  做法一致，可做到零证书导入、零信任存储操作，代价只是多填一个 `sha256` 字段）。用户选择直接用
  HTTP。该替代方案不再作为本轮选项，记录于此仅为保留决策依据。
- **四处硬校验，两端对称，全部是产品代码而非配置开关**：
  | 链路 | 服务端（可写） | 车载端（只读） |
  | --- | --- | --- |
  | A | `OnboardTcpServer.cs:141` 明文仅 loopback | `WireToGateSessionClient.cs:1850` 明文仅 loopback |
  | B | `OnboardSafetyProjectionOptions.cs:23` `RequireHttps must remain true`（设 false 直接拒绝启动） | `Configuration.cs:152` 与 `ControlServerVehicleSafetySignalProvider.cs:95` 必须 https |
- **`8005-agv-onboard-hmi` 对 agent 只读**（根 `AGENTS.md`），且用户 2026-08-25 已把车载端产品代码
  划归王昆。车载端三处改动由**王昆**执行，agent 只出精确转交件并只读回读核验，全程对该仓零写入。
  本地图必然在此阻塞一次，这是已知且被接受的路线成本。
- **不动协议仓**。已查实：`8005-agv-protocol` 不规定传输层安全，`manifest/release.json` 中 `transport`
  仅出现于 `transportDedupKey`（消息去重键），docs 无 TLS 规定。因此本轮不触发协议变更的双人批准
  门禁，`protocol-v0.1.1` 保持不动。
- **凭据明文过网是本轮知情接受的代价**。`credentialProof` 是协议字段
  （`SessionHello.schema.json:73`，且在 required 内），车载端把静态共享密钥原样放进 payload。明文
  之后抓一次包即可永久冒充车载端。用户明确选择接受（工厂内网风险自担），并否决了改挑战应答／HMAC
  （会动协议仓）与来源 IP 白名单（判为安慰剂）。该限制必须原样进发布说明，不得淡化措辞。
- **安全闸门输入变为可篡改**：`motionState=STOPPED` 经明文 HTTP 传输后可被中间人改写，票 14 证过的
  「移动中拦、停稳放行」在不可信网络下不再成立。这是 safety 而非 security 层面的后果，同样须进
  已知限制。
- 验收规格由用户选定为**真车闭环**（同票 29 规格：现场安全 GO、操作员、正数 `dispatchGeneration`、
  完整 WIRE_TO_GATE 闭环），不接受仅隔离实例建会话作为等价。
- 技术实现继续遵守上一轮的「成熟复用优先」与证据规则：判据必须是回读取证，红侧必须证明检测器
  会响；托管构建每次新 MVID，`.dll` 哈希不构成内容证据，要用新增／消失的符号名。
- 凭据、密钥只登记安全引用，不进 Git、发布包、日志或测试证据。

## Decisions so far

<!-- 已解决票据才在此保留一行摘要；详细答案只存在票据中。 -->

## Not yet specified

- 王昆对本改动的回应形态。他可能接受、反对、或提出替代（例如坚持链路 B 保留 TLS）。反对会让本地图
  的完成定义需要重新协商，而不只是延后。票 05 拿到回应前无法具名。
- 明文化之后 G2／G3 测试向量与 fixture 的调整范围。现有 `WireToGateG2Tests` 与服务端边界测试有多少
  绑在 TLS 形态上，要等票 02 让测试先红一次才能看清。
- 发布版本号与既有 release 的关系（`0.1.2` 还是别的，`0.1.1` 是否保留、是否需要在其说明中回指）。
  等票 08 附近再定。
- 异机明文联调可能暴露的新问题（例如 `RemoteCertificateNameMismatch` 之外原本被 TLS 层吸收掉的
  连接错误形态、非 loopback 绑定下的防火墙与监听地址）。票 07 之前无法具名。

## Out of scope

- 把 `credentialProof` 改成挑战应答／HMAC 或任何不使静态密钥过网的认证形态。需要动审批门禁的协议仓
  与双人批准，规模与本轮「简化部署」的动机相反。用户 2026-08-31 明确否决，作为已知限制接受。
- 服务端来源 IP 白名单或任何压制明文暴露面的补偿措施。用户判为安慰剂：挡不住能抓包的人，不构成
  真实防护。
- 把链路 B 改为指纹钉扎而保留 TLS 加密。agent 推荐过，用户重申选择直接用 HTTP。
- 车载端仓的 tag、release、分支、提交与任何写入。该仓对 agent 只读，其版本引用归 owner。
- 协议仓的任何变更，含 `protocol-v0.1.1` 之后的新 tag／release。
- 继承自上一轮且仍然开放：`RESUME_AFTER_REPAIR` 的结果身份收敛；三个 G3 runner 的公共模块抽取。
  均属另起一轮。
