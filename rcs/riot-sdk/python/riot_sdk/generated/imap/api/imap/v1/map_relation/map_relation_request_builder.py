from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .all.all_request_builder import AllRequestBuilder
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .item.map_relation_item_request_builder import MapRelationItemRequestBuilder

class MapRelationRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapRelation
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapRelationRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapRelation", path_parameters)
    
    def by_id(self,id: int) -> MapRelationItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.imap.api.imap.v1.mapRelation.item collection
        param id: 删除关系id
        Returns: MapRelationItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.map_relation_item_request_builder import MapRelationItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return MapRelationItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def all(self) -> AllRequestBuilder:
        """
        The all property
        """
        from .all.all_request_builder import AllRequestBuilder

        return AllRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    

