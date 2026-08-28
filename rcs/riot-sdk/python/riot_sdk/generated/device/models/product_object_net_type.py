from enum import Enum

class ProductObject_netType(str, Enum):
    CELLULAR = "CELLULAR",
    ETHERNET = "ETHERNET",
    LORA = "LORA",
    WIFI = "WIFI",

