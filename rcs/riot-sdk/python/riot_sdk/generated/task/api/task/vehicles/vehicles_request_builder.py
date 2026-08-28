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
    from ....models.response_msg_of_list_of_u673au5668u4ebau5361u7247u8fd4u56de_object import ResponseMsg_Of_List_Of_u673au5668u4ebau5361u7247u8fd4u56deObject
    from .enter_clean_wheel_mode.enter_clean_wheel_mode_request_builder import EnterCleanWheelModeRequestBuilder
    from .exit_clean_wheel_mode.exit_clean_wheel_mode_request_builder import ExitCleanWheelModeRequestBuilder
    from .get_all_task_vehicles.get_all_task_vehicles_request_builder import GetAllTaskVehiclesRequestBuilder
    from .get_all_vehicle_keys.get_all_vehicle_keys_request_builder import GetAllVehicleKeysRequestBuilder
    from .get_all_vehicle_simple_info.get_all_vehicle_simple_info_request_builder import GetAllVehicleSimpleInfoRequestBuilder
    from .get_vehicle_info_by_device_key.get_vehicle_info_by_device_key_request_builder import GetVehicleInfoByDeviceKeyRequestBuilder
    from .park.park_request_builder import ParkRequestBuilder
    from .pass_.pass_request_builder import PassRequestBuilder
    from .query_vehicle_not_assign_order.query_vehicle_not_assign_order_request_builder import QueryVehicleNotAssignOrderRequestBuilder
    from .setting.setting_request_builder import SettingRequestBuilder
    from .start_location.start_location_request_builder import StartLocationRequestBuilder
    from .stop_location.stop_location_request_builder import StopLocationRequestBuilder
    from .update_vehicle_integration_level.update_vehicle_integration_level_request_builder import UpdateVehicleIntegrationLevelRequestBuilder

class VehiclesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/vehicles
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new VehiclesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/vehicles{?deviceIds*,deviceName*,groupIds*,groupName*,order*,orderBy*,pageNum*,pageSize*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[VehiclesRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_List_Of_u673au5668u4ebau5361u7247u8fd4u56deObject]:
        """
        分页查询车辆信息
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_List_Of_u673au5668u4ebau5361u7247u8fd4u56deObject]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.response_msg_of_list_of_u673au5668u4ebau5361u7247u8fd4u56de_object import ResponseMsg_Of_List_Of_u673au5668u4ebau5361u7247u8fd4u56deObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_List_Of_u673au5668u4ebau5361u7247u8fd4u56deObject, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[VehiclesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        分页查询车辆信息
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> VehiclesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: VehiclesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return VehiclesRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def enter_clean_wheel_mode(self) -> EnterCleanWheelModeRequestBuilder:
        """
        The enterCleanWheelMode property
        """
        from .enter_clean_wheel_mode.enter_clean_wheel_mode_request_builder import EnterCleanWheelModeRequestBuilder

        return EnterCleanWheelModeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def exit_clean_wheel_mode(self) -> ExitCleanWheelModeRequestBuilder:
        """
        The exitCleanWheelMode property
        """
        from .exit_clean_wheel_mode.exit_clean_wheel_mode_request_builder import ExitCleanWheelModeRequestBuilder

        return ExitCleanWheelModeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_all_task_vehicles(self) -> GetAllTaskVehiclesRequestBuilder:
        """
        The getAllTaskVehicles property
        """
        from .get_all_task_vehicles.get_all_task_vehicles_request_builder import GetAllTaskVehiclesRequestBuilder

        return GetAllTaskVehiclesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_all_vehicle_keys(self) -> GetAllVehicleKeysRequestBuilder:
        """
        The getAllVehicleKeys property
        """
        from .get_all_vehicle_keys.get_all_vehicle_keys_request_builder import GetAllVehicleKeysRequestBuilder

        return GetAllVehicleKeysRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_all_vehicle_simple_info(self) -> GetAllVehicleSimpleInfoRequestBuilder:
        """
        The getAllVehicleSimpleInfo property
        """
        from .get_all_vehicle_simple_info.get_all_vehicle_simple_info_request_builder import GetAllVehicleSimpleInfoRequestBuilder

        return GetAllVehicleSimpleInfoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_vehicle_info_by_device_key(self) -> GetVehicleInfoByDeviceKeyRequestBuilder:
        """
        The getVehicleInfoByDeviceKey property
        """
        from .get_vehicle_info_by_device_key.get_vehicle_info_by_device_key_request_builder import GetVehicleInfoByDeviceKeyRequestBuilder

        return GetVehicleInfoByDeviceKeyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def park(self) -> ParkRequestBuilder:
        """
        The park property
        """
        from .park.park_request_builder import ParkRequestBuilder

        return ParkRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def pass_(self) -> PassRequestBuilder:
        """
        The pass property
        """
        from .pass_.pass_request_builder import PassRequestBuilder

        return PassRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_vehicle_not_assign_order(self) -> QueryVehicleNotAssignOrderRequestBuilder:
        """
        The queryVehicleNotAssignOrder property
        """
        from .query_vehicle_not_assign_order.query_vehicle_not_assign_order_request_builder import QueryVehicleNotAssignOrderRequestBuilder

        return QueryVehicleNotAssignOrderRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def setting(self) -> SettingRequestBuilder:
        """
        The setting property
        """
        from .setting.setting_request_builder import SettingRequestBuilder

        return SettingRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def start_location(self) -> StartLocationRequestBuilder:
        """
        The startLocation property
        """
        from .start_location.start_location_request_builder import StartLocationRequestBuilder

        return StartLocationRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def stop_location(self) -> StopLocationRequestBuilder:
        """
        The stopLocation property
        """
        from .stop_location.stop_location_request_builder import StopLocationRequestBuilder

        return StopLocationRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def update_vehicle_integration_level(self) -> UpdateVehicleIntegrationLevelRequestBuilder:
        """
        The updateVehicleIntegrationLevel property
        """
        from .update_vehicle_integration_level.update_vehicle_integration_level_request_builder import UpdateVehicleIntegrationLevelRequestBuilder

        return UpdateVehicleIntegrationLevelRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class VehiclesRequestBuilderGetQueryParameters():
        """
        分页查询车辆信息
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "device_ids":
                return "deviceIds"
            if original_name == "device_name":
                return "deviceName"
            if original_name == "group_ids":
                return "groupIds"
            if original_name == "group_name":
                return "groupName"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "order":
                return "order"
            return original_name
        
        # 多个‘，’隔开
        device_ids: Optional[str] = None

        # deviceName
        device_name: Optional[str] = None

        # 多个‘，’隔开
        group_ids: Optional[str] = None

        # groupName
        group_name: Optional[str] = None

        # 正序倒序（desc为降序，asc为正序）
        order: Optional[str] = None

        # 排序字段
        order_by: Optional[str] = None

        # pageNum
        page_num: Optional[int] = None

        # pageSize
        page_size: Optional[int] = None

    
    @dataclass
    class VehiclesRequestBuilderGetRequestConfiguration(RequestConfiguration[VehiclesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

