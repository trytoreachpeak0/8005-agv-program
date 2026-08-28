from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .tag_page_vo import TagPageVo

@dataclass
class TemplateOrderTagPageVOObject(AdditionalDataHolder, Parsable):
    """
    分页查询模板标签返回给前端的实体类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The current property
    current: Optional[int] = None
    # The pages property
    pages: Optional[int] = None
    # The records property
    records: Optional[list[TagPageVo]] = None
    # The size property
    size: Optional[int] = None
    # The total property
    total: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateOrderTagPageVOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateOrderTagPageVOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateOrderTagPageVOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .tag_page_vo import TagPageVo

        from .tag_page_vo import TagPageVo

        fields: dict[str, Callable[[Any], None]] = {
            "current": lambda n : setattr(self, 'current', n.get_int_value()),
            "pages": lambda n : setattr(self, 'pages', n.get_int_value()),
            "records": lambda n : setattr(self, 'records', n.get_collection_of_object_values(TagPageVo)),
            "size": lambda n : setattr(self, 'size', n.get_int_value()),
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
        writer.write_int_value("current", self.current)
        writer.write_int_value("pages", self.pages)
        writer.write_collection_of_object_values("records", self.records)
        writer.write_int_value("size", self.size)
        writer.write_int_value("total", self.total)
        writer.write_additional_data_value(self.additional_data)
    

