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
    from ......models.response_msg_of_page_of_rep_device import ResponseMsg_Of_Page_Of_RepDevice

class QueryDevicesPropertiesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices/queryDevicesProperties
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new QueryDevicesPropertiesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices/queryDevicesProperties{?deviceName*,deviceType*,groupIds*,groupName*,isThingTextuality*,order*,orderBy*,pageNum*,pageSize*,productKey*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryDevicesPropertiesRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_RepDevice]:
        """
        queryDevicesProperties
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_RepDevice]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.response_msg_of_page_of_rep_device import ResponseMsg_Of_Page_Of_RepDevice

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_RepDevice, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryDevicesPropertiesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        queryDevicesProperties
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> QueryDevicesPropertiesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: QueryDevicesPropertiesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return QueryDevicesPropertiesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class QueryDevicesPropertiesRequestBuilderGetQueryParameters():
        """
        queryDevicesProperties
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "device_name":
                return "deviceName"
            if original_name == "device_type":
                return "deviceType"
            if original_name == "group_ids":
                return "groupIds"
            if original_name == "group_name":
                return "groupName"
            if original_name == "is_thing_textuality":
                return "isThingTextuality"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "product_key":
                return "productKey"
            if original_name == "order":
                return "order"
            return original_name
        
        # 设备名称
        device_name: Optional[str] = None

        # 产品类型
        device_type: Optional[str] = None

        # 组id
        group_ids: Optional[str] = None

        # 设备组名称
        group_name: Optional[str] = None

        # 物模型数据可视化
        is_thing_textuality: Optional[bool] = None

        # 正序倒序（desc为降序，asc为正序）
        order: Optional[str] = None

        # 排序字段
        order_by: Optional[str] = None

        # 页码
        page_num: Optional[int] = None

        # 页尺寸
        page_size: Optional[int] = None

        # 产品前缀
        product_key: Optional[str] = None

    
    @dataclass
    class QueryDevicesPropertiesRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryDevicesPropertiesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

