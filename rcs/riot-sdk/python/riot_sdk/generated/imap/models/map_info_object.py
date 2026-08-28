from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .map_info_object_source import MapInfoObject_source
    from .map_info_object_state import MapInfoObject_state
    from .map_info_object_sync_state import MapInfoObject_syncState

@dataclass
class MapInfoObject(AdditionalDataHolder, Parsable):
    """
    地图信息表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 地图描述
    description: Optional[str] = None
    # 地图楼层
    floor: Optional[int] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # 地图错误信息
    map_error: Optional[str] = None
    # 地图文件名
    name: Optional[str] = None
    # 来源 upload, fetch
    source: Optional[MapInfoObject_source] = None
    # 状态 activated, inactivated
    state: Optional[MapInfoObject_state] = None
    # 地图同步状态
    sync_state: Optional[MapInfoObject_syncState] = None
    # 地图url
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapInfoObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapInfoObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapInfoObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .map_info_object_source import MapInfoObject_source
        from .map_info_object_state import MapInfoObject_state
        from .map_info_object_sync_state import MapInfoObject_syncState

        from .map_info_object_source import MapInfoObject_source
        from .map_info_object_state import MapInfoObject_state
        from .map_info_object_sync_state import MapInfoObject_syncState

        fields: dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "floor": lambda n : setattr(self, 'floor', n.get_int_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "mapError": lambda n : setattr(self, 'map_error', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "source": lambda n : setattr(self, 'source', n.get_enum_value(MapInfoObject_source)),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(MapInfoObject_state)),
            "syncState": lambda n : setattr(self, 'sync_state', n.get_enum_value(MapInfoObject_syncState)),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("description", self.description)
        writer.write_int_value("floor", self.floor)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_str_value("mapError", self.map_error)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("source", self.source)
        writer.write_enum_value("state", self.state)
        writer.write_enum_value("syncState", self.sync_state)
        writer.write_str_value("url", self.url)
        writer.write_additional_data_value(self.additional_data)
    

