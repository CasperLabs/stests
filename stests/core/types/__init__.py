from stests.core.types import factory
from stests.core.types.account import AccountStatus
from stests.core.types.account import AccountType
from stests.core.types.account import Account
from stests.core.types.crypto import KeyPair
from stests.core.types.network import Network
from stests.core.types.network import NetworkLifetime
from stests.core.types.network import NetworkOperator
from stests.core.types.network import NetworkStatus
from stests.core.types.node import Node
from stests.core.types.node import NodeStatus



# Supported domain classes.
CLASSES = {
    Account,
    KeyPair,
    Network,
    Node,
}

# Supported domain enums.
ENUMS = {
    AccountStatus,
    AccountType,
    NetworkLifetime,
    NetworkOperator,
    NetworkStatus,
    NodeStatus,
}

# Supported domain types.
TYPESET = CLASSES | ENUMS
