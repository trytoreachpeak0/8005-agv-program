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
    from .....models.custom_park_config_object import CustomParkConfigObject
    from .....models.response_msg_of_list_of_custom_park_config_object import ResponseMsg_Of_List_Of_CustomParkConfigObject
    from .....models.response_msg_of_void import ResponseMsg_Of_Void
    from .delete.delete_request_builder import DeleteRequestBuilder
    from .get_agv_group.get_agv_group_request_builder import GetAgvGroupRequestBuilder
    from .get_default_config.get_default_config_request_builder import GetDefaultConfigRequestBuilder
    from .item.park_config_item_request_builder import ParkConfigItemRequestBuilder

class ParkConfigRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/parkConfig
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ParkConfigRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/parkConfig", path_parameters)
    
    def by_id(self,id: int) -> ParkConfigItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.parkConfig.item collection
        param id: id
        Returns: ParkConfigItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.park_config_item_request_builder import ParkConfigItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return ParkConfigItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_List_Of_CustomParkConfigObject]:
        """
        查询配置列表
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ResponseMsg_Of_List_Of_CustomParkConfigObject]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.response_msg_of_list_of_custom_park_config_object import ResponseMsg_Of_List_Of_CustomParkConfigObject

        return await self.request_adapter.send_async(request_info, ResponseMsg_Of_List_Of_CustomParkConfigObject, None)
    
    async def post(self,body: CustomParkConfigObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[ResponseMsg_Of_Void]:
        """
        新增或者修改配置
        param body: 自定义停靠配置表
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
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        查询配置列表
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: CustomParkConfigObject, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        新增或者修改配置
        param body: 自定义停靠配置表
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
    
    def with_url(self,raw_url: str) -> ParkConfigRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ParkConfigRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return ParkConfigRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def delete_path(self) -> DeleteRequestBuilder:
        """
        The deletePath property
        """
        from .delete.delete_request_builder import DeleteRequestBuilder

        return DeleteRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_agv_group(self) -> GetAgvGroupRequestBuilder:
        """
        The getAgvGroup property
        """
        from .get_agv_group.get_agv_group_request_builder import GetAgvGroupRequestBuilder

        return GetAgvGroupRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_default_config(self) -> GetDefaultConfigRequestBuilder:
        """
        The getDefaultConfig property
        """
        from .get_default_config.get_default_config_request_builder import GetDefaultConfigRequestBuilder

        return GetDefaultConfigRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class ParkConfigRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class ParkConfigRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

