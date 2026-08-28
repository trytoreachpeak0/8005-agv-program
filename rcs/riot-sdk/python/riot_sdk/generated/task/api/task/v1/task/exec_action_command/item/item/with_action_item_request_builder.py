from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_param1_item_request_builder import WithParam1ItemRequestBuilder

class WithActionItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/task/execActionCommand/{deviceKey}/{actionId}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithActionItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/task/execActionCommand/{deviceKey}/{actionId}", path_parameters)
    
    def by_param1(self,param1: int) -> WithParam1ItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.task.execActionCommand.item.item.item collection
        param param1: param1
        Returns: WithParam1ItemRequestBuilder
        """
        if param1 is None:
            raise TypeError("param1 cannot be null.")
        from .item.with_param1_item_request_builder import WithParam1ItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["param1"] = param1
        return WithParam1ItemRequestBuilder(self.request_adapter, url_tpl_params)
    

