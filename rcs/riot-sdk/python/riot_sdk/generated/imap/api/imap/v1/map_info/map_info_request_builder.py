from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .all.all_request_builder import AllRequestBuilder
    from .device_map_list.device_map_list_request_builder import DeviceMapListRequestBuilder
    from .edges.edges_request_builder import EdgesRequestBuilder
    from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder
    from .file.file_request_builder import FileRequestBuilder
    from .get_a_l_l_map_info_exclude_map_json.get_a_l_l_map_info_exclude_map_json_request_builder import GetALLMapInfoExcludeMapJsonRequestBuilder
    from .get_edge_group_custom_attributes.get_edge_group_custom_attributes_request_builder import GetEdgeGroupCustomAttributesRequestBuilder
    from .get_station_custom_attributes.get_station_custom_attributes_request_builder import GetStationCustomAttributesRequestBuilder
    from .item.with_map_item_request_builder import WithMapItemRequestBuilder
    from .map_info_from_file.map_info_from_file_request_builder import MapInfoFromFileRequestBuilder
    from .stations.stations_request_builder import StationsRequestBuilder

class MapInfoRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapInfo
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new MapInfoRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapInfo", path_parameters)
    
    def by_map_id(self,map_id: int) -> WithMapItemRequestBuilder:
        """
        Gets an item from the riot_sdk.generated.imap.api.imap.v1.mapInfo.item collection
        param map_id: 地图id
        Returns: WithMapItemRequestBuilder
        """
        if map_id is None:
            raise TypeError("map_id cannot be null.")
        from .item.with_map_item_request_builder import WithMapItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["mapId"] = map_id
        return WithMapItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def all(self) -> AllRequestBuilder:
        """
        The all property
        """
        from .all.all_request_builder import AllRequestBuilder

        return AllRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def device_map_list(self) -> DeviceMapListRequestBuilder:
        """
        The deviceMapList property
        """
        from .device_map_list.device_map_list_request_builder import DeviceMapListRequestBuilder

        return DeviceMapListRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def edges(self) -> EdgesRequestBuilder:
        """
        The edges property
        """
        from .edges.edges_request_builder import EdgesRequestBuilder

        return EdgesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def empty_path_segment(self) -> EmptyPathSegmentRequestBuilder:
        """
        The EmptyPathSegment property
        """
        from .empty_path_segment_request_builder import EmptyPathSegmentRequestBuilder

        return EmptyPathSegmentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def file(self) -> FileRequestBuilder:
        """
        The file property
        """
        from .file.file_request_builder import FileRequestBuilder

        return FileRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_a_l_l_map_info_exclude_map_json(self) -> GetALLMapInfoExcludeMapJsonRequestBuilder:
        """
        The getALLMapInfoExcludeMapJson property
        """
        from .get_a_l_l_map_info_exclude_map_json.get_a_l_l_map_info_exclude_map_json_request_builder import GetALLMapInfoExcludeMapJsonRequestBuilder

        return GetALLMapInfoExcludeMapJsonRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_edge_group_custom_attributes(self) -> GetEdgeGroupCustomAttributesRequestBuilder:
        """
        The getEdgeGroupCustomAttributes property
        """
        from .get_edge_group_custom_attributes.get_edge_group_custom_attributes_request_builder import GetEdgeGroupCustomAttributesRequestBuilder

        return GetEdgeGroupCustomAttributesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def get_station_custom_attributes(self) -> GetStationCustomAttributesRequestBuilder:
        """
        The getStationCustomAttributes property
        """
        from .get_station_custom_attributes.get_station_custom_attributes_request_builder import GetStationCustomAttributesRequestBuilder

        return GetStationCustomAttributesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_info_from_file(self) -> MapInfoFromFileRequestBuilder:
        """
        The mapInfoFromFile property
        """
        from .map_info_from_file.map_info_from_file_request_builder import MapInfoFromFileRequestBuilder

        return MapInfoFromFileRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def stations(self) -> StationsRequestBuilder:
        """
        The stations property
        """
        from .stations.stations_request_builder import StationsRequestBuilder

        return StationsRequestBuilder(self.request_adapter, self.path_parameters)
    

