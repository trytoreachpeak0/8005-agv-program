from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_parent_device_key_item_request_builder import WithParentDeviceKeyItemRequestBuilder

class BindRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices/bind
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new BindRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices/bind", path_parameters)
    
    def by_parent_device_key(self,parent_device_key: str) -> WithParentDeviceKeyItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.device.api.device.v1.devices.bind.item collection
        param parent_device_key: parentDeviceKey
        Returns: WithParentDeviceKeyItemRequestBuilder
        """
        if parent_device_key is None:
            raise TypeError("parent_device_key cannot be null.")
        from .item.with_parent_device_key_item_request_builder import WithParentDeviceKeyItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["parentDeviceKey"] = parent_device_key
        return WithParentDeviceKeyItemRequestBuilder(self.request_adapter, url_tpl_params)
    

