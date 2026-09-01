# 登记真实仓库、外部输入、权限与责任边界

Type: task
Mode: HITL
Status: resolved

## Question

实际 ControlServer 与 OnboardHmi 仓库的 URL、分支、目标技术栈、构建/测试/发布入口、负责人及访问限制分别是什么；八仓 IO/接线、目标屏幕与输入设备、RIoT、MesIngest、测试环境、部署主机、秘密引用和协议/UI/联调/现场责任中，哪些已经具备、哪些必须在第 1 天提供、分别阻断 Fake 可用、目标硬件可用还是工厂可用？

本票建立可审计登记，区分已验证事实、待提供事实、无秘密引用和测试 Fake；不收集密码、token、私钥或车辆凭据，不以默认值填充安全/硬件/生产事实。仓库尚不存在时，必须由用户明确决定新建位置和所有者；AI 不得从当前单仓布局推断它就是任一生产仓库。

## Comments

### 2026-08-25 用户提供的仓库与责任事实

- ControlServer 仓库：`https://github.com/trytoreachpeak0/8005---AGV.git`，即当前工作区远程；默认分支 `main`，允许开发分支 `ControlServer_MVP`；负责人及批准人为 `szy`；用户确认具有提交和推送权限。
- OnboardHmi：当前没有仓库；负责人及批准人为王昆；用户当前没有一个既有 OnboardHmi 仓库的推送权限。用户允许使用 GitHub 账号 `trytoreachpeak0` 创建新仓库后授予王昆权限，但仓库名、可见性、王昆 GitHub 用户名和权限级别仍待确认。
- 共享协议仓库：当前不存在；目标所有者 `trytoreachpeak0`，目标名称 `8005-agv-protocol`，可见性 `Public`。用户授权在其审阅后创建和推送；共同协议批准人为用户本人。
- 合并策略：产品代码不强制 Pull Request。即使不使用 PR，共享协议仍必须保留精确候选身份和真实批准记录。
- 同事对三个仓库的当前访问状态未知。
- 一周交付首选且仅接受远程仓库；用户不接受以校验 ZIP 作为权限延误时的交付替代。因此远程创建、认证和协作者访问是硬期限门禁。
- 不记录或索取密码、GitHub token、证书、私钥或车辆秘密；只核验现有认证是否能执行已批准动作。

### 2026-08-25 用户修正与新增授权

- 用户修正此前判断：当前 `https://github.com/trytoreachpeak0/8005---AGV.git` 不作为生产 ControlServer 主程序仓库；ControlServer 主程序也必须创建独立仓库。目标仓库名、可见性和分支配置仍待最后确认。
- OnboardHmi 仓库采用推荐配置：所有者 `trytoreachpeak0`，仓库名 `8005-agv-onboard-hmi`，可见性 `Private`，默认分支 `main`，开发分支 `OnboardHmi_MVP`。
- OnboardHmi 负责人王昆的 GitHub 用户名为 `SocialKKKK`。
- 用户允许创建所需远程仓库。OnboardHmi 计划向 `SocialKKKK` 授予 `Write`；共享协议仓库的协作者权限及正式 release/tag 限制仍按协作契约执行。

### 2026-08-25 远程仓库创建与访问结果

- ControlServer 独立生产仓库已创建：`https://github.com/trytoreachpeak0/8005-agv-control-server`；可见性 `Private`，默认分支 `main`，开发分支 `ControlServer_MVP` 已创建；负责人及批准人为 `szy`。
- OnboardHmi 独立生产仓库已创建：`https://github.com/trytoreachpeak0/8005-agv-onboard-hmi`；可见性 `Private`，默认分支 `main`，开发分支 `OnboardHmi_MVP` 已创建；负责人及批准人为王昆。
- 共享协议仓库已创建：`https://github.com/trytoreachpeak0/8005-agv-protocol`；可见性 `Public`，默认分支 `main`；正式协议批准、不可变 tag 与 release 仍由用户控制。
- 已向 `SocialKKKK` 发出 OnboardHmi 仓库协作者邀请；GitHub 当前状态为 `Pending Invite`，接受后获得推荐的直接协作者写权限。
- 已向 `SocialKKKK` 发出共享协议仓库协作者邀请；GitHub 当前状态为 `Pending Invite`，接受后获得推荐的直接协作者写权限。
- 未向 `SocialKKKK` 授予 ControlServer 仓库访问权限，符合已确认的职责边界。
- 下一项外部动作：王昆使用 `SocialKKKK` 接受上述两项 GitHub 邀请；在接受前，不得把“同事已有远程写权限”记为已满足。
- 三个仓库目前只含初始化 README；AI 开发 Spec、候选协议资产及首个可执行切片尚未发布，必须由后续路线票生成、审核并推送。

### 2026-08-25 一周交付目标修正

- 用户明确一周交付是整个可使用的 MVP 软件，不是开发文档或 Spec。本票因此把技术栈、构建发布入口和真实环境输入提升为第 1 天硬门禁；仓库创建本身不再算一周交付结果。

### 2026-08-25 外部集成边界确认

- 八仓 IO：本轮允许并要求用模拟器实现。模拟器用于产品开发和受控软件验收，不代表真实 IO 模块、接线、仓锁或光幕已经通过目标硬件资格。
- RIoT：用户确认无法模拟。本轮不得建设 RIoT 模拟器或用 Fake RIoT 结果冒充集成通过；完整移动闭环必须连接真实 RIoT 测试环境。
- MesIngest：当前已经存在，ControlServer 应复用其发布的只读 V2 契约，不重新实现 MesIngest。
- “目标硬件”指软件最终实际运行设备及其运行条件：ControlServer 主机/VM 的 OS、架构、资源和网络；OnboardHmi 车载工控机的 OS、架构、屏幕分辨率/DPI、触摸、扫码枪、键盘和网络。若只在开发机验收，则结论只适用于该开发机，不能外推为车载硬件通过。
- “测试凭证”不是 GitHub 凭证。当前已知包括：RIoT `BaseUrl` 与 `CallApiKey`（AdminLogin 仅为备用）；MesIngest 非 loopback 读取使用的 `BaseUrl` 与 Bearer `SharedSecret`；ControlServer—OnboardHmi 测试连接的服务端自签名 TLS 固定信任值和测试 AGV 独立共享密钥。秘密值只通过安全渠道/环境变量/受 ACL 保护配置提供，票据只登记引用与核验结果。
- 仍待用户提供或指定：真实 RIoT 测试环境 BaseUrl、CallApiKey 的安全交付方式、测试 AGV/Map/取货站/关卡站绑定和允许执行移动的测试时间窗；MesIngest 部署 BaseUrl，以及若跨机访问时 SharedSecret 的安全交付方式；两端目标机器信息。

### 2026-08-25 用户填写的实施环境表

- 截止时间：2026-08-28 17:00；相对当前日期只有约三个工作日。
- ControlServer：技术栈待快速研究决定；本周运行在开发电脑，Windows 11。
- OnboardHmi：技术栈由王昆决定；本周运行在虚拟工控机，Windows 10 或 Windows 11，1024×768、100% 缩放；触控屏场景本周使用鼠标，扫码结束符 Enter，普通键盘可用。真实工控机、触摸屏和扫码枪型号不纳入本周资格。
- IO 模拟器：具体形式、地址和初始状态由王昆决定；本周不验证真实八仓 IO。
- MesIngest：已存在且能够启动，包含 WIRE_TO_GATE 测试数据；与 ControlServer 同机。本轮开发迁移到另一台电脑时 MesIngest 与 ControlServer 一起迁移，因此不跨机读取、不需要 SharedSecret。实际 loopback BaseUrl 待启动时回读确认。
- RIoT：BaseUrl 按现有 SDK 地址规范化为 `http://172.19.206.222:8888`；测试车辆显示名“老厂前线新多仓位1”，Map `25`，车辆已绑定该 Map；CallApiKey 已准备；允许任何时间实际下发测试移动；安全负责人邵正宇。RIoT 技术车辆 ID、取货站和关卡站待定，须通过真实环境只读查询冻结。
- 安全与网络：ControlServer—HMI 测试自签名 TLS 证书和测试车辆共享密钥按推荐值在开发时生成并安全注入；两台机器网络互通，防火墙端口可配置。
- 验收：最终软件验收人为 `szy`（邵正宇/用户本人），OnboardHmi 验收人为王昆；本周不要求真实物料试运行。
- GitHub 邀请状态一栏填写为“能”，不能确定它表示“能够接受”还是“已经接受”；在 GitHub 显示 accepted 前仍按待确认处理。

## Answer

已完成[《WIRE_TO_GATE 仓库、外部输入与责任边界登记》](../evidence/repository-access-boundary-register.md)，并将资格明确分成 Fake 可用、目标软件可用和工厂可用，避免用一个模糊的“可用”掩盖外部门禁。

2026-08-25 通过已登录 GitHub 页面回读确认：三个目标远程仓库均存在，ControlServer 与 OnboardHmi 为 Private，协议仓库为 Public；`main`、`ControlServer_MVP`、`OnboardHmi_MVP` 按登记存在；三仓当前均只含 1 个初始 commit 和 `README.md`，还没有产品实现。

边界已冻结：ControlServer 由 `szy` 负责，OnboardHmi 由王昆负责，正式 ProtocolRelease 不得由 AI 代替人员批准；密码、token、私钥、证书和车辆密钥只保存安全引用，不进入 Git/日志/证据。MesIngest 复用同机只读 V2；八仓本轮以独立模拟器验证软件闭环；真实 RIoT 移动、真实 IO 与工厂条件保持独立资格门禁。

本次同时暴露一项可操作阻断：当前终端无 `gh`，三仓 `git ls-remote` 均因 `SEC_E_NO_CREDENTIALS` 失败；GitHub 协作设置又需二次认证，因而 `SocialKKKK` 邀请仍只能记为未验证。已新建[《打通三仓终端认证、克隆与推送能力》](05-provision-authenticated-product-repository-access.md)，并将其置于产品骨架之前。
