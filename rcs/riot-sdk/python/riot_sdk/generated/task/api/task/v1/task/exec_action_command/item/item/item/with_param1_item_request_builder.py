from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_param2_item_request_builder import WithParam2ItemRequestBuilder

class WithParam1ItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/task/execActionCommand/{deviceKey}/{actionId}/{param1}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithParam1ItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/task/execActionCommand/{deviceKey}/{actionId}/{param1}", path_parameters)
    
    def by_param2(self,param2: int) -> WithParam2ItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.task.execActionCommand.item.item.item.item collection
        param param2: param2
        Returns: WithParam2ItemRequestBuilder
        """
        if param2 is None:
            raise TypeError("param2 cannot be null.")
        from .item.with_param2_item_request_builder import WithParam2ItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["param2"] = param2
        return WithParam2ItemRequestBuilder(self.request_adapter, url_tpl_params)
    

