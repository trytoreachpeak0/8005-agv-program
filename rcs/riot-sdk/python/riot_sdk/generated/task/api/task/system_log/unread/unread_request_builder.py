from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.unread_item_request_builder import UnreadItemRequestBuilder

class UnreadRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/systemLog/unread
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new UnreadRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/systemLog/unread", path_parameters)
    
    def by_id(self,id: int) -> UnreadItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.systemLog.unread.item collection
        param id: 日志id
        Returns: UnreadItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.unread_item_request_builder import UnreadItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return UnreadItemRequestBuilder(self.request_adapter, url_tpl_params)
    

