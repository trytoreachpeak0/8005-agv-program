# Windows 双网卡 + 5G 模块 + Clash 分流配置与恢复指南

## 1. 使用场景

笔记本同时连接两个网络：

- **无线网卡（WiFi）**：连接公司网络，用于正常上网。
- **有线网卡（Ethernet）**：连接 5G 模块或 CPE。
- **Clash**：开启 TUN 模式和系统代理模式。
- **目标地址**：`http://172.10.1.72/`
- **5G 模块网关**：`192.168.71.1`

期望效果：

```text
访问互联网
    ↓
WiFi
    ↓
公司网络
    ↓
Clash（根据配置决定是否代理）

访问 172.10.1.72
    ↓
有线网卡 Ethernet
    ↓
192.168.71.1
    ↓
5G 模块
```

## 2. 操作前记录当前配置

建议先使用管理员 PowerShell 保存当前网络状态，方便后续恢复。

```powershell
Get-NetAdapter
Get-NetIPConfiguration
Get-NetRoute -AddressFamily IPv4 |
    Sort-Object DestinationPrefix, RouteMetric |
    Format-Table -AutoSize
```

导出到桌面：

```powershell
Get-NetIPConfiguration |
    Out-File "$env:USERPROFILE\Desktop\network-before.txt"

Get-NetRoute -AddressFamily IPv4 |
    Sort-Object DestinationPrefix, RouteMetric |
    Out-File "$env:USERPROFILE\Desktop\routes-before.txt"
```

## 3. 确认有线网卡名称和地址

```powershell
Get-NetAdapter
Get-NetIPConfiguration
```

假设有线网卡名称为 `Ethernet`，地址属于 `192.168.71.0/24`，网关为 `192.168.71.1`。

后续命令中的 `Ethernet` 必须替换为实际网卡名称。

## 4. 在 Clash 中添加直连规则

Clash TUN 模式可能会通过 `198.18.0.0/16` 等虚拟地址接管流量，因此应先让目标 IP 在 Clash 内部走直连。

在 Clash 配置的 `rules` 中，把规则放在较靠前的位置：

```yaml
rules:
  - IP-CIDR,172.10.1.72/32,DIRECT,no-resolve
```

如果整个 `172.10.0.0/16` 网段都应走 5G 模块：

```yaml
rules:
  - IP-CIDR,172.10.0.0/16,DIRECT,no-resolve
```

修改后重新加载配置或重启 Clash。

> `DIRECT` 只表示不经过代理服务器，并不自动决定使用哪块物理网卡。Windows 静态路由仍然需要配置。

## 5. 添加 Windows 静态路由

使用管理员 PowerShell：

```powershell
New-NetRoute `
    -DestinationPrefix "172.10.1.72/32" `
    -InterfaceAlias "Ethernet" `
    -NextHop "192.168.71.1" `
    -PolicyStore PersistentStore
```

参数说明：

- `DestinationPrefix`：需要定向的目标地址。
- `/32`：只匹配 `172.10.1.72` 这一台主机。
- `InterfaceAlias`：连接 5G 模块的有线网卡。
- `NextHop`：5G 模块网关 `192.168.71.1`。
- `PersistentStore`：重启后仍保留。

如果提示路由已经存在：

```powershell
Get-NetRoute -DestinationPrefix "172.10.1.72/32"
```

## 6. 验证路由选择

```powershell
Find-NetRoute -RemoteIPAddress 172.10.1.72
```

理想结果应包含：

```text
InterfaceAlias : Ethernet
NextHop        : 192.168.71.1
```

不应显示：

```text
InterfaceAlias : Clash
NextHop        : 198.18.x.x
```

也可以执行：

```powershell
Get-NetRoute -DestinationPrefix "172.10.1.72/32"
```

## 7. 测试连接

```powershell
tracert -d 172.10.1.72
Test-NetConnection 172.10.1.72 -Port 80
```

重点查看：

```text
InterfaceAlias
SourceAddress
TcpTestSucceeded
```

最后访问：

```text
http://172.10.1.72/
```

## 8. 关于有线网卡默认网关

### 方案 A：保留 `192.168.71.1` 网关

这是更稳妥的做法，因为目标地址需要经由 `192.168.71.1` 转发。

为了避免普通互联网流量误走有线网卡，可提高有线网卡跃点数：

```powershell
Set-NetIPInterface `
    -InterfaceAlias "Ethernet" `
    -AddressFamily IPv4 `
    -AutomaticMetric Disabled `
    -InterfaceMetric 500
```

WiFi 可保持自动跃点，或设为较低值：

```powershell
Set-NetIPInterface `
    -InterfaceAlias "Wi-Fi" `
    -AddressFamily IPv4 `
    -AutomaticMetric Disabled `
    -InterfaceMetric 20
```

### 方案 B：删除有线网卡默认路由

只有在确认目标网络仍可通过明确静态路由到达时才使用。

先查看：

```powershell
Get-NetRoute `
    -InterfaceAlias "Ethernet" `
    -DestinationPrefix "0.0.0.0/0"
```

删除：

```powershell
Remove-NetRoute `
    -InterfaceAlias "Ethernet" `
    -DestinationPrefix "0.0.0.0/0" `
    -Confirm:$false
```

> 不建议一开始就删除网关。保留网关并提高有线网卡跃点数通常更安全。

# 恢复原状

## 9. 删除静态路由

```powershell
Remove-NetRoute `
    -DestinationPrefix "172.10.1.72/32" `
    -InterfaceAlias "Ethernet" `
    -NextHop "192.168.71.1" `
    -Confirm:$false
```

如果提示找不到路由，先查询实际参数：

```powershell
Get-NetRoute -DestinationPrefix "172.10.1.72/32"
```

验证是否删除：

```powershell
Get-NetRoute -DestinationPrefix "172.10.1.72/32" `
    -ErrorAction SilentlyContinue
```

没有输出即表示已删除。

## 10. 恢复网卡自动跃点

```powershell
Set-NetIPInterface `
    -InterfaceAlias "Ethernet" `
    -AddressFamily IPv4 `
    -AutomaticMetric Enabled
```

如果 WiFi 也改过：

```powershell
Set-NetIPInterface `
    -InterfaceAlias "Wi-Fi" `
    -AddressFamily IPv4 `
    -AutomaticMetric Enabled
```

检查：

```powershell
Get-NetIPInterface -AddressFamily IPv4 |
    Sort-Object InterfaceMetric |
    Format-Table InterfaceAlias, AutomaticMetric, InterfaceMetric
```

## 11. 恢复有线网卡默认网关

### 有线网卡原来使用 DHCP

```powershell
Set-NetIPInterface `
    -InterfaceAlias "Ethernet" `
    -Dhcp Enabled

Set-DnsClientServerAddress `
    -InterfaceAlias "Ethernet" `
    -ResetServerAddresses

ipconfig /renew
```

### 有线网卡原来使用静态 IP

如果只是删除了默认路由，可重新添加：

```powershell
New-NetRoute `
    -DestinationPrefix "0.0.0.0/0" `
    -InterfaceAlias "Ethernet" `
    -NextHop "192.168.71.1"
```

如果需要完整恢复静态地址，可根据操作前记录重新设置。例如：

```powershell
New-NetIPAddress `
    -InterfaceAlias "Ethernet" `
    -IPAddress "192.168.71.100" `
    -PrefixLength 24 `
    -DefaultGateway "192.168.71.1"
```

> `192.168.71.100` 只是示例，必须替换为原来的实际地址，避免地址冲突。

## 12. 撤销 Clash 规则

删除或注释之前添加的规则：

```yaml
- IP-CIDR,172.10.1.72/32,DIRECT,no-resolve
```

或者：

```yaml
- IP-CIDR,172.10.0.0/16,DIRECT,no-resolve
```

然后重新加载 Clash 配置。

如果只是临时排查，也可以关闭：

- TUN 模式
- 系统代理

关闭后重新检查：

```powershell
Find-NetRoute -RemoteIPAddress 172.10.1.72
```

## 13. 一键查看当前状态

```powershell
Write-Host "=== Network Adapters ==="
Get-NetAdapter

Write-Host "`n=== IP Configuration ==="
Get-NetIPConfiguration

Write-Host "`n=== Route to 172.10.1.72 ==="
Find-NetRoute -RemoteIPAddress 172.10.1.72

Write-Host "`n=== Matching Static Route ==="
Get-NetRoute `
    -DestinationPrefix "172.10.1.72/32" `
    -ErrorAction SilentlyContinue

Write-Host "`n=== Connectivity Test ==="
Test-NetConnection 172.10.1.72 -Port 80
```

## 14. 常见问题

### `Find-NetRoute` 仍显示 Clash

检查：

1. Clash 直连规则是否位于其他匹配规则之前。
2. Clash 配置是否已经重新加载。
3. `/32` 静态路由是否实际存在。
4. 有线网卡是否为 `Up`。
5. 有线网卡是否具有 `192.168.71.x` 地址。
6. `192.168.71.1` 是否可达。

```powershell
ping 192.168.71.1
```

### 可以访问网关，但不能访问 `172.10.1.72`

可能原因：

- 5G 模块侧没有到 `172.10.1.72` 的路由。
- 运营商专网或 APN 未正确建立。
- 目标设备没有开放 TCP 80。
- 目标端禁止 ICMP，所以 ping 失败但网页可能仍可访问。
- 5G 模块存在 NAT、ACL 或防火墙限制。

```powershell
Test-NetConnection 172.10.1.72 -Port 80
tracert -d 172.10.1.72
```

### 删除路由后仍看到 Clash 路由

Clash TUN 会动态创建自己的路由，这不一定是手动添加的 `/32` 路由。

重点检查：

```powershell
Get-NetRoute -DestinationPrefix "172.10.1.72/32"
```

只要手动创建的 `/32` 路由已删除，Windows 侧的恢复就已完成。
