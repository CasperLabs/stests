import enum



class AccountType(enum.Enum):
    """Enumeration over set of account types.
    
    """
    NETWORK_FAUCET = enum.auto()
    VALIDATOR_BOND = enum.auto()
    GENERATOR_RUN = enum.auto()
    OTHER = enum.auto()


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
    TRANSFER_U512 = enum.auto()
    TRANSFER_U512_STORED = enum.auto()
    TRANSFER_U512_WASM = enum.auto()


class DeployStatus(enum.Flag):
    """Flag over set of deploy states.
    
    """
    DISPATCHED = enum.auto()
    PENDING = enum.auto()
    PROCESSED = enum.auto()
    ADDED = enum.auto()
    FINALIZED = enum.auto()
    DISCARDED = enum.auto()
    REJECTED = enum.auto()


class DeployType(enum.Flag):
    """Flag over set of deploy types.
    
    """
    NULL = enum.auto()
    AUCTION_BID_SUBMIT = enum.auto()
    AUCTION_BID_WITHDRAW = enum.auto()
    AUCTION_DELEGATE = enum.auto()
    AUCTION_UNDELEGATE = enum.auto()
    CONTRACT_INSTALL = enum.auto()
    TRANSFER_WASM = enum.auto()
    TRANSFER_NATIVE = enum.auto()



# Full set of enums.
ENUM_SET = {
    AccountType,    
    BlockStatus,
    ContractType,
    DeployStatus,
    DeployType,
}
