from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class ProductTypesObject(AdditionalDataHolder, Parsable):
    """
    产品分类表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建用户
    created_by: Optional[str] = None
    # 逻辑删除
    deleted: Optional[bool] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 主键ID
    id: Optional[int] = None
    # 更新用户
    modified_by: Optional[str] = None
    # 父类ID
    parent_id: Optional[int] = None
    # 类型名
    type_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ProductTypesObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ProductTypesObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ProductTypesObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "parentId": lambda n : setattr(self, 'parent_id', n.get_int_value()),
            "typeName": lambda n : setattr(self, 'type_name', n.get_str_value()),
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
        writer.write_str_value("createdBy", self.created_by)
        writer.write_bool_value("deleted", self.deleted)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_int_value("parentId", self.parent_id)
        writer.write_str_value("typeName", self.type_name)
        writer.write_additional_data_value(self.additional_data)
    

