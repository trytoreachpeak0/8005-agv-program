from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

@dataclass
class U5f02u5e38u7edfu8ba1u8fd4u56deObject(AdditionalDataHolder, Parsable):
    """
    异常统计返回对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 平均解抱闸
    avg_break_switch: Optional[int] = None
    # 平均急停
    avg_emergency: Optional[int] = None
    # 平均电机异常
    avg_motor_exception: Optional[int] = None
    # 平均掉线
    avg_off_line: Optional[int] = None
    # 车辆数据集合
    exception_statistics_histograms: Optional[list[U8f66u8f86u6570u636e]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U5f02u5e38u7edfu8ba1u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U5f02u5e38u7edfu8ba1u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U5f02u5e38u7edfu8ba1u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        fields: dict[str, Callable[[Any], None]] = {
            "avgBreakSwitch": lambda n : setattr(self, 'avg_break_switch', n.get_int_value()),
            "avgEmergency": lambda n : setattr(self, 'avg_emergency', n.get_int_value()),
            "avgMotorException": lambda n : setattr(self, 'avg_motor_exception', n.get_int_value()),
            "avgOffLine": lambda n : setattr(self, 'avg_off_line', n.get_int_value()),
            "exceptionStatisticsHistograms": lambda n : setattr(self, 'exception_statistics_histograms', n.get_collection_of_object_values(U8f66u8f86u6570u636e)),
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
        writer.write_int_value("avgBreakSwitch", self.avg_break_switch)
        writer.write_int_value("avgEmergency", self.avg_emergency)
        writer.write_int_value("avgMotorException", self.avg_motor_exception)
        writer.write_int_value("avgOffLine", self.avg_off_line)
        writer.write_collection_of_object_values("exceptionStatisticsHistograms", self.exception_statistics_histograms)
        writer.write_additional_data_value(self.additional_data)
    

