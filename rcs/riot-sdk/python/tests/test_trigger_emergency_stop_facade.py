from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotOptions, RiotSession

_DEVICE_KEY = "BROKERX-aee2f93d717546cf9510c98c854fe83e"

# Known-good outer envelope from S4-trigger-call.preview (business code=0)
_TRIGGER_SUCCESS_BODY = (
    '{"code":"0","message":"成功","msgDetail":"","result":{"client":{"deviceKey":'
    '"BROKERX-aee2f93d717546cf9510c98c854fe83e","productKey":"standard.oasis.300ul",'
    '"productType":1,"thingModelVersion":"1"},"code":200,"data":{"reason":"RESPONSE_PROCESSING",'
    '"code":"RESULT_CODE_NONE","responseState":"RESPONSE_OK","state":"1","responseCode":"0"},'
    '"fType":"SERVICE_CALL_REPLY","id":"886875","timestamp":1784534967178},"tid":""}'
)


@pytest.mark.asyncio
async def test_trigger_emergency_stop_succeeds_without_throwing() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_TRIGGER_SUCCESS_BODY,
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
            await session.device.trigger_emergency_stop(_DEVICE_KEY)
