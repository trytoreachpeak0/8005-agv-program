from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotApiException, RiotOptions, RiotSession

# Known-good body from BC-AUTH-001 / A1 invalid-password fixture.
_INVALID_PASSWORD_BODY = '{"code":"2009","message":"密码不正确","result":null}'


async def test_admin_login_with_invalid_password_throws_business_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_INVALID_PASSWORD_BODY)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            username="admin",
            password="wrong-password",
        )
        async with RiotSession(options, client=client) as session:
            with pytest.raises(RiotApiException) as caught:
                await session.login()

    assert caught.value.business_code == "2009"
    assert caught.value.status_code == 200
