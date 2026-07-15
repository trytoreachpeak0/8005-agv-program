from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .page_of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56de_object import Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject

@dataclass
class ResponseMsg_Of_Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The code property
    code: Optional[str] = None
    # The detail property
    detail: Optional[str] = None
    # The message property
    message: Optional[str] = None
    # The msgDetail property
    msg_detail: Optional[str] = None
    # The result property
    result: Optional[Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject] = None
    # The tid property
    tid: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ResponseMsg_Of_Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ResponseMsg_Of_Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ResponseMsg_Of_Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .page_of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56de_object import Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject

        from .page_of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56de_object import Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject

        fields: dict[str, Callable[[Any], None]] = {
            "code": lambda n : setattr(self, 'code', n.get_str_value()),
            "detail": lambda n : setattr(self, 'detail', n.get_str_value()),
            "message": lambda n : setattr(self, 'message', n.get_str_value()),
            "msgDetail": lambda n : setattr(self, 'msg_detail', n.get_str_value()),
            "result": lambda n : setattr(self, 'result', n.get_object_value(Page_Of_u8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject)),
            "tid": lambda n : setattr(self, 'tid', n.get_str_value()),
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
        writer.write_str_value("code", self.code)
        writer.write_str_value("detail", self.detail)
        writer.write_str_value("message", self.message)
        writer.write_str_value("msgDetail", self.msg_detail)
        writer.write_object_value("result", self.result)
        writer.write_str_value("tid", self.tid)
        writer.write_additional_data_value(self.additional_data)
    

