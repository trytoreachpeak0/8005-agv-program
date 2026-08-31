# 从安装、卸载、更新与 G3 runner 中拆除证书机制

Type: task
Mode: AFK
Status: open
Blocked by: 01

## Question

用户选择「全拆」而非「留着不用」：安装链里只要还会生成证书、还带 `-InstallCurrentUserRoot` 这类
参数，他要的部署复杂度下降就没有兑现。本票在 `8005-agv-control-server` 拆掉整条证书机制。

已定位的承载点：

- `scripts/Install-ControlServerLocal.ps1` — 生成自签根与 `localhost` 叶证书、导出 PFX 与 PEM、
  写 `certificate.caCertificateFile`／指纹进安装结果 JSON、健康检查钉扎根证书、
  `-InstallCurrentUserRoot` 参数、失败回滚时「移除导入的根证书」那一支；
- `scripts/Uninstall-ControlServerLocal.ps1` — 结果 JSON 里「根证书移除了几张」及相应逻辑；
- `scripts/Update-ControlServerLocal.ps1` — 同类证书处理；
- `scripts/run-staged-g3.ps1`、`scripts/run-staged-g3-restart.ps1`、
  `scripts/Invoke-AuthorizedAbsentObservationShadow.ps1` — `-InstallTemporaryCurrentUserRoot`
  授权、临时根证书的安装与 `finally` 移除；
- `scripts/New-WireToGateReleaseCandidate.ps1` — 打包时与证书相关的处理和校验。

拆除后健康检查改为直接经 HTTP 请求，不再需要钉扎任何根证书，也不再需要 `--ssl-revoke-best-effort`
之类的绕行参数。数据根下的 `certs\` 目录是否保留由票 01 的配置面决定。

风险与约束：

- 这三个 G3 runner **零测试覆盖，且承载上一轮全部证据**。上一轮票 24 曾拒绝改动它们，理由是风险
  不对称。本轮不得不动它们，因此改动要最小化，只摘证书相关分支，不顺手重构、不抽公共模块（那仍
  在 Out of scope）。
- 安装脚本的失败回滚路径必须保持完整：删服务、删安装目录、还原机器作用域环境变量。只移除其中
  「移除根证书」那一步，不得削弱其余回滚。

完成判据：在隔离实例上跑通安装→启动→停止→再启动→强制重启→卸载全流程，结果 JSON 据实记录服务
与目录状态，全程无任何证书生成、导入或移除动作，且**不弹出任何信任确认对话框**，可在非交互环境
完整跑完。生产服务全程不受影响。
