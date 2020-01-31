from dataclasses import dataclass
from dataclasses_json import dataclass_json
from stests.core.utils.generator import GeneratorArguments
from stests.generators.wg_100 import defaults



@dataclass_json
@dataclass
class Arguments(GeneratorArguments):
    """WG-100 generator arguments.
    
    """
    # Index of node to push deploys to, if 0 then a random node is selected.
    node_idx: str = defaults.NODE_IDX

    # Name of ERC20 token for which an auction is being simulated.
    token_name: str = defaults.TOKEN_NAME

    # Total amount of ERC20 token to be issued.
    token_supply: int = defaults.TOKEN_SUPPLY

    # Number of user accounts to generate.
    user_accounts: int = defaults.USER_ACCOUNTS

    # Number of bids to submit per user.
    user_bids: int = defaults.USER_BIDS

    # Initial user account CLX balance.
    user_initial_clx_balance: int = defaults.USER_INITIAL_CLX_BALANCE
