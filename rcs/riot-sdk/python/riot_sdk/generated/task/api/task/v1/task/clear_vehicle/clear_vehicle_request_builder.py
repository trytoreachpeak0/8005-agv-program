from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_device_key_item_request_builder import WithDeviceKeyItemRequestBuilder

class ClearVehicleRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/task/clearVehicle
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ClearVehicleRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/task/clearVehicle", path_parameters)
    
    def by_device_key(self,device_key: str) -> WithDeviceKeyItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.task.clearVehicle.item collection
        param device_key: deviceKey
        Returns: WithDeviceKeyItemRequestBuilder
        """
        if device_key is None:
            raise TypeError("device_key cannot be null.")
        from .item.with_device_key_item_request_builder import WithDeviceKeyItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["deviceKey"] = device_key
        return WithDeviceKeyItemRequestBuilder(self.request_adapter, url_tpl_params)
    

