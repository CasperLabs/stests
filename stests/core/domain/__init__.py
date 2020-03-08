from stests.core.domain.account import *
from stests.core.domain.block import *
from stests.core.domain.deploy import *
from stests.core.domain.enums import *
from stests.core.domain.identifiers import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.run_context import *
from stests.core.domain.run_phase import *
from stests.core.domain.run_step import *
from stests.core.domain.transfer import *



# Set of supported classes.
DCLASS_SET = {
    # infra entities
    Network,
    Node,
    # chain entities
    Account,
    Block,
    Deploy,
    Transfer,
    # control entities
    RunContext,
    ExecutionRunState,
    RunPhase,
    ExecutionPhaseState,
    RunStep,
    ExecutionStepState,
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
