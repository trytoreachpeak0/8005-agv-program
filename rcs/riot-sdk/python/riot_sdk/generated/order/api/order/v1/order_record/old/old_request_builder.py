from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .export_order_record.export_order_record_request_builder import ExportOrderRecordRequestBuilder

class OldRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/order/v1/orderRecord/old
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new OldRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/order/v1/orderRecord/old", path_parameters)
    
    @property
    def export_order_record(self) -> ExportOrderRecordRequestBuilder:
        """
        The exportOrderRecord property
        """
        from .export_order_record.export_order_record_request_builder import ExportOrderRecordRequestBuilder

        return ExportOrderRecordRequestBuilder(self.request_adapter, self.path_parameters)
    

