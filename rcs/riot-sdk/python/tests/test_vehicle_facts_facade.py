from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotApiException, RiotOptions, RiotSession


async def _read(path: str, body: str, operation):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert request.url.path == path
        return httpx.Response(
            200,
            text=body,
            headers={"Content-Type": "application/json"},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://riot.test/",
    ) as client:
        async with RiotSession(
            RiotOptions(base_url="http://riot.test", call_api_key="test-key"),
            client=client,
        ) as session:
            result = await operation(session)
    return result, requests


@pytest.mark.asyncio
async def test_get_vehicle_card_returns_exact_facts_for_matching_device_key() -> None:
    body = (
        '{"code":"0","result":{"deviceKey":"VEHICLE-1","enable":true,"status":1,'
        '"procState":"IDLE","currentMap":"MAP-25","currentPosition":12,"battery":80,'
        '"batteryState":"NO_CHARGE","speed":0,"lockStatus":0,"orderTaskId":null}}'
    )
    card, requests = await _read(
        "/api/task/vehicles/getVehicleInfoByDeviceKey",
        body,
        lambda session: session.tasks.get_vehicle_card("VEHICLE-1"),
    )

    assert requests[0].url.params["key"] == "VEHICLE-1"
    assert card.device_key == "VEHICLE-1"
    assert card.enable is True
    assert card.status == 1
    assert card.proc_state == "IDLE"
    assert card.current_map == "MAP-25"
    assert card.current_position == 12
    assert card.battery_percent == 80
    assert card.battery_state == "NO_CHARGE"
    assert card.speed == 0
    assert card.lock_status == 0
    assert card.order_task_id is None
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_get_vehicle_card_rejects_mismatched_device_key() -> None:
    with pytest.raises(RiotApiException) as caught:
        await _read(
            "/api/task/vehicles/getVehicleInfoByDeviceKey",
            '{"code":"0","result":{"deviceKey":"OTHER","enable":true,"status":1}}',
            lambda session: session.tasks.get_vehicle_card("VEHICLE-1"),
        )
    assert caught.value.business_code == "vehicle-key-mismatch"


@pytest.mark.asyncio
async def test_get_vehicle_card_rejects_missing_result() -> None:
    with pytest.raises(RiotApiException) as caught:
        await _read(
            "/api/task/vehicles/getVehicleInfoByDeviceKey",
            '{"code":"0","result":null}',
            lambda session: session.tasks.get_vehicle_card("VEHICLE-1"),
        )
    assert caught.value.business_code == "vehicle-card-missing"


@pytest.mark.asyncio
async def test_get_vehicle_execution_facts_returns_vehicle_and_task_facts() -> None:
    body = """
    {
      "vehicle":{"movementState":"MT_FINISHED","controlState":"CONTROL_STATE_OK",
        "emergencyState":"OK","breakSwitchState":"MOVABLE",
        "locationState":"LOCATION_STATE_RUNNING","speed":0},
      "vehicleTaskInfo":{"key":"VEHICLE-1","procState":"IDLE",
        "processingOrder":false,"enable":true,"integrationLevel":"ON_LINE"}
    }
    """
    facts, requests = await _read(
        "/api/task/v1/task/getVehicleInfo/VEHICLE-1",
        body,
        lambda session: session.tasks.get_vehicle_execution_facts("VEHICLE-1"),
    )

    assert facts.device_key == "VEHICLE-1"
    assert facts.movement_state == "MT_FINISHED"
    assert facts.control_state == "CONTROL_STATE_OK"
    assert facts.emergency_state == "OK"
    assert facts.break_switch_state == "MOVABLE"
    assert facts.location_state == "LOCATION_STATE_RUNNING"
    assert facts.speed == 0
    assert facts.proc_state == "IDLE"
    assert facts.processing_order is False
    assert facts.enable is True
    assert facts.integration_level == "ON_LINE"
    assert len(requests) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        '{"vehicleTaskInfo":{"key":"VEHICLE-1"}}',
        '{"vehicle":{"movementState":"MT_FINISHED"}}',
    ],
)
async def test_get_vehicle_execution_facts_rejects_missing_vehicle_or_task_half(
    body: str,
) -> None:
    with pytest.raises(RiotApiException) as caught:
        await _read(
            "/api/task/v1/task/getVehicleInfo/VEHICLE-1",
            body,
            lambda session: session.tasks.get_vehicle_execution_facts("VEHICLE-1"),
        )
    assert caught.value.business_code == "vehicle-execution-facts-missing"


@pytest.mark.asyncio
async def test_get_vehicle_execution_facts_rejects_mismatched_task_key() -> None:
    body = (
        '{"vehicle":{"movementState":"MT_FINISHED"},'
        '"vehicleTaskInfo":{"key":"OTHER","procState":"IDLE"}}'
    )
    with pytest.raises(RiotApiException) as caught:
        await _read(
            "/api/task/v1/task/getVehicleInfo/VEHICLE-1",
            body,
            lambda session: session.tasks.get_vehicle_execution_facts("VEHICLE-1"),
        )
    assert caught.value.business_code == "vehicle-key-mismatch"
