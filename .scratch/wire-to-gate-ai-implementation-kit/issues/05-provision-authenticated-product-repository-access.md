# 打通三仓终端认证、克隆与推送能力

Type: task
Mode: HITL
Status: resolved
Blocked by: 03

## Question

如何在不记录或泄露 token、密码、私钥的前提下，让当前开发终端对 `8005-agv-control-server`、`8005-agv-onboard-hmi` 和 `8005-agv-protocol` 具备可验证的 clone/fetch/push 能力，并建立三个受控本地工作目录？

本票必须使用用户选择的 GitHub 支持认证方式，只回读账户/仓库/分支和最小推送结果，不将凭据写入仓库、票据、日志或证据。共享协议仍禁止未经人员批准创建正式 tag/release；本票只打通开发通道。

## Answer

已在不读取、记录或显示任何 token/密码/私钥的前提下，打通当前开发终端的三仓 Git 通道。本机 Git `2.55.0.windows.4` 使用 Git Credential Manager `2.9.0`；沙箱外只读列表确认已登记 GitHub 账户 `trytoreachpeak0`。先前 `SEC_E_NO_CREDENTIALS` 是沙箱无法访问 Windows 凭据存储的执行环境现象，不是远程凭据真实缺失。

三个独立本地生产工作目录已在 `C:\Users\szy\Desktop\xinji\` 下建立，未嵌入当前规划仓库：

| 工作目录 | 当前分支 / commit | 远程 | 核验 |
| --- | --- | --- | --- |
| `C:\Users\szy\Desktop\xinji\8005-agv-control-server` | `ControlServer_MVP` / `6b93ce4d7d65818661155a312957d0205bc37a1c` | `trytoreachpeak0/8005-agv-control-server` | clean；fetch dry-run 成功；push dry-run 成功 |
| `C:\Users\szy\Desktop\xinji\8005-agv-onboard-hmi` | `OnboardHmi_MVP` / `070ddfe03b801deb860010d51f5396e1d06355bb` | `trytoreachpeak0/8005-agv-onboard-hmi` | clean；fetch dry-run 成功；push dry-run 成功；远程 `main` 为王昆已真实推送的 `bc56fa9aebd98e8cd488fa1f30a0d95bfd40c93e` |
| `C:\Users\szy\Desktop\xinji\8005-agv-protocol` | `main` / `76d571647ed61c32d6f5e40cfc11dd7144ad3879` | `trytoreachpeak0/8005-agv-protocol` | clean；fetch dry-run 成功；push dry-run 成功 |

本票未创建无意义 commit，未推送远程变更，未创建 tag/release，也未改变任何仓库权限。后续产品实施将在上述独立工作目录中进行，并分别遵守各仓的 `AGENTS.md`/`CONTEXT.md` 与测试门禁。
