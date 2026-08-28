from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .charge_count.charge_count_request_builder import ChargeCountRequestBuilder
    from .charge_location_count.charge_location_count_request_builder import ChargeLocationCountRequestBuilder
    from .exception_statistics.exception_statistics_request_builder import ExceptionStatisticsRequestBuilder
    from .exception_statistics_by_duty.exception_statistics_by_duty_request_builder import ExceptionStatisticsByDutyRequestBuilder
    from .mileage_battery.mileage_battery_request_builder import MileageBatteryRequestBuilder
    from .mileage_battery_by_condition.mileage_battery_by_condition_request_builder import MileageBatteryByConditionRequestBuilder
    from .page_query_state_durations_by_update_time.page_query_state_durations_by_update_time_request_builder import PageQueryStateDurationsByUpdateTimeRequestBuilder
    from .state_count.state_count_request_builder import StateCountRequestBuilder
    from .state_durations.state_durations_request_builder import StateDurationsRequestBuilder

class StatisticsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/statistics
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new StatisticsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/statistics", path_parameters)
    
    @property
    def charge_count(self) -> ChargeCountRequestBuilder:
        """
        The chargeCount property
        """
        from .charge_count.charge_count_request_builder import ChargeCountRequestBuilder

        return ChargeCountRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def charge_location_count(self) -> ChargeLocationCountRequestBuilder:
        """
        The chargeLocationCount property
        """
        from .charge_location_count.charge_location_count_request_builder import ChargeLocationCountRequestBuilder

        return ChargeLocationCountRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def exception_statistics(self) -> ExceptionStatisticsRequestBuilder:
        """
        The exceptionStatistics property
        """
        from .exception_statistics.exception_statistics_request_builder import ExceptionStatisticsRequestBuilder

        return ExceptionStatisticsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def exception_statistics_by_duty(self) -> ExceptionStatisticsByDutyRequestBuilder:
        """
        The exceptionStatisticsByDuty property
        """
        from .exception_statistics_by_duty.exception_statistics_by_duty_request_builder import ExceptionStatisticsByDutyRequestBuilder

        return ExceptionStatisticsByDutyRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def mileage_battery(self) -> MileageBatteryRequestBuilder:
        """
        The mileageBattery property
        """
        from .mileage_battery.mileage_battery_request_builder import MileageBatteryRequestBuilder

        return MileageBatteryRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def mileage_battery_by_condition(self) -> MileageBatteryByConditionRequestBuilder:
        """
        The mileageBatteryByCondition property
        """
        from .mileage_battery_by_condition.mileage_battery_by_condition_request_builder import MileageBatteryByConditionRequestBuilder

        return MileageBatteryByConditionRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def page_query_state_durations_by_update_time(self) -> PageQueryStateDurationsByUpdateTimeRequestBuilder:
        """
        The pageQueryStateDurationsByUpdateTime property
        """
        from .page_query_state_durations_by_update_time.page_query_state_durations_by_update_time_request_builder import PageQueryStateDurationsByUpdateTimeRequestBuilder

        return PageQueryStateDurationsByUpdateTimeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def state_count(self) -> StateCountRequestBuilder:
        """
        The stateCount property
        """
        from .state_count.state_count_request_builder import StateCountRequestBuilder

        return StateCountRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def state_durations(self) -> StateDurationsRequestBuilder:
        """
        The stateDurations property
        """
        from .state_durations.state_durations_request_builder import StateDurationsRequestBuilder

        return StateDurationsRequestBuilder(self.request_adapter, self.path_parameters)
    

