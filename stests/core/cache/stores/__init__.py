from enum import Enum



# Enum: set of supported cache store types.
StoreType = Enum("StoreType", [
    "REDIS",
    "STUB"
])
