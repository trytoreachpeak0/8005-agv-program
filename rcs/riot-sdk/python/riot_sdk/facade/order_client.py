from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kiota_abstractions.base_request_configuration import RequestConfiguration

from riot_sdk.core.business_response import ensure_success, require_response
from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.core.order_ref import OrderRef
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
        return _to_order_ref(response.result, "byDefaultMissions")

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
