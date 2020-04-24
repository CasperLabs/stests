import enum



class NetworkStatus(enum.Flag):
    """Flag over set of network states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NetworkType(enum.Enum):
    """Enumeration over set of network types.
    
    """
    LOC = enum.auto()
    DEV = enum.auto()
    LRT = enum.auto()
    SYS = enum.auto()
    STG = enum.auto()
    POC = enum.auto()
    TEST = enum.auto()
    MAIN = enum.auto()


class NodeEventType(enum.Flag):
    """Flag over set of node events.
    
    """
    BLOCK_ADD = enum.auto()
    BLOCK_FINALIZE = enum.auto()
    DEPLOY_ADD = enum.auto()
    DEPLOY_DISCARD = enum.auto()
    DEPLOY_FINALIZE = enum.auto()
    DEPLOY_ORPHAN = enum.auto()
    DEPLOY_PROCESSED = enum.auto()
    DEPLOY_REQUEUE = enum.auto()


class NodeStatus(enum.Flag):
    """Flag over set of node states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NodeType(enum.Enum):
    """Enumeration over set of node types.
    
    """
    FULL = enum.auto()
    READ_ONLY = enum.auto()


# Full set of enums.
ENUM_SET = {
    NetworkStatus,
    NetworkType,
    NodeEventType,
    NodeStatus,
    NodeType,
}
