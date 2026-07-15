# RIoT SDK

位于本仓库 `rcs/riot-sdk`，由 **8005多仓位AGV** 统一做 Git 管理。提供 RIoT（斯坦德 RCS）的 **C#** 与 **Python** 两套 API SDK。

结构：

- `specs/` — device / task / order 三个核心 OpenAPI 原文（来自 `rcs/riot_swagger`）
- `scripts/generate.ps1` — 规范化 swagger + Kiota 重新生成双语言客户端
- `csharp/` — `Core`（手写登录）+ `Generated`（Kiota）+ `Facade`（薄封装）+ `Tests`
- `python/` — 对等的三层包结构（Python 包名 `riot_sdk`）
- `docs/` — 使用与测试说明

## 文档

- [冒烟测试（环境变量与步骤）](docs/smoke-test.md)

## 工具选型

使用 **Kiota**（已在 `metric.json` / `device.json` 上验证可生成；本机无 Java，未继续依赖 openapi-generator）。

`scripts/preprocess_openapi.py` 在生成前会做两件事，否则 Kiota 无法产出可用的强类型模型：

1. 把 Springfox 非法 schema 名（如 `ResponseMsg«Void»`、`Device对象`）改成 OpenAPI 合法标识符
2. 把响应内容类型 `*/*` 改成 `application/json`（Kiota 默认只认 json）

## 生成客户端

前置：已安装 [.NET SDK](https://dotnet.microsoft.com/) 与 Kiota CLI：

```powershell
dotnet tool install --global Microsoft.OpenApi.Kiota
```

在本目录（`rcs/riot-sdk`）执行：

```powershell
cd rcs/riot-sdk
pwsh ./scripts/generate.ps1
```

## C# 快速开始

```csharp
using RIoT.Sdk.Core;
using RIoT.Sdk.Facade;

var options = new RiotOptions
{
    BaseUrl = "http://172.10.1.72:8888",
    Username = "admin",
    Password = "admin",
};

await using var session = new RiotSession(options);
var tokens = await session.LoginAsync();
Console.WriteLine($"token length={tokens.AccessToken.Length}");

var devices = await session.Device.ListDevicesAsync(pageNum: 1, pageSize: 10);
Console.WriteLine(devices?.Code);
```

```powershell
dotnet test ./csharp/RIoT.Sdk.sln
```

端到端冒烟见 **[docs/smoke-test.md](docs/smoke-test.md)**（设置 `RIOT_SMOKE` / `RIOT_BASE_URL` 后执行 `pwsh ./scripts/smoke-csharp.ps1`）。

## Python 快速开始

```powershell
cd python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

```python
import asyncio
from riot_sdk import RiotOptions, RiotSession

async def main():
    options = RiotOptions(
        base_url="http://172.10.1.72:8888",
        username="admin",
        password="admin",
    )
    async with RiotSession(options) as session:
        tokens = await session.login()
        print("token length", len(tokens.access_token))
        devices = await session.device.list_devices(page_num=1, page_size=10)
        print(devices)

asyncio.run(main())
```

Python 冒烟步骤同样见 **[docs/smoke-test.md](docs/smoke-test.md)**。

## 本轮范围

已覆盖：device / task / order + 手写 login/refreshToken。

未覆盖：Gateway、fcs/imap/ithings/完整 security 等其余 swagger 模块（后续按需把 json 放进 `specs/` 后重跑生成脚本即可）。
