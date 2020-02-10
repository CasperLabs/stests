from stests.core.domain.enums import *
from stests.core.domain.identifiers import *

from stests.core.domain.account import *
from stests.core.domain.deploy import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.run import *

# Domain classes.
DCLASS_SET = {
    Account,
    AccountForRun,
    Deploy,
    Network,
    Node,
    RunContext,
    RunEvent,
    RunInfo,
}

# Register types with encoder.
from stests.core.utils import encoder
for i in DCLASS_SET | IDENTIFIER_SET | ENUM_SET:
    encoder.register_type(i)
