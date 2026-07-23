from __future__ import annotations

from typing import TYPE_CHECKING

from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.core.maps import Map
from riot_sdk.core.stations import Station

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


def _is_success_code(code: str | None) -> bool:
    return not code or code in {"0", "200", "OK", "ok", "success", "SUCCESS"}


class MapClient:
    """Thin imap Map facade (BC-MAP-001 / ADR-0007)."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    async def list_maps(self) -> list[Map]:
        """GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson (BC-MAP-001 / ADR-0006)."""
        client = self._session.create_generated_imap_client()
        response = await client.api.imap.v1.map_info.get_a_l_l_map_info_exclude_map_json.get()
        if response is None:
            raise RiotApiException("getALLMapInfoExcludeMapJson returned empty response.")
        if not _is_success_code(response.code):
            raise RiotApiException(
                f"RIoT business failure code={response.code} message={response.message}",
                status_code=200,
                business_code=response.code,
            )
        result = response.result or []
        return [
            Map(map_id=m.id, name=m.name)
            for m in result
            if m.id is not None and m.name
        ]

    async def list_stations(self, map_id: int) -> list[Station]:
        """GET /api/imap/v1/mapInfo/stations/{mapId} (BC-MAP-002 / ADR-0006)."""
        client = self._session.create_generated_imap_client()
        response = await client.api.imap.v1.map_info.stations.by_map_id(map_id).get()
        if response is None:
            raise RiotApiException(f"stations/{map_id} returned empty response.")
        if not _is_success_code(response.code):
            raise RiotApiException(
                f"RIoT business failure code={response.code} message={response.message}",
                status_code=200,
                business_code=response.code,
            )
        result = response.result or []
        return [
            Station(map_id=map_id, station_id=s.id, name=s.name)
            for s in result
            if s.id is not None and s.name
        ]

    @property
    def raw(self):
        """Underlying Kiota imap client for endpoints not yet wrapped."""
        return self._session.create_generated_imap_client()
