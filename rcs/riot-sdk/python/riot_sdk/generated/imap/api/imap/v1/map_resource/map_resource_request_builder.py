from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .removed_edge.removed_edge_request_builder import RemovedEdgeRequestBuilder
    from .removed_edge_detail.removed_edge_detail_request_builder import RemovedEdgeDetailRequestBuilder
    from .removed_station.removed_station_request_builder import RemovedStationRequestBuilder

class MapResourceRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapResource
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapResourceRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapResource", path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def removed_edge(self) -> RemovedEdgeRequestBuilder:
        """
        The removedEdge property
        """
        from .removed_edge.removed_edge_request_builder import RemovedEdgeRequestBuilder

        return RemovedEdgeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def removed_edge_detail(self) -> RemovedEdgeDetailRequestBuilder:
        """
        The removedEdgeDetail property
        """
        from .removed_edge_detail.removed_edge_detail_request_builder import RemovedEdgeDetailRequestBuilder

        return RemovedEdgeDetailRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def removed_station(self) -> RemovedStationRequestBuilder:
        """
        The removedStation property
        """
        from .removed_station.removed_station_request_builder import RemovedStationRequestBuilder

        return RemovedStationRequestBuilder(self.request_adapter, self.path_parameters)
    

