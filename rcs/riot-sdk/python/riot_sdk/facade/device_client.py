from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kiota_abstractions.base_request_configuration import RequestConfiguration

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
