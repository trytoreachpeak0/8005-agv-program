from __future__ import annotations

import asyncio


class RiotTokenProvider:
    """Mutable bearer-token holder shared by Facade clients."""

    def __init__(self) -> None:
        self._access_token: str | None = None
        self._lock = asyncio.Lock()

    @property
    def access_token(self) -> str | None:
        return self._access_token

    def set_access_token(self, token: str) -> None:
        if not token or not token.strip():
            raise ValueError("token is required")
        value = token.strip()
        if value.lower().startswith("bearer "):
            value = value[7:].strip()
        self._access_token = value

    async def get_access_token(self) -> str:
        async with self._lock:
            if not self._access_token:
                raise RuntimeError(
                    "No access token. Call RiotSession.login() before invoking API clients."
                )
            return self._access_token
