from __future__ import annotations

import httpx
import pytest

from riot_sdk import OrderStatePage, OrderStateRecord, RiotApiException, RiotOptions, RiotSession


async def _list(body: str):
    requests: list[httpx.Request] = []

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
            result = await session.order.list_orders_by_states([1, 3, 7, 9])
    return result, requests


@pytest.mark.asyncio
async def test_list_orders_by_states_returns_records_and_complete_page_metadata() -> None:
    page, requests = await _list("""
        {"code":"0","result":{"current":1,"size":100,"total":2,"records":[
          {"id":1,"orderId":"ORDER-1","upperId":"UPPER-1","orderState":1,
           "appointVehicleKey":"VEHICLE-1","executeVehicleKey":null},
          {"id":2,"orderId":"ORDER-2","upperId":"UPPER-2","orderState":3,
           "appointVehicleKey":"VEHICLE-1","executeVehicleKey":"VEHICLE-1"}
        ]}}
        """)

    assert page.current == 1
    assert page.size == 100
    assert page.total == 2
    assert len(page.records) == 2
    assert page.records[1].upper_id == "UPPER-2"
    assert page.covers_all_records
    full_page = tuple(
        OrderStateRecord(i, f"ORDER-{i}", f"UPPER-{i}", 1, None, None)
        for i in range(100)
    )
    assert not OrderStatePage(1, 100, 101, full_page).covers_all_records
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_list_orders_by_states_sends_each_non_final_state_filter() -> None:
    page, requests = await _list(
        '{"code":"0","result":{"current":1,"size":100,"total":0,"records":[]}}'
    )

    request = requests[0]
    assert request.url.path == "/api/order/v1/orderRecord"
    assert request.url.params["pageNum"] == "1"
    assert request.url.params["pageSize"] == "100"
    assert [value for key, value in request.url.params.multi_items() if key == "filterByState"] == [
        "1",
        "3",
        "7",
        "9",
    ]
    assert page.records == ()
    assert page.covers_all_records


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        '{"code":"0"}',
        '{"code":"0","result":{"current":1,"size":100,"total":0}}',
    ],
)
async def test_list_orders_by_states_rejects_missing_page_or_records(body: str) -> None:
    with pytest.raises(RiotApiException) as caught:
        await _list(body)
    assert caught.value.business_code == "order-state-page-missing"
