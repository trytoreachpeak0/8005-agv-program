from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MotionControlState(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The pathNo property
    path_no: Optional[int] = None
    # The state property
    state: Optional[int] = None
    # The vx property
    vx: Optional[int] = None
    # The vy property
    vy: Optional[int] = None
    # The w property
    w: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MotionControlState:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MotionControlState
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MotionControlState()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "pathNo": lambda n : setattr(self, 'path_no', n.get_int_value()),
            "state": lambda n : setattr(self, 'state', n.get_int_value()),
            "vx": lambda n : setattr(self, 'vx', n.get_int_value()),
            "vy": lambda n : setattr(self, 'vy', n.get_int_value()),
            "w": lambda n : setattr(self, 'w', n.get_int_value()),
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
        writer.write_int_value("pathNo", self.path_no)
        writer.write_int_value("state", self.state)
        writer.write_int_value("vx", self.vx)
        writer.write_int_value("vy", self.vy)
        writer.write_int_value("w", self.w)
        writer.write_additional_data_value(self.additional_data)
    

