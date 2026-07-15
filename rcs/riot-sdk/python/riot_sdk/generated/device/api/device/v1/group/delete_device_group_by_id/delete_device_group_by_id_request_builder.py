from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.delete_device_group_by_id_item_request_builder import DeleteDeviceGroupByIdItemRequestBuilder

class DeleteDeviceGroupByIdRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/group/deleteDeviceGroupById
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new DeleteDeviceGroupByIdRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/group/deleteDeviceGroupById", path_parameters)
    
    def by_id(self,id: int) -> DeleteDeviceGroupByIdItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.device.api.device.v1.group.deleteDeviceGroupById.item collection
        param id: id
        Returns: DeleteDeviceGroupByIdItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.delete_device_group_by_id_item_request_builder import DeleteDeviceGroupByIdItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return DeleteDeviceGroupByIdItemRequestBuilder(self.request_adapter, url_tpl_params)
    

