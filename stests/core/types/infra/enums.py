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
    NCTL = enum.auto()
    DEV = enum.auto()
    LRT = enum.auto()
    SYS = enum.auto()
    STG = enum.auto()
    POC = enum.auto()
    TEST = enum.auto()
    MAIN = enum.auto()
    LRTNET = enum.auto()


class NodeGroup(enum.Enum):
    """Enumeration over set of node groups.

    """
    BOOTSTRAP = enum.auto()
    GENESIS = enum.auto()
    OTHER = enum.auto()
    UNKNOWN = enum.auto()


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
    VALIDATOR = enum.auto()
    READ_ONLY = enum.auto()


# Full set of enums.
ENUM_SET = {
    NetworkStatus,
    NetworkType,
    NodeGroup,
    NodeStatus,
    NodeType,
}
