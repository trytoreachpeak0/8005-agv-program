# 重写发布手册中被证书机制贯穿的章节

Type: task
Mode: AFK
Status: resolved
Blocked by: 02, 03, 07

## Question

`docs/RELEASE-CANDIDATE.md` 是随包分发的部署权威，证书机制贯穿了它的多个章节。产品代码与脚本改完
之后，手册若不同步，现场会照着一份已经不成立的步骤部署。

**票 01 之后新增对票 07 的阻塞**：手册要写的异机部署步骤与错配错误对照表都以联调实测为准，先写完
再据联调结果重写反而更贵。

已定位的承载段落（行号以当前 `e5ee065` 为准，实施时按实际重新定位）：

- 第 117～128 行 — 安装脚本流程描述：「生成自签根与 `localhost` 叶证书并导出 PFX 与 PEM」、
  健康检查不依赖系统信任存储的说明、`-InstallCurrentUserRoot`、回滚时移除根证书；
- 第 157～178 行 — 健康检查用 `https://localhost:58007` 并钉扎本次安装生成的根证书、
  `--ssl-revoke-best-effort` 的说明；
- 第 188 行 — 数据根同时容纳 `certs\` 与 `logs\`；
- 第 210～222 行 — 配置注意事项：`REPLACE_*` 占位符清单中的 `serverCertificateSha256`、
  `vehicleSafety.endpoint` 必须指向 HTTPS 端点、异机部署把 `caCertificateFile` 交给车载端管理员
  导入 `CurrentUser\Root`、「不要用跳过 TLS 校验代替信任配置」；
- 第 223 行附近 — 随包默认配置中 `useTls=false` 的说明（语义已变，不再是「开发默认」而是唯一形态）；
- 第 295～296 行 — 已知限制中的「TLS 身份」条目：现场部署必须换成受控签发的证书并同步指纹；
- 第 333～334 行 — G3 runner 的 `-InstallTemporaryCurrentUserRoot` 授权说明。
- **票 03 补入，原清单遗漏**：第 **245** 行的 `-TrustedRootThumbprint <安装结果里的指纹>`（该参数已从
  `Uninstall-ControlServerLocal.ps1` 删除），以及 `README.md` 第 **92** 行的 `-InstallCurrentUserRoot`
  （票 02 已把 `README.md` 整体留给本票）。

  **实施时不要照抄本清单的行号**：以上行号以 `e5ee065` 为准，票 02／03 之后须按实际重新定位；且
  已经出现过一次「照清单走会漏」的情况，请对 `docs/` 与 `README.md` 重新全量搜
  `certificate|cert|thumbprint|CurrentUserRoot|pfx|pem|https|TLS|ssl` 后逐条判定。

同时必须**新增**而非仅删除的内容：

- 异机明文部署的实际步骤：服务端监听地址（票 03 新增的 `-ListenAddress` / `-HealthBindAddress`）、
  防火墙端口、车载端配置的对应项；
- **已知限制里三条新条目**，措辞不得淡化：其一，车载凭据 `credentialProof` 以明文经网络传输，抓包
  即可永久冒充车载端；其二，`motionState` 等安全闸门输入经明文传输后可被篡改，票 14 证过的
  「移动中拦、停稳放行」在不可信网络下不再成立；其三（票 01 第 3 节新增），Kestrel 单一绑定意味着
  异机部署下 `/health/live` 与 `/version` 随投影端点一并暴露于厂内网。三条均为用户 2026-08-31 知情
  接受的代价，手册须据实写明适用前提是受控的工厂内网；
- **升级已有安装的人工清理步骤**（票 01 第 5 节）：`CurrentUser\Root` 里当初经 `-InstallCurrentUserRoot`
  导入的自签根证书不由脚本删除，手册须给出指纹来源与手工删除步骤，并写明脚本清理结果不覆盖这一项；
- **新旧两端错配的错误对照表**（票 01 第 7 节）：两端必须同版本升级；附票 07 实测到的双向错误文本，
  使现场能把版本错配与「网络不通」区分开。

完成判据：手册中不再残留任何要求生成、分发、导入或续期证书的步骤；新增的异机明文步骤与票 02、03
的实际实现逐条对应（对着改后的脚本与配置回读核对，不得凭记忆撰写）；两条已知限制原文进入手册。

## Answer

手册与 `README.md` 已改完并推送：`ControlServer_MVP@56d4b1c`（`Rewrite the release manual for the
plaintext transport`）。全程只动 `8005-agv-control-server`，车载端仓写入仍为零（只用
`git show 238b46e:<path>` 只读取证）。

### 0. 不照抄清单，重新全量定位

按票的要求没有按 `e5ee065` 的行号走，而是对 `docs/` 与 `README.md` 重搜
`certificate|cert|thumbprint|CurrentUserRoot|pfx|pem|https|TLS|ssl|证书|指纹|信任` 逐条判定。结果：

- 承载段落全在 `docs/RELEASE-CANDIDATE.md` 与 `README.md` 两个文件里；`docs/ai-spec/`、
  `docs/defects/`、`docs/authorized-absent-observation-manual-runbook.md` 搜
  `InstallCurrentUserRoot|TrustedRootThumbprint|serverCertificateSha256|useTls|--cacert|localhost-development-root|InstallTemporaryCurrentUserRoot`
  命中 0，无需改动。
- 清单遗漏两处已按票 03 的补充处理：`RELEASE-CANDIDATE.md` 卸载命令里的 `-TrustedRootThumbprint`、
  `README.md` 的 `-InstallCurrentUserRoot`。
- 清单**未列、本次新发现**的还有三处：§9 「保留数据根（数据库、证书、日志）」、§9 结果 JSON
  「根证书移除了几张」（该字段在现脚本的结果对象里已不存在）、§8 那句「随包开发默认
  `useTls=false`」旁边的 `wireToGate.enabled=false` 也需要连带核对（现车载端 dev 配置里
  `vehicleSafety.enabled` 也是 `false`，原文没提）。

### 1. 逐条对着改后的实现回读，不凭记忆

| 手册写的 | 回读来源 |
| --- | --- |
| 安装不再生成／导入证书；`-ListenAddress`／`-HealthBindAddress` 默认 `127.0.0.1` | `Install-ControlServerLocal.ps1` param 块与 `$healthOrigin`／`$healthCheckHost` 的通配回落逻辑 |
| 健康检查直连 http、不带 `--cacert` | 同文件 `Invoke-LiveCheck`／`Get-ReadyCheck`／`Get-VersionCheck` |
| 安装结果字段 `onboardTransportEndpoint`／`httpEndpoint`／`httpCheckOrigin`／`transport` | 同文件结果对象（`schemaVersion = 2`） |
| 卸载脚本无 `-TrustedRootThumbprint`、结果 JSON 无根证书计数 | `Uninstall-ControlServerLocal.ps1` param 块与结果对象 |
| 升级自动做的三件事、`certificateRemoval` 段字段名 | `Update-ControlServerLocal.ps1` 的 `Convert-RetainedConfigurationToPlaintext` 与结果对象 |
| 四个过时键、启动期拒绝 | `OnboardTransportOptionsValidator.RemovedKeys` |
| 车载端模板占位符清单、`endpoint` 为 http、无 `serverCertificateSha256`／`useTls` | `238b46e:src/SQCD.Agv.Wpf/appsettings.Production.example.json` |
| 车载端拒绝残留键的逐字文案 | `238b46e:src/SQCD.Agv.Infrastructure/Configuration.cs:138-144` |
| 车载端 dev 默认 `wireToGate.enabled=false`、`vehicleSafety.enabled=false` | `238b46e:src/SQCD.Agv.Wpf/appsettings.json` |
| G3 runner 不再需要 `-InstallTemporaryCurrentUserRoot` | 三个 runner 的 param 块与顶部注释 |

人工清理步骤里的指纹来源也是回读的，不是编的：TLS 期安装脚本（`3d8b00c7`）的结果对象里字段名为
`certificate.trustedRootThumbprint`，根证书主题固定为
`CN=8005 AGV ControlServer Local Development Root <runId>`，故手册给出「旧结果 JSON 优先、丢失时按
主题前缀查」两条来源，并要求删除后回读确认（无输出才算删掉）。

### 2. 新增的四块内容

- **§4.4 异机（非 loopback）明文部署**：两个地址参数、通配时脚本自身改拨 loopback 的原因、防火墙
  放行 58005／58007 且「放行范围就是暴露范围」、判可达只用 body 往返（全局代理会让 ping 与 TCP
  connect 对不存在的主机都成功）、车载端两项对应配置。
- **§4.5 从证书版本升级已有安装**：升级器自动做的三件事（删四个过时键、`Health:url` 改写、删
  `certs\` 与机器级证书口令变量），以及**脚本不做的那一件**——`CurrentUser\Root` 的旧自签根。明确写了
  `certificateDirectoryRemoved: true` 不代表根证书没了，避免假绿。
- **§8.1 错配错误对照表**：票 07 实测的双向逐字文本，点名方向 B 的「ControlServer在会话恢复期间
  关闭了连接」最具误导性，并给出三步排除顺序（服务端日志 → `SessionHello` 计数 → 才怀疑网络）。
- **§11.1 明文传输的已知限制**：三条按票的要求不淡化措辞——凭据抓一次包即可永久冒充（静态密钥、
  重放无时间窗）；`motionState` 可篡改使「移动中拦、停稳放行」在不可信网络下不再成立，并写明这是
  safety 而非 security 后果；health／version 随投影一并暴露，且写明有意不加端点过滤与 IP 白名单的
  理由。结尾点明适用前提是受控厂内网，不满足时该解决网络隔离而非叠补偿。

原 §11 的「TLS 身份」条目替换为「受控厂内网是部署前提」并指向 §11.1。

### 3. 完成判据核对

- **不再残留任何要求生成／分发／导入／续期证书的步骤**：复扫后剩余命中全部属于三类——三个仓库的
  `https://` 克隆 URL、§4.5 的历史遗留**清理**步骤（本就是要写的）、§10 秘密扫描闸门里对
  `.pfx`／`.pem` 等密钥材料文件的**拦截**规则（是发布门禁，保留正确）。无一条要求现场制备证书。
- **新增步骤与票 02／03 实现逐条对应**：见第 1 节表格，全部回读取证。
- **已知限制原文进手册**：§11.1 三条，含票 01 §3 新增的第三条。

### 4. 未做与留待

- 手册第 2 节的构建流程、第 12 节的门禁状态（`W2G-IS-00～07` 与 RC 仍为 `INCONCLUSIVE`）未动，
  那是票 08／11 的范围。
- 手册没有写发布版本号，仍以 `release-manifest.json` 为准——版本号归票 08 附近再定。
- 本票只改文档，未触产品代码、脚本与测试，按 AGENTS.md 的 tier 规则不触发 tier 1。
