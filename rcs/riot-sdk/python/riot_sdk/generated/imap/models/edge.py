from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge_user_defined_properties import Edge_userDefinedProperties

@dataclass
class Edge(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The cost property
    cost: Optional[float] = None
    # The cx property
    cx: Optional[int] = None
    # The cy property
    cy: Optional[int] = None
    # The desc property
    desc: Optional[str] = None
    # The direction property
    direction: Optional[int] = None
    # The dx property
    dx: Optional[int] = None
    # The dy property
    dy: Optional[int] = None
    # The efacing property
    efacing: Optional[float] = None
    # The enode property
    enode: Optional[int] = None
    # The ex property
    ex: Optional[int] = None
    # The ey property
    ey: Optional[int] = None
    # The id property
    id: Optional[int] = None
    # The isBackEdge property
    is_back_edge: Optional[bool] = None
    # The limitV property
    limit_v: Optional[int] = None
    # The limitW property
    limit_w: Optional[int] = None
    # The param property
    param: Optional[int] = None
    # The radius property
    radius: Optional[int] = None
    # The robotDirection property
    robot_direction: Optional[int] = None
    # The rotateDirection property
    rotate_direction: Optional[int] = None
    # The sfacing property
    sfacing: Optional[float] = None
    # The snode property
    snode: Optional[int] = None
    # The sx property
    sx: Optional[int] = None
    # The sy property
    sy: Optional[int] = None
    # The type property
    type: Optional[int] = None
    # The userDefinedProperties property
    user_defined_properties: Optional[Edge_userDefinedProperties] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Edge:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Edge
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Edge()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .edge_user_defined_properties import Edge_userDefinedProperties

        from .edge_user_defined_properties import Edge_userDefinedProperties

        fields: dict[str, Callable[[Any], None]] = {
            "cost": lambda n : setattr(self, 'cost', n.get_float_value()),
            "cx": lambda n : setattr(self, 'cx', n.get_int_value()),
            "cy": lambda n : setattr(self, 'cy', n.get_int_value()),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "direction": lambda n : setattr(self, 'direction', n.get_int_value()),
            "dx": lambda n : setattr(self, 'dx', n.get_int_value()),
            "dy": lambda n : setattr(self, 'dy', n.get_int_value()),
            "efacing": lambda n : setattr(self, 'efacing', n.get_float_value()),
            "enode": lambda n : setattr(self, 'enode', n.get_int_value()),
            "ex": lambda n : setattr(self, 'ex', n.get_int_value()),
            "ey": lambda n : setattr(self, 'ey', n.get_int_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isBackEdge": lambda n : setattr(self, 'is_back_edge', n.get_bool_value()),
            "limitV": lambda n : setattr(self, 'limit_v', n.get_int_value()),
            "limitW": lambda n : setattr(self, 'limit_w', n.get_int_value()),
            "param": lambda n : setattr(self, 'param', n.get_int_value()),
            "radius": lambda n : setattr(self, 'radius', n.get_int_value()),
            "robotDirection": lambda n : setattr(self, 'robot_direction', n.get_int_value()),
            "rotateDirection": lambda n : setattr(self, 'rotate_direction', n.get_int_value()),
            "sfacing": lambda n : setattr(self, 'sfacing', n.get_float_value()),
            "snode": lambda n : setattr(self, 'snode', n.get_int_value()),
            "sx": lambda n : setattr(self, 'sx', n.get_int_value()),
            "sy": lambda n : setattr(self, 'sy', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_int_value()),
            "userDefinedProperties": lambda n : setattr(self, 'user_defined_properties', n.get_object_value(Edge_userDefinedProperties)),
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
        writer.write_float_value("cost", self.cost)
        writer.write_int_value("cx", self.cx)
        writer.write_int_value("cy", self.cy)
        writer.write_str_value("desc", self.desc)
        writer.write_int_value("direction", self.direction)
        writer.write_int_value("dx", self.dx)
        writer.write_int_value("dy", self.dy)
        writer.write_float_value("efacing", self.efacing)
        writer.write_int_value("enode", self.enode)
        writer.write_int_value("ex", self.ex)
        writer.write_int_value("ey", self.ey)
        writer.write_int_value("id", self.id)
        writer.write_bool_value("isBackEdge", self.is_back_edge)
        writer.write_int_value("limitV", self.limit_v)
        writer.write_int_value("limitW", self.limit_w)
        writer.write_int_value("param", self.param)
        writer.write_int_value("radius", self.radius)
        writer.write_int_value("robotDirection", self.robot_direction)
        writer.write_int_value("rotateDirection", self.rotate_direction)
        writer.write_float_value("sfacing", self.sfacing)
        writer.write_int_value("snode", self.snode)
        writer.write_int_value("sx", self.sx)
        writer.write_int_value("sy", self.sy)
        writer.write_int_value("type", self.type)
        writer.write_object_value("userDefinedProperties", self.user_defined_properties)
        writer.write_additional_data_value(self.additional_data)
    

