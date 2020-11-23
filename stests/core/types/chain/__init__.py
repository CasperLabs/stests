from stests.core.types.chain.account import Account
from stests.core.types.chain.account import AccountIdentifier
from stests.core.types.chain.block import Block
from stests.core.types.chain.block import BlockStatistics
from stests.core.types.chain.deploy import Deploy
from stests.core.types.chain.enums import AccountType
from stests.core.types.chain.enums import BlockStatus
from stests.core.types.chain.enums import ContractType
from stests.core.types.chain.enums import DeployStatus
from stests.core.types.chain.enums import DeployType
from stests.core.types.chain.enums import ENUM_SET
from stests.core.types.chain.named_key import NamedKey



TYPE_SET = {
    Account,
    AccountIdentifier,
    Block,
    BlockStatistics,
    Deploy,
    NamedKey,
} | ENUM_SET
