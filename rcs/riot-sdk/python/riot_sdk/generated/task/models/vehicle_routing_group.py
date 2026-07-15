from enum import Enum

class Vehicle_routingGroup(str, Enum):
    EXECUTE_ALL = "EXECUTE_ALL",
    EXECUTE_FREE = "EXECUTE_FREE",
    EXECUTE_LOAD = "EXECUTE_LOAD",

