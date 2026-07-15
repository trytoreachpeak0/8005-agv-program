from enum import Enum

class Vehicle_state(str, Enum):
    CHARGING = "CHARGING",
    ERROR = "ERROR",
    EXECUTING = "EXECUTING",
    IDLE = "IDLE",
    PAUSE = "PAUSE",
    UNKNOWN = "UNKNOWN",

