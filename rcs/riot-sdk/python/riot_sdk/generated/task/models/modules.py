from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class Modules(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The actionTask property
    action_task: Optional[bool] = None
    # The commandHander property
    command_hander: Optional[bool] = None
    # The device property
    device: Optional[bool] = None
    # The execRrror property
    exec_rrror: Optional[bool] = None
    # The modbus property
    modbus: Optional[bool] = None
    # The movementTask property
    movement_task: Optional[bool] = None
    # The protobuf property
    protobuf: Optional[bool] = None
    # The sros property
    sros: Optional[bool] = None
    # The task property
    task: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Modules:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Modules
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Modules()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "actionTask": lambda n : setattr(self, 'action_task', n.get_bool_value()),
            "commandHander": lambda n : setattr(self, 'command_hander', n.get_bool_value()),
            "device": lambda n : setattr(self, 'device', n.get_bool_value()),
            "execRrror": lambda n : setattr(self, 'exec_rrror', n.get_bool_value()),
            "modbus": lambda n : setattr(self, 'modbus', n.get_bool_value()),
            "movementTask": lambda n : setattr(self, 'movement_task', n.get_bool_value()),
            "protobuf": lambda n : setattr(self, 'protobuf', n.get_bool_value()),
            "sros": lambda n : setattr(self, 'sros', n.get_bool_value()),
            "task": lambda n : setattr(self, 'task', n.get_bool_value()),
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
        writer.write_bool_value("actionTask", self.action_task)
        writer.write_bool_value("commandHander", self.command_hander)
        writer.write_bool_value("device", self.device)
        writer.write_bool_value("execRrror", self.exec_rrror)
        writer.write_bool_value("modbus", self.modbus)
        writer.write_bool_value("movementTask", self.movement_task)
        writer.write_bool_value("protobuf", self.protobuf)
        writer.write_bool_value("sros", self.sros)
        writer.write_bool_value("task", self.task)
        writer.write_additional_data_value(self.additional_data)
    

