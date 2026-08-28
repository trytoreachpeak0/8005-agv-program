from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VehicleCard:
    device_key: str
    enable: bool | None
    status: int | None
    proc_state: str | None
    current_map: str | None
    current_position: int | None
    battery_percent: int | None
    battery_state: str | None
    speed: float | None
    lock_status: int | None
    order_task_id: str | None


@dataclass(frozen=True, slots=True)
class VehicleExecutionFacts:
    device_key: str
    movement_state: str | None
    control_state: str | None
    emergency_state: str | None
    break_switch_state: str | None
    location_state: str | None
    speed: float | None
    proc_state: str | None
    processing_order: bool | None
    enable: bool | None
    integration_level: str | None
