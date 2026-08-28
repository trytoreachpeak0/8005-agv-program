from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_DEVICE_KEY = "BROKERX-aee2f93d717546cf9510c98c854fe83e"

# Known-good body from R15-map29-costs[0].body
_REACHABLE_BODY = (
    '{"code":"0","message":"成功","msgDetail":"",'
    '"result":{"deviceCostsList":[{"costs":2210,"deviceKey":'
    '"BROKERX-aee2f93d717546cf9510c98c854fe83e","message":"ok"}],'
    '"mapId":29,"stationId":1},"tid":""}'
)

# Known-good body from Round15 R2 getRouteCostsBy (map28 / station 1, cross-map unreachable)
_UNREACHABLE_BODY = (
    '{"code":"0","message":"成功","msgDetail":"",'
    '"result":{"deviceCostsList":[{"costs":-1,"deviceKey":'
    '"BROKERX-aee2f93d717546cf9510c98c854fe83e",'
    '"message":"vehicle route to station unreachable"}],'
    '"mapId":28,"stationId":1},"tid":""}'
)


@pytest.mark.asyncio
async def test_get_route_cost_reachable_returns_non_negative_costs_mm() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_REACHABLE_BODY,
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
            cost = await session.tasks.get_route_cost(
                map_id=29,
                station_id=1,
                device_key=_DEVICE_KEY,
            )

    assert cost.costs_mm == 2210
    assert cost.is_reachable


@pytest.mark.asyncio
async def test_get_route_cost_unreachable_returns_minus_one_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_UNREACHABLE_BODY,
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
            cost = await session.tasks.get_route_cost(
                map_id=28,
                station_id=1,
                device_key=_DEVICE_KEY,
            )

    assert cost.costs_mm == -1
    assert not cost.is_reachable
