from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_ORDER_ID = "order-2079797271662297088"

# Known-good body from Q006-held-call.body / S3-probe-CMD_ORDER_HELD.call.body
_HOLD_SUCCESS_BODY = '{"code":"0","message":"成功","msgDetail":"","tid":""}'


@pytest.mark.asyncio
async def test_order_hold_succeeds_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_HOLD_SUCCESS_BODY,
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
            await session.tasks.order_hold(_ORDER_ID)
