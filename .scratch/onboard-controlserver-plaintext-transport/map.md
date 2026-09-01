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
- **车载端 production 守卫的真实结构（票 07 现场核实）**：只有 `WireToGateSettings` 与
  `VehicleSafetySettings` 的 production 分支会跑 `IsForbiddenProductionHost`（**拒绝** loopback）；
  `RuleGatewaySettings` 与 `IoModuleSettings` 的 production 分支只拒占位值，loopback 是允许的。
  推论：异机取证应当用 `environment=Production` 而不是 G3 那套 `Development`——那是唯一让守卫真正
  生效的模式，从原理上排除了 loopback 蒙混；同时 ruleGateway／ioModule 可以留在 `127.0.0.1`，不会
  因此启动失败。Production 另外强制 `vehicleSafety.enabled=true`、AgvId／OnboardInstanceId 非占位、
  以及三个环境变量（凭据、投影凭据、操作员 ID）非空。
- **错配的错误文本会骗人，手册要指向服务端日志**（票 07 取证）。明文车载端连 TLS 服务端时，车载端
  只说「ControlServer在会话恢复期间关闭了连接」（听起来像业务层恢复问题）、链路 B 只说
  「An error occurred while sending the request.」；唯一点出真因的是服务端的
  `AuthenticationException: Cannot determine the frame size or a corrupted frame was received.`。
  反方向（老车载端连明文服务端）车载端只报 `Received an unexpected EOF or 0 bytes from the
  transport stream.` 并**无限重连不退出**。两个方向都不含 TLS 字样，现场极易误判成「网络不通」。
- **PowerShell Direct 会话里启动的进程会随会话关闭被杀**，日志停在正常行、看不出是被杀的。异机取证
  若要证明「进程不依赖远程会话」，必须用 `Win32_Process.Create` 之类脱离启动，再从**另一个独立
  会话**采样。票 07 有一轮差点因此把「进程还活着」记错。
- **票 07 的异机环境保留可复用**：Hyper-V VM `plaintext_onboard_07`（金机父盘的独立副本，金机零写入）
  `192.168.200.50`，宿主侧 `192.168.200.1`，stage 目录 `F:\w2g-ticket07`（含两个车载端与两个服务端
  publish 包、一次性 PFX、凭据）。票 08／09 要复现异机形态可直接接上。凭据与 PFX 只在该 stage 的
  `secrets\` 下，不进 Git、发布包与证据。
- **PowerShell 里 `@($hashtable[$missingKey])` 的 `Count` 是 1，不是 0**（票 08 踩过）。缺键取值得到
  `$null`，`@($null)` 是长度 1 的数组，于是「有没有命中」的判断无条件为真——票 08 的符号探测器第一版
  因此把十六个符号全报 PRESENT，包括只存在于新包的两个。凡用哈希表累计命中再判 `Count -gt 0` 的取证
  脚本，必须先 `ContainsKey`。**这次是靠「不可能的全绿」发现的**：探测设计里放了新增符号那一栏，老包
  本该 ABSENT；只放「该消失的」符号就发现不了。取证表里同时放正反两向的期望，是能自曝检测器坏掉的
  最便宜手段。
- **符号级判据要提防框架携带者**（票 08）。`RequireHttps` 这类短名在自有程序集之外还有 ASP.NET Core
  自己的 `RequireHttpsAttribute`，整包扫会永远 PRESENT。判定按两端自有程序集做，但整包状态与携带者
  文件名要一并记录，不要把命中藏起来。
- **apphost `.exe` 是唯一一个哈希差异有意义的文件**（票 08）。托管 `.dll` 每次新 MVID，哈希差异是噪声；
  但 `.exe` 不由源码编译，其 Win32 版本资源里嵌着 `InformationalVersion`，本仓两端都带 `+<commit>`。
  两版候选的 apphost 逐字节相同，只差那段 79 字节的 UTF-16 字符串——它反而能证明 commit 绑定。
- **`@()` 包错位置是同一族的第二个坑**（票 13）。`@(Get-ChildItem -Directory).Name` 在**单元素**结果上
  经成员枚举退化成一个字符串，`[0]` 于是取到首字符，与目录名的比较永远不等。与
  `@($hash[$missingKey]).Count -eq 1` 是同一类：`@()` 要包**投影**（`@((...).Name)`）而不是包源，
  否则 PowerShell 的标量／集合退化会把判断悄悄换成另一件事。同样是靠正反两向并排打印当场暴露的
  ——`expected` 与 `observed` 字面相同却判 FAIL，一眼就知道是检测器坏了而不是真发现。
- **`tls = $false` 这类证据字段本身不是证据**（票 13）。三个 G3 runner 里
  `tls` / `temporaryTrustRootInstalled` / `certificatesGenerated` 都是硬编码字面量，不会因为真装了
  证书而变。要证「本轮无 TLS」得另取 runner 没有写过的观测：证书存储的**指纹集合摘要**跨运行不变
  （不是只比数量）、stage 与证据根零密钥材料与零 `certs\`、publish 出来的车载端配置回读无三个 TLS 键、
  全部日志搜 `Schannel|SslStream|AuthenticationException|X509|certificate` 命中 0。
- **`@($null).Count -eq 1` 这一族已经踩到第三、第四次了（票 09）**，所以判据换成一条规则：
  **`@()` 永远包投影，不包源**。`@(<空管道>.FullName)` 与 `@(@(Select-String …).Matches)` 都会先得到
  `$null` 再被 `@()` 包成长度 1 的数组，于是「有没有命中」无条件为真；票 09 因此一次报出「无名的密钥
  材料发现」、一次在零残留的文件上报出 1 个 `REPLACE_` 占位符（**假红**）。正确写法是让投影留在管道里
  （`| ForEach-Object { $_.FullName }`），或先 `ContainsKey`。
- **`-f` 写在 .NET 方法调用的参数表里会静默少收参数（票 09）**。
  `$list.Add('{0}…{4}' -f $a, $b, $c, $d, $e)` 中的逗号绑给的是 **`Add()` 调用**而不是 `-f`，格式化
  只拿到一个参数、在 `{1}` 上抛 index 异常，`Add` 从未执行——检测器于是**永远报不出差异**。先把字符串
  算进变量再 `Add`。这条与上一条都不是靠 review 发现的，是红侧「该响没响」当场抓出来的。
- **取证 harness 自身要有隔离（票 09）**。第一轮五条红里三条是 harness 缺陷：扫描范围套住了 harness
  自己种的对照 `.pfx`；`Add-Type -Path` 指向安装根锁住 `e_sqlite3.dll`，导致收尾卸载删不掉目录；以及
  上面那个假红。推论：**扫描要指向被测对象的根，不要指向 run root**；**从被测安装目录加载程序集会给
  它上锁**，要从不会被删的发布包里加载；**数据根被卸载删掉之前先把日志复制进证据目录**，否则事后无从
  诊断。
- **判定链的顺序决定了「拒绝理由」意味着什么（票 10）**。票 09 把
  `BATTERY_POLICY_NOT_SATISFIED=1` 读成「没有需求满足现场条件」，但它在
  `JourneyRuntimeEngine.ValidateDynamicFacts` 里排在 area、AREA_EQP 唯一性、站点解析、包装容量
  **之后**——那一条其实已经通过了全部静态闸门。**看到一个靠后的 ReasonCode，等于同时看到了它
  前面每一道闸门都放行了**；把它当成「什么都没通过」会得出相反的结论。凡按 ReasonCode 分布下
  判断的，先把产生它的判定链顺序读一遍。
- **RIoT 的 `CallApiKey` 走 `Authorization: Bearer`（票 10）**。SDK 的 `RiotOptions.CallApiKey`
  属性名会让人以为有个同名请求头；`CallApiKey` / `X-Call-Api-Key` / `apiKey` 三种头名都回 401。
  SDK 程序集里唯一的线索是 `BearerPrefix` 这个字符串。已批准的只读地图查询因此是
  `GET /api/imap/v1/mapInfo/stations/25` 加 `Authorization: Bearer <key>`，响应体是
  `{code,message,result[]}`，`result` 里每站带 `id` 与 `name`。
- **`-f` 写在 hashtable 成员赋值的 `if` 分支里会解析失败（票 10）**。
  `Station = if ($x) { '{0}/{1}' -f $a, $b } else { '' }` 直接报
  `Unexpected token ','`——与「`-f` 写进方法调用参数表」是同一族：**`-f` 的右操作数一旦处在别的
  语法结构的逗号作用域里就会被抢走**。修法一致：先把字符串算进变量，再赋值／再 `Add`。
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
- [`把 G3 runner 对齐到明文车载端 238b46e`](issues/12-align-g3-runners-to-the-plaintext-onboard-commit.md)
  — 两处具名改动已提交推送（`ControlServer_MVP@65841df`）：restart runner 第 508 行改成条件式（红侧重现
  `SetValueInvocationException`、绿侧写回不含该键、对照证明分支进得去），共享 `OnboardCommit` 移到
  `238b46e` 且三个 runner 各按自身解析链读到同一值、其余三个 commit 逐字未变。`serverCertificateSha256`
  经回读两侧 dev `appsettings.json` **核实为不需要处理**（两侧都无此键），不加死代码。**新发现的实跑
  前置**：`ControlServerCommit` 仍锁 TLS 期的 `3d8b00c7`，实跑前必须一并移到含明文改造的服务端提交；
  本票不改它，因目标值要等票 08 定发布候选身份。实跑建议为**推到票 08 之后**（同机 loopback 证不了异机
  明文，现在跑要先做一次注定作废的绑定更新），单次成本 20–40 分钟；**用户 2026-08-31 选定 A**，实跑
  连同 `ControlServerCommit` 的更新一起落为
  [`在明文绑定上实跑 staged G3`](issues/13-run-staged-g3-on-the-plaintext-binding.md)（blocked by 08）。
  另记：`StagedG3TlsHarness` 等 TLS 期命名残留不影响行为，改名打击面等于本票杠杆面，另起。
  对车载端仓写入仍为零。
- [`异机明文形态下的跨机联调`](issues/07-run-cross-machine-plaintext-integration.md)
  — **跨机明文形态成立**。宿主 `192.168.200.1`（服务端 `65841df`）↔ Hyper-V guest `192.168.200.50`
  （车载端 `238b46e`）在真正的异机上建立 4 次会话，`SessionHello/CapabilitySnapshot/
  SafetyStateSnapshot/RecoveryStateReport` 各 4、`Heartbeat` 108 全部以明文 NDJSON 过网；投影经明文
  HTTP 送达且 `vehicleKey` 精确匹配。断连重连代次 1→2→3→4 单调推进，协议层行为未因换传输层而改变。
  判可达全程只用 body 往返，三条红侧对照都响。**Ready 未达成，原因不在传输层**：三项是 guest 无
  Modbus IO 硬件（归票 10），`VEHICLE_STATE_UNKNOWN` 已用 RIoT 停/开对照证明可清除、检测器会响。
  **双向错配文本已取全**，其中方向 B 车载端说「ControlServer在会话恢复期间关闭了连接」极具误导性，
  只有服务端侧的 `AuthenticationException` 点出真因。环境用 Production 而非 Development，因为那是
  `IsForbiddenProductionHost` 唯一生效的模式，从原理上排除了 loopback 蒙混。金机零写入、
  `CurrentUser\Root` 全程 44 张、生产服务未受影响、车载端仓写入仍为零。

- [`重写发布手册中被证书机制贯穿的章节`](issues/04-rewrite-the-release-manual-certificate-sections.md)
  — 手册与 `README.md` 已改净并推送（`ControlServer_MVP@56d4b1c`）：不再有任何要求生成／分发／导入／
  续期证书的步骤，剩余命中只有三个仓库的克隆 URL、§4.5 的历史遗留**清理**步骤与 §10 秘密扫描的密钥
  材料**拦截**规则。新增四块：§4.4 异机明文部署（两个地址参数、防火墙 58005／58007「放行范围即暴露
  范围」、判可达只用 body 往返）、§4.5 从证书版本升级（升级器自动做的三件事 ＋ `CurrentUser\Root`
  旧自签根必须人工删，含两条指纹来源与回读确认，明确 `certificateDirectoryRemoved: true` 不代表根证书
  没了）、§8.1 双向错配对照表与三步排除顺序、§11.1 三条明文已知限制（不淡化措辞）。清单外新发现三处
  残留（§9「保留数据根（数据库、证书、日志）」、§9 结果 JSON 的根证书计数、§8 车载端 dev 默认那句），
  按「重新全量搜、不照抄行号」的要求扫出来一并改掉。全部写法对着改后的脚本与两端配置逐条回读取证，
  车载端仓只用 `git show 238b46e:<path>` 读，写入仍为零。

- [`重建不含证书机制的发布候选`](issues/08-rebuild-the-release-candidate-without-tls.md)
  — 候选已重建并冻结为 **0.2.0**（`w2g-rc-20260901-238b46e`，服务端 `56d4b1c` ＋ 车载端 `238b46e` ＋
  `protocol-v0.1.1`），证据提交 `ControlServer_MVP@eaaa5b1`。版本号取 0.2.0 而非 0.1.2：两端不可互通、
  旧站点配置会被显式拒绝启动，patch 位会被读成可就地替换；`0.1.0`／`0.1.1` 保留不可变，回指写进 0.1.1
  说明（动作归票 11）。两端 0 warning、扫描闸门 PASS 且**发布脚本与造出 0.1.1 的那份逐字节相同**
  （这才是「没顺手放宽闸门」的判据），协议九个身份字段与 0.1.1 逐字相同，868/868 哈希且发布根无未哈希
  载荷、红侧翻红。符号级：十个证书相关符号老包 PRESENT→新包 ABSENT，两个新增符号反向，四个对照两侧都在
  ——检测器**两个方向都证明会响**。`RequireHttps` 有框架携带者（ASP.NET Core 自己的 `RequireHttpsAttribute`），
  按自有程序集判定并具名记录。运维要改的两个配置文件里证书字段已消失，站点占位符由七减到六。
  **雾区两条一并答完**：车载端 `238b46e` 在一次性克隆里实测 **113 绿 0 跳过**（对只读仓写入仍为零）；
  版本号与旧 release 关系已定。未安装、未启动、未发布。
  另据实记录：符号探测器第一版因 `@($null).Count -eq 1` 全报 PRESENT，是「不可能的全绿」暴露的假绿，
  已修并归档。
  **票 09 更正**：本票冻结的候选（`56d4b1c`）已作废——手册 §4.5 让站点用包内相对路径跑
  `Update-ControlServerLocal.ps1`，而发布脚本的复制清单里根本没有它，交付包跑不了自己文档化的升级
  路径。候选在 `19ce7db` 重建（`w2g-rc-20260901b-19ce7db`，869 条哈希）。版本号仍 0.2.0；
  「发布脚本与造出 0.1.1 的那份逐字节相同」这条判据形态改为 diff 本身（只有两处新增，秘密扫描闸门
  逐字未动）。详见票 08 的「更正」节。

- [`在明文绑定上实跑 staged G3`](issues/13-run-staged-g3-on-the-plaintext-binding.md)
  — **三个 runner 全跑了，全绿**（票正文记为「视条件」的 vectors runner，其现场库
  `fullloop-20260829T131549Z\controlserver.db` 仍在，故不记未跑）：staged 19/19、restart 20/20、
  vectors 20/20，五十九条断言零失败，全部由 runner 自身发射。先决动作把 `$ControlServerCommit` 从
  TLS 期 `3d8b00c7` 移到候选 `56d4b1c`（单行，`c0f1e84`），`$OnboardCommit` 经自核远端头后不动；
  三条解析链各自回读一致。**比文件哈希更强的判据是进程自报**：restart 的 `sessionIdentity` 跨三次
  重启各报一次 `56d4b1c`／`238b46e`，证明握手的确实是候选服务端与王昆那版车载端。红侧十三行、两个
  检测器各自双向（`useTls` 守卫的 RED／GREEN／**CONTROL**，以及绑定读取器的老 SHA／大写／截断三个
  变异体）。三个 `tls=$false` 类字段本是硬编码字面量，另用二十四行独立观测佐证（四个证书存储指纹
  集合摘要不变、六个根零密钥材料、publish 出的车载端配置无三个 TLS 键、全部日志零 TLS 诊断、生产
  服务 PID 8632 未动、只读仓零写入）。**明确不是候选包验收**：三次 `classification` 均
  `formalSlicePass: false`，四个正式切片保持 `INCONCLUSIVE`。证据 `ControlServer_MVP@b6524ca`。
  票 09 后记：`$ControlServerCommit` 已随候选重建移到 `19ce7db`，但**最后一次真实 G3 执行仍是这一次、
  在 `56d4b1c` 上**；未重跑，理由是两个 commit 之间产品源码零差异（见票 09 第 0 节）。

- [`在新候选上完成干净安装验收`](issues/09-run-clean-install-acceptance.md)
  — **干净安装验收 35 PASS／0 FAIL／4 具名 INCONCLUSIVE，升级路径排练 18/18，红侧 7/7**
  （证据 `ControlServer_MVP@a0f1b3f`）。先决动作发现票 08 候选的**交付缺口**：手册 §4.5 让站点用包内
  相对路径跑升级脚本，而发布脚本的复制清单里没有它——候选遂在 `19ce7db` 重建，票 08／11 已更正。
  票 03 留下的两条都答掉了：**参数化选「补」**（五个参数，默认值等于原硬写值，生产调用形态逐字不变；
  第五个 `-CertificatePasswordVariable` 不补的话排练会清掉生产正在用的机器级口令），于是证书目录删除／
  机器级口令清除／**备份回滚**三段第一次有了真实执行证据——回滚是用「manifest 自洽但起不来」的包把失败
  逼到备份之后触发的，回滚后安装树 0 差异、口令原值恢复、`certs\` 带 3 个文件回来。「安装不碰证书」在
  真实安装里证到：四个存储的**排序指纹集合摘要**全程零变动，加上 30461 行服务端日志搜
  `Schannel|SslStream|AuthenticationException|X509|certificate|https://` 命中 0 作独立佐证。票 14 的
  `INSTALL-AS-SERVICE` 与 `PERSISTENT-LOGS` 两条 INCONCLUSIVE 关掉。`DEMAND-ACCEPTED` 记
  **INCONCLUSIVE 而非 FAIL**：运行时刻 MES 里没有一条需求满足现场条件，改由
  `DEMAND-DECISION-REACHED`（12 条 WIRE_TO_GATE 逐条走到具名判定、零行未分类）承担可证的部分。
  安装器按设计写 `JourneyRuntime.enabled=false`，本票在隔离实例上显式翻开并记为偏离，两个建单闸门
  保持 false、车未动。生产服务 PID 8632 全程零漂移，车载端仓写入仍为零。

- [`在明文候选上完成真车闭环现场验收`](issues/10-run-field-closed-loop-acceptance.md)
  — **闭环走通**：generation 8 在 `w2g-rc-20260901b-19ce7db` 上 `Stage=Completed`、`BlockReasonCode`
  为空、`SessionGeneration` 全程 1（车载端「上层会话已建立」12 分钟内只出现一次，无重连无代次跳变），
  全程 11 分 25 秒。两条真单各建一次、各五步审计齐全、`RiotDispatchAuditEvents=10` 无重复建单，
  `Load`／`Unload` 均 `Committed`。**`DEMAND-ACCEPTED` 本轮第一次绿**，票 09 转来的那条关掉。
  本票的必须重证项成立：明文形态下安全闸门在两条腿各拦一次、停稳各自动放行一次，未卡死旅程；
  安全投影 556 次明文 HTTP GET 全部 200。「本轮无 TLS」用运行没写过的观测证：进程自报
  `transport=plaintext` 与 `http://192.168.200.1:58707`、车载端 `environment=Production` 绑非
  loopback、四个证书存储指纹集合摘要零变动、零密钥材料文件、27336 行日志搜六个 TLS 词命中 0；
  红侧四检测器双向 **8/8**（跑同一份 `-DetectorsOnly`，指纹那条特意数量不变只换一张）。生产服务
  PID 8632 未漂移，车载端仓写入仍为零。证据 `ControlServer_MVP@17aec50`。
  **开跑前的只读预检把「有没有合格需求」变成可查的**，并更正票 09：那 12 条里的
  `BATTERY_POLICY_NOT_SATISFIED` 排在全部静态闸门之后，所以当时**其实有一条需求通过了静态闸门**，
  卡住的是电量策略而非需求池空。
  **三条据实记录**：`HW-REAL-IO` 仍 INCONCLUSIVE（IO 是八仓模拟器，用户选定）；HMI 截图未采集，
  业务节点记录改由车载端日志承担，是取证方式偏离而非等价替换；完成之后暴露一个先于本轮存在的
  受理重放冲突（见 Out of scope）。

## Not yet specified

  （服务端 G2 侧无遗留：票 02 已证 `test-wire-to-gate.ps1` 只是按 `IntegrationSlice` trait 过滤同一套
  xunit 测试，零 TLS 字样，`W2G-IS-00` 过滤后 24 条全绿。车载端 `WireToGateG2Tests` 的 4 行改动已由
  票 06 读过，是纯适配。）
  （车载端 `238b46e` 的测试状态与发布版本号这两条已由票 08 答完，不再是雾：前者在一次性克隆里实测
  113 绿 0 跳过，后者定为 0.2.0 且旧 release 保留加回指。未派生新票，回指的编辑动作并入票 11。）
  （异机明文联调可能暴露的新问题这一条已由票 07 答完，不再是雾：连接错误形态已具名并写成双向
  对照表；非 loopback 绑定下宿主防火墙对内部交换机网段未阻挡，监听地址参数化票 03 已做。未派生新票。）
  （「会话真正走到 `Ready` 需要真实 Modbus 槽位硬件」这条已由票 09 收窄，不再是雾：本机用八仓模拟器
  即可到 `Ready` 并完成 503→200、重启后 generation 推进，票 07 的 `VEHICLE_STATE_UNKNOWN` 是 guest 上
  连模拟器都没有所致。**真实 IO 模块、接线、锁与光幕的资格仍归票 10**，票 09 把它记为具名
  INCONCLUSIVE `HW-REAL-IO`。未派生新票，也不需要中间档位的 IO 取证。）
  （票 09 的 `DEMAND-ACCEPTED` 这条已由票 10 答完，不再是雾：generation 8 真实受理了
  `Q26084908-12|WIRE_TO_GATE` 并走完闭环。附带更正——票 09 那 12 条里的
  `BATTERY_POLICY_NOT_SATISFIED` 排在全部静态闸门之后，当时其实有一条需求通过了静态闸门，
  「MES 里长期取不到合格需求」这个假设不成立。未派生新票。）

  **雾已散尽：票 11 之外没有未具名的待决项。** 票 11 是最后一张，且其前置全部就绪。

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
- **旅程完成后的受理重放冲突**（票 10 现场抓到）。demand 仍留在 MES 目录时，完成后的每次轮询都抛
  `BusinessIdentityConflictException: Accepted demand replay does not match its original order
  intent.`（`WireToGateStore.cs:235`），日志记 `Journey runtime iteration failed closed`。
  fail-closed、不污染已完成的旅程，但会让运行期在完成后无法再受理其他合格需求。**不是本轮改造
  引入的**——调用链在 `WireToGateStore.AcceptCoreAsync` / `DemandIntakeService.AcceptCoreAsync`，
  与传输层无关，且 TLS 期的票 14 gen7 完成之后出现同一条 `failed closed`。本 map 的 Destination
  是传输层安全形态，这属产品行为缺陷，另起一轮。
- **真实 IO 模块（`HW-REAL-IO`）的资格**。票 10 的 IO 输入由用户选定为八仓模拟器，真实 IO 模块、
  接线、锁与光幕仍未取证。本轮 Destination 不含 IO 硬件资格，票 09／10 均按具名外部资格保留。
- **票 29 式 HMI 截图取证**。票 10 现场由用户操作 HMI，未截图，业务节点记录改由车载端日志承担。
  若发布需要截图，属另行补采的动作，不改变票 10 的闭环结论。
- G3 runner 里的 TLS 期**命名与叙述**残留（合成对端类名 `StagedG3TlsHarness`、讲历史的注释）。票 12
  具名但未改：不影响行为，Destination 要的是证书**机制**移除而非改名；改名会同时打穿三个 runner 与
  vectors runner 的 here-string 匹配串，与公共模块抽取同属另起一轮。证据字段 `tls = $false` 等是有意
  记录本轮无 TLS 的，应保留。
