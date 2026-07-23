from __future__ import annotations

from dataclasses import dataclass

from riot_sdk.core.exceptions import RiotApiException


@dataclass(frozen=True, slots=True)
class DispatchableVehicle:
    """A vehicle that can be appointed for dispatch (task simpleInfo)."""

    device_key: str
    device_name: str


def resolve_device_key(vehicles: list[DispatchableVehicle], device_name: str) -> str:
    """Exact deviceName → deviceKey resolution (BC-VEH-002)."""
    if not device_name or not device_name.strip():
        raise ValueError("device_name is required")

    matches = [v for v in vehicles if v.device_name == device_name]
    if not matches:
        raise RiotApiException(
            f"No dispatchable vehicle with deviceName={device_name}.",
            business_code="vehicle-name-not-found",
        )
    if len(matches) > 1:
        raise RiotApiException(
            f"deviceName={device_name} is not unique ({len(matches)} matches); refusing to pick arbitrarily.",
            business_code="vehicle-name-ambiguous",
        )
    return matches[0].device_key
