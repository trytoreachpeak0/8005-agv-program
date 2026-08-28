from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotApiException, RiotOptions, RiotSession
from riot_sdk.core.business_response import is_success_code

_LIST_DEVICES_SUCCESS = """{"code":"0","message":"成功","result":{"current":1,"size":10,"total":1,"records":[{"deviceKey":"DEV-1","deviceName":"agv-1"}]}}"""
_LIST_DEVICES_FAILURE = """{"code":"500","message":"内部错误","result":null}"""
_STATISTICS_SUCCESS = """{"code":"0","message":"成功","result":{"allCount":2,"onlineCount":1,"offlineCount":1,"enable":1,"unEnable":1,"inactiveCount":0}}"""


@pytest.mark.asyncio
async def test_list_devices_unwraps_page_on_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_LIST_DEVICES_SUCCESS,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://riot.test/") as client:
        options = RiotOptions(base_url="http://riot.test", call_api_key="test-key")
        async with RiotSession(options, client=client) as session:
            page = await session.device.list_devices(page_num=1, page_size=10)

    assert page.total == 1
    assert page.records is not None
    assert len(page.records) == 1
    assert page.records[0].device_key == "DEV-1"


@pytest.mark.asyncio
async def test_list_devices_throws_on_business_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_LIST_DEVICES_FAILURE,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://riot.test/") as client:
        options = RiotOptions(base_url="http://riot.test", call_api_key="test-key")
        async with RiotSession(options, client=client) as session:
            with pytest.raises(RiotApiException) as exc_info:
                await session.device.list_devices(page_num=1, page_size=10)

    assert exc_info.value.business_code == "500"


@pytest.mark.asyncio
async def test_get_device_status_statistics_unwraps_dto_on_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_STATISTICS_SUCCESS,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://riot.test/") as client:
        options = RiotOptions(base_url="http://riot.test", call_api_key="test-key")
        async with RiotSession(options, client=client) as session:
            stats = await session.device.get_device_status_statistics()

    assert stats.all_count == 2
    assert stats.online_count == 1


def test_is_success_code_accepts_common_tokens() -> None:
    assert is_success_code("0")
    assert is_success_code("200")
    assert is_success_code("OK")
    assert is_success_code(None)
    assert is_success_code("   ")
    assert is_success_code(" 0 ")
    assert not is_success_code("500")
