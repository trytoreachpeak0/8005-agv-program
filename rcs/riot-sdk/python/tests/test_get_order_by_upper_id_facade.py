from __future__ import annotations

import asyncio
import httpx
import pytest

from riot_sdk import OrderLookupStatus, RiotApiException, RiotOptions, RiotSession

_UPPER_ID = "riot-lab-I-20260720-120949"

# Known-good body from E1-order-success-detail-station2.body
_DETAIL_SUCCESS_BODY = (
    '{"code":"0","message":"成功","msgDetail":"","result":{"appointMapId":0,"appointStationId":0,'
    '"appointVehicleGroupId":0,"appointVehicleGroupName":"0",'
    '"appointVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e","changeVehicle":0,'
    '"changeVehicleReason":"","changeVehicleRecord":"","createTime":"2026-07-20 12:11:32",'
    '"createdBy":"api-test","distance":0,"doneTime":"2026-07-20 12:11:40",'
    '"endStationName":"站点2","endStationNo":2,"eta":0,"executeTime":"2026-07-20 12:11:36",'
    '"executeVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e",'
    '"executeVehicleName":"新基测试300c协作1","executingIndex":-1,"failReason":"",'
    '"finalState":true,"id":488003,"isAppointEnable":1,"isDeleted":0,"lockStatus":0,'
    '"missions":[{"actionId":0,"actionName":"","actionParam1":0,"actionParam2":0,'
    '"actionParamStr":"","createTime":"2026-07-20 12:11:35","createType":0,"destination":2,'
    '"destinationName":"站点2","executeTime":"2026-07-20 12:11:36","executingIndex":0,'
    '"failStrategy":"FAIL_STRATEGY_VOID","failValue":"0","finishTime":"2026-07-20 12:11:40",'
    '"functionKey":"","id":7416323,"isDeleted":0,"length":0,"mapId":29,"mapName":"api测试",'
    '"missionState":2,"orderId":488003,"orderUuid":"be8cb2d2-c50c-4b36-b04b-fb034a2ca3fb",'
    '"resultCode":900,"resultStr":"订单完成","speed":0.0,"successStrategy":"SUCCESS_STRATEGY_VOID",'
    '"type":"move","updateTime":"2026-07-20 12:11:40","width":0}],"modifiedBy":"internal",'
    '"orderId":"order-2079056586101358592","orderName":"riot-lab-I-20260720-120949",'
    '"orderState":5,"orderType":1,"priority":0,"priorityQueue":0,"progress":100,"source":"FMS",'
    '"startEndStationNameDetail":"api测试 站点2 > api测试 站点2","startStationName":"站点2",'
    '"startStationNo":2,"taskState":"1","totalCosts":0,"updateTime":"2026-07-20 12:11:40",'
    '"upperId":"riot-lab-I-20260720-120949","userId":0},"tid":""}'
)


@pytest.mark.asyncio
async def test_get_order_by_upper_id_returns_order_identifiers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_DETAIL_SUCCESS_BODY,
            headers={"Content-Type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            order = await session.order.get_order_by_upper_id(_UPPER_ID)

    assert order.id == 488003
    assert order.order_id == "order-2079056586101358592"
    assert order.upper_id == _UPPER_ID
    assert order.order_state == 5


async def _find(
    upper_id: str,
    body: str,
    *,
    status_code: int = 200,
):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            status_code,
            text=body,
            headers={"Content-Type": "application/json"},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            result = await session.order.find_order_by_upper_id(upper_id)
    return result, requests


@pytest.mark.asyncio
async def test_find_order_by_upper_id_returns_found_for_matching_complete_result() -> None:
    result, requests = await _find(
        "UPPER-7",
        '{"code":"0","result":{"id":7,"orderId":"ORDER-7","upperId":"UPPER-7",'
        '"orderState":3,"appointVehicleKey":"VEHICLE-1","executeVehicleKey":"VEHICLE-1",'
        '"endStationNo":12,"missions":[{"type":"move","mapId":25,"destination":12}]}}',
    )

    assert result.status is OrderLookupStatus.Found
    assert result.requested_upper_id == "UPPER-7"
    assert result.order is not None
    assert result.order.order_id == "ORDER-7"
    assert result.order.execute_vehicle_key == "VEHICLE-1"
    assert result.order.missions[0].map_id == 25
    assert requests[0].url.path == "/api/order/v1/orderRecord/detailByUpperId/UPPER-7"
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_find_order_by_upper_id_returns_not_found_only_for_http_404() -> None:
    result, requests = await _find("UPPER-404", "{}", status_code=404)

    assert result.status is OrderLookupStatus.NotFound
    assert result.order is None
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_find_order_by_upper_id_returns_absent_at_observation_for_success_without_result() -> None:
    result, requests = await _find(
        "UPPER-ABSENT",
        '{"code":"0","message":"成功","msgDetail":"","tid":""}',
    )

    assert result.status is OrderLookupStatus.AbsentAtObservation
    assert result.status is not OrderLookupStatus.NotFound
    assert result.order is None
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_find_order_by_upper_id_returns_indeterminate_for_incomplete_result() -> None:
    result, requests = await _find(
        "UPPER-INCOMPLETE",
        '{"code":"0","result":{"upperId":"UPPER-INCOMPLETE","orderState":1}}',
    )

    assert result.status is OrderLookupStatus.Indeterminate
    assert result.order is None
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_find_order_by_upper_id_returns_indeterminate_for_mismatched_upper_id() -> None:
    result, requests = await _find(
        "EXPECTED-UPPER",
        '{"code":"0","result":{"id":8,"orderId":"ORDER-8",'
        '"upperId":"OTHER-UPPER","orderState":1}}',
    )

    assert result.status is OrderLookupStatus.Indeterminate
    assert result.order is None
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_find_order_by_upper_id_propagates_task_cancellation() -> None:
    class CancellationTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
            raise asyncio.CancelledError

    async with httpx.AsyncClient(
        transport=CancellationTransport(),
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            with pytest.raises(asyncio.CancelledError):
                await session.order.find_order_by_upper_id("UPPER-CANCEL")


@pytest.mark.asyncio
async def test_find_order_by_upper_id_wraps_http_500_as_riot_api_exception() -> None:
    body = '{"error":"upstream unavailable"}'
    with pytest.raises(RiotApiException) as caught:
        await _find("UPPER-500", body, status_code=500)

    assert caught.value.status_code == 500
    assert caught.value.response_body == body


@pytest.mark.asyncio
async def test_find_order_by_upper_id_wraps_invalid_json_as_riot_api_exception() -> None:
    body = "not-json"
    with pytest.raises(RiotApiException) as caught:
        await _find("UPPER-JSON", body)

    assert caught.value.status_code == 200
    assert caught.value.business_code == "riot-response-invalid"
    assert caught.value.response_body == body


@pytest.mark.asyncio
async def test_find_order_by_upper_id_preserves_business_failure_evidence() -> None:
    body = '{"code":"500","message":"业务失败","result":null}'
    with pytest.raises(RiotApiException) as caught:
        await _find("UPPER-BUSINESS", body)

    assert caught.value.status_code == 200
    assert caught.value.business_code == "500"
    assert caught.value.response_body == body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("error_type", "expected_business_code"),
    [
        (httpx.ConnectError, "riot-read-failed"),
        (httpx.ReadTimeout, "riot-read-timeout"),
    ],
)
async def test_find_order_by_upper_id_wraps_transport_and_read_failures(
    error_type: type[httpx.TransportError],
    expected_business_code: str,
) -> None:
    class FailureTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
            raise error_type("simulated failure", request=request)

    async with httpx.AsyncClient(
        transport=FailureTransport(),
        base_url="http://riot.test/",
    ) as client:
        options = RiotOptions(
            base_url="http://riot.test",
            call_api_key="test-call-api-key",
        )
        async with RiotSession(options, client=client) as session:
            with pytest.raises(RiotApiException) as caught:
                await session.order.find_order_by_upper_id("UPPER-FAIL")

    assert caught.value.business_code == expected_business_code
