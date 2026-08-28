from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Station:
    """A station on a Map; always paired with map_id (BC-MAP-002)."""

    map_id: int
    station_id: int
    name: str
