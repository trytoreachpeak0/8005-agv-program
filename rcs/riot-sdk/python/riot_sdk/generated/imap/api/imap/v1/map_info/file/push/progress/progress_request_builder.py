from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_map_sync_record_item_request_builder import WithMapSyncRecordItemRequestBuilder

class ProgressRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapInfo/file/push/progress
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ProgressRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapInfo/file/push/progress", path_parameters)
    
    def by_map_sync_record_id(self,map_sync_record_id: int) -> WithMapSyncRecordItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.imap.api.imap.v1.mapInfo.file.push.progress.item collection
        param map_sync_record_id: 同步记录Id
        Returns: WithMapSyncRecordItemRequestBuilder
        """
        if map_sync_record_id is None:
            raise TypeError("map_sync_record_id cannot be null.")
        from .item.with_map_sync_record_item_request_builder import WithMapSyncRecordItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["mapSyncRecordId"] = map_sync_record_id
        return WithMapSyncRecordItemRequestBuilder(self.request_adapter, url_tpl_params)
    

