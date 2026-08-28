from enum import Enum

class MapInfoObject_source(str, Enum):
    Fetch = "fetch",
    NewCAD = "newCAD",
    Upload = "upload",

