from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MovementState(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The avoidPolicy property
    avoid_policy: Optional[int] = None
    # The curCheckpointNo property
    cur_checkpoint_no: Optional[int] = None
    # The curPathNo property
    cur_path_no: Optional[int] = None
    # The dstStationType property
    dst_station_type: Optional[int] = None
    # The no property
    no: Optional[int] = None
    # The remainDistance property
    remain_distance: Optional[int] = None
    # The remainTime property
    remain_time: Optional[int] = None
    # The state property
    state: Optional[int] = None
    # The taskResult property
    task_result: Optional[int] = None
    # The totalDistance property
    total_distance: Optional[int] = None
    # The type property
    type: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MovementState:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MovementState
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MovementState()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "avoidPolicy": lambda n : setattr(self, 'avoid_policy', n.get_int_value()),
            "curCheckpointNo": lambda n : setattr(self, 'cur_checkpoint_no', n.get_int_value()),
            "curPathNo": lambda n : setattr(self, 'cur_path_no', n.get_int_value()),
            "dstStationType": lambda n : setattr(self, 'dst_station_type', n.get_int_value()),
            "no": lambda n : setattr(self, 'no', n.get_int_value()),
            "remainDistance": lambda n : setattr(self, 'remain_distance', n.get_int_value()),
            "remainTime": lambda n : setattr(self, 'remain_time', n.get_int_value()),
            "state": lambda n : setattr(self, 'state', n.get_int_value()),
            "taskResult": lambda n : setattr(self, 'task_result', n.get_int_value()),
            "totalDistance": lambda n : setattr(self, 'total_distance', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_int_value()),
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
        writer.write_int_value("avoidPolicy", self.avoid_policy)
        writer.write_int_value("curCheckpointNo", self.cur_checkpoint_no)
        writer.write_int_value("curPathNo", self.cur_path_no)
        writer.write_int_value("dstStationType", self.dst_station_type)
        writer.write_int_value("no", self.no)
        writer.write_int_value("remainDistance", self.remain_distance)
        writer.write_int_value("remainTime", self.remain_time)
        writer.write_int_value("state", self.state)
        writer.write_int_value("taskResult", self.task_result)
        writer.write_int_value("totalDistance", self.total_distance)
        writer.write_int_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

