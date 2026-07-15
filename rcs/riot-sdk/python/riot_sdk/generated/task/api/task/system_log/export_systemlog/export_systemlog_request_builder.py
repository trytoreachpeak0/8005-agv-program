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
    from .....models.response_msg import ResponseMsg

class ExportSystemlogRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/systemLog/exportSystemlog
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ExportSystemlogRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/systemLog/exportSystemlog?endTimeDate={endTimeDate}&startTimeDate={startTimeDate}{&deviceName*,endLocalDateTime*,logLevel*,order*,orderBy*,orderId*,pageNum*,pageSize*,source*,startLocalDateTime*,status*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[ExportSystemlogRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg]:
        """
        分页导出消息记录
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg import ResponseMsg

        return await self.request_adapter.send_async(request_info, ResponseMsg, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[ExportSystemlogRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        分页导出消息记录
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> ExportSystemlogRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ExportSystemlogRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return ExportSystemlogRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ExportSystemlogRequestBuilderGetQueryParameters():
        """
        分页导出消息记录
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
            if original_name == "end_local_date_time":
                return "endLocalDateTime"
            if original_name == "end_time_date":
                return "endTimeDate"
            if original_name == "log_level":
                return "logLevel"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "order_id":
                return "orderId"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "start_local_date_time":
                return "startLocalDateTime"
            if original_name == "start_time_date":
                return "startTimeDate"
            if original_name == "order":
                return "order"
            if original_name == "source":
                return "source"
            if original_name == "status":
                return "status"
            return original_name
        
        # 车辆名称
        device_name: Optional[str] = None

        end_local_date_time: Optional[datetime.datetime] = None

        # 结束时间 yyyy-MM-dd HH:mm:ss
        end_time_date: Optional[str] = None

        # 日志级别
        log_level: Optional[int] = None

        # 正序倒序（DESC为降序，ASC为正序）
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 输入订单ID或订单名称
        order_id: Optional[str] = None

        page_num: Optional[int] = None

        page_size: Optional[int] = None

        # 告警类型
        source: Optional[int] = None

        start_local_date_time: Optional[datetime.datetime] = None

        # 开始时间 yyyy-MM-dd HH:mm:ss
        start_time_date: Optional[str] = None

        # 日志状态
        status: Optional[int] = None

    
    @dataclass
    class ExportSystemlogRequestBuilderGetRequestConfiguration(RequestConfiguration[ExportSystemlogRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

