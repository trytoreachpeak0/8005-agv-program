from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class DeviceGroupObject(AdditionalDataHolder, Parsable):
    """
    设备组信息
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建人
    create_by: Optional[int] = None
    # 是否删除
    deleted: Optional[bool] = None
    # 车辆组名
    device_group_name: Optional[str] = None
    # 自增id
    id: Optional[int] = None
    # 长
    length: Optional[int] = None
    # 载货时长
    length_loaded: Optional[int] = None
    # 描述
    remark: Optional[str] = None
    # 类型
    type: Optional[int] = None
    # 更新人
    update_by: Optional[int] = None
    # 宽
    width: Optional[int] = None
    # 载货时宽
    width_loaded: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DeviceGroupObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeviceGroupObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DeviceGroupObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "deviceGroupName": lambda n : setattr(self, 'device_group_name', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "length": lambda n : setattr(self, 'length', n.get_int_value()),
            "lengthLoaded": lambda n : setattr(self, 'length_loaded', n.get_int_value()),
            "remark": lambda n : setattr(self, 'remark', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_int_value()),
            "updateBy": lambda n : setattr(self, 'update_by', n.get_int_value()),
            "width": lambda n : setattr(self, 'width', n.get_int_value()),
            "widthLoaded": lambda n : setattr(self, 'width_loaded', n.get_int_value()),
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
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("deviceGroupName", self.device_group_name)
        writer.write_int_value("id", self.id)
        writer.write_int_value("length", self.length)
        writer.write_int_value("lengthLoaded", self.length_loaded)
        writer.write_str_value("remark", self.remark)
        writer.write_int_value("type", self.type)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_int_value("width", self.width)
        writer.write_int_value("widthLoaded", self.width_loaded)
        writer.write_additional_data_value(self.additional_data)
    

