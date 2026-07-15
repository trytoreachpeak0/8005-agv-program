from __future__ import annotations
import datetime
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
    from .....models.response_msg_of_page_of_system_log_object import ResponseMsg_Of_Page_Of_SystemLogObject

class PageRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/systemLog/page
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new PageRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/systemLog/page{?desc*,endDate*,id*,logLevel*,order*,orderId*,pageNum*,pageSize*,source*,startDate*,status*}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration[PageRequestBuilderPostQueryParameters]] = None) -> Optional[ResponseMsg_Of_Page_Of_SystemLogObject]:
        """
        分页查询系统日志
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Page_Of_SystemLogObject]
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_page_of_system_log_object import ResponseMsg_Of_Page_Of_SystemLogObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Page_Of_SystemLogObject, None)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration[PageRequestBuilderPostQueryParameters]] = None) -> RequestInformation:
        """
        分页查询系统日志
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> PageRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: PageRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return PageRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class PageRequestBuilderPostQueryParameters():
        """
        分页查询系统日志
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "end_date":
                return "endDate"
            if original_name == "log_level":
                return "logLevel"
            if original_name == "order_id":
                return "orderId"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "start_date":
                return "startDate"
            if original_name == "desc":
                return "desc"
            if original_name == "id":
                return "id"
            if original_name == "order":
                return "order"
            if original_name == "source":
                return "source"
            if original_name == "status":
                return "status"
            return original_name
        
        desc: Optional[bool] = None

        end_date: Optional[datetime.datetime] = None

        id: Optional[int] = None

        log_level: Optional[int] = None

        order: Optional[str] = None

        order_id: Optional[str] = None

        # pageNum
        page_num: Optional[int] = None

        # pageSize
        page_size: Optional[int] = None

        source: Optional[int] = None

        start_date: Optional[datetime.datetime] = None

        status: Optional[int] = None

    
    @dataclass
    class PageRequestBuilderPostRequestConfiguration(RequestConfiguration[PageRequestBuilderPostQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

