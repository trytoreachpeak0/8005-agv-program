from __future__ import annotations

import httpx
import pytest

from riot_sdk import DispatchableVehicle, RiotOptions, RiotSession

# Known-good envelope + items from B1-getAllVehicleSimpleInfo / B1-name-to-deviceKey.
_SIMPLE_INFO_BODY = """{"code":"0","message":"成功","result":[
  {"deviceKey":"BROKERX-8ffb2294db594d7480125d379b39cfd6","deviceName":"新基测试300c顶升2"},
  {"deviceKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","deviceName":"新基测试300c协作1"},
  {"deviceKey":"BROKERX-757de62710d84cec9fe9907691672cbc","deviceName":"尊阳-多仓位1"}
]}"""


@pytest.mark.asyncio
async def test_get_dispatchable_vehicles_returns_domain_vehicles_from_simple_info() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_SIMPLE_INFO_BODY,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            vehicles = await session.tasks.get_dispatchable_vehicles()

    assert len(vehicles) == 3
    assert DispatchableVehicle(
        "BROKERX-aee2f93d717546cf9510c98c854fe83e",
        "新基测试300c协作1",
    ) in vehicles


@pytest.mark.asyncio
async def test_resolve_device_key_exact_name_returns_unique_key() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_SIMPLE_INFO_BODY,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            key = await session.tasks.resolve_device_key("新基测试300c协作1")

    assert key == "BROKERX-aee2f93d717546cf9510c98c854fe83e"
