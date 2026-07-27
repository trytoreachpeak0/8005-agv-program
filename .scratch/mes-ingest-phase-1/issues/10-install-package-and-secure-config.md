# 10 — 工厂可拷贝安装包与安全配置

**What to build:** 自包含安装目录（Service、可选 WPF、配置模板、queries/）可整包拷到工厂机；含安装/启停/卸载说明；默认只绑 localhost；若开放非本机访问须配置共享密钥或等效鉴权；真实凭证不进包、不进仓。

**Blocked by:** 08 — Oracle 生产快照源与诊断探针; 09 — WPF 盯盘薄客户端

**Status:** ready-for-agent

- [ ] 发布产物为自包含安装目录：Service、配置模板、queries/、可选 WPF
- [ ] 文档覆盖 Windows Service 安装、启动、停止、卸载
- [ ] 默认 HTTP 仅监听 localhost
- [ ] 若绑定超出 localhost，须启用可配置共享密钥或等效鉴权，并在安装配置中说明
- [ ] 安装包与仓库均不含真实 MES/SQL 凭证；仅提供填空模板
- [ ] 说明日志位置、版本信息与基本故障排查入口
