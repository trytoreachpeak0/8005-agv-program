from __future__ import annotations

import random
from typing import TYPE_CHECKING

from kiota_abstractions.base_request_configuration import RequestConfiguration

from riot_sdk.core.business_response import ensure_success, require_response
from riot_sdk.generated.device.models.device_command_dto import DeviceCommandDto
from riot_sdk.generated.device.models.device_command_dto_things_properties import (
    DeviceCommandDto_thingsProperties,
)
from riot_sdk.generated.device.models.device_status_statistics_dto import (
    DeviceStatusStatisticsDto,
)
from riot_sdk.generated.device.models.mq_callback import MqCallback
from riot_sdk.generated.device.models.page_of_device_object import Page_Of_DeviceObject

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


class DeviceClient:
    """Thin device-module facade. Method names align with the C# DeviceClient."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    async def list_devices(
        self,
        page_num: int | None = None,
        page_size: int | None = None,
    ) -> Page_Of_DeviceObject:
        """GET /api/device/v1/devices — unwrap page; throw on business failure (ADR-sdk-0005)."""
        client = self._session.create_generated_device_client()
        request = client.api.device.v1.devices
        query = request.DevicesRequestBuilderGetQueryParameters()
        query.page_num = page_num
        query.page_size = page_size
        config = RequestConfiguration(query_parameters=query)
        response = require_response(
            await request.get(request_configuration=config),
            "ListDevices",
        )
        ensure_success(response.code, response.message)
        return response.result or Page_Of_DeviceObject()

    async def get_device_status_statistics(self) -> DeviceStatusStatisticsDto:
        """GET /api/device/v1/devices/statistics/status — unwrap DTO (ADR-sdk-0005)."""
        client = self._session.create_generated_device_client()
        response = require_response(
            await client.api.device.v1.devices.statistics.status.get(),
            "GetDeviceStatusStatistics",
        )
        ensure_success(response.code, response.message)
        return response.result or DeviceStatusStatisticsDto()

    async def trigger_emergency_stop(self, device_key: str) -> None:
        """POST sync/service/{deviceKey}/triggerEmergency (BC-VEH-005)."""
        await self._post_emergency_service(device_key, "triggerEmergency")

    async def cancel_emergency_stop(self, device_key: str) -> None:
        """POST sync/service/{deviceKey}/cancelEmergency (BC-VEH-005)."""
        await self._post_emergency_service(device_key, "cancelEmergency")

    async def _post_emergency_service(self, device_key: str, service_id: str) -> None:
        if not device_key or not device_key.strip():
            raise ValueError("device_key is required")

        client = self._session.create_generated_device_client()
        body = DeviceCommandDto(
            message_id=str(random.randint(100000, 999999)),
            mq_callback=MqCallback(tag="string", topic="string"),
            things_properties=DeviceCommandDto_thingsProperties(),
        )
        response = require_response(
            await (
                client.api.device.v1.command.sync.service.by_device_key(device_key)
                .by_service_id(service_id)
                .post(body)
            ),
            service_id,
        )
        ensure_success(response.code, response.message)
