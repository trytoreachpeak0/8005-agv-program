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

class ExportOrderRecordRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1/orderRecord/exportOrderRecord
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ExportOrderRecordRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1/orderRecord/exportOrderRecord?pageNum={pageNum}&pageSize={pageSize}{&endStationName*,endStationNo*,endTime*,executeVehicleKey*,executeVehicleName*,filterBySource*,filterByState,order*,orderBy*,orderType,query*,startStationName*,startStationNo*,startTime*,userId*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[ExportOrderRecordRequestBuilderGetQueryParameters]] = None) -> Optional[bytes]:
        """
        分页导出订单记录
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[ExportOrderRecordRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        分页导出订单记录
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        return request_info
    
    def with_url(self,raw_url: str) -> ExportOrderRecordRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ExportOrderRecordRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return ExportOrderRecordRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ExportOrderRecordRequestBuilderGetQueryParameters():
        """
        分页导出订单记录
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "end_station_name":
                return "endStationName"
            if original_name == "end_station_no":
                return "endStationNo"
            if original_name == "end_time":
                return "endTime"
            if original_name == "execute_vehicle_key":
                return "executeVehicleKey"
            if original_name == "execute_vehicle_name":
                return "executeVehicleName"
            if original_name == "filter_by_source":
                return "filterBySource"
            if original_name == "filter_by_state":
                return "filterByState"
            if original_name == "order_by":
                return "orderBy"
            if original_name == "order_type":
                return "orderType"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "start_station_name":
                return "startStationName"
            if original_name == "start_station_no":
                return "startStationNo"
            if original_name == "start_time":
                return "startTime"
            if original_name == "user_id":
                return "userId"
            if original_name == "order":
                return "order"
            if original_name == "query":
                return "query"
            return original_name
        
        # 终点名称
        end_station_name: Optional[str] = None

        # 终点编号
        end_station_no: Optional[int] = None

        # 订单执行时间查-结束  yyyy-MM-dd HH:mm:ss
        end_time: Optional[str] = None

        # 执行的车辆id：
        execute_vehicle_key: Optional[str] = None

        # 执行的车辆名
        execute_vehicle_name: Optional[str] = None

        # 订单来源过滤器：1:WMS；2:FMS；
        filter_by_source: Optional[str] = None

        # 订单状态过滤器： 1 QUEUEING 队列中 , 2 CANCELLED 已取消, 3 EXECUTING 执行中, 4 FAILED 已失败, 5 SUCCESS 已完成, 6 DELETED  已移除, 7 PAUSED已暂停 ,8 SUSPENDED 已移除，9 HEAD 挂起, 10 队列优先执行
        filter_by_state: Optional[list[str]] = None

        # 正序倒序（DESC为降序，ASC为正序）
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 订单类型 1 NORMAL 工作订单, 2 CHARGE 充电订单 , 3 CMD 停靠订单 4 MAINTAIN 电池保养
        order_type: Optional[list[str]] = None

        # 页码
        page_num: Optional[int] = None

        # 页大小
        page_size: Optional[int] = None

        # 输入订单ID或订单名称
        query: Optional[str] = None

        # 订单起点名称
        start_station_name: Optional[str] = None

        # 订单起点编号
        start_station_no: Optional[int] = None

        # 订单执行时间查询-开始  yyyy-MM-dd HH:mm:ss
        start_time: Optional[str] = None

        # 用户id
        user_id: Optional[int] = None

    
    @dataclass
    class ExportOrderRecordRequestBuilderGetRequestConfiguration(RequestConfiguration[ExportOrderRecordRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

