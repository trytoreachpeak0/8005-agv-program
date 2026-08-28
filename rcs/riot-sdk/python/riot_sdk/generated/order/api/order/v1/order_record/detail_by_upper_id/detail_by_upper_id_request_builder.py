from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_upper_item_request_builder import WithUpperItemRequestBuilder

class DetailByUpperIdRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1/orderRecord/detailByUpperId
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DetailByUpperIdRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1/orderRecord/detailByUpperId", path_parameters)
    
    def by_upper_id(self,upper_id: str) -> WithUpperItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.order.api.order.v1.orderRecord.detailByUpperId.item collection
        param upper_id: upperId
        Returns: WithUpperItemRequestBuilder
        """
        if upper_id is None:
            raise TypeError("upper_id cannot be null.")
        from .item.with_upper_item_request_builder import WithUpperItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["upperId"] = upper_id
        return WithUpperItemRequestBuilder(self.request_adapter, url_tpl_params)
    

