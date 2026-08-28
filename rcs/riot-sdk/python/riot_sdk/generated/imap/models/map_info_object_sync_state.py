from enum import Enum

class MapInfoObject_syncState(str, Enum):
    Asynced = "asynced",
    Partition = "partition",
    Synced = "synced",

