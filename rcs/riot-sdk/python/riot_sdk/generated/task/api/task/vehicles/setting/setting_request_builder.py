from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .get.get_request_builder import GetRequestBuilder
    from .update.update_request_builder import UpdateRequestBuilder

class SettingRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/vehicles/setting
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SettingRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/vehicles/setting", path_parameters)
    
    @property
    def get_path(self) -> GetRequestBuilder:
        """
        The getPath property
        """
        from .get.get_request_builder import GetRequestBuilder

        return GetRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def update(self) -> UpdateRequestBuilder:
        """
        The update property
        """
        from .update.update_request_builder import UpdateRequestBuilder

        return UpdateRequestBuilder(self.request_adapter, self.path_parameters)
    

