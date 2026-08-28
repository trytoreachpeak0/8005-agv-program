from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteCost:
    """Path cost (mm) to a station (BC-ROUTE-001). costs_mm=-1 means unreachable."""

    costs_mm: int

    @property
    def is_reachable(self) -> bool:
        return self.costs_mm >= 0
