from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .mission_d_t_o_extend_params import MissionDTO_extendParams

@dataclass
class MissionDTO(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The actionId property
    action_id: Optional[int] = None
    # The actionName property
    action_name: Optional[str] = None
    # The actionParamStr property
    action_param_str: Optional[str] = None
    # The actionParam1 property
    action_param1: Optional[int] = None
    # The actionParam2 property
    action_param2: Optional[int] = None
    # The destination property
    destination: Optional[int] = None
    # The extendParams property
    extend_params: Optional[MissionDTO_extendParams] = None
    # The failStrategy property
    fail_strategy: Optional[str] = None
    # The failValue property
    fail_value: Optional[str] = None
    # The functionKey property
    function_key: Optional[str] = None
    # The index property
    index: Optional[int] = None
    # The length property
    length: Optional[int] = None
    # The mapId property
    map_id: Optional[int] = None
    # The mapName property
    map_name: Optional[str] = None
    # The orderId property
    order_id: Optional[str] = None
    # The orderUuid property
    order_uuid: Optional[str] = None
    # The speed property
    speed: Optional[float] = None
    # The stationName property
    station_name: Optional[str] = None
    # The successStrategy property
    success_strategy: Optional[str] = None
    # The type property
    type: Optional[str] = None
    # The width property
    width: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MissionDTO:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MissionDTO
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MissionDTO()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .mission_d_t_o_extend_params import MissionDTO_extendParams

        from .mission_d_t_o_extend_params import MissionDTO_extendParams

        fields: dict[str, Callable[[Any], None]] = {
            "actionId": lambda n : setattr(self, 'action_id', n.get_int_value()),
            "actionName": lambda n : setattr(self, 'action_name', n.get_str_value()),
            "actionParamStr": lambda n : setattr(self, 'action_param_str', n.get_str_value()),
            "actionParam1": lambda n : setattr(self, 'action_param1', n.get_int_value()),
            "actionParam2": lambda n : setattr(self, 'action_param2', n.get_int_value()),
            "destination": lambda n : setattr(self, 'destination', n.get_int_value()),
            "extendParams": lambda n : setattr(self, 'extend_params', n.get_object_value(MissionDTO_extendParams)),
            "failStrategy": lambda n : setattr(self, 'fail_strategy', n.get_str_value()),
            "failValue": lambda n : setattr(self, 'fail_value', n.get_str_value()),
            "functionKey": lambda n : setattr(self, 'function_key', n.get_str_value()),
            "index": lambda n : setattr(self, 'index', n.get_int_value()),
            "length": lambda n : setattr(self, 'length', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "orderId": lambda n : setattr(self, 'order_id', n.get_str_value()),
            "orderUuid": lambda n : setattr(self, 'order_uuid', n.get_str_value()),
            "speed": lambda n : setattr(self, 'speed', n.get_float_value()),
            "stationName": lambda n : setattr(self, 'station_name', n.get_str_value()),
            "successStrategy": lambda n : setattr(self, 'success_strategy', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
            "width": lambda n : setattr(self, 'width', n.get_int_value()),
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
        writer.write_int_value("actionId", self.action_id)
        writer.write_str_value("actionName", self.action_name)
        writer.write_str_value("actionParamStr", self.action_param_str)
        writer.write_int_value("actionParam1", self.action_param1)
        writer.write_int_value("actionParam2", self.action_param2)
        writer.write_int_value("destination", self.destination)
        writer.write_object_value("extendParams", self.extend_params)
        writer.write_str_value("failStrategy", self.fail_strategy)
        writer.write_str_value("failValue", self.fail_value)
        writer.write_str_value("functionKey", self.function_key)
        writer.write_int_value("index", self.index)
        writer.write_int_value("length", self.length)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("mapName", self.map_name)
        writer.write_str_value("orderId", self.order_id)
        writer.write_str_value("orderUuid", self.order_uuid)
        writer.write_float_value("speed", self.speed)
        writer.write_str_value("stationName", self.station_name)
        writer.write_str_value("successStrategy", self.success_strategy)
        writer.write_str_value("type", self.type)
        writer.write_int_value("width", self.width)
        writer.write_additional_data_value(self.additional_data)
    

