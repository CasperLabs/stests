from stests.core.types.infra.enums import NetworkStatus
from stests.core.types.infra.enums import NetworkType
from stests.core.types.infra.enums import NodeGroup
from stests.core.types.infra.enums import NodeStatus
from stests.core.types.infra.enums import NodeType
from stests.core.types.infra.enums import ENUM_SET
from stests.core.types.infra.network import Network
from stests.core.types.infra.network import NetworkIdentifier
from stests.core.types.infra.node import Node
from stests.core.types.infra.node import NodeEventInfo
from stests.core.types.infra.node import NodeIdentifier
from stests.core.types.infra.node import NodeMonitoringLock



TYPE_SET = {
    Network,
    NetworkIdentifier,
    Node,
    NodeEventInfo,
    NodeIdentifier,
    NodeMonitoringLock,
} | ENUM_SET
