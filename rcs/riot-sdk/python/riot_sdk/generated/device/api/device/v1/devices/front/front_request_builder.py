from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .front_query_device_properties.front_query_device_properties_request_builder import FrontQueryDevicePropertiesRequestBuilder

class FrontRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices/front
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new FrontRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices/front", path_parameters)
    
    @property
    def front_query_device_properties(self) -> FrontQueryDevicePropertiesRequestBuilder:
        """
        The frontQueryDeviceProperties property
        """
        from .front_query_device_properties.front_query_device_properties_request_builder import FrontQueryDevicePropertiesRequestBuilder

        return FrontQueryDevicePropertiesRequestBuilder(self.request_adapter, self.path_parameters)
    

