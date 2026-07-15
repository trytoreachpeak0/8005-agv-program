# RIoT SDK 冒烟测试

对真实 RIoT 实例做最小端到端验证：登录拿 token，再调一个只读接口（设备列表）。

默认**不跑**真实联调（避免离线/CI 失败）。只有设置 `RIOT_SMOKE=1` 时才会访问现场。

## 前置条件

- 本机已安装 [.NET SDK](https://dotnet.microsoft.com/)（跑 C# smoke）
- 能访问目标 RIoT（浏览器能打开同一地址并登录更稳妥）
- 工作目录为仓库内的 `rcs/riot-sdk`

```powershell
cd rcs/riot-sdk
```

Python smoke 另需一次性准备虚拟环境（见下文）。

## 环境变量

| 变量 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `RIOT_SMOKE` | 是（联调时） | 设为 `1` 或 `true` 才执行真实调用 | `1` |
| `RIOT_BASE_URL` | 否 | RIoT 基址（协议+IP+端口）；不设则脚本用内置默认 | `http://172.10.1.72:8888` |
| `RIOT_USERNAME` | 否 | 登录用户名；默认 `admin` | `admin` |
| `RIOT_PASSWORD` | 否 | 登录密码；默认 `admin` | `admin` |

PowerShell 示例（现场已验证可用的一组）：

```powershell
$env:RIOT_SMOKE = "1"
$env:RIOT_BASE_URL = "http://172.10.1.72:8888"
$env:RIOT_USERNAME = "admin"
$env:RIOT_PASSWORD = "admin"
```

换环境时只改 `RIOT_BASE_URL`（以及账号密码）即可，不必改代码。

## C# 冒烟

在已设置上述环境变量后：

```powershell
pwsh ./scripts/smoke-csharp.ps1
```

等价手动命令：

```powershell
dotnet test ./csharp/RIoT.Sdk.Tests --filter FullyQualifiedName~Smoke
```

脚本会强制打开 `RIOT_SMOKE=1`；`RIOT_BASE_URL` 等若已设置则沿用，未设置则回落到脚本内默认值。

### 成功判据

- 输出类似：`Smoke against http://172.10.1.72:8888 as admin`
- 工程编译通过
- 测试摘要：`failed: 0, succeeded: 1`
- 控制台出现类似：`devices.code=0`（业务成功码为 `0`）
- `message=` 后中文可能乱码（控制台编码问题），可忽略；以 `code=0` 为准

## Python 冒烟

### 一次性准备

```powershell
cd python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
cd ..
```

### 执行

在已设置 `RIOT_SMOKE` / `RIOT_BASE_URL` 等环境变量后：

```powershell
pwsh ./scripts/smoke-python.ps1
```

等价手动命令（需已激活 venv 或使用 `.venv\Scripts\python.exe`）：

```powershell
cd python
$env:RIOT_SMOKE = "1"
# 以及 RIOT_BASE_URL / USERNAME / PASSWORD
python -m pytest -q -k smoke --tb=short
```

### 成功判据

- pytest 对应 smoke 用例通过
- 登录拿到非空 token，并能返回设备列表结果（业务 `code` 为成功时与 C# 一致）

未设置 `RIOT_SMOKE` 时，该用例会 **skip**，这是预期行为。

## 失败排查

1. **先浏览器打开** `RIOT_BASE_URL`（例如 `http://172.10.1.72:8888`），确认能登录。
2. TCP 能通但 HTTP **502 / connection reset**：多为现场网络、代理或网关问题，不是 SDK 编译错误。
3. 确认当前 PowerShell 会话里环境变量仍在（新开终端需重新 `$env:... =`）。
4. Python 报找不到 venv：按上文「一次性准备」创建 `.venv` 后再跑脚本。

## 离线 / CI

不设 `RIOT_SMOKE` 时：

- C#：`Login_And_ListDevices_Smoke` 直接返回，计为通过
- Python：smoke 用例 skip

本地只验证编译与单元逻辑时：

```powershell
dotnet test ./csharp/RIoT.Sdk.sln
# 或
cd python && python -m pytest -q
```
