from enum import Enum

class Vehicle_fleetMode(str, Enum):
    FLEET_MODE_NONE = "FLEET_MODE_NONE",
    FLEET_MODE_OFFLINE = "FLEET_MODE_OFFLINE",
    FLEET_MODE_ONLINE = "FLEET_MODE_ONLINE",

