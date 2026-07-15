from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .template_order_object import TemplateOrderObject

@dataclass
class Page_Of_TemplateOrderObject(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The countId property
    count_id: Optional[str] = None
    # The current property
    current: Optional[int] = None
    # The maxLimit property
    max_limit: Optional[int] = None
    # The optimizeCountSql property
    optimize_count_sql: Optional[bool] = None
    # The orders property
    orders: Optional[list[OrderItem]] = None
    # The pages property
    pages: Optional[int] = None
    # The records property
    records: Optional[list[TemplateOrderObject]] = None
    # The searchCount property
    search_count: Optional[bool] = None
    # The size property
    size: Optional[int] = None
    # The total property
    total: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Page_Of_TemplateOrderObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Page_Of_TemplateOrderObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Page_Of_TemplateOrderObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_item import OrderItem
        from .template_order_object import TemplateOrderObject

        from .order_item import OrderItem
        from .template_order_object import TemplateOrderObject

        fields: dict[str, Callable[[Any], None]] = {
            "countId": lambda n : setattr(self, 'count_id', n.get_str_value()),
            "current": lambda n : setattr(self, 'current', n.get_int_value()),
            "maxLimit": lambda n : setattr(self, 'max_limit', n.get_int_value()),
            "optimizeCountSql": lambda n : setattr(self, 'optimize_count_sql', n.get_bool_value()),
            "orders": lambda n : setattr(self, 'orders', n.get_collection_of_object_values(OrderItem)),
            "pages": lambda n : setattr(self, 'pages', n.get_int_value()),
            "records": lambda n : setattr(self, 'records', n.get_collection_of_object_values(TemplateOrderObject)),
            "searchCount": lambda n : setattr(self, 'search_count', n.get_bool_value()),
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
        writer.write_str_value("countId", self.count_id)
        writer.write_int_value("current", self.current)
        writer.write_int_value("maxLimit", self.max_limit)
        writer.write_bool_value("optimizeCountSql", self.optimize_count_sql)
        writer.write_collection_of_object_values("orders", self.orders)
        writer.write_int_value("pages", self.pages)
        writer.write_collection_of_object_values("records", self.records)
        writer.write_bool_value("searchCount", self.search_count)
        writer.write_int_value("size", self.size)
        writer.write_int_value("total", self.total)
        writer.write_additional_data_value(self.additional_data)
    

