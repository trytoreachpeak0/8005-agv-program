from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .import_.import_request_builder import ImportRequestBuilder
    from .template.template_request_builder import TemplateRequestBuilder

class ExcelRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/device/v1/devices/excel
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ExcelRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/device/v1/devices/excel", path_parameters)
    
    @property
    def import_(self) -> ImportRequestBuilder:
        """
        The import property
        """
        from .import_.import_request_builder import ImportRequestBuilder

        return ImportRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def template(self) -> TemplateRequestBuilder:
        """
        The template property
        """
        from .template.template_request_builder import TemplateRequestBuilder

        return TemplateRequestBuilder(self.request_adapter, self.path_parameters)
    

