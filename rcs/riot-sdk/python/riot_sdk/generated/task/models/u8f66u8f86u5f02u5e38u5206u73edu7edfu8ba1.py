from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty import U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty

@dataclass
class U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1(AdditionalDataHolder, Parsable):
    """
    车辆异常分班统计
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 解抱闸
    break_switch: Optional[int] = None
    # 班次
    duty: Optional[U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty] = None
    # 急停
    emergency: Optional[int] = None
    # 电机异常
    motor_exception: Optional[int] = None
    # 掉线
    off_line: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty import U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty

        from .u8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty import U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty

        fields: dict[str, Callable[[Any], None]] = {
            "breakSwitch": lambda n : setattr(self, 'break_switch', n.get_int_value()),
            "duty": lambda n : setattr(self, 'duty', n.get_enum_value(U8f66u8f86u5f02u5e38u5206u73edu7edfu8ba1_duty)),
            "emergency": lambda n : setattr(self, 'emergency', n.get_int_value()),
            "motorException": lambda n : setattr(self, 'motor_exception', n.get_int_value()),
            "offLine": lambda n : setattr(self, 'off_line', n.get_int_value()),
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
        writer.write_int_value("breakSwitch", self.break_switch)
        writer.write_enum_value("duty", self.duty)
        writer.write_int_value("emergency", self.emergency)
        writer.write_int_value("motorException", self.motor_exception)
        writer.write_int_value("offLine", self.off_line)
        writer.write_additional_data_value(self.additional_data)
    

