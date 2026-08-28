from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .rep_device_costs import RepDeviceCosts

@dataclass
class U56deu590du8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7(AdditionalDataHolder, Parsable):
    """
    回复车辆列表到达站点代价
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆代价列表
    device_costs_list: Optional[list[RepDeviceCosts]] = None
    # 地图id
    map_id: Optional[int] = None
    # 站点id
    station_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U56deu590du8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U56deu590du8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U56deu590du8f66u8f86u5217u8868u5230u8fbeu7ad9u70b9u4ee3u4ef7()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .rep_device_costs import RepDeviceCosts

        from .rep_device_costs import RepDeviceCosts

        fields: dict[str, Callable[[Any], None]] = {
            "deviceCostsList": lambda n : setattr(self, 'device_costs_list', n.get_collection_of_object_values(RepDeviceCosts)),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "stationId": lambda n : setattr(self, 'station_id', n.get_int_value()),
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
        writer.write_collection_of_object_values("deviceCostsList", self.device_costs_list)
        writer.write_int_value("mapId", self.map_id)
        writer.write_int_value("stationId", self.station_id)
        writer.write_additional_data_value(self.additional_data)
    

