from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotApiException, RiotOptions, RiotSession

_DEVICE_KEY = "BROKERX-aee2f93d717546cf9510c98c854fe83e"
_UPPER_ID = "riot-behavior-lab-E1b-2to1-20260720-121102"

# Known-good body from E1-byDefaultMissions-create-2to1.responseBody
_CREATE_SUCCESS_BODY = (
    '{"code":"0","message":"成功","msgDetail":"","result":{"appointVehicleGroupId":0,'
    '"appointVehicleKey":"BROKERX-aee2f93d717546cf9510c98c854fe83e",'
    '"createTime":"2026-07-20 12:12:44","createdBy":"api-test","endStationName":"站点1",'
    '"endStationNo":1,"finalState":false,"id":488004,"isAppointEnable":1,"lockStatus":0,'
    '"missions":[{"actionId":0,"actionName":"","actionParam1":0,"actionParam2":0,'
    '"actionParamStr":"","createTime":"2026-07-20 12:12:44","createType":0,"destination":1,'
    '"destinationName":"","executingIndex":0,"failStrategy":"","failValue":"",'
    '"functionKey":"","id":7416324,"isDeleted":0,"length":0,"mapId":29,"mapName":"",'
    '"missionState":0,"orderId":488004,"orderUuid":"72461016-4273-4d35-b6f1-ad9f0e726643",'
    '"resultCode":0,"resultStr":"","speed":0.0,"successStrategy":"SUCCESS_STRATEGY_VOID",'
    '"type":"move","updateTime":"2026-07-20 12:12:44","width":0}],"modifiedBy":"api-test",'
    '"orderId":"order-2079056892281356288",'
    '"orderName":"riot-behavior-lab-E1b-2to1-20260720-121102","orderState":1,"orderType":1,'
    '"priority":0,"source":"FMS","startEndStationNameDetail":"null null > null null",'
    '"startStationName":"站点1","startStationNo":1,"updateTime":"2026-07-20 12:12:44",'
    '"upperId":"riot-behavior-lab-E1b-2to1-20260720-121102","userId":0},"tid":""}'
)


@pytest.mark.asyncio
async def test_create_move_order_returns_order_identifiers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_CREATE_SUCCESS_BODY,
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
            order = await session.order.create_move_order(
                upper_id=_UPPER_ID,
                appoint_vehicle_key=_DEVICE_KEY,
                map_id=29,
                destination_station_id=1,
            )

    assert order.id == 488004
    assert order.order_id == "order-2079056892281356288"
    assert order.upper_id == _UPPER_ID
    assert order.order_state == 1


@pytest.mark.asyncio
async def test_create_move_order_success_without_result_throws_and_does_not_retry() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            text='{"code":"0","message":"成功","msgDetail":"","tid":""}',
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
            with pytest.raises(RiotApiException) as caught:
                await session.order.create_move_order(
                    upper_id="UPPER-EMPTY",
                    appoint_vehicle_key=_DEVICE_KEY,
                    map_id=29,
                    destination_station_id=1,
                )

    assert caught.value.business_code == "order-ref-missing"
    assert len(requests) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [503, 429, 307])
async def test_create_move_order_owned_transport_does_not_retry_or_follow_redirect(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    class RecordingTransport(httpx.AsyncBaseTransport):
        def __init__(self) -> None:
            self.call_count = 0

        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
            self.call_count += 1
            if self.call_count > 1:
                return httpx.Response(
                    200,
                    text=_CREATE_SUCCESS_BODY,
                    headers={"Content-Type": "application/json"},
                    request=request,
                )
            headers = {"Location": "/must-not-follow"} if status_code == 307 else {}
            return httpx.Response(status_code, json={}, headers=headers, request=request)

    transport = RecordingTransport()

    def transport_factory(*, retries: int):
        assert retries == 0
        return transport

    monkeypatch.setattr(httpx, "AsyncHTTPTransport", transport_factory)
    options = RiotOptions(
        base_url="http://riot.test",
        call_api_key="test-call-api-key",
    )
    async with RiotSession(options) as session:
        assert session._http_client.follow_redirects is False
        with pytest.raises(Exception):
            await session.order.create_move_order(
                upper_id="UPPER-TRANSPORT",
                appoint_vehicle_key=_DEVICE_KEY,
                map_id=29,
                destination_station_id=1,
            )

    assert transport.call_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("map_id", "destination_station_id"),
    [(0, 1), (29, 0), (-1, 1), (29, -1)],
)
async def test_create_move_order_rejects_non_positive_map_or_destination_without_http(
    map_id: int,
    destination_station_id: int,
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, text=_CREATE_SUCCESS_BODY)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="http://riot.test/",
    ) as client:
        async with RiotSession(
            RiotOptions(base_url="http://riot.test", call_api_key="test-key"),
            client=client,
        ) as session:
            with pytest.raises(ValueError):
                await session.order.create_move_order(
                    upper_id="UPPER-INVALID",
                    appoint_vehicle_key=_DEVICE_KEY,
                    map_id=map_id,
                    destination_station_id=destination_station_id,
                )

    assert requests == []


@pytest.mark.asyncio
async def test_create_move_order_rejects_mismatched_response_upper_id_without_retry() -> None:
    requests: list[httpx.Request] = []
    body = (
        '{"code":"0","result":{"id":9,"orderId":"ORDER-9",'
        '"upperId":"OTHER-UPPER","orderState":1}}'
    )

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
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
            with pytest.raises(RiotApiException) as caught:
                await session.order.create_move_order(
                    upper_id="EXPECTED-UPPER",
                    appoint_vehicle_key=_DEVICE_KEY,
                    map_id=29,
                    destination_station_id=1,
                )

    assert caught.value.business_code == "order-upper-id-mismatch"
    assert len(requests) == 1
