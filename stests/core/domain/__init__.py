from stests.core.domain.account import *
from stests.core.domain.deploy import *
from stests.core.domain.enums import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.run import *



# Domain classes.
DCLASS_SET = {
    Account,
    AccountTransfer,
    Deploy,
    Network,
    Node,
    
    RunContext,
    RunEvent,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET

# Register domain types with encoder.
from stests.core.utils import encoder
for i in TYPE_SET:
    encoder.register_type(i)
