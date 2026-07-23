from __future__ import annotations

from kiota_abstractions.authentication import BaseBearerTokenAuthenticationProvider
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
import httpx

from riot_sdk.core.auth import AuthTokens, RiotAuthClient
from riot_sdk.core.options import RiotOptions
from riot_sdk.core.token_provider import RiotTokenProvider
from riot_sdk.facade.auth_provider import KiotaAccessTokenProvider
from riot_sdk.facade.device_client import DeviceClient
from riot_sdk.facade.map_client import MapClient
from riot_sdk.facade.order_client import OrderClient
from riot_sdk.facade.task_client import TaskClient


class RiotSession:
    """Shared session: default CallApiKey Bearer, or AdminLogin backup; reuse across facades."""

    def __init__(
        self,
        options: RiotOptions,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.options = options
        self.token_provider = RiotTokenProvider()
        # ADR-0001: CallApiKey is the default Bearer credential; AdminLogin is optional.
        if options.call_api_key and options.call_api_key.strip():
            self.token_provider.set_access_token(options.call_api_key)
        self._auth = RiotAuthClient(options, client)
        auth_provider = BaseBearerTokenAuthenticationProvider(
            KiotaAccessTokenProvider(self.token_provider)
        )
        # Inject httpx client when provided so Facade unit tests can mock at the HTTP boundary.
        self._adapter = HttpxRequestAdapter(
            auth_provider,
            http_client=client,
            base_url=options.base_url.rstrip("/"),
        )
        self.device = DeviceClient(self)
        self.tasks = TaskClient(self)
        self.order = OrderClient(self)
        self.maps = MapClient(self)

    async def login(self) -> AuthTokens:
        tokens = await self._auth.login()
        self.token_provider.set_access_token(tokens.access_token)
        return tokens

    async def refresh_token(self) -> AuthTokens:
        current = await self.token_provider.get_access_token()
        tokens = await self._auth.refresh_token(current)
        self.token_provider.set_access_token(tokens.access_token)
        return tokens

    def create_generated_device_client(self):
        from riot_sdk.generated.device.device_client import DeviceClient as GenDeviceClient

        return GenDeviceClient(self._adapter)

    def create_generated_task_client(self):
        from riot_sdk.generated.task.task_client import TaskClient as GenTaskClient

        return GenTaskClient(self._adapter)

    def create_generated_order_client(self):
        from riot_sdk.generated.order.order_client import OrderClient as GenOrderClient

        return GenOrderClient(self._adapter)

    def create_generated_imap_client(self):
        from riot_sdk.generated.imap.imap_client import ImapClient as GenImapClient

        return GenImapClient(self._adapter)

    async def aclose(self) -> None:
        await self._auth.aclose()

    async def __aenter__(self) -> RiotSession:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()
