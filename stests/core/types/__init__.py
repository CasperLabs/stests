from stests.core.types.account import Account
from stests.core.types.account import AccountStatus
from stests.core.types.account import AccountType
from stests.core.types.key_pair import KeyEncoding
from stests.core.types.key_pair import KeyPair
from stests.core.types.network import Network
from stests.core.types.network import NetworkStatus
from stests.core.types.network import NetworkType
from stests.core.types.node import Node
from stests.core.types.node import NodeStatus
from stests.core.types.node import NodeType
from stests.core.types.utils_factory import create_account



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
    KeyEncoding,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
}

# Supported domain types.
TYPESET = CLASSES | ENUMS
