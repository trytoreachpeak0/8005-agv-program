from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u6587u4ef6u540du79f0_type import U8f66u8f86u6587u4ef6u540du79f0_type

@dataclass
class U8f66u8f86u6587u4ef6u540du79f0(AdditionalDataHolder, Parsable):
    """
    车辆文件名称
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建人
    create_by: Optional[int] = None
    # 文件名
    file_name: Optional[str] = None
    # 文件url
    file_url: Optional[str] = None
    # 记录生成时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 自增id
    id: Optional[int] = None
    # 文件类型
    type: Optional[U8f66u8f86u6587u4ef6u540du79f0_type] = None
    # 更新人
    update_by: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u6587u4ef6u540du79f0:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u6587u4ef6u540du79f0
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u6587u4ef6u540du79f0()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u6587u4ef6u540du79f0_type import U8f66u8f86u6587u4ef6u540du79f0_type

        from .u8f66u8f86u6587u4ef6u540du79f0_type import U8f66u8f86u6587u4ef6u540du79f0_type

        fields: dict[str, Callable[[Any], None]] = {
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "fileName": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "fileUrl": lambda n : setattr(self, 'file_url', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(U8f66u8f86u6587u4ef6u540du79f0_type)),
            "updateBy": lambda n : setattr(self, 'update_by', n.get_int_value()),
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
        writer.write_int_value("createBy", self.create_by)
        writer.write_str_value("fileName", self.file_name)
        writer.write_str_value("fileUrl", self.file_url)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_enum_value("type", self.type)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_additional_data_value(self.additional_data)
    

