from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .http_callback_form import HttpCallback_form
    from .http_callback_header import HttpCallback_header
    from .http_callback_request_method import HttpCallback_requestMethod

@dataclass
class HttpCallback(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The body property
    body: Optional[str] = None
    # The contentType property
    content_type: Optional[str] = None
    # The expireTime property
    expire_time: Optional[int] = None
    # The form property
    form: Optional[HttpCallback_form] = None
    # The header property
    header: Optional[HttpCallback_header] = None
    # The requestMethod property
    request_method: Optional[HttpCallback_requestMethod] = None
    # The timeout property
    timeout: Optional[int] = None
    # The url property
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HttpCallback:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HttpCallback
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return HttpCallback()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .http_callback_form import HttpCallback_form
        from .http_callback_header import HttpCallback_header
        from .http_callback_request_method import HttpCallback_requestMethod

        from .http_callback_form import HttpCallback_form
        from .http_callback_header import HttpCallback_header
        from .http_callback_request_method import HttpCallback_requestMethod

        fields: dict[str, Callable[[Any], None]] = {
            "body": lambda n : setattr(self, 'body', n.get_str_value()),
            "contentType": lambda n : setattr(self, 'content_type', n.get_str_value()),
            "expireTime": lambda n : setattr(self, 'expire_time', n.get_int_value()),
            "form": lambda n : setattr(self, 'form', n.get_object_value(HttpCallback_form)),
            "header": lambda n : setattr(self, 'header', n.get_object_value(HttpCallback_header)),
            "requestMethod": lambda n : setattr(self, 'request_method', n.get_enum_value(HttpCallback_requestMethod)),
            "timeout": lambda n : setattr(self, 'timeout', n.get_int_value()),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
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
        writer.write_str_value("body", self.body)
        writer.write_str_value("contentType", self.content_type)
        writer.write_int_value("expireTime", self.expire_time)
        writer.write_object_value("form", self.form)
        writer.write_object_value("header", self.header)
        writer.write_enum_value("requestMethod", self.request_method)
        writer.write_int_value("timeout", self.timeout)
        writer.write_str_value("url", self.url)
        writer.write_additional_data_value(self.additional_data)
    

