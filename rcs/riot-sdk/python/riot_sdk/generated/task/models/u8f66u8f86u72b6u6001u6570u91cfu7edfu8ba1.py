from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .state_count_statistics_histogram import StateCountStatisticsHistogram

@dataclass
class U8f66u8f86u72b6u6001u6570u91cfu7edfu8ba1(AdditionalDataHolder, Parsable):
    """
    车辆状态数量统计
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 状态统计列表
    state_count_statistics_histograms: Optional[list[StateCountStatisticsHistogram]] = None
    # 总数
    total: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u72b6u6001u6570u91cfu7edfu8ba1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u72b6u6001u6570u91cfu7edfu8ba1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u72b6u6001u6570u91cfu7edfu8ba1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .state_count_statistics_histogram import StateCountStatisticsHistogram

        from .state_count_statistics_histogram import StateCountStatisticsHistogram

        fields: dict[str, Callable[[Any], None]] = {
            "stateCountStatisticsHistograms": lambda n : setattr(self, 'state_count_statistics_histograms', n.get_collection_of_object_values(StateCountStatisticsHistogram)),
            "total": lambda n : setattr(self, 'total', n.get_int_value()),
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
        writer.write_collection_of_object_values("stateCountStatisticsHistograms", self.state_count_statistics_histograms)
        writer.write_int_value("total", self.total)
        writer.write_additional_data_value(self.additional_data)
    

