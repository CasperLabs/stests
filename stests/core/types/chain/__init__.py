from stests.core.types.chain.account import *
from stests.core.types.chain.block import *
from stests.core.types.chain.deploy import *
from stests.core.types.chain.enums import *
from stests.core.types.chain.named_key import *
from stests.core.types.chain.transfer import *



# Set of supported classes.
DCLASS_SET = {
    Account,
    Block,
    Deploy,
    NamedKey,
    Transfer,
}

# Set of supported identifiers.
IDENTIFIER_SET = {
    AccountIdentifier,
}

# Set of supported identifiers.
LOCK_SET = {
    BlockLock,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | IDENTIFIER_SET | ENUM_SET | LOCK_SET
