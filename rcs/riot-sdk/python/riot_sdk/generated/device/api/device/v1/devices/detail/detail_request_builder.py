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
    from ......models.device_dto import DeviceDto
    from ......models.response_msg_of_page_of_device_dto import ResponseMsg_Of_Page_Of_DeviceDto

class DetailRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices/detail
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DetailRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices/detail{?deviceKey*,deviceName*,deviceType*,isBrokerxManager*,nodeType*,pageNum*,pageSize*,parentDeviceKey*,productKey*,queryCondition*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[DetailRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_DeviceDto]:
        """
        getDevicesDetail
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_DeviceDto]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.response_msg_of_page_of_device_dto import ResponseMsg_Of_Page_Of_DeviceDto

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_DeviceDto, None)
    
    async def post(self,body: DeviceDto, request_configuration: Optional[RequestConfiguration[DetailRequestBuilderPostQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_DeviceDto]:
        """
        getDevicesDetail
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_DeviceDto]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.response_msg_of_page_of_device_dto import ResponseMsg_Of_Page_Of_DeviceDto

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_DeviceDto, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[DetailRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        getDevicesDetail
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: DeviceDto, request_configuration: Optional[RequestConfiguration[DetailRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        getDevicesDetail
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
    
    def with_url(self,raw_url: str) -> DetailRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DetailRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return DetailRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class DetailRequestBuilderGetQueryParameters():
        """
        getDevicesDetail
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
    class DetailRequestBuilderGetRequestConfiguration(RequestConfiguration[DetailRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class DetailRequestBuilderPostQueryParameters():
        """
        getDevicesDetail
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            return original_name
        
        # pageNum
        page_num: Optional[int] = None

        # pageSize
        page_size: Optional[int] = None

    
    @dataclass
    class DetailRequestBuilderPostRequestConfiguration(RequestConfiguration[DetailRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

