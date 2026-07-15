from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_command_d_t_o_object import OrderCommandDTOObject

@dataclass
class OperateOrderDTOObject(AdditionalDataHolder, Parsable):
    """
    默认的operateOrder对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 订单具体操作
    order_command_d_t_o: Optional[OrderCommandDTOObject] = None
    # 订单id
    order_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OperateOrderDTOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OperateOrderDTOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OperateOrderDTOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_command_d_t_o_object import OrderCommandDTOObject

        from .order_command_d_t_o_object import OrderCommandDTOObject

        fields: dict[str, Callable[[Any], None]] = {
            "orderCommandDTO": lambda n : setattr(self, 'order_command_d_t_o', n.get_object_value(OrderCommandDTOObject)),
            "orderId": lambda n : setattr(self, 'order_id', n.get_int_value()),
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
        writer.write_object_value("orderCommandDTO", self.order_command_d_t_o)
        writer.write_int_value("orderId", self.order_id)
        writer.write_additional_data_value(self.additional_data)
    

