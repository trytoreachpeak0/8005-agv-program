from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

@dataclass
class U8f66u8f86u7535u91cfu7edfu8ba1(AdditionalDataHolder, Parsable):
    """
    车辆电量统计
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 平均电量
    avg_battery: Optional[int] = None
    # 平均充电次数
    avg_charge_count: Optional[int] = None
    # 平均充电时长
    avg_charge_time: Optional[int] = None
    # 车辆充电数据集合
    charge_statistics_histograms: Optional[list[U8f66u8f86u6570u636e]] = None
    # 总充电次数
    total_charge_count: Optional[int] = None
    # 总充电时长
    total_charge_time: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u7535u91cfu7edfu8ba1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u7535u91cfu7edfu8ba1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u7535u91cfu7edfu8ba1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        from .u8f66u8f86u6570u636e import U8f66u8f86u6570u636e

        fields: dict[str, Callable[[Any], None]] = {
            "avgBattery": lambda n : setattr(self, 'avg_battery', n.get_int_value()),
            "avgChargeCount": lambda n : setattr(self, 'avg_charge_count', n.get_int_value()),
            "avgChargeTime": lambda n : setattr(self, 'avg_charge_time', n.get_int_value()),
            "chargeStatisticsHistograms": lambda n : setattr(self, 'charge_statistics_histograms', n.get_collection_of_object_values(U8f66u8f86u6570u636e)),
            "totalChargeCount": lambda n : setattr(self, 'total_charge_count', n.get_int_value()),
            "totalChargeTime": lambda n : setattr(self, 'total_charge_time', n.get_int_value()),
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
        writer.write_int_value("avgBattery", self.avg_battery)
        writer.write_int_value("avgChargeCount", self.avg_charge_count)
        writer.write_int_value("avgChargeTime", self.avg_charge_time)
        writer.write_collection_of_object_values("chargeStatisticsHistograms", self.charge_statistics_histograms)
        writer.write_int_value("totalChargeCount", self.total_charge_count)
        writer.write_int_value("totalChargeTime", self.total_charge_time)
        writer.write_additional_data_value(self.additional_data)
    

