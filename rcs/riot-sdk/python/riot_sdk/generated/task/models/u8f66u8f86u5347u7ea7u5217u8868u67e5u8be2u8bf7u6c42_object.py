from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u6761u4ef6_object import U8f66u8f86u6761u4ef6Object

@dataclass
class U8f66u8f86u5347u7ea7u5217u8868u67e5u8be2u8bf7u6c42Object(AdditionalDataHolder, Parsable):
    """
    车辆升级列表查询请求对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆组id集合
    group_ids: Optional[list[int]] = None
    # 页码
    page_num: Optional[int] = None
    # 页尺寸(page:1,size:-1查询所有)
    page_size: Optional[int] = None
    # 车辆条件对象
    query_device_dto: Optional[U8f66u8f86u6761u4ef6Object] = None
    # 任务类型(SROS_SYNC，SRC_SYNC)
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u5347u7ea7u5217u8868u67e5u8be2u8bf7u6c42Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u5347u7ea7u5217u8868u67e5u8be2u8bf7u6c42Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u5347u7ea7u5217u8868u67e5u8be2u8bf7u6c42Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u6761u4ef6_object import U8f66u8f86u6761u4ef6Object

        from .u8f66u8f86u6761u4ef6_object import U8f66u8f86u6761u4ef6Object

        fields: dict[str, Callable[[Any], None]] = {
            "groupIds": lambda n : setattr(self, 'group_ids', n.get_collection_of_primitive_values(int)),
            "pageNum": lambda n : setattr(self, 'page_num', n.get_int_value()),
            "pageSize": lambda n : setattr(self, 'page_size', n.get_int_value()),
            "queryDeviceDto": lambda n : setattr(self, 'query_device_dto', n.get_object_value(U8f66u8f86u6761u4ef6Object)),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
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
        writer.write_collection_of_primitive_values("groupIds", self.group_ids)
        writer.write_int_value("pageNum", self.page_num)
        writer.write_int_value("pageSize", self.page_size)
        writer.write_object_value("queryDeviceDto", self.query_device_dto)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

