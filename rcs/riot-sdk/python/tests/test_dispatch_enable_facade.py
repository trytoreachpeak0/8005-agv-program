from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_DEVICE_KEY = "BROKERX-aee2f93d717546cf9510c98c854fe83e"

# Known-good body from R12-enable-restore.call.body
_ENABLE_SUCCESS_BODY = '{"code":"0","message":"成功","msgDetail":"","tid":""}'


@pytest.mark.asyncio
async def test_dispatch_enable_succeeds_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_ENABLE_SUCCESS_BODY,
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
            await session.tasks.dispatch_enable(_DEVICE_KEY)
