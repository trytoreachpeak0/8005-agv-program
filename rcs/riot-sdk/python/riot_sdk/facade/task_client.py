from __future__ import annotations

from typing import TYPE_CHECKING

from riot_sdk.core.business_response import (
    ensure_success,
    require_response,
    require_result,
)
from riot_sdk.core.dispatchable_vehicles import DispatchableVehicle, resolve_device_key
from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.core.route_cost import RouteCost
from riot_sdk.generated.task.models.batch_vehicle_operation import BatchVehicleOperation
from riot_sdk.generated.task.models.order_command_d_t_o_object import OrderCommandDTOObject
from riot_sdk.generated.task.models.order_command_d_t_o_object_command_type import (
    OrderCommandDTOObject_commandType,
)
from riot_sdk.generated.task.models.u627eu6700u8fd1u7684u7ec8u70b9u53c2u6570_object import (
    U627eu6700u8fd1u7684u7ec8u70b9u53c2u6570Object,
)
from riot_sdk.generated.task.models.u627eu6700u8fd1u7684u8d77u70b9u53c2u6570_object import (
    U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object,
)
from riot_sdk.generated.task.models.u7533u8bf7u8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7 import (
    U7533u8bf7u8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7,
)

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


class TaskClient:
    """Thin task-module facade."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    async def get_dispatchable_vehicles(self) -> list[DispatchableVehicle]:
        """GET /api/task/vehicles/getAllVehicleSimpleInfo (BC-VEH-002 / ADR-sdk-0005)."""
        client = self._session.create_generated_task_client()
        response = require_response(
            await client.api.task.vehicles.get_all_vehicle_simple_info.get(),
            "getAllVehicleSimpleInfo",
        )
        ensure_success(response.code, response.message)
        result = response.result or []
        return [
            DispatchableVehicle(device_key=v.device_key, device_name=v.device_name)
            for v in result
            if v.device_key and v.device_name
        ]

    async def resolve_device_key(self, device_name: str) -> str:
        """Exact deviceName → deviceKey via getAllVehicleSimpleInfo (BC-VEH-002)."""
        vehicles = await self.get_dispatchable_vehicles()
        return resolve_device_key(vehicles, device_name)

    async def get_route_cost(
        self,
        map_id: int,
        station_id: int,
        device_key: str,
    ) -> RouteCost:
        """POST /api/task/v1/route/getRouteCostsBy (BC-ROUTE-001 / ADR-sdk-0005)."""
        if not device_key or not device_key.strip():
            raise ValueError("device_key is required")

        client = self._session.create_generated_task_client()
        body = U7533u8bf7u8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7(
            map_id=map_id,
            station_id=station_id,
            device_keys=[device_key],
        )
        response = require_response(
            await client.api.task.v1.route.get_route_costs_by.post(body),
            "getRouteCostsBy",
        )
        ensure_success(response.code, response.message)

        costs_list = (response.result.device_costs_list if response.result else None) or []
        entry = next((c for c in costs_list if c.device_key == device_key), None)
        if entry is None or entry.costs is None:
            raise RiotApiException(
                f"getRouteCostsBy returned no costs for deviceKey={device_key}.",
                business_code="route-cost-missing",
            )
        return RouteCost(costs_mm=int(entry.costs))

    async def query_nearest_end(
        self,
        map_id: int,
        start_station_id: int,
        end_station_ids: list[int],
    ) -> int:
        """POST /api/task/v1/route/queryNearEnd — nearest end stationId (NearStationQuery)."""
        if not end_station_ids:
            raise ValueError("end_station_ids must not be empty")

        client = self._session.create_generated_task_client()
        body = U627eu6700u8fd1u7684u7ec8u70b9u53c2u6570Object(
            map_id=map_id,
            start_station_id=start_station_id,
            end_station_ids=list(end_station_ids),
        )
        response = require_response(
            await client.api.task.v1.route.query_near_end.post(body),
            "queryNearEnd",
        )
        ensure_success(response.code, response.message)
        return int(
            require_result(response.result, "queryNearEnd", "near-end-missing")
        )

    async def query_nearest_start(
        self,
        map_id: int,
        end_station_id: int,
        start_station_ids: list[int],
    ) -> int:
        """POST /api/task/v1/route/queryNearestStart — nearest start stationId (NearStationQuery)."""
        if not start_station_ids:
            raise ValueError("start_station_ids must not be empty")

        client = self._session.create_generated_task_client()
        body = U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object(
            map_id=map_id,
            end_station_id=end_station_id,
            start_station_ids=list(start_station_ids),
        )
        response = require_response(
            await client.api.task.v1.route.query_nearest_start.post(body),
            "queryNearestStart",
        )
        ensure_success(response.code, response.message)
        return int(
            require_result(response.result, "queryNearestStart", "near-start-missing")
        )

    async def cancel_order(self, order_id: str, reason: str | None = None) -> None:
        """POST /api/task/v1/order/command/{orderId} CMD_ORDER_CANCEL (BC-ORDER-003)."""
        await self._post_order_command(
            order_id,
            OrderCommandDTOObject_commandType.CMD_ORDER_CANCEL,
            reason,
        )

    async def order_hold(self, order_id: str, reason: str | None = None) -> None:
        """POST /api/task/v1/order/command/{orderId} CMD_ORDER_HELD (BC-ORDER-006)."""
        await self._post_order_command(
            order_id,
            OrderCommandDTOObject_commandType.CMD_ORDER_HELD,
            reason,
        )

    async def order_continue(self, order_id: str, reason: str | None = None) -> None:
        """POST /api/task/v1/order/command/{orderId} CMD_ORDER_CONTINUE_FROM_HELD (BC-ORDER-006)."""
        await self._post_order_command(
            order_id,
            OrderCommandDTOObject_commandType.CMD_ORDER_CONTINUE_FROM_HELD,
            reason,
        )

    async def hang_continue(self, order_id: str, reason: str | None = None) -> None:
        """POST /api/task/v1/order/command/{orderId} CMD_ORDER_CONTINUE_FROM_HANG (BC-ORDER-015)."""
        await self._post_order_command(
            order_id,
            OrderCommandDTOObject_commandType.CMD_ORDER_CONTINUE_FROM_HANG,
            reason,
        )

    async def dispatch_enable(self, device_key: str) -> None:
        """POST updateVehicleIntegrationLevel serviceId=enable (BC-VEH-003)."""
        await self._update_integration_level(device_key, enable=True)

    async def dispatch_disable(self, device_key: str) -> None:
        """POST updateVehicleIntegrationLevel serviceId=disable (BC-VEH-003)."""
        await self._update_integration_level(device_key, enable=False)

    @property
    def raw(self):
        """Underlying Kiota client for endpoints not yet wrapped."""
        return self._session.create_generated_task_client()

    async def _post_order_command(
        self,
        order_id: str,
        command_type: OrderCommandDTOObject_commandType,
        reason: str | None,
    ) -> None:
        if not order_id or not order_id.strip():
            raise ValueError("order_id is required")

        client = self._session.create_generated_task_client()
        body = OrderCommandDTOObject(
            command_type=command_type,
            disable_vehicle=False,
            reason=reason,
        )
        response = require_response(
            await client.api.task.v1.order.command.by_order_key(order_id).post(body),
            str(command_type.value),
        )
        ensure_success(response.code, response.message)

    async def _update_integration_level(self, device_key: str, *, enable: bool) -> None:
        if not device_key or not device_key.strip():
            raise ValueError("device_key is required")

        service_id = "enable" if enable else "disable"
        operation = "DispatchEnable" if enable else "DispatchDisable"
        client = self._session.create_generated_task_client()
        body = BatchVehicleOperation(
            device_keys=[device_key],
            service_id=service_id,
        )
        response = require_response(
            await client.api.task.vehicles.update_vehicle_integration_level.post(body),
            operation,
        )
        ensure_success(response.code, response.message)
