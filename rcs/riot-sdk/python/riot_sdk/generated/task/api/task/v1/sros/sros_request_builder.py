from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .import_batch.import_batch_request_builder import ImportBatchRequestBuilder
    from .restart_s_r_o_s_batch.restart_s_r_o_s_batch_request_builder import RestartSROSBatchRequestBuilder

class SrosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/sros
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SrosRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/sros", path_parameters)
    
    @property
    def import_batch(self) -> ImportBatchRequestBuilder:
        """
        The importBatch property
        """
        from .import_batch.import_batch_request_builder import ImportBatchRequestBuilder

        return ImportBatchRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def restart_s_r_o_s_batch(self) -> RestartSROSBatchRequestBuilder:
        """
        The restartSROSBatch property
        """
        from .restart_s_r_o_s_batch.restart_s_r_o_s_batch_request_builder import RestartSROSBatchRequestBuilder

        return RestartSROSBatchRequestBuilder(self.request_adapter, self.path_parameters)
    

