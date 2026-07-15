from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


class OrderClient:
    """Thin order-module facade."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    @property
    def raw(self):
        """Underlying Kiota client for endpoints not yet wrapped."""
        return self._session.create_generated_order_client()
