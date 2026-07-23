from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderRef:
    """Identifiers for an order from byDefaultMissions (BC-ORDER-001 / BC-ORDER-005)."""

    id: int
    order_id: str
    upper_id: str
    order_state: int
