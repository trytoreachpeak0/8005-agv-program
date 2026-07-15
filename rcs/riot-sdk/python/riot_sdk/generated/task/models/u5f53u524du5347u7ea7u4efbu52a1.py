from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u5347u7ea7u4efbu52a1u8fd4u56de_object import U5347u7ea7u4efbu52a1u8fd4u56deObject

@dataclass
class U5f53u524du5347u7ea7u4efbu52a1(AdditionalDataHolder, Parsable):
    """
    当前升级任务
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 开始时间
    start_time: Optional[datetime.datetime] = None
    # 预约升级
    upgrade_appointment_list: Optional[list[U5347u7ea7u4efbu52a1u8fd4u56deObject]] = None
    # 升级失败
    upgrade_failed_list: Optional[list[U5347u7ea7u4efbu52a1u8fd4u56deObject]] = None
    # 升级完成
    upgrade_finished_list: Optional[list[U5347u7ea7u4efbu52a1u8fd4u56deObject]] = None
    # 升级中
    upgrading_list: Optional[list[U5347u7ea7u4efbu52a1u8fd4u56deObject]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U5f53u524du5347u7ea7u4efbu52a1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U5f53u524du5347u7ea7u4efbu52a1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U5f53u524du5347u7ea7u4efbu52a1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u5347u7ea7u4efbu52a1u8fd4u56de_object import U5347u7ea7u4efbu52a1u8fd4u56deObject

        from .u5347u7ea7u4efbu52a1u8fd4u56de_object import U5347u7ea7u4efbu52a1u8fd4u56deObject

        fields: dict[str, Callable[[Any], None]] = {
            "startTime": lambda n : setattr(self, 'start_time', n.get_datetime_value()),
            "upgradeAppointmentList": lambda n : setattr(self, 'upgrade_appointment_list', n.get_collection_of_object_values(U5347u7ea7u4efbu52a1u8fd4u56deObject)),
            "upgradeFailedList": lambda n : setattr(self, 'upgrade_failed_list', n.get_collection_of_object_values(U5347u7ea7u4efbu52a1u8fd4u56deObject)),
            "upgradeFinishedList": lambda n : setattr(self, 'upgrade_finished_list', n.get_collection_of_object_values(U5347u7ea7u4efbu52a1u8fd4u56deObject)),
            "upgradingList": lambda n : setattr(self, 'upgrading_list', n.get_collection_of_object_values(U5347u7ea7u4efbu52a1u8fd4u56deObject)),
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
        writer.write_datetime_value("startTime", self.start_time)
        writer.write_collection_of_object_values("upgradeAppointmentList", self.upgrade_appointment_list)
        writer.write_collection_of_object_values("upgradeFailedList", self.upgrade_failed_list)
        writer.write_collection_of_object_values("upgradeFinishedList", self.upgrade_finished_list)
        writer.write_collection_of_object_values("upgradingList", self.upgrading_list)
        writer.write_additional_data_value(self.additional_data)
    

