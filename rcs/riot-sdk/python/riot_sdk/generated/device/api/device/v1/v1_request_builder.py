from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .command.command_request_builder import CommandRequestBuilder
    from .connect.connect_request_builder import ConnectRequestBuilder
    from .devices.devices_request_builder import DevicesRequestBuilder
    from .group.group_request_builder import GroupRequestBuilder
    from .runtime.runtime_request_builder import RuntimeRequestBuilder

class V1RequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new V1RequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1", path_parameters)
    
    @property
    def command(self) -> CommandRequestBuilder:
        """
        The command property
        """
        from .command.command_request_builder import CommandRequestBuilder

        return CommandRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def connect(self) -> ConnectRequestBuilder:
        """
        The connect property
        """
        from .connect.connect_request_builder import ConnectRequestBuilder

        return ConnectRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def devices(self) -> DevicesRequestBuilder:
        """
        The devices property
        """
        from .devices.devices_request_builder import DevicesRequestBuilder

        return DevicesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def group(self) -> GroupRequestBuilder:
        """
        The group property
        """
        from .group.group_request_builder import GroupRequestBuilder

        return GroupRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def runtime(self) -> RuntimeRequestBuilder:
        """
        The runtime property
        """
        from .runtime.runtime_request_builder import RuntimeRequestBuilder

        return RuntimeRequestBuilder(self.request_adapter, self.path_parameters)
    

