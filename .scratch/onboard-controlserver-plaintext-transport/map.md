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
- **硬校验共九处（服务端 5 ＋ 车载端 4），全部是产品代码而非配置开关**。开票时记的「2 ＋ 3」不全，
  票 01 已现场核实并列全清单；两端两条链路**共用同一张 PFX**（Kestrel 证书取自
  `OnboardTransport:serverCertificatePath`）。完整表见
  [`冻结两端安全校验的放开形态与配置面终态`](issues/01-freeze-the-plaintext-configuration-surface.md)
  的 Answer 第 0 节。两处最容易踩空的：
  - 车载端 `WireToGateSettings.Validate(production: true)` 强制 `ServerCertificateSha256` 非空且非全零，
    **该检查不看 `UseTls`**，漏改则 production 启动直接抛异常，其余改动全部白改；
  - 车载端 `ControlServerVehicleSafetySignalProvider.cs:95` 漏改不崩溃，而是 fail-closed 到
    `UnknownSignal("HTTPS_REQUIRED")`——现场症状是安全信号恒 UNKNOWN、永不放行。
- **`8005-agv-onboard-hmi` 对 agent 只读**（根 `AGENTS.md`），且用户 2026-08-25 已把车载端产品代码
  划归王昆。车载端三处改动由**王昆**执行，agent 只出精确转交件并只读回读核验，全程对该仓零写入。
  本地图必然在此阻塞一次，这是已知且被接受的路线成本。
- **不动协议仓**。票 01 在 `1531489`（`protocol-v0.1.1` 线）上复核：tracked 文件搜
  `tls|ssl|certificate|encrypt|证书|加密` 命中数为 0（表面命中全是 JSON Schema 的 `$id` URL 与第三方
  许可链接），`transport` 仅出现于 `transportDedupKey`／`transportDemandKey`，`58005` 零出现。协议对
  `credentialProof` 只规定「是 `minLength: 1` 的字符串且必填」，不规定取值与保护方式。因此本轮不触发
  协议变更的双人批准门禁，`protocol-v0.1.1` 保持不动。
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

- [`冻结两端安全校验的放开形态与配置面终态`](issues/01-freeze-the-plaintext-configuration-surface.md)
  — 彻底删除 TLS/HTTPS 代码路径与全部证书配置字段（不留开关）；Kestrel 单一绑定并把安装脚本的监听地址
  参数化、默认仍 loopback；不加误配补偿；升级时脚本清 certs 与证书口令环境变量、根证书走手册人工步骤；
  过时配置键在启动期显式拒绝；新旧两端不做协商，改为票 07 取证的双向错配对照表。校验点实为 9 处而非 5 处，
  协议仓零传输层规定已复核。
- [`按冻结形态改掉服务端产品代码的 TLS/HTTPS`](issues/02-strip-tls-from-controlserver-product-code.md)
  — 服务端 TLS/HTTPS 代码路径已删净并提交 `ControlServer_MVP@ae4a17d`（2026-08-31 随票 03 一并推送）；`0.0.0.0` 明文启动、
  `/health/live` 200、投影经 HTTP 可达且无凭据仍 401，四个过时键任一存在即拒绝启动，均为回读取证；
  tier 1 249 绿 0 跳过。另删掉票 01 漏列的 `FakeOnboard --tls` 死分支；本仓自此再无测试触及 Schannel。

## Not yet specified

- 王昆对本改动的回应形态。他可能接受、反对、或提出替代（例如坚持链路 B 保留 TLS）。反对会让本地图
  的完成定义需要重新协商，而不只是延后。票 05 拿到回应前无法具名。
- 明文化之后 G3 runner 的调整范围。**服务端 G2 侧已在票 02 清空**：`test-wire-to-gate.ps1` 就是按
  `IntegrationSlice` trait 过滤同一套 xunit 测试，不存在独立的 G2 向量或 fixture，脚本本身零 TLS 字样，
  `W2G-IS-00` 过滤后仍选出 24 条且全绿——服务端 G2 无需任何调整。**三个 G3 runner 已在票 03 改完并
  推送**（`c7874f0`），但它们的实际可运行性仍未证：`run-staged-g3.ps1` 默认锁定的 `OnboardCommit`
  仍是 TLS 期车载端提交，要等票 06 拿到王昆的新提交后才能重跑。仍未定的是车载端
  `WireToGateG2Tests`（归王昆，随票 05 转交件交出，范围等他的回应）。
- 发布版本号与既有 release 的关系（`0.1.2` 还是别的，`0.1.1` 是否保留、是否需要在其说明中回指）。
  等票 08 附近再定。
- 异机明文联调可能暴露的新问题（例如 `RemoteCertificateNameMismatch` 之外原本被 TLS 层吸收掉的
  连接错误形态、非 loopback 绑定下的防火墙与监听地址）。票 07 之前无法具名。

## Out of scope

- 把 `credentialProof` 改成挑战应答／HMAC 或任何不使静态密钥过网的认证形态。用户 2026-08-31 明确否决，
  作为已知限制接受。**理由更正（票 01）**：这条路并不需要动协议仓——`credentialProof` 是不透明字符串，
  换成 HMAC 结果同样满足 schema，因此不触发双人批准门禁。真正的成本是两端实现改造与一次协调升级，与
  本轮「简化部署」的动机相反。
- 服务端来源 IP 白名单或任何压制明文暴露面的补偿措施。用户判为安慰剂：挡不住能抓包的人，不构成
  真实防护。
- 把链路 B 改为指纹钉扎而保留 TLS 加密。agent 推荐过，用户重申选择直接用 HTTP。
- 车载端仓的 tag、release、分支、提交与任何写入。该仓对 agent 只读，其版本引用归 owner。
- 协议仓的任何变更，含 `protocol-v0.1.1` 之后的新 tag／release。
- 继承自上一轮且仍然开放：`RESUME_AFTER_REPAIR` 的结果身份收敛；三个 G3 runner 的公共模块抽取。
  均属另起一轮。
