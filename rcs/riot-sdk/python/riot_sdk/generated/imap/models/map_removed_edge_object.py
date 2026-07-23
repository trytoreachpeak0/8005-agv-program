from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge import Edge

@dataclass
class MapRemovedEdgeObject(AdditionalDataHolder, Parsable):
    """
    地图移除边表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The edge property
    edge: Optional[Edge] = None
    # 边id
    edge_id: Optional[int] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_update: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MapRemovedEdgeObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MapRemovedEdgeObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MapRemovedEdgeObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .edge import Edge

        from .edge import Edge

        fields: dict[str, Callable[[Any], None]] = {
            "edge": lambda n : setattr(self, 'edge', n.get_object_value(Edge)),
            "edgeId": lambda n : setattr(self, 'edge_id', n.get_int_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtUpdate": lambda n : setattr(self, 'gmt_update', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
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
        writer.write_object_value("edge", self.edge)
        writer.write_int_value("edgeId", self.edge_id)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtUpdate", self.gmt_update)
        writer.write_int_value("id", self.id)
        writer.write_int_value("mapId", self.map_id)
        writer.write_additional_data_value(self.additional_data)
    

