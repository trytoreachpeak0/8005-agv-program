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
    from ......models.response_msg_of_page_of_device_group_dto import ResponseMsg_Of_Page_Of_DeviceGroupDto

class QueryDevicesGroupsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/group/queryDevicesGroups
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new QueryDevicesGroupsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/group/queryDevicesGroups{?groupName*,order*,orderBy*,pageNum*,pageSize*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryDevicesGroupsRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_DeviceGroupDto]:
        """
        queryDevicesGroups
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_DeviceGroupDto]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.response_msg_of_page_of_device_group_dto import ResponseMsg_Of_Page_Of_DeviceGroupDto

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_DeviceGroupDto, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryDevicesGroupsRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        queryDevicesGroups
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> QueryDevicesGroupsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: QueryDevicesGroupsRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return QueryDevicesGroupsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class QueryDevicesGroupsRequestBuilderGetQueryParameters():
        """
        queryDevicesGroups
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
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
        
        # 机器人组名称
        group_name: Optional[str] = None

        # 正序倒序（DESC为降序，ASC为正序）
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 页码
        page_num: Optional[int] = None

        # 页尺寸
        page_size: Optional[int] = None

    
    @dataclass
    class QueryDevicesGroupsRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryDevicesGroupsRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

