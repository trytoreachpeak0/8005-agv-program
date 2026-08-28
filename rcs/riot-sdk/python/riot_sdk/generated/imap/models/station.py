from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .station_user_defined_properties import Station_userDefinedProperties

@dataclass
class Station(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The checkPosX property
    check_pos_x: Optional[int] = None
    # The checkPosY property
    check_pos_y: Optional[int] = None
    # The checkPosYaw property
    check_pos_yaw: Optional[int] = None
    # The desc property
    desc: Optional[str] = None
    # The dmcodeId property
    dmcode_id: Optional[str] = None
    # The edgeId property
    edge_id: Optional[int] = None
    # The enterBackward property
    enter_backward: Optional[bool] = None
    # The enterPosX property
    enter_pos_x: Optional[int] = None
    # The enterPosY property
    enter_pos_y: Optional[int] = None
    # The enterPosYaw property
    enter_pos_yaw: Optional[int] = None
    # The exitBackWard property
    exit_back_ward: Optional[bool] = None
    # The exitPosX property
    exit_pos_x: Optional[int] = None
    # The exitPosY property
    exit_pos_y: Optional[int] = None
    # The exitPosYaw property
    exit_pos_yaw: Optional[int] = None
    # The id property
    id: Optional[int] = None
    # The name property
    name: Optional[str] = None
    # The noRotate property
    no_rotate: Optional[bool] = None
    # The param property
    param: Optional[int] = None
    # The pgvOffsetX property
    pgv_offset_x: Optional[int] = None
    # The pgvOffsetY property
    pgv_offset_y: Optional[int] = None
    # The pgvOffsetYaw property
    pgv_offset_yaw: Optional[int] = None
    # The posDynamic property
    pos_dynamic: Optional[bool] = None
    # The posX property
    pos_x: Optional[float] = None
    # The posY property
    pos_y: Optional[float] = None
    # The posYaw property
    pos_yaw: Optional[float] = None
    # The stationOffset property
    station_offset: Optional[int] = None
    # The type property
    type: Optional[int] = None
    # The userDefinedProperties property
    user_defined_properties: Optional[Station_userDefinedProperties] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Station:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Station
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Station()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .station_user_defined_properties import Station_userDefinedProperties

        from .station_user_defined_properties import Station_userDefinedProperties

        fields: dict[str, Callable[[Any], None]] = {
            "checkPosX": lambda n : setattr(self, 'check_pos_x', n.get_int_value()),
            "checkPosY": lambda n : setattr(self, 'check_pos_y', n.get_int_value()),
            "checkPosYaw": lambda n : setattr(self, 'check_pos_yaw', n.get_int_value()),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "dmcodeId": lambda n : setattr(self, 'dmcode_id', n.get_str_value()),
            "edgeId": lambda n : setattr(self, 'edge_id', n.get_int_value()),
            "enterBackward": lambda n : setattr(self, 'enter_backward', n.get_bool_value()),
            "enterPosX": lambda n : setattr(self, 'enter_pos_x', n.get_int_value()),
            "enterPosY": lambda n : setattr(self, 'enter_pos_y', n.get_int_value()),
            "enterPosYaw": lambda n : setattr(self, 'enter_pos_yaw', n.get_int_value()),
            "exitBackWard": lambda n : setattr(self, 'exit_back_ward', n.get_bool_value()),
            "exitPosX": lambda n : setattr(self, 'exit_pos_x', n.get_int_value()),
            "exitPosY": lambda n : setattr(self, 'exit_pos_y', n.get_int_value()),
            "exitPosYaw": lambda n : setattr(self, 'exit_pos_yaw', n.get_int_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "noRotate": lambda n : setattr(self, 'no_rotate', n.get_bool_value()),
            "param": lambda n : setattr(self, 'param', n.get_int_value()),
            "pgvOffsetX": lambda n : setattr(self, 'pgv_offset_x', n.get_int_value()),
            "pgvOffsetY": lambda n : setattr(self, 'pgv_offset_y', n.get_int_value()),
            "pgvOffsetYaw": lambda n : setattr(self, 'pgv_offset_yaw', n.get_int_value()),
            "posDynamic": lambda n : setattr(self, 'pos_dynamic', n.get_bool_value()),
            "posX": lambda n : setattr(self, 'pos_x', n.get_float_value()),
            "posY": lambda n : setattr(self, 'pos_y', n.get_float_value()),
            "posYaw": lambda n : setattr(self, 'pos_yaw', n.get_float_value()),
            "stationOffset": lambda n : setattr(self, 'station_offset', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_int_value()),
            "userDefinedProperties": lambda n : setattr(self, 'user_defined_properties', n.get_object_value(Station_userDefinedProperties)),
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
        writer.write_int_value("checkPosX", self.check_pos_x)
        writer.write_int_value("checkPosY", self.check_pos_y)
        writer.write_int_value("checkPosYaw", self.check_pos_yaw)
        writer.write_str_value("desc", self.desc)
        writer.write_str_value("dmcodeId", self.dmcode_id)
        writer.write_int_value("edgeId", self.edge_id)
        writer.write_bool_value("enterBackward", self.enter_backward)
        writer.write_int_value("enterPosX", self.enter_pos_x)
        writer.write_int_value("enterPosY", self.enter_pos_y)
        writer.write_int_value("enterPosYaw", self.enter_pos_yaw)
        writer.write_bool_value("exitBackWard", self.exit_back_ward)
        writer.write_int_value("exitPosX", self.exit_pos_x)
        writer.write_int_value("exitPosY", self.exit_pos_y)
        writer.write_int_value("exitPosYaw", self.exit_pos_yaw)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("noRotate", self.no_rotate)
        writer.write_int_value("param", self.param)
        writer.write_int_value("pgvOffsetX", self.pgv_offset_x)
        writer.write_int_value("pgvOffsetY", self.pgv_offset_y)
        writer.write_int_value("pgvOffsetYaw", self.pgv_offset_yaw)
        writer.write_bool_value("posDynamic", self.pos_dynamic)
        writer.write_float_value("posX", self.pos_x)
        writer.write_float_value("posY", self.pos_y)
        writer.write_float_value("posYaw", self.pos_yaw)
        writer.write_int_value("stationOffset", self.station_offset)
        writer.write_int_value("type", self.type)
        writer.write_object_value("userDefinedProperties", self.user_defined_properties)
        writer.write_additional_data_value(self.additional_data)
    

