from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .all_traffic_resource.all_traffic_resource_request_builder import AllTrafficResourceRequestBuilder
    from .all_traffic_resource_detail.all_traffic_resource_detail_request_builder import AllTrafficResourceDetailRequestBuilder
    from .applied_resource.applied_resource_request_builder import AppliedResourceRequestBuilder
    from .check_fail_detail.check_fail_detail_request_builder import CheckFailDetailRequestBuilder
    from .dump.dump_request_builder import DumpRequestBuilder
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .item.with_vehicle_key_item_request_builder import WithVehicleKeyItemRequestBuilder
    from .locked_resource.locked_resource_request_builder import LockedResourceRequestBuilder

class TrafficRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/traffic
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new TrafficRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/traffic", path_parameters)
    
    def by_vehicle_key(self,vehicle_key: str) -> WithVehicleKeyItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.task.api.task.v1.traffic.item collection
        param vehicle_key: 车的key
        Returns: WithVehicleKeyItemRequestBuilder
        """
        if vehicle_key is None:
            raise TypeError("vehicle_key cannot be null.")
        from .item.with_vehicle_key_item_request_builder import WithVehicleKeyItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["vehicleKey"] = vehicle_key
        return WithVehicleKeyItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def all_traffic_resource(self) -> AllTrafficResourceRequestBuilder:
        """
        The allTrafficResource property
        """
        from .all_traffic_resource.all_traffic_resource_request_builder import AllTrafficResourceRequestBuilder

        return AllTrafficResourceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def all_traffic_resource_detail(self) -> AllTrafficResourceDetailRequestBuilder:
        """
        The allTrafficResourceDetail property
        """
        from .all_traffic_resource_detail.all_traffic_resource_detail_request_builder import AllTrafficResourceDetailRequestBuilder

        return AllTrafficResourceDetailRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def applied_resource(self) -> AppliedResourceRequestBuilder:
        """
        The appliedResource property
        """
        from .applied_resource.applied_resource_request_builder import AppliedResourceRequestBuilder

        return AppliedResourceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def check_fail_detail(self) -> CheckFailDetailRequestBuilder:
        """
        The checkFailDetail property
        """
        from .check_fail_detail.check_fail_detail_request_builder import CheckFailDetailRequestBuilder

        return CheckFailDetailRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def dump(self) -> DumpRequestBuilder:
        """
        The dump property
        """
        from .dump.dump_request_builder import DumpRequestBuilder

        return DumpRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def locked_resource(self) -> LockedResourceRequestBuilder:
        """
        The lockedResource property
        """
        from .locked_resource.locked_resource_request_builder import LockedResourceRequestBuilder

        return LockedResourceRequestBuilder(self.request_adapter, self.path_parameters)
    

