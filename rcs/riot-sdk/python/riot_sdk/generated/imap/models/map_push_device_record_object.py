from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .map_push_device_record_object_sync_result import MapPushDeviceRecordObject_syncResult

@dataclass
class MapPushDeviceRecordObject(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 设备请求端口
    device_host_port: Optional[str] = None
    # 设备唯一标识
    device_id: Optional[int] = None
    # The deviceName property
    device_name: Optional[str] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 修改时间
    gmt_update: Optional[datetime.datetime] = None
    # 推送记录id 
    id: Optional[int] = None
    # 推送地图id
    map_id: Optional[int] = None
    # 推送地图名称
    map_name: Optional[str] = None
    # 推送进度
    progress: Optional[int] = None
    # 地图同步记录id
    sync_record_id: Optional[int] = None
    # 推送结果
    sync_result: Optional[MapPushDeviceRecordObject_syncResult] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapPushDeviceRecordObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapPushDeviceRecordObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapPushDeviceRecordObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .map_push_device_record_object_sync_result import MapPushDeviceRecordObject_syncResult

        from .map_push_device_record_object_sync_result import MapPushDeviceRecordObject_syncResult

        fields: dict[str, Callable[[Any], None]] = {
            "deviceHostPort": lambda n : setattr(self, 'device_host_port', n.get_str_value()),
            "deviceId": lambda n : setattr(self, 'device_id', n.get_int_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_int_value()),
            "syncRecordId": lambda n : setattr(self, 'sync_record_id', n.get_int_value()),
            "syncResult": lambda n : setattr(self, 'sync_result', n.get_enum_value(MapPushDeviceRecordObject_syncResult)),
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
        writer.write_str_value("deviceHostPort", self.device_host_port)
        writer.write_int_value("deviceId", self.device_id)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("mapName", self.map_name)
        writer.write_int_value("progress", self.progress)
        writer.write_int_value("syncRecordId", self.sync_record_id)
        writer.write_enum_value("syncResult", self.sync_result)
        writer.write_additional_data_value(self.additional_data)
    

