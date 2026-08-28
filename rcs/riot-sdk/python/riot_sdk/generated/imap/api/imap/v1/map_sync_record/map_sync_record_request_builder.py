from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .map_sync_source.map_sync_source_request_builder import MapSyncSourceRequestBuilder

class MapSyncRecordRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapSyncRecord
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapSyncRecordRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapSyncRecord", path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_sync_source(self) -> MapSyncSourceRequestBuilder:
        """
        The mapSyncSource property
        """
        from .map_sync_source.map_sync_source_request_builder import MapSyncSourceRequestBuilder

        return MapSyncSourceRequestBuilder(self.request_adapter, self.path_parameters)
    

