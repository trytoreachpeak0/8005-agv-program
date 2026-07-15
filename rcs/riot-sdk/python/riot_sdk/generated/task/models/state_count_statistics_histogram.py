from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .state_count_statistics_histogram_agv_statistics_state import StateCountStatisticsHistogram_agvStatisticsState

@dataclass
class StateCountStatisticsHistogram(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 状态
    agv_statistics_state: Optional[StateCountStatisticsHistogram_agvStatisticsState] = None
    # 数量
    count: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> StateCountStatisticsHistogram:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: StateCountStatisticsHistogram
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return StateCountStatisticsHistogram()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .state_count_statistics_histogram_agv_statistics_state import StateCountStatisticsHistogram_agvStatisticsState

        from .state_count_statistics_histogram_agv_statistics_state import StateCountStatisticsHistogram_agvStatisticsState

        fields: dict[str, Callable[[Any], None]] = {
            "agvStatisticsState": lambda n : setattr(self, 'agv_statistics_state', n.get_enum_value(StateCountStatisticsHistogram_agvStatisticsState)),
            "count": lambda n : setattr(self, 'count', n.get_int_value()),
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
        writer.write_enum_value("agvStatisticsState", self.agv_statistics_state)
        writer.write_int_value("count", self.count)
        writer.write_additional_data_value(self.additional_data)
    

