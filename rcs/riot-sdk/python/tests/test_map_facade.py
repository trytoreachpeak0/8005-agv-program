from __future__ import annotations

import httpx
import pytest

from riot_sdk import Map, RiotOptions, RiotSession

# Known-good envelope; items from C1-mapInfo-excludeMapJson.
_EXCLUDE_MAP_JSON_BODY = """{"code":"0","message":"成功","result":[
  {"id":6,"name":"尊阳电镀线"},
  {"id":29,"name":"api测试"},
  {"id":26,"name":"新基测试1"}
]}"""


@pytest.mark.asyncio
async def test_list_maps_returns_domain_maps_from_exclude_map_json() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_EXCLUDE_MAP_JSON_BODY,
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
            maps = await session.maps.list_maps()

    assert len(maps) == 3
    assert Map(29, "api测试") in maps
