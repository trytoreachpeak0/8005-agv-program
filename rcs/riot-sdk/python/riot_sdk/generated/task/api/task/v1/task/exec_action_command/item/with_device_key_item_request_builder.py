from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_action_item_request_builder import WithActionItemRequestBuilder

class WithDeviceKeyItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/task/execActionCommand/{deviceKey}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithDeviceKeyItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/task/execActionCommand/{deviceKey}", path_parameters)
    
    def by_action_id(self,action_id: int) -> WithActionItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.task.execActionCommand.item.item collection
        param action_id: actionId
        Returns: WithActionItemRequestBuilder
        """
        if action_id is None:
            raise TypeError("action_id cannot be null.")
        from .item.with_action_item_request_builder import WithActionItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["actionId"] = action_id
        return WithActionItemRequestBuilder(self.request_adapter, url_tpl_params)
    

