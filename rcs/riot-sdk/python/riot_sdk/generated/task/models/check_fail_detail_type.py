from enum import Enum

class CheckFailDetail_type(str, Enum):
    Collision = "collision",
    EdgeGroup = "edgeGroup",
    OutsideTraffic = "outsideTraffic",
    PositionCheck = "positionCheck",
    TwoWayLoadCheck = "twoWayLoadCheck",

