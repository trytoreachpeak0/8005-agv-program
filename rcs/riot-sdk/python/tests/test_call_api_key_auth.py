from __future__ import annotations

from riot_sdk import RiotOptions, RiotSession


async def test_session_with_call_api_key_can_authenticate_without_admin_login() -> None:
    options = RiotOptions(
        base_url="http://riot.test",
        call_api_key="test-call-api-key",
    )

    async with RiotSession(options) as session:
        # Never called login() — CallApiKey is the default Bearer credential.
        bearer = await session.token_provider.get_access_token()

    assert bearer == "test-call-api-key"
