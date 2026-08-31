# 重写发布手册中被证书机制贯穿的章节

Type: task
Mode: AFK
Status: open
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
