from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .by_default_missions.by_default_missions_request_builder import ByDefaultMissionsRequestBuilder
    from .by_dynamic_template.by_dynamic_template_request_builder import ByDynamicTemplateRequestBuilder
    from .by_order_group.by_order_group_request_builder import ByOrderGroupRequestBuilder
    from .by_static_template.by_static_template_request_builder import ByStaticTemplateRequestBuilder

class AddRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1/add
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new AddRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1/add", path_parameters)
    
    @property
    def by_default_missions(self) -> ByDefaultMissionsRequestBuilder:
        """
        The byDefaultMissions property
        """
        from .by_default_missions.by_default_missions_request_builder import ByDefaultMissionsRequestBuilder

        return ByDefaultMissionsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def by_dynamic_template(self) -> ByDynamicTemplateRequestBuilder:
        """
        The byDynamicTemplate property
        """
        from .by_dynamic_template.by_dynamic_template_request_builder import ByDynamicTemplateRequestBuilder

        return ByDynamicTemplateRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def by_order_group(self) -> ByOrderGroupRequestBuilder:
        """
        The byOrderGroup property
        """
        from .by_order_group.by_order_group_request_builder import ByOrderGroupRequestBuilder

        return ByOrderGroupRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def by_static_template(self) -> ByStaticTemplateRequestBuilder:
        """
        The byStaticTemplate property
        """
        from .by_static_template.by_static_template_request_builder import ByStaticTemplateRequestBuilder

        return ByStaticTemplateRequestBuilder(self.request_adapter, self.path_parameters)
    

