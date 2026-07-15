from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from .....models.device_group_dto import DeviceGroupDto
    from .....models.response_msg_of_device_group_dto import ResponseMsg_Of_DeviceGroupDto
    from .delete_device_group_by_id.delete_device_group_by_id_request_builder import DeleteDeviceGroupByIdRequestBuilder
    from .query_devices_groups.query_devices_groups_request_builder import QueryDevicesGroupsRequestBuilder
    from .query_device_groups_bydevice_key.query_device_groups_bydevice_key_request_builder import QueryDeviceGroupsBydeviceKeyRequestBuilder
    from .query_device_group_by_id.query_device_group_by_id_request_builder import QueryDeviceGroupByIdRequestBuilder

class GroupRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/group
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new GroupRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/group", path_parameters)
    
    async def post(self,body: DeviceGroupDto, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_DeviceGroupDto]:
        """
        addDeviceGroup
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_DeviceGroupDto]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_device_group_dto import ResponseMsg_Of_DeviceGroupDto

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_DeviceGroupDto, None)
    
    def to_post_request_information(self,body: DeviceGroupDto, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        addDeviceGroup
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> GroupRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: GroupRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return GroupRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def delete_device_group_by_id(self) -> DeleteDeviceGroupByIdRequestBuilder:
        """
        The deleteDeviceGroupById property
        """
        from .delete_device_group_by_id.delete_device_group_by_id_request_builder import DeleteDeviceGroupByIdRequestBuilder

        return DeleteDeviceGroupByIdRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_device_group_by_id(self) -> QueryDeviceGroupByIdRequestBuilder:
        """
        The queryDeviceGroupById property
        """
        from .query_device_group_by_id.query_device_group_by_id_request_builder import QueryDeviceGroupByIdRequestBuilder

        return QueryDeviceGroupByIdRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_device_groups_bydevice_key(self) -> QueryDeviceGroupsBydeviceKeyRequestBuilder:
        """
        The queryDeviceGroupsBydeviceKey property
        """
        from .query_device_groups_bydevice_key.query_device_groups_bydevice_key_request_builder import QueryDeviceGroupsBydeviceKeyRequestBuilder

        return QueryDeviceGroupsBydeviceKeyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_devices_groups(self) -> QueryDevicesGroupsRequestBuilder:
        """
        The queryDevicesGroups property
        """
        from .query_devices_groups.query_devices_groups_request_builder import QueryDevicesGroupsRequestBuilder

        return QueryDevicesGroupsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class GroupRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

