from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_command_d_t_o_object_command_type import OrderCommandDTOObject_commandType

@dataclass
class OrderCommandDTOObject(AdditionalDataHolder, Parsable):
    """
    订单具体操作
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 订单操作类型
    command_type: Optional[OrderCommandDTOObject_commandType] = None
    # 是否下线车辆
    disable_vehicle: Optional[bool] = None
    # 原因
    reason: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderCommandDTOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderCommandDTOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderCommandDTOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_command_d_t_o_object_command_type import OrderCommandDTOObject_commandType

        from .order_command_d_t_o_object_command_type import OrderCommandDTOObject_commandType

        fields: dict[str, Callable[[Any], None]] = {
            "commandType": lambda n : setattr(self, 'command_type', n.get_enum_value(OrderCommandDTOObject_commandType)),
            "disableVehicle": lambda n : setattr(self, 'disable_vehicle', n.get_bool_value()),
            "reason": lambda n : setattr(self, 'reason', n.get_str_value()),
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
        writer.write_enum_value("commandType", self.command_type)
        writer.write_bool_value("disableVehicle", self.disable_vehicle)
        writer.write_str_value("reason", self.reason)
        writer.write_additional_data_value(self.additional_data)
    

