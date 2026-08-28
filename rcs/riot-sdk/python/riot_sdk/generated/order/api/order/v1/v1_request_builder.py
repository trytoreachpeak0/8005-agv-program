from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .add.add_request_builder import AddRequestBuilder
    from .operate.operate_request_builder import OperateRequestBuilder
    from .order_group.order_group_request_builder import OrderGroupRequestBuilder
    from .order_record.order_record_request_builder import OrderRecordRequestBuilder
    from .order_record_change_vehicle.order_record_change_vehicle_request_builder import OrderRecordChangeVehicleRequestBuilder
    from .order_record_priority_exec.order_record_priority_exec_request_builder import OrderRecordPriorityExecRequestBuilder
    from .template_action.template_action_request_builder import TemplateActionRequestBuilder
    from .template_order.template_order_request_builder import TemplateOrderRequestBuilder
    from .template_order_tag.template_order_tag_request_builder import TemplateOrderTagRequestBuilder
    from .update_order_task.update_order_task_request_builder import UpdateOrderTaskRequestBuilder

class V1RequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new V1RequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1", path_parameters)
    
    @property
    def add(self) -> AddRequestBuilder:
        """
        The add property
        """
        from .add.add_request_builder import AddRequestBuilder

        return AddRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def operate(self) -> OperateRequestBuilder:
        """
        The operate property
        """
        from .operate.operate_request_builder import OperateRequestBuilder

        return OperateRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def order_group(self) -> OrderGroupRequestBuilder:
        """
        The orderGroup property
        """
        from .order_group.order_group_request_builder import OrderGroupRequestBuilder

        return OrderGroupRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def order_record(self) -> OrderRecordRequestBuilder:
        """
        The orderRecord property
        """
        from .order_record.order_record_request_builder import OrderRecordRequestBuilder

        return OrderRecordRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def order_record_change_vehicle(self) -> OrderRecordChangeVehicleRequestBuilder:
        """
        The orderRecordChangeVehicle property
        """
        from .order_record_change_vehicle.order_record_change_vehicle_request_builder import OrderRecordChangeVehicleRequestBuilder

        return OrderRecordChangeVehicleRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def order_record_priority_exec(self) -> OrderRecordPriorityExecRequestBuilder:
        """
        The orderRecordPriorityExec property
        """
        from .order_record_priority_exec.order_record_priority_exec_request_builder import OrderRecordPriorityExecRequestBuilder

        return OrderRecordPriorityExecRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def template_action(self) -> TemplateActionRequestBuilder:
        """
        The templateAction property
        """
        from .template_action.template_action_request_builder import TemplateActionRequestBuilder

        return TemplateActionRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def template_order(self) -> TemplateOrderRequestBuilder:
        """
        The templateOrder property
        """
        from .template_order.template_order_request_builder import TemplateOrderRequestBuilder

        return TemplateOrderRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def template_order_tag(self) -> TemplateOrderTagRequestBuilder:
        """
        The templateOrderTag property
        """
        from .template_order_tag.template_order_tag_request_builder import TemplateOrderTagRequestBuilder

        return TemplateOrderTagRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def update_order_task(self) -> UpdateOrderTaskRequestBuilder:
        """
        The updateOrderTask property
        """
        from .update_order_task.update_order_task_request_builder import UpdateOrderTaskRequestBuilder

        return UpdateOrderTaskRequestBuilder(self.request_adapter, self.path_parameters)
    

