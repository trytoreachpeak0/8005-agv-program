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
    from .....models.device_object import DeviceObject
    from .....models.response_msg_of_device_object import ResponseMsg_Of_DeviceObject
    from .....models.response_msg_of_page_of_device_object import ResponseMsg_Of_Page_Of_DeviceObject
    from .bind.bind_request_builder import BindRequestBuilder
    from .delete_all.delete_all_request_builder import DeleteAllRequestBuilder
    from .delete_device_by_device_key.delete_device_by_device_key_request_builder import DeleteDeviceByDeviceKeyRequestBuilder
    from .detail.detail_request_builder import DetailRequestBuilder
    from .disable.disable_request_builder import DisableRequestBuilder
    from .enable.enable_request_builder import EnableRequestBuilder
    from .excel.excel_request_builder import ExcelRequestBuilder
    from .front.front_request_builder import FrontRequestBuilder
    from .item.devices_item_request_builder import DevicesItemRequestBuilder
    from .query.query_request_builder import QueryRequestBuilder
    from .query_devices_properties.query_devices_properties_request_builder import QueryDevicesPropertiesRequestBuilder
    from .query_device_by_device_key.query_device_by_device_key_request_builder import QueryDeviceByDeviceKeyRequestBuilder
    from .query_device_by_type.query_device_by_type_request_builder import QueryDeviceByTypeRequestBuilder
    from .statistical_vehicle.statistical_vehicle_request_builder import StatisticalVehicleRequestBuilder
    from .statistics.statistics_request_builder import StatisticsRequestBuilder
    from .unbind.unbind_request_builder import UnbindRequestBuilder

class DevicesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DevicesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices{?deviceKey*,deviceName*,deviceType*,isBrokerxManager*,nodeType*,order*,orderBy*,pageNum*,pageSize*,parentDeviceKey*,productKey*,queryCondition*}", path_parameters)
    
    def by_id(self,id: int) -> DevicesItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.device.api.device.v1.devices.item collection
        param id: id
        Returns: DevicesItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.devices_item_request_builder import DevicesItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return DevicesItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[DevicesRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_DeviceObject]:
        """
        getDevices
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_DeviceObject]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_page_of_device_object import ResponseMsg_Of_Page_Of_DeviceObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_DeviceObject, None)
    
    async def post(self,body: DeviceObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_DeviceObject]:
        """
        createDevice
        param body: 设备信息
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_DeviceObject]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_device_object import ResponseMsg_Of_DeviceObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_DeviceObject, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[DevicesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        getDevices
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: DeviceObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        createDevice
        param body: 设备信息
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
    
    def with_url(self,raw_url: str) -> DevicesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DevicesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return DevicesRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def bind(self) -> BindRequestBuilder:
        """
        The bind property
        """
        from .bind.bind_request_builder import BindRequestBuilder

        return BindRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def delete_all(self) -> DeleteAllRequestBuilder:
        """
        The deleteAll property
        """
        from .delete_all.delete_all_request_builder import DeleteAllRequestBuilder

        return DeleteAllRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def delete_device_by_device_key(self) -> DeleteDeviceByDeviceKeyRequestBuilder:
        """
        The deleteDeviceByDeviceKey property
        """
        from .delete_device_by_device_key.delete_device_by_device_key_request_builder import DeleteDeviceByDeviceKeyRequestBuilder

        return DeleteDeviceByDeviceKeyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def detail(self) -> DetailRequestBuilder:
        """
        The detail property
        """
        from .detail.detail_request_builder import DetailRequestBuilder

        return DetailRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def disable(self) -> DisableRequestBuilder:
        """
        The disable property
        """
        from .disable.disable_request_builder import DisableRequestBuilder

        return DisableRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def enable(self) -> EnableRequestBuilder:
        """
        The enable property
        """
        from .enable.enable_request_builder import EnableRequestBuilder

        return EnableRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def excel(self) -> ExcelRequestBuilder:
        """
        The excel property
        """
        from .excel.excel_request_builder import ExcelRequestBuilder

        return ExcelRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def front(self) -> FrontRequestBuilder:
        """
        The front property
        """
        from .front.front_request_builder import FrontRequestBuilder

        return FrontRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query(self) -> QueryRequestBuilder:
        """
        The query property
        """
        from .query.query_request_builder import QueryRequestBuilder

        return QueryRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_device_by_device_key(self) -> QueryDeviceByDeviceKeyRequestBuilder:
        """
        The queryDeviceByDeviceKey property
        """
        from .query_device_by_device_key.query_device_by_device_key_request_builder import QueryDeviceByDeviceKeyRequestBuilder

        return QueryDeviceByDeviceKeyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_device_by_type(self) -> QueryDeviceByTypeRequestBuilder:
        """
        The queryDeviceByType property
        """
        from .query_device_by_type.query_device_by_type_request_builder import QueryDeviceByTypeRequestBuilder

        return QueryDeviceByTypeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_devices_properties(self) -> QueryDevicesPropertiesRequestBuilder:
        """
        The queryDevicesProperties property
        """
        from .query_devices_properties.query_devices_properties_request_builder import QueryDevicesPropertiesRequestBuilder

        return QueryDevicesPropertiesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def statistical_vehicle(self) -> StatisticalVehicleRequestBuilder:
        """
        The statisticalVehicle property
        """
        from .statistical_vehicle.statistical_vehicle_request_builder import StatisticalVehicleRequestBuilder

        return StatisticalVehicleRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def statistics(self) -> StatisticsRequestBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_request_builder import StatisticsRequestBuilder

        return StatisticsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def unbind(self) -> UnbindRequestBuilder:
        """
        The unbind property
        """
        from .unbind.unbind_request_builder import UnbindRequestBuilder

        return UnbindRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class DevicesRequestBuilderGetQueryParameters():
        """
        getDevices
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "device_key":
                return "deviceKey"
            if original_name == "device_name":
                return "deviceName"
            if original_name == "device_type":
                return "deviceType"
            if original_name == "is_brokerx_manager":
                return "isBrokerxManager"
            if original_name == "node_type":
                return "nodeType"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "parent_device_key":
                return "parentDeviceKey"
            if original_name == "product_key":
                return "productKey"
            if original_name == "query_condition":
                return "queryCondition"
            if original_name == "order":
                return "order"
            return original_name
        
        # 设备Key
        device_key: Optional[str] = None

        # 设备名
        device_name: Optional[str] = None

        # 设备类型（1:AGV 2:生产设备 3：非生产设备
        device_type: Optional[str] = None

        # 是否为brokerx接入设备
        is_brokerx_manager: Optional[bool] = None

        # 设备节点类型(1直连设备，2网关，3网关设备)
        node_type: Optional[int] = None

        # 正序倒序（DESC为降序，ASC为正序）
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 页码
        page_num: Optional[int] = None

        # 页尺寸
        page_size: Optional[int] = None

        # 父设备Key
        parent_device_key: Optional[str] = None

        # 产品key
        product_key: Optional[str] = None

        # 设备Key或者设备名、产品Key
        query_condition: Optional[str] = None

    
    @dataclass
    class DevicesRequestBuilderGetRequestConfiguration(RequestConfiguration[DevicesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class DevicesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

