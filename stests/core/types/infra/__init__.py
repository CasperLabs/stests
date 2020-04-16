from stests.core.types.infra.enums import *
from stests.core.types.infra.network import *
from stests.core.types.infra.node import *



# Set of supported classes.
DCLASS_SET = {
    Network,
    Node,
}

# Set of supported identifiers.
IDENTIFIER_SET = {
    NetworkIdentifier,
    NodeIdentifier,
}

# Set of supported locks.
LOCK_SET = {
    NodeMonitorLock,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | IDENTIFIER_SET | ENUM_SET | LOCK_SET
