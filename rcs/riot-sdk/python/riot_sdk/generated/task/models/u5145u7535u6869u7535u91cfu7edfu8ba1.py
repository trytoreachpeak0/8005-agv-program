from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u5145u7535u6869u6570u636e import U5145u7535u6869u6570u636e

@dataclass
class U5145u7535u6869u7535u91cfu7edfu8ba1(AdditionalDataHolder, Parsable):
    """
    充电桩电量统计
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 平均充电次数
    avg_charge_location_count: Optional[float] = None
    # 平均充电时长
    avg_charge_location_time: Optional[float] = None
    # 充电桩数据集合
    charge_location_statistics_histograms: Optional[list[U5145u7535u6869u6570u636e]] = None
    # 总充电次数
    total_charge_location_count: Optional[float] = None
    # 总充电时长
    total_charge_location_time: Optional[float] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U5145u7535u6869u7535u91cfu7edfu8ba1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U5145u7535u6869u7535u91cfu7edfu8ba1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U5145u7535u6869u7535u91cfu7edfu8ba1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u5145u7535u6869u6570u636e import U5145u7535u6869u6570u636e

        from .u5145u7535u6869u6570u636e import U5145u7535u6869u6570u636e

        fields: dict[str, Callable[[Any], None]] = {
            "avgChargeLocationCount": lambda n : setattr(self, 'avg_charge_location_count', n.get_float_value()),
            "avgChargeLocationTime": lambda n : setattr(self, 'avg_charge_location_time', n.get_float_value()),
            "chargeLocationStatisticsHistograms": lambda n : setattr(self, 'charge_location_statistics_histograms', n.get_collection_of_object_values(U5145u7535u6869u6570u636e)),
            "totalChargeLocationCount": lambda n : setattr(self, 'total_charge_location_count', n.get_float_value()),
            "totalChargeLocationTime": lambda n : setattr(self, 'total_charge_location_time', n.get_float_value()),
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
        writer.write_float_value("avgChargeLocationCount", self.avg_charge_location_count)
        writer.write_float_value("avgChargeLocationTime", self.avg_charge_location_time)
        writer.write_collection_of_object_values("chargeLocationStatisticsHistograms", self.charge_location_statistics_histograms)
        writer.write_float_value("totalChargeLocationCount", self.total_charge_location_count)
        writer.write_float_value("totalChargeLocationTime", self.total_charge_location_time)
        writer.write_additional_data_value(self.additional_data)
    

