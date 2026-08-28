from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class Pose(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The confidence property
    confidence: Optional[int] = None
    # The pitch property
    pitch: Optional[int] = None
    # The roll property
    roll: Optional[int] = None
    # The x property
    x: Optional[int] = None
    # The y property
    y: Optional[int] = None
    # The yaw property
    yaw: Optional[int] = None
    # The z property
    z: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Pose:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Pose
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Pose()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "confidence": lambda n : setattr(self, 'confidence', n.get_int_value()),
            "pitch": lambda n : setattr(self, 'pitch', n.get_int_value()),
            "roll": lambda n : setattr(self, 'roll', n.get_int_value()),
            "x": lambda n : setattr(self, 'x', n.get_int_value()),
            "y": lambda n : setattr(self, 'y', n.get_int_value()),
            "yaw": lambda n : setattr(self, 'yaw', n.get_int_value()),
            "z": lambda n : setattr(self, 'z', n.get_int_value()),
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
        writer.write_int_value("confidence", self.confidence)
        writer.write_int_value("pitch", self.pitch)
        writer.write_int_value("roll", self.roll)
        writer.write_int_value("x", self.x)
        writer.write_int_value("y", self.y)
        writer.write_int_value("yaw", self.yaw)
        writer.write_int_value("z", self.z)
        writer.write_additional_data_value(self.additional_data)
    

