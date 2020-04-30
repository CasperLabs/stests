import enum



class MonitoringEventType(enum.Enum):
    """Enum over set of sub-system events.
    
    """
    API_ERROR = enum.auto()

    ACCOUNT_NOT_FOUND = enum.auto()

    BLOCK_ADD = enum.auto()
    BLOCK_FINALIZED = enum.auto()
    BLOCK_NOT_FOUND = enum.auto()

    DEPLOY_ADDED = enum.auto()
    DEPLOY_CORRELATED = enum.auto()
    DEPLOY_DISCARDED = enum.auto()
    DEPLOY_DISPATCHED = enum.auto()
    DEPLOY_FINALIZED = enum.auto()
    DEPLOY_NOT_FOUND = enum.auto()
    DEPLOY_ORPHANED = enum.auto()
    DEPLOY_PROCESSED = enum.auto()
    DEPLOY_REQUEUED = enum.auto()