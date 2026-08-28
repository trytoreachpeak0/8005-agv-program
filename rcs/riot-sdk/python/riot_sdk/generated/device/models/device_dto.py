from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .connect_info_object import ConnectInfoObject
    from .device_object import DeviceObject
    from .product_object import ProductObject
    from .thing_model import ThingModel

@dataclass
class DeviceDto(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The condition property
    condition: Optional[str] = None
    # 设备连接配置表
    connect_info: Optional[ConnectInfoObject] = None
    # 设备信息
    device: Optional[DeviceObject] = None
    # The deviceTypes property
    device_types: Optional[list[int]] = None
    # The ids property
    ids: Optional[list[int]] = None
    # The isBrokerxManager property
    is_brokerx_manager: Optional[bool] = None
    # 产品表
    product: Optional[ProductObject] = None
    # The productKeys property
    product_keys: Optional[list[str]] = None
    # The thingModel property
    thing_model: Optional[ThingModel] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DeviceDto:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeviceDto
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DeviceDto()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .connect_info_object import ConnectInfoObject
        from .device_object import DeviceObject
        from .product_object import ProductObject
        from .thing_model import ThingModel

        from .connect_info_object import ConnectInfoObject
        from .device_object import DeviceObject
        from .product_object import ProductObject
        from .thing_model import ThingModel

        fields: dict[str, Callable[[Any], None]] = {
            "condition": lambda n : setattr(self, 'condition', n.get_str_value()),
            "connectInfo": lambda n : setattr(self, 'connect_info', n.get_object_value(ConnectInfoObject)),
            "device": lambda n : setattr(self, 'device', n.get_object_value(DeviceObject)),
            "deviceTypes": lambda n : setattr(self, 'device_types', n.get_collection_of_primitive_values(int)),
            "ids": lambda n : setattr(self, 'ids', n.get_collection_of_primitive_values(int)),
            "isBrokerxManager": lambda n : setattr(self, 'is_brokerx_manager', n.get_bool_value()),
            "product": lambda n : setattr(self, 'product', n.get_object_value(ProductObject)),
            "productKeys": lambda n : setattr(self, 'product_keys', n.get_collection_of_primitive_values(str)),
            "thingModel": lambda n : setattr(self, 'thing_model', n.get_object_value(ThingModel)),
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
        writer.write_str_value("condition", self.condition)
        writer.write_object_value("connectInfo", self.connect_info)
        writer.write_object_value("device", self.device)
        writer.write_collection_of_primitive_values("deviceTypes", self.device_types)
        writer.write_collection_of_primitive_values("ids", self.ids)
        writer.write_bool_value("isBrokerxManager", self.is_brokerx_manager)
        writer.write_object_value("product", self.product)
        writer.write_collection_of_primitive_values("productKeys", self.product_keys)
        writer.write_object_value("thingModel", self.thing_model)
        writer.write_additional_data_value(self.additional_data)
    

