from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import NetworkOperatorType
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.enums import NodeStatus
from stests.core.types.enums import NodeType

from stests.core.types.account import Account
from stests.core.types.generator import GeneratorContext
from stests.core.types.generator import GeneratorReference
from stests.core.types.key_pair import KeyPair
from stests.core.types.network import Network
from stests.core.types.network import NetworkReference
from stests.core.types.node import Node

# Domain classes.
CLASSES = {
    Account,
    GeneratorContext,
    GeneratorReference,
    KeyPair,
    Network,
    NetworkReference,
    Node,
}

# Domain enums.
ENUMS = {
    AccountStatus,
    AccountType,
    NetworkOperatorType,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
}

# Domain model.
TYPESET = CLASSES | ENUMS
