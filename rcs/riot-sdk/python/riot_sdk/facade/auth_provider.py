from __future__ import annotations

from typing import Any

from kiota_abstractions.authentication import AccessTokenProvider, AllowedHostsValidator

from riot_sdk.core.token_provider import RiotTokenProvider


class KiotaAccessTokenProvider(AccessTokenProvider):
    def __init__(self, tokens: RiotTokenProvider) -> None:
        self._tokens = tokens
        self._validator = AllowedHostsValidator([])

    def get_allowed_hosts_validator(self) -> AllowedHostsValidator:
        return self._validator

    async def get_authorization_token(
        self,
        uri: str,
        additional_authentication_context: dict[str, Any] = {},
    ) -> str:
        return await self._tokens.get_access_token()
