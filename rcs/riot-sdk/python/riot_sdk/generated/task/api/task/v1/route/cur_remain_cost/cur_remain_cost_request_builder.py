from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_order_key_item_request_builder import WithOrderKeyItemRequestBuilder

class CurRemainCostRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/route/curRemainCost
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new CurRemainCostRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/route/curRemainCost", path_parameters)
    
    def by_order_key(self,order_key: str) -> WithOrderKeyItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.route.curRemainCost.item collection
        param order_key: orderKey
        Returns: WithOrderKeyItemRequestBuilder
        """
        if order_key is None:
            raise TypeError("order_key cannot be null.")
        from .item.with_order_key_item_request_builder import WithOrderKeyItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["orderKey"] = order_key
        return WithOrderKeyItemRequestBuilder(self.request_adapter, url_tpl_params)
    

