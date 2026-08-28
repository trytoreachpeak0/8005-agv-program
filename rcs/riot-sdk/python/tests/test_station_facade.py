from __future__ import annotations

import httpx
import pytest

from riot_sdk import RiotApiException, RiotOptions, RiotSession, Station

# Known-good envelope; items from C2-stations-map-29.
_STATIONS_MAP_29_BODY = """{"code":"0","message":"成功","result":[
  {"id":1,"name":"站点1"},
  {"id":2,"name":"站点2"}
]}"""


@pytest.mark.asyncio
async def test_list_stations_for_map_29_returns_domain_stations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=_STATIONS_MAP_29_BODY,
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
            stations = await session.maps.list_stations(map_id=29)

    assert len(stations) == 2
    assert Station(29, 1, "站点1") in stations
    assert Station(29, 2, "站点2") in stations


async def _strict(body: str) -> list[Station]:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
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
            return await session.maps.list_stations_strict(map_id=29)


@pytest.mark.asyncio
async def test_list_stations_strict_returns_all_valid_rows() -> None:
    stations = await _strict(_STATIONS_MAP_29_BODY)
    assert [station.station_id for station in stations] == [1, 2]


@pytest.mark.asyncio
async def test_list_stations_strict_rejects_malformed_row_instead_of_filtering() -> None:
    with pytest.raises(RiotApiException) as caught:
        await _strict(
            '{"code":"0","result":[{"id":1,"name":"站点1"},{"id":0,"name":""}]}'
        )
    assert caught.value.business_code == "station-catalog-entry-invalid"


@pytest.mark.asyncio
async def test_list_stations_strict_rejects_duplicate_station_id() -> None:
    with pytest.raises(RiotApiException) as caught:
        await _strict(
            '{"code":"0","result":[{"id":1,"name":"站点1"},'
            '{"id":1,"name":"重复站点"}]}'
        )
    assert caught.value.business_code == "station-catalog-duplicate"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("body", "expected_business_code"),
    [
        ('{"code":"0","result":null}', "station-catalog-missing"),
        ('{"code":"0","result":[]}', "station-catalog-empty"),
    ],
)
async def test_list_stations_strict_rejects_null_or_empty_catalog(
    body: str,
    expected_business_code: str,
) -> None:
    with pytest.raises(RiotApiException) as caught:
        await _strict(body)
    assert caught.value.business_code == expected_business_code
