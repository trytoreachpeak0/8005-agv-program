from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object(AdditionalDataHolder, Parsable):
    """
    找最近的起点参数对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 终点站点id
    end_station_id: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    # 起点候选站点id列表
    start_station_ids: Optional[list[int]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U627eu6700u8fd1u7684u8d77u70b9u53c2u6570Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "endStationId": lambda n : setattr(self, 'end_station_id', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "startStationIds": lambda n : setattr(self, 'start_station_ids', n.get_collection_of_primitive_values(int)),
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
        writer.write_int_value("endStationId", self.end_station_id)
        writer.write_int_value("mapId", self.map_id)
        writer.write_collection_of_primitive_values("startStationIds", self.start_station_ids)
        writer.write_additional_data_value(self.additional_data)
    

