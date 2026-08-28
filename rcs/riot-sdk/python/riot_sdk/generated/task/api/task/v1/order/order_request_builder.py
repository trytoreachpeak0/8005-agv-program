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
    from .....models.order_d_t_o import OrderDTO
    from .....models.response_msg_of_void import ResponseMsg_Of_Void
    from .charge.charge_request_builder import ChargeRequestBuilder
    from .command.command_request_builder import CommandRequestBuilder
    from .current_map_exist_not_final_order_task.current_map_exist_not_final_order_task_request_builder import CurrentMapExistNotFinalOrderTaskRequestBuilder
    from .edit.edit_request_builder import EditRequestBuilder
    from .interrupt.interrupt_request_builder import InterruptRequestBuilder
    from .route.route_request_builder import RouteRequestBuilder

class OrderRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/order
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new OrderRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/order", path_parameters)
    
    async def post(self,body: OrderDTO, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_Void]:
        """
        创建订单
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_Void]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_void import ResponseMsg_Of_Void

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_Void, None)
    
    def to_post_request_information(self,body: OrderDTO, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        创建订单
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
    
    def with_url(self,raw_url: str) -> OrderRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: OrderRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return OrderRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def charge(self) -> ChargeRequestBuilder:
        """
        The charge property
        """
        from .charge.charge_request_builder import ChargeRequestBuilder

        return ChargeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def command(self) -> CommandRequestBuilder:
        """
        The command property
        """
        from .command.command_request_builder import CommandRequestBuilder

        return CommandRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def current_map_exist_not_final_order_task(self) -> CurrentMapExistNotFinalOrderTaskRequestBuilder:
        """
        The currentMapExistNotFinalOrderTask property
        """
        from .current_map_exist_not_final_order_task.current_map_exist_not_final_order_task_request_builder import CurrentMapExistNotFinalOrderTaskRequestBuilder

        return CurrentMapExistNotFinalOrderTaskRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def edit(self) -> EditRequestBuilder:
        """
        The edit property
        """
        from .edit.edit_request_builder import EditRequestBuilder

        return EditRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def interrupt(self) -> InterruptRequestBuilder:
        """
        The interrupt property
        """
        from .interrupt.interrupt_request_builder import InterruptRequestBuilder

        return InterruptRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def route(self) -> RouteRequestBuilder:
        """
        The route property
        """
        from .route.route_request_builder import RouteRequestBuilder

        return RouteRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class OrderRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

