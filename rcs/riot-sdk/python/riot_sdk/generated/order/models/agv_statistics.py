from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agv_sub_statistics import AgvSubStatistics

@dataclass
class AgvStatistics(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The agvSubStatistics property
    agv_sub_statistics: Optional[list[AgvSubStatistics]] = None
    # The chargeOrderFinishedCount property
    charge_order_finished_count: Optional[int] = None
    # The maintainOrderFinishedCount property
    maintain_order_finished_count: Optional[int] = None
    # The orderAvgExecTime property
    order_avg_exec_time: Optional[float] = None
    # The orderAvgTime property
    order_avg_time: Optional[float] = None
    # The orderAvgWaitExecTime property
    order_avg_wait_exec_time: Optional[float] = None
    # The orderCancelCount property
    order_cancel_count: Optional[int] = None
    # The orderCount property
    order_count: Optional[int] = None
    # The orderFailCount property
    order_fail_count: Optional[int] = None
    # The orderFinishedCount property
    order_finished_count: Optional[int] = None
    # The parkOrderFinishedCount property
    park_order_finished_count: Optional[int] = None
    # The workOrderFinishedCount property
    work_order_finished_count: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AgvStatistics:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AgvStatistics
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AgvStatistics()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .agv_sub_statistics import AgvSubStatistics

        from .agv_sub_statistics import AgvSubStatistics

        fields: dict[str, Callable[[Any], None]] = {
            "agvSubStatistics": lambda n : setattr(self, 'agv_sub_statistics', n.get_collection_of_object_values(AgvSubStatistics)),
            "chargeOrderFinishedCount": lambda n : setattr(self, 'charge_order_finished_count', n.get_int_value()),
            "maintainOrderFinishedCount": lambda n : setattr(self, 'maintain_order_finished_count', n.get_int_value()),
            "orderAvgExecTime": lambda n : setattr(self, 'order_avg_exec_time', n.get_float_value()),
            "orderAvgTime": lambda n : setattr(self, 'order_avg_time', n.get_float_value()),
            "orderAvgWaitExecTime": lambda n : setattr(self, 'order_avg_wait_exec_time', n.get_float_value()),
            "orderCancelCount": lambda n : setattr(self, 'order_cancel_count', n.get_int_value()),
            "orderCount": lambda n : setattr(self, 'order_count', n.get_int_value()),
            "orderFailCount": lambda n : setattr(self, 'order_fail_count', n.get_int_value()),
            "orderFinishedCount": lambda n : setattr(self, 'order_finished_count', n.get_int_value()),
            "parkOrderFinishedCount": lambda n : setattr(self, 'park_order_finished_count', n.get_int_value()),
            "workOrderFinishedCount": lambda n : setattr(self, 'work_order_finished_count', n.get_int_value()),
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
        writer.write_collection_of_object_values("agvSubStatistics", self.agv_sub_statistics)
        writer.write_int_value("chargeOrderFinishedCount", self.charge_order_finished_count)
        writer.write_int_value("maintainOrderFinishedCount", self.maintain_order_finished_count)
        writer.write_float_value("orderAvgExecTime", self.order_avg_exec_time)
        writer.write_float_value("orderAvgTime", self.order_avg_time)
        writer.write_float_value("orderAvgWaitExecTime", self.order_avg_wait_exec_time)
        writer.write_int_value("orderCancelCount", self.order_cancel_count)
        writer.write_int_value("orderCount", self.order_count)
        writer.write_int_value("orderFailCount", self.order_fail_count)
        writer.write_int_value("orderFinishedCount", self.order_finished_count)
        writer.write_int_value("parkOrderFinishedCount", self.park_order_finished_count)
        writer.write_int_value("workOrderFinishedCount", self.work_order_finished_count)
        writer.write_additional_data_value(self.additional_data)
    

