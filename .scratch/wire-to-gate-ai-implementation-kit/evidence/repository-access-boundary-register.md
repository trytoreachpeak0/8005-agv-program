# WIRE_TO_GATE 仓库、外部输入与责任边界登记

核查日期：2026-08-25（Asia/Taipei）

## 资格用语

- **Fake 可用**：产品可在受控开发环境与模拟对端/模拟 IO 完成软件闭环；不证明真实 RIoT、真实 IO 或目标硬件。
- **目标软件可用**：两端在本周指定的 Windows 运行环境安装、启动、重启并通过适配器核验；不外推到真实车载工控机和真实八仓 IO。
- **工厂可用**：还需真实 RIoT 移动、安全负责人、现场/物料条件与后续真实硬件证据；本轮不得由 Fake 结果替代。

## 三仓登记

| 产品 | 远程仓库 | 可见性 / 分支 | 负责人 / 批准人 | 2026-08-25 回读 |
| --- | --- | --- | --- | --- |
| ControlServer | `https://github.com/trytoreachpeak0/8005-agv-control-server` | Private；`main`；`ControlServer_MVP` | `szy` | 已登录 GitHub 页面可见；主分支与开发分支均存在；各显示 1 个初始 commit，仅 `README.md` |
| OnboardHmi | `https://github.com/trytoreachpeak0/8005-agv-onboard-hmi` | Private；`main`；`OnboardHmi_MVP` | 王昆 / 王昆 | 已登录 GitHub 页面可见；主分支与开发分支均存在；各显示 1 个初始 commit，仅 `README.md` |
| 共享协议 | `https://github.com/trytoreachpeak0/8005-agv-protocol` | Public；`main`；正式协议用不可变 tag/release | `szy`；正式 release 需两名真实负责人确认 | 已登录 GitHub 页面可见；显示 1 个初始 commit，仅 `README.md` |

## 访问与发布边界

- 当前浏览器会话以 `trytoreachpeak0` 登录，可读取三仓及私有仓库设置入口。
- 本机终端无 `gh` 命令；三仓 `git ls-remote` 均因 `SEC_E_NO_CREDENTIALS` 失败。因此当前终端尚不具备可验证的 clone/fetch/push 能力，这会阻断产品分支的远程实施。
- `SocialKKKK` 的 OnboardHmi 与协议仓库邀请曾记录为 `Pending Invite`；本次进入协作设置时 GitHub 要求 sudo 二次认证，未输入密码，所以不将“能接受”推断为“已接受”。
- 不收集、写入或发布密码、token、私钥、PFX、CallApiKey 或车辆共享密钥。证据只保存安全引用名与核验结果。
- 产品代码不强制 PR；每次跨端变更仍必须绑定精确协议候选/release 身份。AI 不代替人员批准正式 tag/release。

## 外部输入与阻断层级

| 输入 | 已具备 / 已验证 | 待提供 / 待回读 | 阻断层级 |
| --- | --- | --- | --- |
| ControlServer 本周主机 | Windows 11 开发电脑；技术栈已在研究票冻结 | 最终 CPU/内存/端口/服务账户在安装候选时回读 | 目标软件可用 |
| OnboardHmi 本周主机 | 虚拟工控机；Windows 10/11；1024×768；100%；鼠标；普通键盘；扫码结束符 Enter | 王昆冻结 UI/运行时/持久化/测试入口 | Fake 可用与目标软件可用 |
| 八仓 IO | 本轮使用独立模拟器；真实 IO 资格不在本轮声称 | 王昆冻结协议、进程边界、地址、八仓初始状态与故障注入 | Fake 可用；真实 IO 留作后续目标硬件门禁 |
| MesIngest | 现有实现可启动；含 WIRE_TO_GATE 测试数据；与 ControlServer 同机；使用只读 V2 | 运行时回读 loopback `BaseUrl`；同机不需 `SharedSecret` | 目标软件可用 |
| RIoT | `BaseUrl=http://172.19.206.222:8888`；Map `25`；显示车名“老厂前线新多仓位1”；CallApiKey 已准备；安全负责人 `szy`；用户已表示可以在测试环境移动 | 通过真实环境只读解析技术车辆 ID、取货站、关卡站；在实际移动前仍需当轮明确授权和安全条件 | 真实移动闭环 / 工厂可用；不阻断 Fake 软件开发 |
| ControlServer—HMI 安全链路 | 两机网络互通；防火墙端口可配 | 开发时生成自签名 TLS 证书、固定信任指纹和测试车辆独立共享密钥，仅通过安全引用注入 | Fake 可用与目标软件可用 |
| 本周验收 | 最终软件验收人 `szy`；OnboardHmi 验收人王昆；本周不要求真实物料 | 王昆完成车载端责任人决策；发布前用户完成可用性验收 | Release Candidate / 正式发布 |

## 结论

仓库身份、分支、本周目标环境、责任人和安全边界已足以完成登记。下一步不应继续补写登记文档，而是单独打通终端 Git 认证/克隆推送能力，并由王昆完成 OnboardHmi/IO 决策与仓库邀请回读。
