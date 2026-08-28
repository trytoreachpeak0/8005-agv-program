from enum import Enum

class Vehicle_locationState(str, Enum):
    ERROR = "ERROR",
    LOCATION_STATE_RUNNING = "LOCATION_STATE_RUNNING",
    UNKNOWN = "UNKNOWN",

