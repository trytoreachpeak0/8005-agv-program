from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .cur_remain_cost.cur_remain_cost_request_builder import CurRemainCostRequestBuilder
    from .dynamic_route_cost.dynamic_route_cost_request_builder import DynamicRouteCostRequestBuilder
    from .dynamic_route_cost_by_vehicle.dynamic_route_cost_by_vehicle_request_builder import DynamicRouteCostByVehicleRequestBuilder
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .get_cost_unit.get_cost_unit_request_builder import GetCostUnitRequestBuilder
    from .get_route_costs_by.get_route_costs_by_request_builder import GetRouteCostsByRequestBuilder
    from .query_nearest_start.query_nearest_start_request_builder import QueryNearestStartRequestBuilder
    from .query_near_end.query_near_end_request_builder import QueryNearEndRequestBuilder

class RouteRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/route
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new RouteRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/route", path_parameters)
    
    @property
    def cur_remain_cost(self) -> CurRemainCostRequestBuilder:
        """
        The curRemainCost property
        """
        from .cur_remain_cost.cur_remain_cost_request_builder import CurRemainCostRequestBuilder

        return CurRemainCostRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def dynamic_route_cost(self) -> DynamicRouteCostRequestBuilder:
        """
        The dynamicRouteCost property
        """
        from .dynamic_route_cost.dynamic_route_cost_request_builder import DynamicRouteCostRequestBuilder

        return DynamicRouteCostRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def dynamic_route_cost_by_vehicle(self) -> DynamicRouteCostByVehicleRequestBuilder:
        """
        The dynamicRouteCostByVehicle property
        """
        from .dynamic_route_cost_by_vehicle.dynamic_route_cost_by_vehicle_request_builder import DynamicRouteCostByVehicleRequestBuilder

        return DynamicRouteCostByVehicleRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_cost_unit(self) -> GetCostUnitRequestBuilder:
        """
        The getCostUnit property
        """
        from .get_cost_unit.get_cost_unit_request_builder import GetCostUnitRequestBuilder

        return GetCostUnitRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_route_costs_by(self) -> GetRouteCostsByRequestBuilder:
        """
        The getRouteCostsBy property
        """
        from .get_route_costs_by.get_route_costs_by_request_builder import GetRouteCostsByRequestBuilder

        return GetRouteCostsByRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_near_end(self) -> QueryNearEndRequestBuilder:
        """
        The queryNearEnd property
        """
        from .query_near_end.query_near_end_request_builder import QueryNearEndRequestBuilder

        return QueryNearEndRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_nearest_start(self) -> QueryNearestStartRequestBuilder:
        """
        The queryNearestStart property
        """
        from .query_nearest_start.query_nearest_start_request_builder import QueryNearestStartRequestBuilder

        return QueryNearestStartRequestBuilder(self.request_adapter, self.path_parameters)
    

