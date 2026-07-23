from enum import Enum

class GetMapSyncTypeQueryParameterType(str, Enum):
    Pull = "pull",
    Push = "push",
    Upload = "upload",

