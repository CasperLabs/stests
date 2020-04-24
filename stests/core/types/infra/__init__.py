from stests.core.types.infra.enums import NodeEventType
from stests.core.types.infra.enums import NetworkStatus
from stests.core.types.infra.enums import NetworkType
from stests.core.types.infra.enums import NodeStatus
from stests.core.types.infra.enums import NodeType
from stests.core.types.infra.enums import ENUM_SET
from stests.core.types.infra.network import Network
from stests.core.types.infra.network import NetworkIdentifier
from stests.core.types.infra.node import Node
from stests.core.types.infra.node import NodeEventLock
from stests.core.types.infra.node import NodeIdentifier
from stests.core.types.infra.node import NodeMonitoringLock



TYPE_SET = {
    Network,
    NodeEventType,
    NetworkIdentifier,
    Node,
    NodeEventLock,
    NodeIdentifier,
    NodeMonitoringLock,
} | ENUM_SET
