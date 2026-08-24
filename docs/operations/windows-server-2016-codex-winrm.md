# Windows Server 2016 的 Codex 双账户 WinRM 运维

本文说明如何从联网管理机使用 Codex 管理同一厂区网络内、不允许访问互联网的 Windows Server 2016。服务器不运行 Codex；Codex 在管理机上运行，通过 WinRM 调用服务器上的 Windows PowerShell 5.1。

## 已确认的部署信息

| 项目 | 值 |
| --- | --- |
| 服务器 | `WIN-0HD72AV4K31` |
| 服务器地址 | `172.19.205.222` |
| 操作系统 | Windows Server 2016 Standard，build `14393.1884` |
| 服务器网络 | 无互联网访问 |
| 管理机地址 | `172.19.162.241` |
| 远程协议 | WinRM/WS-Management，TCP 5985，`Negotiate` |
| 管理机 TrustedHosts | 仅 `172.19.205.222` |
| WinRM 入站来源 | 仅 `172.19.162.241` |
| SQL Server 实例 | 默认实例 `MSSQLSERVER`（注册标识 `MSSQL16.MSSQLSERVER`） |
| SQL 命令行 | `C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE` |

`14393.1884` 是 2017 年的补丁级别。安装 SQL Server、迁移数据库或部署生产程序之前，必须规划并验证离线 Windows 累积更新；“服务器不能上网”不能作为跳过安全更新的理由。

## 架构和账户

```text
OpenAI/Codex
     |
     | 互联网（仅管理机）
     v
联网管理机 172.19.162.241
     |
     | 厂区网络：WinRM TCP 5985
     v
离线服务器 172.19.205.222
```

使用两个独立本地账户：

- `WIN-0HD72AV4K31\codex-ops`：普通远程管理账户。用于连通性检查、上传经过审核的文件以及将来明确授予的应用目录操作。
- `WIN-0HD72AV4K31\codex-admin`：专用本地管理员。仅在安装离线更新、部署服务、配置 Windows、查看受保护的系统信息或执行已授权的 SQL Server 管理时使用。

不得把内置 `Administrator` 的凭据保留为日常 Codex 凭据。不得将 `codex-ops` 提升为 Administrators。日常任务先尝试 `codex-ops`；只有确实需要提升时才使用 `codex-admin`。

服务器处于工作组而非 Active Directory 域。为了让非内置本地管理员通过 WinRM获得完整管理员令牌，服务器设置：

```text
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
LocalAccountTokenFilterPolicy = 1 (DWORD)
```

该设置会取消所有本地管理员账户的远程 UAC令牌过滤，因此必须同时满足：每个管理员使用唯一强密码、5985仅允许固定管理机地址、管理机 `TrustedHosts` 不使用通配符、日常任务不用管理员账户。若服务器以后加入受管理的 AD域并改用 Kerberos域身份，应评估把该值恢复为 `0`。

## 凭据存储

凭据仅保存在管理机当前 Windows 用户的本地 DPAPI 加密文件中：

```text
%LOCALAPPDATA%\CodexSecrets\agv-server-ops.xml
%LOCALAPPDATA%\CodexSecrets\agv-server-admin.xml
```

这些文件：

- 不得提交到 Git；
- 不得复制到服务器、共享目录、聊天或工单；
- 只能由创建它们的 Windows 用户在同一台管理机上解密；
- 仍应视为高敏感凭据，因为以该 Windows 用户身份运行的程序可以使用它们；
- 应纳入管理机磁盘加密、恶意软件防护和登录保护范围。

临时引导凭据 `%LOCALAPPDATA%\CodexSecrets\server-bootstrap.xml` 只允许在创建或轮换专用账户时短暂存在，完成后立即删除。

## Codex 的连接方法

### 普通账户

```powershell
$server = '172.19.205.222'
$ops = Import-Clixml "$env:LOCALAPPDATA\CodexSecrets\agv-server-ops.xml"

Invoke-Command `
    -ComputerName $server `
    -Credential $ops `
    -Authentication Negotiate `
    -ScriptBlock {
        hostname
        whoami
    }
```

### 管理员账户

```powershell
$server = '172.19.205.222'
$admin = Import-Clixml "$env:LOCALAPPDATA\CodexSecrets\agv-server-admin.xml"

Invoke-Command `
    -ComputerName $server `
    -Credential $admin `
    -Authentication Negotiate `
    -ScriptBlock {
        Get-Service
    }
```

连接前可执行无身份的 WinRM 探测：

```powershell
Test-WSMan -ComputerName 172.19.205.222
```

`Test-WSMan` 成功只证明监听器可达，不证明账户认证或目标命令权限正确。

## 文件传输

使用 PSSession 和 `Copy-Item`，不要开放临时匿名共享：

```powershell
$server = '172.19.205.222'
$ops = Import-Clixml "$env:LOCALAPPDATA\CodexSecrets\agv-server-ops.xml"
$session = New-PSSession -ComputerName $server -Credential $ops -Authentication Negotiate

try {
    Copy-Item `
        -LiteralPath 'C:\path\to\approved-package.zip' `
        -Destination 'C:\Users\codex-ops\Downloads\approved-package.zip' `
        -ToSession $session
}
finally {
    Remove-PSSession $session
}
```

已验证的权限不变量：

```text
WIN-0HD72AV4K31\codex-admin -> IsAdministrator = True
WIN-0HD72AV4K31\codex-ops   -> IsAdministrator = False
```

正式部署时应改用固定的 staging、release 和 rollback 目录；目录权限只授予所需账户，部署脚本必须校验包哈希并保留上一版。

## 使用约定

向 Codex 下达服务器任务时，明确说明目标、账户层级和验证要求，例如：

```text
使用 codex-ops 检查 172.19.205.222 上的部署包是否已上传，只读，不提升权限。
```

```text
使用 codex-admin 在 172.19.205.222 上部署已审核的版本；先备份，失败自动回滚，最后报告服务状态和日志。
```

管理员任务至少遵守：

1. 操作前记录当前状态。
2. 数据库迁移前完成可恢复备份并验证备份文件。
3. 使用明确路径、服务名、实例名和数据库名，不使用宽泛通配符。
4. 不直接编辑正在运行的二进制文件；使用 staging → 验证 → 切换流程。
5. 返回退出码、服务状态、版本、验证结果和回滚位置。
6. 不在聊天或命令输出中打印密码、连接字符串、令牌或真实业务数据。

## SQL Server 边界

SQL Server 部署后优先使用 Windows 身份验证。Windows 本地管理员并不自动等同于每个 SQL Server 实例的 `sysadmin`；应为部署和应用身份分别建立最小数据库权限。

当前服务器已经安装 SQL Server 默认实例 `MSSQLSERVER`，对应注册标识为 `MSSQL16.MSSQLSERVER`；`MSSQLSERVER` 服务当前配置为自动启动。记录这些信息不表示已经验证数据库内容、备份策略、兼容级别或 `codex-admin` 的 SQL权限。

- 应用服务账户只取得运行所需数据库权限。
- 数据库迁移身份与应用运行身份分离。
- 不使用 `sa` 作为 Codex 日常凭据。
- SQL Server TCP端口不因 Codex 运维而对公网开放；程序与数据库同机时优先使用本机连接。
- 查询输出应脱敏；服务器虽然不联网，但 Codex会通过管理机处理必要的命令输出。

根据 [ADR-mes-0028](../adr/mes/0028-high-risk-state-recovery-is-local-administration.md)，`HistoryResetAcknowledgement` 和 `StoragePressurePause` 恢复不得通过远程 WinRM执行。这两类操作只允许授权管理员在数据库主机本地控制台运行 MesIngestLocalAdministration CLI/PowerShell 命令，并保留完整审计。`codex-admin` 不能绕过该边界。

## 网络加固

管理机当前地址是 `172.19.162.241`。在把服务器 WinRM防火墙收紧为单一来源前，应先在 DHCP服务器上为管理机做地址保留，或者为管理机配置经网络管理员批准的固定地址。

加固目标：

- 管理机 `TrustedHosts` 仅包含 `172.19.205.222`；
- 服务器只允许管理机固定地址访问 TCP 5985；
- 不把 WinRM、RDP、SMB或 SQL Server端口暴露到互联网；
- 管理机地址变化时，必须在服务器本地控制台修订防火墙规则后才能恢复远程管理。

如网络不能保证固定来源地址，应使用受控管理子网或部署证书认证的 WinRM HTTPS，不要恢复为 `TrustedHosts=*`。

当前服务器使用规则 `AGV-WinRM-Management-PC` 允许 `172.19.162.241` 访问 TCP 5985，系统默认的宽泛规则 `WINRM-HTTP-In-TCP` 和 `WINRM-HTTP-In-TCP-PUBLIC` 已禁用。管理机地址在 DHCP侧固定前，不得把当前地址视为永久配置；地址发生变化会按设计阻断远程连接。

## 审计和凭据轮换

至少定期检查：

```powershell
Get-WinEvent -LogName 'Microsoft-Windows-WinRM/Operational' -MaxEvents 100
```

```powershell
Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4624,4625 } -MaxEvents 100
```

轮换账户密码时，在管理机安全提示中输入新密码，先在服务器更新账户，再覆盖对应 DPAPI文件；验证新凭据成功后才结束维护窗口。不要在命令行参数或脚本文件中写明文密码。

## 故障处理

- `Access is denied`：确认选用的账户层级以及该任务是否真的需要管理员；不要把 `codex-ops` 临时加入 Administrators。
- `TrustedHosts` 错误：检查管理机的 `WSMan:\localhost\Client\TrustedHosts`，不得改回 `*`。
- 连接超时：检查服务器地址、路由、WinRM服务和服务器防火墙。
- 管理机IP变化：在服务器本地控制台更新允许来源；不要临时开放所有来源。
- `WSMan:\localhost` 返回 HTTP错误8：当前旧系统已复现该本地 WSMan配置提供程序故障。普通远程 WinRM会话仍可使用；本方案不依赖 JEA。完成离线系统更新后再评估该故障，不执行未经验证的 WinRM重置。

## 未启用的 JEA 残留清理

`AGVOps` JEA端点从未成功注册，不属于本方案。由于本机 `WSMan:` Provider 当前存在 HTTP错误8，不用 `Get-PSSessionConfiguration` 验证；在服务器管理员控制台直接检查其插件注册表项：

```powershell
Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WSMAN\Plugin\AGVOps'
```

确认结果为 `False` 后，删除仅由失败尝试产生的两个目录：

```powershell
Remove-Item 'C:\ProgramData\AGVOps' -Recurse -Force
Remove-Item 'C:\Program Files\WindowsPowerShell\Modules\AgvOpsJEA' -Recurse -Force
```

删除后不得再创建或使用 `AGVOps` 端点。
