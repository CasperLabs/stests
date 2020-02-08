from stests.core.domain.enums import AccountStatus
from stests.core.domain.enums import AccountType
from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import NetworkStatus
from stests.core.domain.enums import NetworkType
from stests.core.domain.enums import NodeStatus
from stests.core.domain.enums import NodeType

from stests.core.domain.account import Account
from stests.core.domain.deploy import Deploy
from stests.core.domain.network import Network
from stests.core.domain.node import Node

from stests.core.domain.identifiers import NetworkIdentifier
from stests.core.domain.identifiers import NodeIdentifier
from stests.core.domain.identifiers import RunIdentifier

from stests.core.domain.meta import TypeMetadata


# Domain classes.
CLASSES = {
    Account,
    Deploy,
    Network,
    Node,
    TypeMetadata,
}

# Domain identifiers.
IDENTIFIERS = {
    NetworkIdentifier,
    NodeIdentifier,
    RunIdentifier,
}

# Domain enums.
ENUMS = {
    AccountStatus,
    AccountType,
    DeployStatus,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
}

# Domain model.
TYPESET = CLASSES | IDENTIFIERS | ENUMS
