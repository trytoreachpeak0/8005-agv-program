from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from kiota_abstractions.base_request_configuration import RequestConfiguration

from riot_sdk.core.exceptions import RiotApiException
from riot_sdk.generated.device.models.device_command_dto import DeviceCommandDto
from riot_sdk.generated.device.models.device_command_dto_things_properties import (
    DeviceCommandDto_thingsProperties,
)
from riot_sdk.generated.device.models.mq_callback import MqCallback

if TYPE_CHECKING:
    from riot_sdk.facade.session import RiotSession


def _is_success_code(code: str | None) -> bool:
    return code is None or code == "" or code == "0"


class DeviceClient:
    """Thin device-module facade. Method names align with the C# DeviceClient."""

    def __init__(self, session: RiotSession) -> None:
        self._session = session

    async def list_devices(
        self,
        page_num: int | None = None,
        page_size: int | None = None,
    ) -> Any:
        """GET /api/device/v1/devices"""
        client = self._session.create_generated_device_client()
        request = client.api.device.v1.devices
        query = request.DevicesRequestBuilderGetQueryParameters()
        query.page_num = page_num
        query.page_size = page_size
        config = RequestConfiguration(query_parameters=query)
        return await request.get(request_configuration=config)

    async def get_device_status_statistics(self) -> Any:
        """GET /api/device/v1/devices/statistics/status"""
        client = self._session.create_generated_device_client()
        return await client.api.device.v1.devices.statistics.status.get()

    async def trigger_emergency_stop(self, device_key: str) -> None:
        """POST sync/service/{deviceKey}/triggerEmergency (BC-VEH-005)."""
        if not device_key or not device_key.strip():
            raise ValueError("device_key is required")

        client = self._session.create_generated_device_client()
        body = DeviceCommandDto(
            message_id=str(random.randint(100000, 999999)),
            mq_callback=MqCallback(tag="string", topic="string"),
            things_properties=DeviceCommandDto_thingsProperties(),
        )
        response = await (
            client.api.device.v1.command.sync.service.by_device_key(device_key)
            .by_service_id("triggerEmergency")
            .post(body)
        )
        if response is None:
            raise RiotApiException("TriggerEmergencyStop returned empty response.")
        if not _is_success_code(response.code):
            raise RiotApiException(
                f"RIoT business failure code={response.code} message={response.message}",
                status_code=200,
                business_code=response.code,
            )

    async def cancel_emergency_stop(self, device_key: str) -> None:
        """POST sync/service/{deviceKey}/cancelEmergency (BC-VEH-005)."""
        if not device_key or not device_key.strip():
            raise ValueError("device_key is required")

        client = self._session.create_generated_device_client()
        body = DeviceCommandDto(
            message_id=str(random.randint(100000, 999999)),
            mq_callback=MqCallback(tag="string", topic="string"),
            things_properties=DeviceCommandDto_thingsProperties(),
        )
        response = await (
            client.api.device.v1.command.sync.service.by_device_key(device_key)
            .by_service_id("cancelEmergency")
            .post(body)
        )
        if response is None:
            raise RiotApiException("CancelEmergencyStop returned empty response.")
        if not _is_success_code(response.code):
            raise RiotApiException(
                f"RIoT business failure code={response.code} message={response.message}",
                status_code=200,
                business_code=response.code,
            )
