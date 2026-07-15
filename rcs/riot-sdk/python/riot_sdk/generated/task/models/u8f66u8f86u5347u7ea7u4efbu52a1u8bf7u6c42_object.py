from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U8f66u8f86u5347u7ea7u4efbu52a1u8bf7u6c42Object(AdditionalDataHolder, Parsable):
    """
    车辆升级任务请求对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆集合
    device_keys: Optional[list[str]] = None
    # 文件名称
    file_name: Optional[str] = None
    # 任务类型(SROS_SYNC，SRC_SYNC)
    vehicle_sync_task_type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u5347u7ea7u4efbu52a1u8bf7u6c42Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u5347u7ea7u4efbu52a1u8bf7u6c42Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u5347u7ea7u4efbu52a1u8bf7u6c42Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "deviceKeys": lambda n : setattr(self, 'device_keys', n.get_collection_of_primitive_values(str)),
            "fileName": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "vehicleSyncTaskType": lambda n : setattr(self, 'vehicle_sync_task_type', n.get_str_value()),
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
        writer.write_collection_of_primitive_values("deviceKeys", self.device_keys)
        writer.write_str_value("fileName", self.file_name)
        writer.write_str_value("vehicleSyncTaskType", self.vehicle_sync_task_type)
        writer.write_additional_data_value(self.additional_data)
    

