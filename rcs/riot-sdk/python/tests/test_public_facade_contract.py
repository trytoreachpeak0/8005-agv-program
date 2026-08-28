from __future__ import annotations

import pytest

from riot_sdk import (
    OrderLookupResult,
    OrderLookupStatus,
    OrderSnapshot,
)
from riot_sdk.facade.map_client import MapClient
from riot_sdk.facade.order_client import OrderClient
from riot_sdk.facade.task_client import TaskClient


def test_public_facade_contract_matches_declared_cross_language_manifest() -> None:
    assert [status.value for status in OrderLookupStatus] == [
        "Found",
        "NotFound",
        "AbsentAtObservation",
        "Indeterminate",
    ]
    assert hasattr(OrderClient, "find_order_by_upper_id")
    assert hasattr(OrderClient, "list_orders_by_states")
    assert hasattr(TaskClient, "get_vehicle_card")
    assert hasattr(TaskClient, "get_vehicle_execution_facts")
    assert hasattr(MapClient, "list_stations_strict")


def test_order_lookup_result_enforces_status_payload_invariants() -> None:
    order = OrderSnapshot(1, "ORDER-1", "UPPER-1", 1, None, None, None, ())
    assert OrderLookupResult.found("UPPER-1", order).order is order

    with pytest.raises(ValueError):
        OrderLookupResult.found("OTHER", order)
    with pytest.raises(ValueError):
        OrderLookupResult("UPPER-1", OrderLookupStatus.Found, None)
    with pytest.raises(ValueError):
        OrderLookupResult("UPPER-1", OrderLookupStatus.NotFound, order)
