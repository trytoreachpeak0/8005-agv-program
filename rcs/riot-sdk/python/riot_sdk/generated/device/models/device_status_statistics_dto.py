from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class DeviceStatusStatisticsDto(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The allCount property
    all_count: Optional[int] = None
    # The enable property
    enable: Optional[int] = None
    # The inactiveCount property
    inactive_count: Optional[int] = None
    # The offlineCount property
    offline_count: Optional[int] = None
    # The onlineCount property
    online_count: Optional[int] = None
    # The unEnable property
    un_enable: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DeviceStatusStatisticsDto:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeviceStatusStatisticsDto
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DeviceStatusStatisticsDto()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "allCount": lambda n : setattr(self, 'all_count', n.get_int_value()),
            "enable": lambda n : setattr(self, 'enable', n.get_int_value()),
            "inactiveCount": lambda n : setattr(self, 'inactive_count', n.get_int_value()),
            "offlineCount": lambda n : setattr(self, 'offline_count', n.get_int_value()),
            "onlineCount": lambda n : setattr(self, 'online_count', n.get_int_value()),
            "unEnable": lambda n : setattr(self, 'un_enable', n.get_int_value()),
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
        writer.write_int_value("allCount", self.all_count)
        writer.write_int_value("enable", self.enable)
        writer.write_int_value("inactiveCount", self.inactive_count)
        writer.write_int_value("offlineCount", self.offline_count)
        writer.write_int_value("onlineCount", self.online_count)
        writer.write_int_value("unEnable", self.un_enable)
        writer.write_additional_data_value(self.additional_data)
    

