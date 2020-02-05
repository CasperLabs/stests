import enum
from dataclasses import field
from dataclasses_json import config



class AccountStatus(enum.Flag):
    """Flag over set of account states.
    
    """
    NEW = enum.auto()
    FUNDING = enum.auto()
    FUNDED = enum.auto()
    ACTIVE = enum.auto()


class AccountType(enum.Enum):
    """Enumeration over set of account types.
    
    """
    CONTRACT = enum.auto()
    FAUCET = enum.auto()
    USER = enum.auto()
    BOND = enum.auto()


class DeployStatus(enum.Flag):
    """Flag over set of deploy states.
    
    """
    NULL = enum.auto()
    FINALIZED = enum.auto()
    REJECTED = enum.auto()


class GeneratorExecutionStatus(enum.Enum):
    """Enumeration over set of generation execution states.
    
    """
    NULL = enum.auto()
    ACTIVE = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()


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


def get_enum_field(enum: enum.Enum, default: str=None) -> field:
    """Returns an enumeration dataclass field with implicit encoding support.
    
    :param enum: An enum or flag being declared within a dataclass.
    :param default: Dataclass field's default value.

    """
    if default is not None:
        return field(
            default = default,
            metadata=config(
                encoder=lambda x: str(x),
                decoder=lambda x: enum[x.split('.')[-1]]
            ))
    return field(
        metadata=config(
            encoder=lambda x: str(x),
            decoder=lambda x: enum[x.split('.')[-1]]
        ))
