from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .check_all.check_all_request_builder import CheckAllRequestBuilder
    from .check_result.check_result_request_builder import CheckResultRequestBuilder

class MapSyncStateRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapSyncState
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapSyncStateRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapSyncState", path_parameters)
    
    @property
    def check_all(self) -> CheckAllRequestBuilder:
        """
        The checkAll property
        """
        from .check_all.check_all_request_builder import CheckAllRequestBuilder

        return CheckAllRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def check_result(self) -> CheckResultRequestBuilder:
        """
        The checkResult property
        """
        from .check_result.check_result_request_builder import CheckResultRequestBuilder

        return CheckResultRequestBuilder(self.request_adapter, self.path_parameters)
    

