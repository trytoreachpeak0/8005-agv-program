from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

@dataclass
class U72b6u6001u65f6u957fu7edfu8ba1u8fd4u56deObject(AdditionalDataHolder, Parsable):
    """
    状态时长统计返回对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 平均充电时长
    avg_charging: Optional[float] = None
    # 平均异常时长
    avg_exception: Optional[float] = None
    # 平均执行时长
    avg_executing: Optional[float] = None
    # 平均空闲时长
    avg_idle: Optional[float] = None
    # 平均掉线时长
    avg_off_line: Optional[float] = None
    # 平均避障时长
    avg_pause: Optional[float] = None
    # 车辆数据集合
    state_statistics_histograms: Optional[list[U8f66u8f86u6570u636e]] = None
    # 总充电时长
    total_charging: Optional[float] = None
    # 总开动率
    total_efficiency: Optional[float] = None
    # 总异常时长
    total_exception: Optional[float] = None
    # 总执行时长
    total_executing: Optional[float] = None
    # 总空闲时长
    total_idle: Optional[float] = None
    # 总掉线时长
    total_off_line: Optional[float] = None
    # 总避障时长
    total_pause: Optional[float] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U72b6u6001u65f6u957fu7edfu8ba1u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U72b6u6001u65f6u957fu7edfu8ba1u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U72b6u6001u65f6u957fu7edfu8ba1u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        fields: dict[str, Callable[[Any], None]] = {
            "avgCharging": lambda n : setattr(self, 'avg_charging', n.get_float_value()),
            "avgException": lambda n : setattr(self, 'avg_exception', n.get_float_value()),
            "avgExecuting": lambda n : setattr(self, 'avg_executing', n.get_float_value()),
            "avgIdle": lambda n : setattr(self, 'avg_idle', n.get_float_value()),
            "avgOffLine": lambda n : setattr(self, 'avg_off_line', n.get_float_value()),
            "avgPause": lambda n : setattr(self, 'avg_pause', n.get_float_value()),
            "stateStatisticsHistograms": lambda n : setattr(self, 'state_statistics_histograms', n.get_collection_of_object_values(U8f66u8f86u6570u636e)),
            "totalCharging": lambda n : setattr(self, 'total_charging', n.get_float_value()),
            "totalEfficiency": lambda n : setattr(self, 'total_efficiency', n.get_float_value()),
            "totalException": lambda n : setattr(self, 'total_exception', n.get_float_value()),
            "totalExecuting": lambda n : setattr(self, 'total_executing', n.get_float_value()),
            "totalIdle": lambda n : setattr(self, 'total_idle', n.get_float_value()),
            "totalOffLine": lambda n : setattr(self, 'total_off_line', n.get_float_value()),
            "totalPause": lambda n : setattr(self, 'total_pause', n.get_float_value()),
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
        writer.write_float_value("avgCharging", self.avg_charging)
        writer.write_float_value("avgException", self.avg_exception)
        writer.write_float_value("avgExecuting", self.avg_executing)
        writer.write_float_value("avgIdle", self.avg_idle)
        writer.write_float_value("avgOffLine", self.avg_off_line)
        writer.write_float_value("avgPause", self.avg_pause)
        writer.write_collection_of_object_values("stateStatisticsHistograms", self.state_statistics_histograms)
        writer.write_float_value("totalCharging", self.total_charging)
        writer.write_float_value("totalEfficiency", self.total_efficiency)
        writer.write_float_value("totalException", self.total_exception)
        writer.write_float_value("totalExecuting", self.total_executing)
        writer.write_float_value("totalIdle", self.total_idle)
        writer.write_float_value("totalOffLine", self.total_off_line)
        writer.write_float_value("totalPause", self.total_pause)
        writer.write_additional_data_value(self.additional_data)
    

