from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession, Station

# Known-good envelope; items from C2-stations-map-29.
_STATIONS_MAP_29_BODY = """{"code":"0","message":"成功","result":[
  {"id":1,"name":"站点1"},
  {"id":2,"name":"站点2"}
]}"""


@pytest.mark.asyncio
async def test_list_stations_for_map_29_returns_domain_stations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_STATIONS_MAP_29_BODY,
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
            stations = await session.maps.list_stations(map_id=29)

    assert len(stations) == 2
    assert Station(29, 1, "站点1") in stations
    assert Station(29, 2, "站点2") in stations
