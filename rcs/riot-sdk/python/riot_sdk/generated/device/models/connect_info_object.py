from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class ConnectInfoObject(AdditionalDataHolder, Parsable):
    """
    设备连接配置表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 连接地址
    address: Optional[str] = None
    # The createBy property
    create_by: Optional[int] = None
    # The deleted property
    deleted: Optional[bool] = None
    # 详细
    detail: Optional[str] = None
    # 设备Key
    device_key: Optional[str] = None
    # The gmtCreate property
    gmt_create: Optional[datetime.datetime] = None
    # The gmtModified property
    gmt_modified: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # memberId主机ID
    member_id: Optional[str] = None
    # 记录时间
    record_time_stamp: Optional[datetime.datetime] = None
    # 类型
    type: Optional[str] = None
    # The updateBy property
    update_by: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ConnectInfoObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ConnectInfoObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ConnectInfoObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "address": lambda n : setattr(self, 'address', n.get_str_value()),
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "detail": lambda n : setattr(self, 'detail', n.get_str_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "memberId": lambda n : setattr(self, 'member_id', n.get_str_value()),
            "recordTimeStamp": lambda n : setattr(self, 'record_time_stamp', n.get_datetime_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
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
        writer.write_str_value("address", self.address)
        writer.write_int_value("createBy", self.create_by)
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("detail", self.detail)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_str_value("memberId", self.member_id)
        writer.write_datetime_value("recordTimeStamp", self.record_time_stamp)
        writer.write_str_value("type", self.type)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_additional_data_value(self.additional_data)
    

