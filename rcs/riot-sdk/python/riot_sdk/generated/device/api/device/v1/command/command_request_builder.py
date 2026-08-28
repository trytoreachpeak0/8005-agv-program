from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .batch_service_set.batch_service_set_request_builder import BatchServiceSetRequestBuilder
    from .properties.properties_request_builder import PropertiesRequestBuilder
    from .receive.receive_request_builder import ReceiveRequestBuilder
    from .service.service_request_builder import ServiceRequestBuilder
    from .sync.sync_request_builder import SyncRequestBuilder

class CommandRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/command
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new CommandRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/command", path_parameters)
    
    @property
    def batch_service_set(self) -> BatchServiceSetRequestBuilder:
        """
        The batchServiceSet property
        """
        from .batch_service_set.batch_service_set_request_builder import BatchServiceSetRequestBuilder

        return BatchServiceSetRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def properties(self) -> PropertiesRequestBuilder:
        """
        The properties property
        """
        from .properties.properties_request_builder import PropertiesRequestBuilder

        return PropertiesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def receive(self) -> ReceiveRequestBuilder:
        """
        The receive property
        """
        from .receive.receive_request_builder import ReceiveRequestBuilder

        return ReceiveRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def service(self) -> ServiceRequestBuilder:
        """
        The service property
        """
        from .service.service_request_builder import ServiceRequestBuilder

        return ServiceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sync(self) -> SyncRequestBuilder:
        """
        The sync property
        """
        from .sync.sync_request_builder import SyncRequestBuilder

        return SyncRequestBuilder(self.request_adapter, self.path_parameters)
    

