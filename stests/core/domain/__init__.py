from stests.core.domain.account import *
from stests.core.domain.block import *
from stests.core.domain.deploy import *
from stests.core.domain.enums import *
from stests.core.domain.identifiers import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.run_context import *
from stests.core.domain.run_event import *
from stests.core.domain.run_step import *
from stests.core.domain.transfer import *



# Set of supported classes.
DCLASS_SET = {
    Account,
    Transfer,
    Block,
    Deploy,
    Network,
    Node,
    RunContext,
    RunEvent,
    RunStep,
    Transfer,
}

# Set of supported identifiers.
IDENTIFIER_SET = {
    AccountIdentifier,
    NetworkIdentifier,
    NodeIdentifier,
    RunIdentifier
}

# Full domain type set.
TYPE_SET = DCLASS_SET | IDENTIFIER_SET | ENUM_SET

# Register domain types with encoder.
from stests.core.utils import encoder
for i in TYPE_SET:
    encoder.register_type(i)
