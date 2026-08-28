from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .device_object import DeviceObject
    from .vehicle_setting_v_o_item_map import VehicleSettingVO_itemMap

@dataclass
class VehicleSettingVO(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 设备信息
    device: Optional[DeviceObject] = None
    # The itemMap property
    item_map: Optional[VehicleSettingVO_itemMap] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VehicleSettingVO:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VehicleSettingVO
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VehicleSettingVO()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .device_object import DeviceObject
        from .vehicle_setting_v_o_item_map import VehicleSettingVO_itemMap

        from .device_object import DeviceObject
        from .vehicle_setting_v_o_item_map import VehicleSettingVO_itemMap

        fields: dict[str, Callable[[Any], None]] = {
            "device": lambda n : setattr(self, 'device', n.get_object_value(DeviceObject)),
            "itemMap": lambda n : setattr(self, 'item_map', n.get_object_value(VehicleSettingVO_itemMap)),
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
        writer.write_object_value("device", self.device)
        writer.write_object_value("itemMap", self.item_map)
        writer.write_additional_data_value(self.additional_data)
    

