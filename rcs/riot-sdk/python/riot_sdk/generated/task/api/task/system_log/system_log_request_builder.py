from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .export_systemlog.export_systemlog_request_builder import ExportSystemlogRequestBuilder
    from .page.page_request_builder import PageRequestBuilder
    from .query_not_read.query_not_read_request_builder import QueryNotReadRequestBuilder
    from .read.read_request_builder import ReadRequestBuilder
    from .read_all.read_all_request_builder import ReadAllRequestBuilder
    from .unread.unread_request_builder import UnreadRequestBuilder
    from .update_status.update_status_request_builder import UpdateStatusRequestBuilder

class SystemLogRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/systemLog
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SystemLogRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/systemLog", path_parameters)
    
    @property
    def export_systemlog(self) -> ExportSystemlogRequestBuilder:
        """
        The exportSystemlog property
        """
        from .export_systemlog.export_systemlog_request_builder import ExportSystemlogRequestBuilder

        return ExportSystemlogRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def page(self) -> PageRequestBuilder:
        """
        The page property
        """
        from .page.page_request_builder import PageRequestBuilder

        return PageRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_not_read(self) -> QueryNotReadRequestBuilder:
        """
        The queryNotRead property
        """
        from .query_not_read.query_not_read_request_builder import QueryNotReadRequestBuilder

        return QueryNotReadRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def read(self) -> ReadRequestBuilder:
        """
        The read property
        """
        from .read.read_request_builder import ReadRequestBuilder

        return ReadRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def read_all(self) -> ReadAllRequestBuilder:
        """
        The readAll property
        """
        from .read_all.read_all_request_builder import ReadAllRequestBuilder

        return ReadAllRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def unread(self) -> UnreadRequestBuilder:
        """
        The unread property
        """
        from .unread.unread_request_builder import UnreadRequestBuilder

        return UnreadRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def update_status(self) -> UpdateStatusRequestBuilder:
        """
        The updateStatus property
        """
        from .update_status.update_status_request_builder import UpdateStatusRequestBuilder

        return UpdateStatusRequestBuilder(self.request_adapter, self.path_parameters)
    

