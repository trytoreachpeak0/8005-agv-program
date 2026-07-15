from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.delete_item_request_builder import DeleteItemRequestBuilder

class DeleteRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/chargeConfig/delete
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DeleteRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/chargeConfig/delete", path_parameters)
    
    def by_id(self,id: int) -> DeleteItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.chargeConfig.delete.item collection
        param id: id
        Returns: DeleteItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.delete_item_request_builder import DeleteItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return DeleteItemRequestBuilder(self.request_adapter, url_tpl_params)
    

