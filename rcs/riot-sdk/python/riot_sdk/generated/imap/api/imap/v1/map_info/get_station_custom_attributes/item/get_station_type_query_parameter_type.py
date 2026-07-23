from enum import Enum

class GetStationTypeQueryParameterType(str, Enum):
    CHARGE_POSITION = "CHARGE_POSITION",
    PARK_POSITION = "PARK_POSITION",

