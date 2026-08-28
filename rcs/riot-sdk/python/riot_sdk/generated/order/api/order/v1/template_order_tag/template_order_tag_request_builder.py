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
    from .....models.response_msg_of_template_order_tag_object import ResponseMsg_Of_TemplateOrderTagObject
    from .....models.response_msg_of_template_order_tag_page_v_o_object import ResponseMsg_Of_TemplateOrderTagPageVOObject
    from .....models.template_order_tag_v_o_object import TemplateOrderTagVOObject
    from .item.template_order_tag_item_request_builder import TemplateOrderTagItemRequestBuilder
    from .list_.list_request_builder import ListRequestBuilder

class TemplateOrderTagRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1/templateOrderTag
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new TemplateOrderTagRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1/templateOrderTag{?order*,orderBy*,pageNum*,pageSize*,query*}", path_parameters)
    
    def by_id(self,id: int) -> TemplateOrderTagItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.order.api.order.v1.templateOrderTag.item collection
        param id: id
        Returns: TemplateOrderTagItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.template_order_tag_item_request_builder import TemplateOrderTagItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return TemplateOrderTagItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[TemplateOrderTagRequestBuilderGetQueryParameters]] = None) -> Optional[ResponseMsg_Of_TemplateOrderTagPageVOObject]:
        """
        查询订单模板标签列表
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_TemplateOrderTagPageVOObject]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_template_order_tag_page_v_o_object import ResponseMsg_Of_TemplateOrderTagPageVOObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_TemplateOrderTagPageVOObject, None)
    
    async def post(self,body: TemplateOrderTagVOObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_TemplateOrderTagObject]:
        """
        新增订单模板标签
        param body: 订单模板标签参数接收类
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_TemplateOrderTagObject]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_template_order_tag_object import ResponseMsg_Of_TemplateOrderTagObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_TemplateOrderTagObject, None)
    
    async def put(self,body: TemplateOrderTagVOObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_TemplateOrderTagObject]:
        """
        编辑订单模板标签
        param body: 订单模板标签参数接收类
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_TemplateOrderTagObject]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_template_order_tag_object import ResponseMsg_Of_TemplateOrderTagObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_TemplateOrderTagObject, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[TemplateOrderTagRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        查询订单模板标签列表
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: TemplateOrderTagVOObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        新增订单模板标签
        param body: 订单模板标签参数接收类
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
    
    def to_put_request_information(self,body: TemplateOrderTagVOObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        编辑订单模板标签
        param body: 订单模板标签参数接收类
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.PUT, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> TemplateOrderTagRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: TemplateOrderTagRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return TemplateOrderTagRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def list_(self) -> ListRequestBuilder:
        """
        The list property
        """
        from .list_.list_request_builder import ListRequestBuilder

        return ListRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class TemplateOrderTagRequestBuilderGetQueryParameters():
        """
        查询订单模板标签列表
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "order_by":
                return "orderBy"
            if original_name == "page_num":
                return "pageNum"
            if original_name == "page_size":
                return "pageSize"
            if original_name == "order":
                return "order"
            if original_name == "query":
                return "query"
            return original_name
        
        # 正序倒序(DESC为降序,ASC为正序)
        order: Optional[str] = None

        # 排序的列名
        order_by: Optional[str] = None

        # 页码(默认:1)
        page_num: Optional[int] = None

        # 页尺寸(默认:10)
        page_size: Optional[int] = None

        # 查询条件
        query: Optional[str] = None

    
    @dataclass
    class TemplateOrderTagRequestBuilderGetRequestConfiguration(RequestConfiguration[TemplateOrderTagRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class TemplateOrderTagRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class TemplateOrderTagRequestBuilderPutRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

