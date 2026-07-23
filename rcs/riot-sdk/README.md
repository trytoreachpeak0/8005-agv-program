# RIoT SDK

位于本仓库 `rcs/riot-sdk`，由 **8005多仓位AGV** 统一做 Git 管理。提供 RIoT（斯坦德 RCS）的 **C#** 与 **Python** 两套 API SDK。

结构：

- `specs/` — device / task / order / **imap** OpenAPI 原文
- `scripts/generate.ps1` — 规范化 swagger + Kiota 重新生成双语言客户端
- `csharp/` — `Core`（手写）+ `Generated`（Kiota）+ `Facade`（薄封装）+ `Tests`
- `python/` — 对等的三层包结构（Python 包名 `riot_sdk`）
- `docs/` — 使用说明、Facade 清单、ADR
- `CONTEXT.md` — 领域用语（Ubiquitous Language）

## 文档

- [Facade V1 方法清单](docs/facade-v1.md)（C# ↔ Python 对照）
- [冒烟测试](docs/smoke-test.md)
- [领域用语 CONTEXT](CONTEXT.md)
- [ADR 决策记录](docs/adr/)

## V1 范围（DispatchLoop）

第一版具名 Facade 已按 [ADR-0004](docs/adr/0004-v1-facade-method-scope.md) 交付：鉴权、可调度车发现、Map/Station、RouteCost / NearStationQuery、建单与查单、取消、Enable/Disable、急停触发/解除、PriorityExec、OrderHold / OrderContinue、HangContinue。

默认鉴权为 **CallApiKey**（[ADR-0001](docs/adr/0001-default-auth-callapikey.md)）。明确排除项见 [ADR-0009](docs/adr/0009-v1-explicit-non-goals.md)。

## 工具选型

使用 **Kiota**。`scripts/preprocess_openapi.py` 在生成前会：

1. 把 Springfox 非法 schema 名改成 OpenAPI 合法标识符
2. 把响应内容类型 `*/*` 改成 `application/json`

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
    CallApiKey = "<call-api-key>", // default auth; or Username/Password + LoginAsync
};

await using var session = new RiotSession(options);

var vehicles = await session.Tasks.GetDispatchableVehiclesAsync();
var maps = await session.Maps.ListMapsAsync();
var order = await session.Order.CreateMoveOrderAsync(
    upperId: "mes-demo-1",
    appointVehicleKey: vehicles[0].DeviceKey,
    mapId: maps[0].MapId,
    destinationStationId: 1);
```

```powershell
dotnet test ./csharp/RIoT.Sdk.sln
```

端到端冒烟见 **[docs/smoke-test.md](docs/smoke-test.md)**。

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
        call_api_key="<call-api-key>",
    )
    async with RiotSession(options) as session:
        vehicles = await session.tasks.get_dispatchable_vehicles()
        maps = await session.maps.list_maps()
        order = await session.order.create_move_order(
            upper_id="mes-demo-1",
            appoint_vehicle_key=vehicles[0].device_key,
            map_id=maps[0].map_id,
            destination_station_id=1,
        )
        print(order)

asyncio.run(main())
```

Python 冒烟步骤同样见 **[docs/smoke-test.md](docs/smoke-test.md)**。

## 生成模块

已纳入 Kiota：`device` / `task` / `order` / `imap`。

未纳入：Gateway、fcs/ithings/完整 security 等其余 swagger（按需放入 `specs/` 后重跑生成即可）。
