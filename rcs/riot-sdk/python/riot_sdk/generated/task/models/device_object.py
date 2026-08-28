from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class DeviceObject(AdditionalDataHolder, Parsable):
    """
    设备信息
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建人
    create_by: Optional[int] = None
    # 是否删除
    deleted: Optional[bool] = None
    # 设备Key
    device_key: Optional[str] = None
    # [require] 备注名
    device_name: Optional[str] = None
    # 设备密钥
    device_secret: Optional[str] = None
    # 设备序列号
    device_serial_no: Optional[str] = None
    # 设备类型;1:AGV 2:生产设备 3:非生产设备
    device_type: Optional[str] = None
    # 是否禁用
    enable: Optional[bool] = None
    # 启用、禁用修改时间
    enable_update_time: Optional[datetime.datetime] = None
    # 记录生成时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 设备作为server端时需要指定，ip:port
    host_port: Optional[str] = None
    # 自增id
    id: Optional[int] = None
    # 设备状态上报时间
    last_status_report_time: Optional[datetime.datetime] = None
    # 产品型号
    model: Optional[str] = None
    # 物模型版本号
    model_version: Optional[str] = None
    # 节点类型
    node_type: Optional[int] = None
    # 父产品名称（网关）
    parent_device_key: Optional[str] = None
    # 设备作为client端时需要指定，设备物理id,如mac地址、ip
    physics_id: Optional[str] = None
    # [require] 关联产品Key
    product_key: Optional[str] = None
    # 设备说明
    remark_name: Optional[str] = None
    # 产品系列
    series: Optional[str] = None
    # 设备上下线状态
    status: Optional[int] = None
    # 更新人
    update_by: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DeviceObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeviceObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DeviceObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "deviceSecret": lambda n : setattr(self, 'device_secret', n.get_str_value()),
            "deviceSerialNo": lambda n : setattr(self, 'device_serial_no', n.get_str_value()),
            "deviceType": lambda n : setattr(self, 'device_type', n.get_str_value()),
            "enable": lambda n : setattr(self, 'enable', n.get_bool_value()),
            "enableUpdateTime": lambda n : setattr(self, 'enable_update_time', n.get_datetime_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "hostPort": lambda n : setattr(self, 'host_port', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "lastStatusReportTime": lambda n : setattr(self, 'last_status_report_time', n.get_datetime_value()),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
            "modelVersion": lambda n : setattr(self, 'model_version', n.get_str_value()),
            "nodeType": lambda n : setattr(self, 'node_type', n.get_int_value()),
            "parentDeviceKey": lambda n : setattr(self, 'parent_device_key', n.get_str_value()),
            "physicsId": lambda n : setattr(self, 'physics_id', n.get_str_value()),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "remarkName": lambda n : setattr(self, 'remark_name', n.get_str_value()),
            "series": lambda n : setattr(self, 'series', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
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
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("deviceSecret", self.device_secret)
        writer.write_str_value("deviceSerialNo", self.device_serial_no)
        writer.write_str_value("deviceType", self.device_type)
        writer.write_bool_value("enable", self.enable)
        writer.write_datetime_value("enableUpdateTime", self.enable_update_time)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_str_value("hostPort", self.host_port)
        writer.write_int_value("id", self.id)
        writer.write_datetime_value("lastStatusReportTime", self.last_status_report_time)
        writer.write_str_value("model", self.model)
        writer.write_str_value("modelVersion", self.model_version)
        writer.write_int_value("nodeType", self.node_type)
        writer.write_str_value("parentDeviceKey", self.parent_device_key)
        writer.write_str_value("physicsId", self.physics_id)
        writer.write_str_value("productKey", self.product_key)
        writer.write_str_value("remarkName", self.remark_name)
        writer.write_str_value("series", self.series)
        writer.write_int_value("status", self.status)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_additional_data_value(self.additional_data)
    

