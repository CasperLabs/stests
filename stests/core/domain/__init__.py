from stests.core.domain.account import *
from stests.core.domain.contract import *
from stests.core.domain.block import *
from stests.core.domain.deploy import *
from stests.core.domain.enums import *
from stests.core.domain.named_key import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.transfer import *



# Set of supported classes.
DCLASS_SET = {
    Account,
    Contract,
    Block,
    Deploy,
    NamedKey,
    Network,
    Node,
    Transfer,
}

# Set of supported identifiers.
IDENTIFIER_SET = {
    AccountIdentifier,
    NetworkIdentifier,
    NodeIdentifier,
}

# Set of supported identifiers.
LOCK_SET = {
    BlockLock,
    NodeMonitorLock,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | IDENTIFIER_SET | ENUM_SET | LOCK_SET
