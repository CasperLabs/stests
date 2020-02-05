from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.enums import NodeStatus
from stests.core.types.enums import NodeType

from stests.core.types.account import Account
from stests.core.types.generator_run import GeneratorRun
from stests.core.types.key_pair import KeyPair
from stests.core.types.network import Network
from stests.core.types.node import Node

from stests.core.types.identifiers import AccountIdentifier
from stests.core.types.identifiers import GeneratorRunIdentifier
from stests.core.types.identifiers import NodeIdentifier
from stests.core.types.identifiers import NetworkIdentifier

from stests.core.types.utils import get_isodatetime_field
from stests.core.types.utils import get_uuid_field


# Domain classes.
CLASSES = {
    Account,
    GeneratorRun,
    KeyPair,
    Network,
    Node,
}

# Domain class instance identifiers.
IDENTIFIERS = {
    AccountIdentifier,
    GeneratorRunIdentifier,
    NetworkIdentifier,
    NodeIdentifier,
}

# Domain enums.
ENUMS = {
    AccountStatus,
    AccountType,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
}

# Domain model.
TYPESET = CLASSES | IDENTIFIERS | ENUMS
