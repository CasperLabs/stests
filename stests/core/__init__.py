import enum



class CoreEventType(enum.Enum):
    """Enum over set of sub-system events.
    
    """
    BROKER_CONNECTION_ESTABLISHED = enum.auto()
    ENCODING_ERROR = enum.auto()
    ACTOR_ERROR = enum.auto()
