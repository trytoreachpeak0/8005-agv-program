from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .map_resources import MapResources
    from .order_path import OrderPath

@dataclass
class U673au5668u4ebau8ba2u5355u8f68u8ff9(AdditionalDataHolder, Parsable):
    """
    机器人订单轨迹
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The currentTaskPath property
    current_task_path: Optional[MapResources] = None
    # The orderPath property
    order_path: Optional[OrderPath] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U673au5668u4ebau8ba2u5355u8f68u8ff9:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U673au5668u4ebau8ba2u5355u8f68u8ff9
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U673au5668u4ebau8ba2u5355u8f68u8ff9()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .map_resources import MapResources
        from .order_path import OrderPath

        from .map_resources import MapResources
        from .order_path import OrderPath

        fields: dict[str, Callable[[Any], None]] = {
            "currentTaskPath": lambda n : setattr(self, 'current_task_path', n.get_object_value(MapResources)),
            "orderPath": lambda n : setattr(self, 'order_path', n.get_object_value(OrderPath)),
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
        writer.write_object_value("currentTaskPath", self.current_task_path)
        writer.write_object_value("orderPath", self.order_path)
        writer.write_additional_data_value(self.additional_data)
    

