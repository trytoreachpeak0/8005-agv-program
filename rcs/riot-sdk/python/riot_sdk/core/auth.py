from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from riot_sdk.core.business_response import is_success_code
from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.core.options import RiotOptions


@dataclass(slots=True)
class AuthTokens:
    access_token: str
    refresh_token: str | None = None
    raw_result: dict[str, str] = field(default_factory=dict)


class RiotAuthClient:
    """Hand-written auth client for login / refreshToken only."""

    def __init__(self, options: RiotOptions, client: httpx.AsyncClient | None = None) -> None:
        self.options = options
        self._owns_client = client is None
        base = options.base_url if options.base_url.endswith("/") else options.base_url + "/"
        self._client = client or httpx.AsyncClient(base_url=base, timeout=options.timeout)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def login(
        self,
        username: str | None = None,
        password: str | None = None,
    ) -> AuthTokens:
        payload = {
            "username": username or self.options.username,
            "password": password or self.options.password,
        }
        return await self._send_auth("POST", "/api/auth/v1/admin/login", json=payload)

    async def refresh_token(self, access_token: str) -> AuthTokens:
        token = _strip_bearer(access_token)
        return await self._send_auth(
            "PUT",
            "/api/auth/v1/admin/refreshToken",
            headers={"Authorization": f"Bearer {token}"},
        )

    async def _send_auth(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> AuthTokens:
        try:
            response = await self._client.request(method, path, json=json, headers=headers)
        except httpx.HTTPError as exc:
            raise RiotApiException(f"RIoT auth request failed: {exc}") from exc

        body = response.text
        if response.status_code >= 400:
            raise RiotApiException(
                f"RIoT auth HTTP {response.status_code}: {body[:500]}",
                status_code=response.status_code,
                response_body=body,
            )

        data = response.json() if body else {}
        business_code = str(data.get("code")) if data.get("code") is not None else None
        if not is_success_code(business_code):
            raise RiotApiException(
                f"RIoT auth business failure code={business_code} message={data.get('message')}",
                status_code=response.status_code,
                business_code=business_code,
                response_body=body,
            )

        result = data.get("result") or {}
        raw: dict[str, str] = {}
        if isinstance(result, dict):
            for key, value in result.items():
                raw[str(key)] = "" if value is None else str(value)

        access = _find_token(raw, "token", "accessToken", "access_token", "authorization", "Authorization")
        if not access:
            raise RiotApiException(
                "RIoT auth succeeded but no token field was found in result.",
                status_code=response.status_code,
                business_code=business_code,
                response_body=body,
            )

        refresh = _find_token(raw, "refreshToken", "refresh_token")
        return AuthTokens(
            access_token=_strip_bearer(access),
            refresh_token=_strip_bearer(refresh) if refresh else None,
            raw_result=raw,
        )


def _strip_bearer(token: str) -> str:
    value = token.strip()
    if value.lower().startswith("bearer "):
        return value[7:].strip()
    return value


def _find_token(raw: dict[str, str], *keys: str) -> str | None:
    lower_map = {k.lower(): v for k, v in raw.items()}
    for key in keys:
        value = lower_map.get(key.lower())
        if value:
            return value
    for value in raw.values():
        if len(value) > 20:
            return value
    return None
