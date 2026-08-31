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
- **触及 Windows 服务的票一律 HITL**。`Install-/Uninstall-/Update-ControlServerLocal.ps1` 都以
  `Assert-Administrator` 开头，Claude 会话默认不是管理员。票 03 开票时误记为 `Mode: AFK`，代码改完才
  发现跑不了验收。票 09（干净安装验收）与后续任何装卸服务的票**开票时**就要标 HITL 并写明需要用户在
  UAC 上确认，不要事后补。
- **票 02 式的「显式拒绝已删配置键」改动，必须同时扫全仓的环境变量注入点**，而不只是
  `appsettings*.json`。过时键校验比对的是键名，`Key__Sub=''` 这类空值注入同样算键存在。票 02 与票 03
  之间，`run-staged-g3-restart.ps1` 与 `run-demand-bearing-g3-vectors.ps1` 因此静默失效过一段。
- **逐处改写时，「值恰好已经对了」的那一行最容易被跳过**。票 03 把两个 runner 的 `useTls = $true` 改成
  条件式，却漏了 restart runner 里的 `useTls = $false`——后者的值本来就是要的值，肉眼扫过时不像待改项。
  删键类改动的正确判据是**键名出现即处理**，不是「值对不对」。票 06 发现，归票 12。
- **PowerShell 语义更正（票 06 实测）**：`ConvertFrom-Json` 产出 `PSCustomObject`，给**不存在**的属性
  无条件赋值会抛 `SetValueInvocationException`，**不会**静默新增该属性——只有 `Add-Member` 或
  `-AsHashtable` 才会。票 05 §5.4 按「静默写回错键」推断的机理是错的（结论方向不变，失效形态从静默
  变成硬失败）。凡涉及脚本改配置的判据，按这条重读。

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
- [`从安装、卸载、更新与 G3 runner 中拆除证书机制`](issues/03-strip-certificates-from-the-install-chain.md)
  — 安装／卸载／更新脚本与三个 G3 runner 的证书机制已拆净（`c7874f0`）；隔离实例上安装→启动→停止→
  再启动→强制重启→卸载全流程 `PASS`，`CurrentUser\Root` 44 张指纹跨安装与卸载零变动、无 certs 目录、
  无任何密钥材料文件，健康检查直连 http，生产服务不受影响。安装脚本新增 `-ListenAddress`／
  `-HealthBindAddress`（默认仍 `127.0.0.1`）；升级路径**额外**加了配置迁移（超出票的字面范围，但不做
  升级必然失败并回滚，有红侧证据）；`New-WireToGateReleaseCandidate.ps1` 有意不改（其证书相关规则是
  阻止密钥进包的发布门禁）。`Update-ControlServerLocal.ps1` 硬写生产值、无法在隔离实例排练，证书目录
  删除／机器级口令清除／备份回滚三段的真实执行仍无证据，是否参数化留给票 09。
- [`向车载端 owner 交付明文改造转交件`](issues/05-hand-off-the-onboard-changes-to-the-owner.md)
  — 转交件已由用户发出，王昆**接受**，以提交 `OnboardHmi_MVP@238b46e`（`refactor: switch onboard
  transports to plaintext`，2026-08-31 22:11，`31263b1` 的快进）代替文字答复，未提反对或替代方案，
  故完成定义无需重新协商。`--stat` 显示转交件点名的三个校验源文件、两个配置文件、三个测试文件、
  §5.4 那处 G3 runner 全部动了，§5.5 的证据快照未动；他另外多改了五个未点名文件。本票只看元信息与
  `--stat`，**未读一行改动后的代码**，四处校验终态、两端配置互用性、他多改的部分一概归票 06。对该仓
  写入仍为零。
- [`只读回读核验 owner 的车载端改动`](issues/06-verify-the-owner-onboard-commit-read-only.md)
  — 车载端 `238b46e` **逐行读过并通过**，固定为候选车载端身份；四处硬校验（含最易漏的
  `Validate(production: true)` 指纹强制）全部按冻结形态改到位，两处 `IsForbiddenProductionHost` 与那份
  证据快照原样保留，全仓再无 TLS 残留。他还对称加了车载端过时键拒绝（转交件 §4.3 留给他定的，他选「加」），
  测试两侧都补了红侧对照。多改的五个文件读过，全是措辞对齐加一条他主动补的已知限制，无害。两端配置面
  逐项对表未发现「一端删字段、另一端仍要求」。**他是否跑过车载端测试仍为未知**（无 CI、无证据、无文字答复），
  据实记录不推定。核验中发现的唯一问题在**服务端仓**：`run-staged-g3-restart.ps1:508` 会在明文车载端上
  硬失败，归票 12。对该仓写入仍为零。

## Not yet specified

- G3 runner 的**静态对齐已在票 06 具名并开票 12**（restart runner 第 508 行的无条件赋值、
  `run-staged-g3.ps1:12` 的默认 `OnboardCommit` 仍锁 `304e6ad`）。剩在雾里的只有一件：**三个 runner
  的实际可运行性至今零证据**——票 02 只证服务端单侧，票 03 只证安装链，没有任何一次改后的 staged G3
  真跑过。是在票 12 就跑、还是并进票 07 的联调、还是推到票 08 之后，等票 12 给出成本后再定。
  （服务端 G2 侧无遗留：票 02 已证 `test-wire-to-gate.ps1` 只是按 `IntegrationSlice` trait 过滤同一套
  xunit 测试，零 TLS 字样，`W2G-IS-00` 过滤后 24 条全绿。车载端 `WireToGateG2Tests` 的 4 行改动已由
  票 06 读过，是纯适配。）
- 车载端 `238b46e` 上的测试是否仍全绿。票 06 查实该仓无 CI、该提交无证据、王昆无文字答复，只能记为
  未知。要不要补这条证据、由谁补（向王昆索取，还是在仓外一次性克隆里跑），等票 08 需要时再定——
  它是发布候选身份的一部分，不是本轮改造的判据。
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
