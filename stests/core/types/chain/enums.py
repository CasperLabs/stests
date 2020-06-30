import enum



class AccountType(enum.Enum):
    """Enumeration over set of account types.
    
    """
    CONTRACT = enum.auto()
    FAUCET = enum.auto()
    USER = enum.auto()
    BOND = enum.auto()


class BlockStatus(enum.Flag):
    """Flag over set of block states.
    
    """
    NULL = enum.auto()
    ADDED = enum.auto()
    FINALIZED = enum.auto()
    REJECTED = enum.auto()


class ContractType(enum.Enum):
    """Enumeration over set of bundled client contract types.
    
    """
    COUNTER_DEFINE = enum.auto()
    COUNTER_DEFINE_STORED = enum.auto()
    TRANSFER_U512 = enum.auto()
    TRANSFER_U512_STORED = enum.auto()
    TRANSFER_U512_WASM = enum.auto()


class DeployStatus(enum.Flag):
    """Flag over set of deploy states.
    
    """
    DISPATCHED = 0
    PENDING = 1
    PROCESSED = 2
    FINALIZED = 3
    DISCARDED = 4
    REJECTED = 5


class DeployType(enum.Flag):
    """Flag over set of deploy types.
    
    """
    NULL = enum.auto()
    CONTRACT_INSTALL = enum.auto()
    COUNTER_DEFINE = enum.auto()
    TRANSFER = enum.auto()
    TRANSFER_REFUND = enum.auto()


class TransferStatus(enum.Flag):
    """Flag over set of transfer states.
    
    """
    NULL = enum.auto()
    PENDING = enum.auto()
    ERROR = enum.auto()
    COMPLETE = enum.auto()


# Full set of enums.
ENUM_SET = {
    AccountType,    
    BlockStatus,
    ContractType,
    DeployStatus,
    DeployType,
    TransferStatus,
}
