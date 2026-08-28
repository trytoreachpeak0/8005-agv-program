from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .device_object import DeviceObject
    from .map_sync_record_object_map_sync_result import MapSyncRecordObject_mapSyncResult
    from .map_sync_record_object_map_sync_type import MapSyncRecordObject_mapSyncType

@dataclass
class MapSyncRecordObject(AdditionalDataHolder, Parsable):
    """
    地图同步记录表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 推送记录中的设备列表
    device_list: Optional[list[DeviceObject]] = None
    # 同步时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # 同步记录id
    id: Optional[int] = None
    # 同步记录地图名称
    map_name: Optional[str] = None
    # 同步结果
    map_sync_result: Optional[MapSyncRecordObject_mapSyncResult] = None
    # 同步来源
    map_sync_source: Optional[str] = None
    # 同步对象
    map_sync_target: Optional[str] = None
    # 同步的类型
    map_sync_type: Optional[MapSyncRecordObject_mapSyncType] = None
    # 同步备注
    note: Optional[str] = None
    # 操作者
    operator: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapSyncRecordObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapSyncRecordObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapSyncRecordObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .device_object import DeviceObject
        from .map_sync_record_object_map_sync_result import MapSyncRecordObject_mapSyncResult
        from .map_sync_record_object_map_sync_type import MapSyncRecordObject_mapSyncType

        from .device_object import DeviceObject
        from .map_sync_record_object_map_sync_result import MapSyncRecordObject_mapSyncResult
        from .map_sync_record_object_map_sync_type import MapSyncRecordObject_mapSyncType

        fields: dict[str, Callable[[Any], None]] = {
            "deviceList": lambda n : setattr(self, 'device_list', n.get_collection_of_object_values(DeviceObject)),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "mapSyncResult": lambda n : setattr(self, 'map_sync_result', n.get_enum_value(MapSyncRecordObject_mapSyncResult)),
            "mapSyncSource": lambda n : setattr(self, 'map_sync_source', n.get_str_value()),
            "mapSyncTarget": lambda n : setattr(self, 'map_sync_target', n.get_str_value()),
            "mapSyncType": lambda n : setattr(self, 'map_sync_type', n.get_enum_value(MapSyncRecordObject_mapSyncType)),
            "note": lambda n : setattr(self, 'note', n.get_str_value()),
            "operator": lambda n : setattr(self, 'operator', n.get_str_value()),
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
        writer.write_collection_of_object_values("deviceList", self.device_list)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_str_value("mapName", self.map_name)
        writer.write_enum_value("mapSyncResult", self.map_sync_result)
        writer.write_str_value("mapSyncSource", self.map_sync_source)
        writer.write_str_value("mapSyncTarget", self.map_sync_target)
        writer.write_enum_value("mapSyncType", self.map_sync_type)
        writer.write_str_value("note", self.note)
        writer.write_str_value("operator", self.operator)
        writer.write_additional_data_value(self.additional_data)
    

