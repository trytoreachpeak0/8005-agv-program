from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

# Known-good body; result from R15-near-tight-map28 nearEnd-1to234
_NEAR_END_BODY = (
    '{"code":"0","message":"成功","msgDetail":"","result":2,"tid":""}'
)

# result from R15-near-tight-map28 nearStart-4from123
_NEAR_START_BODY = (
    '{"code":"0","message":"成功","msgDetail":"","result":3,"tid":""}'
)


@pytest.mark.asyncio
async def test_query_nearest_end_returns_closest_end_station_id() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_NEAR_END_BODY,
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
            station_id = await session.tasks.query_nearest_end(
                map_id=28,
                start_station_id=1,
                end_station_ids=[2, 3, 4],
            )

    assert station_id == 2


@pytest.mark.asyncio
async def test_query_nearest_start_returns_closest_start_station_id() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_NEAR_START_BODY,
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
            station_id = await session.tasks.query_nearest_start(
                map_id=28,
                end_station_id=4,
                start_station_ids=[1, 2, 3],
            )

    assert station_id == 3
