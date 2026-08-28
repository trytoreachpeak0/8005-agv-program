from enum import Enum

class Vehicle_batteryState(str, Enum):
    CHARGING = "CHARGING",
    NO_CHARGE = "NO_CHARGE",
    UNKNOWN = "UNKNOWN",

