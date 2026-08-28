from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agv_log.agv_log_request_builder import AgvLogRequestBuilder
    from .charge_config.charge_config_request_builder import ChargeConfigRequestBuilder
    from .config.config_request_builder import ConfigRequestBuilder
    from .file.file_request_builder import FileRequestBuilder
    from .map.map_request_builder import MapRequestBuilder
    from .order.order_request_builder import OrderRequestBuilder
    from .park_config.park_config_request_builder import ParkConfigRequestBuilder
    from .route.route_request_builder import RouteRequestBuilder
    from .sros.sros_request_builder import SrosRequestBuilder
    from .statistics.statistics_request_builder import StatisticsRequestBuilder
    from .task.task_request_builder import TaskRequestBuilder
    from .traffic.traffic_request_builder import TrafficRequestBuilder
    from .vehicle_sync_task.vehicle_sync_task_request_builder import VehicleSyncTaskRequestBuilder

class V1RequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new V1RequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1", path_parameters)
    
    @property
    def agv_log(self) -> AgvLogRequestBuilder:
        """
        The agvLog property
        """
        from .agv_log.agv_log_request_builder import AgvLogRequestBuilder

        return AgvLogRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def charge_config(self) -> ChargeConfigRequestBuilder:
        """
        The chargeConfig property
        """
        from .charge_config.charge_config_request_builder import ChargeConfigRequestBuilder

        return ChargeConfigRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def config(self) -> ConfigRequestBuilder:
        """
        The config property
        """
        from .config.config_request_builder import ConfigRequestBuilder

        return ConfigRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def file(self) -> FileRequestBuilder:
        """
        The file property
        """
        from .file.file_request_builder import FileRequestBuilder

        return FileRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map(self) -> MapRequestBuilder:
        """
        The map property
        """
        from .map.map_request_builder import MapRequestBuilder

        return MapRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def order(self) -> OrderRequestBuilder:
        """
        The order property
        """
        from .order.order_request_builder import OrderRequestBuilder

        return OrderRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def park_config(self) -> ParkConfigRequestBuilder:
        """
        The parkConfig property
        """
        from .park_config.park_config_request_builder import ParkConfigRequestBuilder

        return ParkConfigRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def route(self) -> RouteRequestBuilder:
        """
        The route property
        """
        from .route.route_request_builder import RouteRequestBuilder

        return RouteRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sros(self) -> SrosRequestBuilder:
        """
        The sros property
        """
        from .sros.sros_request_builder import SrosRequestBuilder

        return SrosRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def statistics(self) -> StatisticsRequestBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_request_builder import StatisticsRequestBuilder

        return StatisticsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def task(self) -> TaskRequestBuilder:
        """
        The task property
        """
        from .task.task_request_builder import TaskRequestBuilder

        return TaskRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def traffic(self) -> TrafficRequestBuilder:
        """
        The traffic property
        """
        from .traffic.traffic_request_builder import TrafficRequestBuilder

        return TrafficRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def vehicle_sync_task(self) -> VehicleSyncTaskRequestBuilder:
        """
        The vehicleSyncTask property
        """
        from .vehicle_sync_task.vehicle_sync_task_request_builder import VehicleSyncTaskRequestBuilder

        return VehicleSyncTaskRequestBuilder(self.request_adapter, self.path_parameters)
    

