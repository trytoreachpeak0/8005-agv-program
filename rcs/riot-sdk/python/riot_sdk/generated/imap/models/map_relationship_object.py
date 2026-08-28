from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MapRelationshipObject(AdditionalDataHolder, Parsable):
    """
    多地图关系表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 转移代价（消耗）
    cost: Optional[float] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # 起始地图id
    source_map_id: Optional[int] = None
    # 起始地图名
    source_map_name: Optional[str] = None
    # 起始站点id
    source_station_id: Optional[int] = None
    # 起始站点名
    source_station_name: Optional[str] = None
    # 目的地图id
    target_map_id: Optional[int] = None
    # 目的地图名
    target_map_name: Optional[str] = None
    # 目的站点id
    target_station_id: Optional[int] = None
    # 目的站点名
    target_station_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapRelationshipObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapRelationshipObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapRelationshipObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "cost": lambda n : setattr(self, 'cost', n.get_float_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "sourceMapId": lambda n : setattr(self, 'source_map_id', n.get_int_value()),
            "sourceMapName": lambda n : setattr(self, 'source_map_name', n.get_str_value()),
            "sourceStationId": lambda n : setattr(self, 'source_station_id', n.get_int_value()),
            "sourceStationName": lambda n : setattr(self, 'source_station_name', n.get_str_value()),
            "targetMapId": lambda n : setattr(self, 'target_map_id', n.get_int_value()),
            "targetMapName": lambda n : setattr(self, 'target_map_name', n.get_str_value()),
            "targetStationId": lambda n : setattr(self, 'target_station_id', n.get_int_value()),
            "targetStationName": lambda n : setattr(self, 'target_station_name', n.get_str_value()),
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
        writer.write_float_value("cost", self.cost)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_int_value("sourceMapId", self.source_map_id)
        writer.write_str_value("sourceMapName", self.source_map_name)
        writer.write_int_value("sourceStationId", self.source_station_id)
        writer.write_str_value("sourceStationName", self.source_station_name)
        writer.write_int_value("targetMapId", self.target_map_id)
        writer.write_str_value("targetMapName", self.target_map_name)
        writer.write_int_value("targetStationId", self.target_station_id)
        writer.write_str_value("targetStationName", self.target_station_name)
        writer.write_additional_data_value(self.additional_data)
    

