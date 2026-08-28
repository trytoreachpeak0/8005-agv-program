from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Map:
    """A dispatchable map: map_id (= RIoT mapInfo.id) and display name (BC-MAP-001)."""

    map_id: int
    name: str
