from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .map_edge_group.map_edge_group_request_builder import MapEdgeGroupRequestBuilder
    from .map_info.map_info_request_builder import MapInfoRequestBuilder
    from .map_relation.map_relation_request_builder import MapRelationRequestBuilder
    from .map_resource.map_resource_request_builder import MapResourceRequestBuilder
    from .map_sync_record.map_sync_record_request_builder import MapSyncRecordRequestBuilder
    from .map_sync_state.map_sync_state_request_builder import MapSyncStateRequestBuilder

class V1RequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new V1RequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1", path_parameters)
    
    @property
    def map_edge_group(self) -> MapEdgeGroupRequestBuilder:
        """
        The mapEdgeGroup property
        """
        from .map_edge_group.map_edge_group_request_builder import MapEdgeGroupRequestBuilder

        return MapEdgeGroupRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_info(self) -> MapInfoRequestBuilder:
        """
        The mapInfo property
        """
        from .map_info.map_info_request_builder import MapInfoRequestBuilder

        return MapInfoRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_relation(self) -> MapRelationRequestBuilder:
        """
        The mapRelation property
        """
        from .map_relation.map_relation_request_builder import MapRelationRequestBuilder

        return MapRelationRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_resource(self) -> MapResourceRequestBuilder:
        """
        The mapResource property
        """
        from .map_resource.map_resource_request_builder import MapResourceRequestBuilder

        return MapResourceRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_sync_record(self) -> MapSyncRecordRequestBuilder:
        """
        The mapSyncRecord property
        """
        from .map_sync_record.map_sync_record_request_builder import MapSyncRecordRequestBuilder

        return MapSyncRecordRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_sync_state(self) -> MapSyncStateRequestBuilder:
        """
        The mapSyncState property
        """
        from .map_sync_state.map_sync_state_request_builder import MapSyncStateRequestBuilder

        return MapSyncStateRequestBuilder(self.request_adapter, self.path_parameters)
    

