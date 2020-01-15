from enum import Enum



# Enum: set of supported mq broker types.
BrokerType = Enum("BrokerType", [
    "RABBIT",
    "REDIS",
    "STUB"
])
