from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .map_edge_group_object_type import MapEdgeGroupObject_type

@dataclass
class MapEdgeGroupObject(AdditionalDataHolder, Parsable):
    """
    地图边组合表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 边id
    edge_id: Optional[int] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # 逻辑删除
    is_delete: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    # 地图名称
    map_name: Optional[str] = None
    # 边组合名称
    name: Optional[str] = None
    # 边组合类型:SINGLE_VEHICLE_ONLY,SAME_DIRECTION_ONLY
    type: Optional[MapEdgeGroupObject_type] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapEdgeGroupObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapEdgeGroupObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapEdgeGroupObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .map_edge_group_object_type import MapEdgeGroupObject_type

        from .map_edge_group_object_type import MapEdgeGroupObject_type

        fields: dict[str, Callable[[Any], None]] = {
            "edgeId": lambda n : setattr(self, 'edge_id', n.get_int_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isDelete": lambda n : setattr(self, 'is_delete', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(MapEdgeGroupObject_type)),
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
        writer.write_int_value("edgeId", self.edge_id)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isDelete", self.is_delete)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("mapName", self.map_name)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

