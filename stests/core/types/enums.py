import enum
from dataclasses import field
from dataclasses_json import config



class AccountStatus(enum.Flag):
    """Flag over set account states.
    
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


class NetworkOperatorType(enum.Enum):
    """Enumeration over set of network operator types.
    
    """
    LOCAL = enum.auto()
    INTERNAL = enum.auto()
    EXTERNAL = enum.auto()


class NetworkStatus(enum.Flag):
    """Flag over set network states.
    
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
    LOC = (NetworkOperatorType.LOCAL, "Developer tests")
    DEV = (NetworkOperatorType.INTERNAL, "Developer tests")
    LRT = (NetworkOperatorType.INTERNAL, "Long running tests")
    SYS = (NetworkOperatorType.INTERNAL, "Full system tests")
    STG = (NetworkOperatorType.INTERNAL, "Release staging")
    POC = (NetworkOperatorType.EXTERNAL, "Proof of concept")
    TEST = (NetworkOperatorType.EXTERNAL, "Chain candidate")
    MAIN = (NetworkOperatorType.EXTERNAL, "Main")


class NodeStatus(enum.Flag):
    """Flag over set node states.
    
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
    return field(
        default = default,
        metadata=config(
            encoder=lambda x: str(x).split('.')[-1],
            decoder=lambda x: enum[x]
        ))
