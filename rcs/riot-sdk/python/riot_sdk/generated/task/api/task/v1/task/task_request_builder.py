from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .clear_all_vehicle.clear_all_vehicle_request_builder import ClearAllVehicleRequestBuilder
    from .clear_order_sequence.clear_order_sequence_request_builder import ClearOrderSequenceRequestBuilder
    from .clear_vehicle.clear_vehicle_request_builder import ClearVehicleRequestBuilder
    from .clear_vehicle_and_cancel_order_task.clear_vehicle_and_cancel_order_task_request_builder import ClearVehicleAndCancelOrderTaskRequestBuilder
    from .exec_action_command.exec_action_command_request_builder import ExecActionCommandRequestBuilder
    from .get_vehicle_info.get_vehicle_info_request_builder import GetVehicleInfoRequestBuilder
    from .test_play.test_play_request_builder import TestPlayRequestBuilder

class TaskRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/task
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new TaskRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/task", path_parameters)
    
    @property
    def clear_all_vehicle(self) -> ClearAllVehicleRequestBuilder:
        """
        The clearAllVehicle property
        """
        from .clear_all_vehicle.clear_all_vehicle_request_builder import ClearAllVehicleRequestBuilder

        return ClearAllVehicleRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def clear_order_sequence(self) -> ClearOrderSequenceRequestBuilder:
        """
        The clearOrderSequence property
        """
        from .clear_order_sequence.clear_order_sequence_request_builder import ClearOrderSequenceRequestBuilder

        return ClearOrderSequenceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def clear_vehicle(self) -> ClearVehicleRequestBuilder:
        """
        The clearVehicle property
        """
        from .clear_vehicle.clear_vehicle_request_builder import ClearVehicleRequestBuilder

        return ClearVehicleRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def clear_vehicle_and_cancel_order_task(self) -> ClearVehicleAndCancelOrderTaskRequestBuilder:
        """
        The clearVehicleAndCancelOrderTask property
        """
        from .clear_vehicle_and_cancel_order_task.clear_vehicle_and_cancel_order_task_request_builder import ClearVehicleAndCancelOrderTaskRequestBuilder

        return ClearVehicleAndCancelOrderTaskRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def exec_action_command(self) -> ExecActionCommandRequestBuilder:
        """
        The execActionCommand property
        """
        from .exec_action_command.exec_action_command_request_builder import ExecActionCommandRequestBuilder

        return ExecActionCommandRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_vehicle_info(self) -> GetVehicleInfoRequestBuilder:
        """
        The getVehicleInfo property
        """
        from .get_vehicle_info.get_vehicle_info_request_builder import GetVehicleInfoRequestBuilder

        return GetVehicleInfoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def test_play(self) -> TestPlayRequestBuilder:
        """
        The testPlay property
        """
        from .test_play.test_play_request_builder import TestPlayRequestBuilder

        return TestPlayRequestBuilder(self.request_adapter, self.path_parameters)
    

