from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from kiota_abstractions.base_request_configuration import RequestConfiguration

from riot_sdk.core.business_response import ensure_success, is_success_code, require_response
from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.core.order_ref import OrderRef
from riot_sdk.core.order_snapshots import (
    OrderLookupResult,
    OrderMissionSnapshot,
    OrderSnapshot,
)
from riot_sdk.core.order_state_page import OrderStatePage, OrderStateRecord
from riot_sdk.generated.order.models.mission_d_t_o import MissionDTO
from riot_sdk.generated.order.models.order_record_d_t_o_object import OrderRecordDTOObject

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


def _to_order_ref(result: Any, source: str) -> OrderRef:
    if (
        result is None
        or result.id is None
        or not result.order_id
        or not result.upper_id
        or result.order_state is None
    ):
        raise RiotApiException(
            f"{source} returned incomplete order identifiers.",
            business_code="order-ref-missing",
        )
    return OrderRef(
        id=int(result.id),
        order_id=result.order_id,
        upper_id=result.upper_id,
        order_state=int(result.order_state),
    )


def _snapshot_from_payload(result: Any) -> OrderSnapshot | None:
    if not isinstance(result, dict):
        return None
    order_id = result.get("orderId")
    upper_id = result.get("upperId")
    if (
        result.get("id") is None
        or not isinstance(order_id, str)
        or not order_id.strip()
        or not isinstance(upper_id, str)
        or not upper_id.strip()
        or result.get("orderState") is None
    ):
        return None
    missions = result.get("missions")
    mission_rows = missions if isinstance(missions, list) else []
    return OrderSnapshot(
        id=int(result["id"]),
        order_id=order_id,
        upper_id=upper_id,
        order_state=int(result["orderState"]),
        appoint_vehicle_key=result.get("appointVehicleKey"),
        execute_vehicle_key=result.get("executeVehicleKey"),
        end_station_no=result.get("endStationNo"),
        missions=tuple(
            OrderMissionSnapshot(
                type=mission.get("type"),
                map_id=mission.get("mapId"),
                destination=mission.get("destination"),
            )
            for mission in mission_rows
            if isinstance(mission, dict)
        ),
    )


class OrderClient:
    """Thin order-module facade."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    async def create_move_order(
        self,
        upper_id: str,
        appoint_vehicle_key: str,
        map_id: int,
        destination_station_id: int,
        order_name: str | None = None,
    ) -> OrderRef:
        """POST /api/order/v1/add/byDefaultMissions — single-segment move (BC-ORDER-001)."""
        if not upper_id or not upper_id.strip():
            raise ValueError("upper_id is required")
        if not appoint_vehicle_key or not appoint_vehicle_key.strip():
            raise ValueError("appoint_vehicle_key is required")
        if map_id <= 0:
            raise ValueError("map_id must be positive")
        if destination_station_id <= 0:
            raise ValueError("destination_station_id must be positive")

        client = self._session.create_generated_order_client()
        body = OrderRecordDTOObject(
            appoint_vehicle_key=appoint_vehicle_key,
            is_appoint_enable=1,
            lock_status=0,
            order_name=order_name.strip() if order_name and order_name.strip() else upper_id,
            upper_id=upper_id,
            mission=[
                MissionDTO(
                    type="move",
                    map_id=map_id,
                    destination=destination_station_id,
                )
            ],
        )
        response = require_response(
            await client.api.order.v1.add.by_default_missions.post(body),
            "byDefaultMissions",
        )
        ensure_success(response.code, response.message)
        created = _to_order_ref(response.result, "byDefaultMissions")
        if created.upper_id != upper_id:
            raise RiotApiException(
                "byDefaultMissions returned a mismatched upperId.",
                business_code="order-upper-id-mismatch",
            )
        return created

    async def get_order_by_upper_id(self, upper_id: str) -> OrderRef:
        """GET /api/order/v1/orderRecord/detailByUpperId/{upperId} (BC-ORDER-005)."""
        if not upper_id or not upper_id.strip():
            raise ValueError("upper_id is required")

        client = self._session.create_generated_order_client()
        response = require_response(
            await client.api.order.v1.order_record.detail_by_upper_id.by_upper_id(
                upper_id
            ).get(),
            "detailByUpperId",
        )
        ensure_success(response.code, response.message)
        return _to_order_ref(response.result, "detailByUpperId")

    async def find_order_by_upper_id(self, upper_id: str) -> OrderLookupResult:
        """Observe upper_id; only HTTP 404 is authoritative NotFound."""
        if not upper_id or not upper_id.strip():
            raise ValueError("upper_id is required")

        response = await self._session._request_raw(
            "GET",
            "/api/order/v1/orderRecord/detailByUpperId/"
            + quote(upper_id, safe=""),
        )
        if response.status_code == 404:
            return OrderLookupResult.not_found(upper_id)
        if response.status_code >= 400:
            raise RiotApiException(
                f"detailByUpperId HTTP {response.status_code}.",
                status_code=response.status_code,
                response_body=response.text,
            )
        try:
            payload = response.json()
        except ValueError as error:
            raise RiotApiException(
                "detailByUpperId returned invalid JSON.",
                status_code=response.status_code,
                business_code="riot-response-invalid",
                response_body=response.text,
            ) from error
        if not isinstance(payload, dict):
            raise RiotApiException(
                "detailByUpperId returned a non-object response.",
                status_code=response.status_code,
                business_code="riot-response-invalid",
                response_body=response.text,
            )

        raw_code = payload.get("code")
        code = str(raw_code) if raw_code is not None else None
        if not is_success_code(code):
            raise RiotApiException(
                f"RIoT business failure code={code} message={payload.get('message')}",
                status_code=response.status_code,
                business_code=code,
                response_body=response.text,
            )
        if payload.get("result") is None:
            return OrderLookupResult.absent_at_observation(upper_id)
        snapshot = _snapshot_from_payload(payload["result"])
        if snapshot is None or snapshot.upper_id != upper_id:
            return OrderLookupResult.indeterminate(upper_id)
        return OrderLookupResult.found(upper_id, snapshot)

    async def get_order_by_order_id(self, order_id: str) -> OrderRef:
        """GET /api/order/v1/orderRecord/detailByOrderId/{orderId} (BC-ORDER-005)."""
        if not order_id or not order_id.strip():
            raise ValueError("order_id is required")

        client = self._session.create_generated_order_client()
        response = require_response(
            await client.api.order.v1.order_record.detail_by_order_id.by_order_id(
                order_id
            ).get(),
            "detailByOrderId",
        )
        ensure_success(response.code, response.message)
        return _to_order_ref(response.result, "detailByOrderId")

    async def list_orders_by_states(
        self,
        order_states: list[int] | tuple[int, ...],
        page_num: int = 1,
        page_size: int = 100,
    ) -> OrderStatePage:
        """Return an identity-preserving order page with repeated state filters."""
        if not order_states:
            raise ValueError("order_states must not be empty")
        if page_num <= 0:
            raise ValueError("page_num must be positive")
        if page_size <= 0:
            raise ValueError("page_size must be positive")

        filters = "&".join(f"filterByState={int(state)}" for state in order_states)
        raw_url = (
            f"{self._session.options.base_url.rstrip('/')}"
            f"/api/order/v1/orderRecord?pageNum={page_num}&pageSize={page_size}&{filters}"
        )
        client = self._session.create_generated_order_client()
        response = require_response(
            await client.api.order.v1.order_record.with_url(raw_url).get(),
            "orderRecord",
        )
        ensure_success(response.code, response.message)
        if response.result is None or response.result.records is None:
            raise RiotApiException(
                "orderRecord returned missing page or records.",
                business_code="order-state-page-missing",
            )

        return OrderStatePage(
            current=response.result.current,
            size=response.result.size,
            total=response.result.total,
            records=tuple(
                OrderStateRecord(
                    id=record.id,
                    order_id=record.order_id,
                    upper_id=record.upper_id,
                    order_state=record.order_state,
                    appoint_vehicle_key=record.appoint_vehicle_key,
                    execute_vehicle_key=record.execute_vehicle_key,
                )
                for record in response.result.records
            ),
        )

    async def priority_exec(self, order_id: str) -> None:
        """POST /api/order/v1/orderRecordPriorityExec?orderTaskKey={orderId} (BC-ORDER-014)."""
        if not order_id or not order_id.strip():
            raise ValueError("order_id is required")

        client = self._session.create_generated_order_client()
        request = client.api.order.v1.order_record_priority_exec
        query = request.OrderRecordPriorityExecRequestBuilderPostQueryParameters()
        query.order_task_key = order_id
        config = RequestConfiguration(query_parameters=query)
        response = require_response(
            await request.post(request_configuration=config),
            "orderRecordPriorityExec",
        )
        ensure_success(response.code, response.message)

    @property
    def raw(self):
        """Underlying Kiota client for endpoints not yet wrapped."""
        return self._session.create_generated_order_client()
