from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MapRemovedStationObject(AdditionalDataHolder, Parsable):
    """
    地图移除站点表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # 移除站点记录id
    id: Optional[int] = None
    # 移除站点的地图id
    map_id: Optional[int] = None
    # 移除站点id
    station_id: Optional[int] = None
    # 移除站点名称
    station_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapRemovedStationObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapRemovedStationObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapRemovedStationObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "stationId": lambda n : setattr(self, 'station_id', n.get_int_value()),
            "stationName": lambda n : setattr(self, 'station_name', n.get_str_value()),
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
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_int_value("mapId", self.map_id)
        writer.write_int_value("stationId", self.station_id)
        writer.write_str_value("stationName", self.station_name)
        writer.write_additional_data_value(self.additional_data)
    

