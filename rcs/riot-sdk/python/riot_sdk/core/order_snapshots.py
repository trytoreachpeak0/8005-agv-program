from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderLookupStatus(str, Enum):
    """Semantic result of observing an order by caller-owned upper_id."""

    Found = "Found"
    NotFound = "NotFound"
    AbsentAtObservation = "AbsentAtObservation"
    Indeterminate = "Indeterminate"


@dataclass(frozen=True, slots=True)
class OrderMissionSnapshot:
    type: str | None
    map_id: int | None
    destination: int | None


@dataclass(frozen=True, slots=True)
class OrderSnapshot:
    id: int
    order_id: str
    upper_id: str
    order_state: int
    appoint_vehicle_key: str | None
    execute_vehicle_key: str | None
    end_station_no: int | None
    missions: tuple[OrderMissionSnapshot, ...]


@dataclass(frozen=True, slots=True)
class OrderLookupResult:
    requested_upper_id: str
    status: OrderLookupStatus
    order: OrderSnapshot | None = None

    def __post_init__(self) -> None:
        if not self.requested_upper_id or not self.requested_upper_id.strip():
            raise ValueError("requested_upper_id is required")
        if self.status is OrderLookupStatus.Found:
            if self.order is None:
                raise ValueError("Found requires an order")
            if self.order.upper_id != self.requested_upper_id:
                raise ValueError("Found order upper_id must match requested_upper_id")
        elif self.order is not None:
            raise ValueError(f"{self.status.value} must not carry an order")

    @classmethod
    def found(cls, requested_upper_id: str, order: OrderSnapshot) -> OrderLookupResult:
        return cls(requested_upper_id, OrderLookupStatus.Found, order)

    @classmethod
    def not_found(cls, requested_upper_id: str) -> OrderLookupResult:
        return cls(requested_upper_id, OrderLookupStatus.NotFound)

    @classmethod
    def absent_at_observation(cls, requested_upper_id: str) -> OrderLookupResult:
        return cls(requested_upper_id, OrderLookupStatus.AbsentAtObservation)

    @classmethod
    def indeterminate(cls, requested_upper_id: str) -> OrderLookupResult:
        return cls(requested_upper_id, OrderLookupStatus.Indeterminate)
