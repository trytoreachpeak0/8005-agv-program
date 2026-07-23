from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_ORDER_ID = "order-2079529938297421824"

# Known-good body from Round27 Fok-CONTINUE_FROM_HANG.body
_CONTINUE_SUCCESS_BODY = '{"code":"0","message":"成功","msgDetail":"","tid":""}'


@pytest.mark.asyncio
async def test_hang_continue_succeeds_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_CONTINUE_SUCCESS_BODY,
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
            await session.tasks.hang_continue(_ORDER_ID)
