from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .client import Client
    from .srlink_message_data import SrlinkMessage_data
    from .srlink_message_ftype import SrlinkMessage_ftype
    from .srlink_message_params import SrlinkMessage_params
    from .sys_info import SysInfo

@dataclass
class SrlinkMessage(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The client property
    client: Optional[Client] = None
    # The code property
    code: Optional[int] = None
    # The data property
    data: Optional[SrlinkMessage_data] = None
    # The ftype property
    ftype: Optional[SrlinkMessage_ftype] = None
    # The id property
    id: Optional[str] = None
    # The message property
    message: Optional[str] = None
    # The method property
    method: Optional[str] = None
    # The params property
    params: Optional[SrlinkMessage_params] = None
    # The subDevice property
    sub_device: Optional[list[SrlinkMessage]] = None
    # The sysInfo property
    sys_info: Optional[SysInfo] = None
    # The timestamp property
    timestamp: Optional[int] = None
    # The type property
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SrlinkMessage:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SrlinkMessage
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SrlinkMessage()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .client import Client
        from .srlink_message_data import SrlinkMessage_data
        from .srlink_message_ftype import SrlinkMessage_ftype
        from .srlink_message_params import SrlinkMessage_params
        from .sys_info import SysInfo

        from .client import Client
        from .srlink_message_data import SrlinkMessage_data
        from .srlink_message_ftype import SrlinkMessage_ftype
        from .srlink_message_params import SrlinkMessage_params
        from .sys_info import SysInfo

        fields: dict[str, Callable[[Any], None]] = {
            "client": lambda n : setattr(self, 'client', n.get_object_value(Client)),
            "code": lambda n : setattr(self, 'code', n.get_int_value()),
            "data": lambda n : setattr(self, 'data', n.get_object_value(SrlinkMessage_data)),
            "ftype": lambda n : setattr(self, 'ftype', n.get_enum_value(SrlinkMessage_ftype)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "message": lambda n : setattr(self, 'message', n.get_str_value()),
            "method": lambda n : setattr(self, 'method', n.get_str_value()),
            "params": lambda n : setattr(self, 'params', n.get_object_value(SrlinkMessage_params)),
            "subDevice": lambda n : setattr(self, 'sub_device', n.get_collection_of_object_values(SrlinkMessage)),
            "sysInfo": lambda n : setattr(self, 'sys_info', n.get_object_value(SysInfo)),
            "timestamp": lambda n : setattr(self, 'timestamp', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
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
        writer.write_object_value("client", self.client)
        writer.write_int_value("code", self.code)
        writer.write_object_value("data", self.data)
        writer.write_enum_value("ftype", self.ftype)
        writer.write_str_value("id", self.id)
        writer.write_str_value("message", self.message)
        writer.write_str_value("method", self.method)
        writer.write_object_value("params", self.params)
        writer.write_collection_of_object_values("subDevice", self.sub_device)
        writer.write_object_value("sysInfo", self.sys_info)
        writer.write_int_value("timestamp", self.timestamp)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

