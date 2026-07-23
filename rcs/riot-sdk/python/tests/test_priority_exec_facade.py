from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_ORDER_ID = "order-2079101767542505472"

# Known-good body from S2-priority-calls.attempts[0].body
_PRIORITY_SUCCESS_BODY = '{"code":"0","message":"成功","msgDetail":"","tid":""}'


@pytest.mark.asyncio
async def test_priority_exec_succeeds_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_PRIORITY_SUCCESS_BODY,
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
            await session.order.priority_exec(_ORDER_ID)
