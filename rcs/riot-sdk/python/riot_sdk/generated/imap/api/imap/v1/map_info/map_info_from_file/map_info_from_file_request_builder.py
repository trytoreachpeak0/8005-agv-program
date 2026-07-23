from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_map_item_request_builder import WithMapItemRequestBuilder

class MapInfoFromFileRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapInfo/mapInfoFromFile
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapInfoFromFileRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapInfo/mapInfoFromFile", path_parameters)
    
    def by_map_id(self,map_id: int) -> WithMapItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.imap.api.imap.v1.mapInfo.mapInfoFromFile.item collection
        param map_id: 地图id
        Returns: WithMapItemRequestBuilder
        """
        if map_id is None:
            raise TypeError("map_id cannot be null.")
        from .item.with_map_item_request_builder import WithMapItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["mapId"] = map_id
        return WithMapItemRequestBuilder(self.request_adapter, url_tpl_params)
    

