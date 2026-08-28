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
    from .....models.response_msg_of_page_of_map_sync_record_object import ResponseMsg_Of_Page_Of_MapSyncRecordObject
    from .get_map_sync_type_query_parameter_type import GetMapSyncTypeQueryParameterType

class EmptyPathSegmentRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapSyncRecord/
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new EmptyPathSegmentRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapSyncRecord/{?keyword*,mapSyncSource*,mapSyncType*,order*,orderBy*,pageNum*,pageSize*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[EmptyPathSegmentRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_MapSyncRecordObject]:
        """
        查询地图同步信息
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_MapSyncRecordObject]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_page_of_map_sync_record_object import ResponseMsg_Of_Page_Of_MapSyncRecordObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_MapSyncRecordObject, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[EmptyPathSegmentRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        查询地图同步信息
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> EmptyPathSegmentRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: EmptyPathSegmentRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return EmptyPathSegmentRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class EmptyPathSegmentRequestBuilderGetQueryParameters():
        """
        查询地图同步信息
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "map_sync_source":
                return "mapSyncSource"
            if original_name == "map_sync_type":
                return "mapSyncType"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "keyword":
                return "keyword"
            if original_name == "order":
                return "order"
            return original_name
        
        # 搜索关键词
        keyword: Optional[str] = None

        # 同步来源
        map_sync_source: Optional[str] = None

        # 同步类型
        map_sync_type: Optional[GetMapSyncTypeQueryParameterType] = None

        # 正序倒序（DESC为降序，ASC为正序）
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 页码
        page_num: Optional[int] = None

        # 页尺寸
        page_size: Optional[int] = None

    
    @dataclass
    class EmptyPathSegmentRequestBuilderGetRequestConfiguration(RequestConfiguration[EmptyPathSegmentRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

