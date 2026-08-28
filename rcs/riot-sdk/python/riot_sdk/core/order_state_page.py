from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderStateRecord:
    id: int | None
    order_id: str | None
    upper_id: str | None
    order_state: int | None
    appoint_vehicle_key: str | None
    execute_vehicle_key: str | None


@dataclass(frozen=True, slots=True)
class OrderStatePage:
    current: int | None
    size: int | None
    total: int | None
    records: tuple[OrderStateRecord, ...]

    @property
    def covers_all_records(self) -> bool:
        return (
            self.current == 1
            and self.total is not None
            and self.total >= 0
            and self.total == len(self.records)
            and (self.size is None or self.total <= self.size)
        )
