from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils.generator import GeneratorContext
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata



@dataclass_json
@dataclass
class Arguments:
    """Contextual information passed through workflow.
    
    """
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


    @classmethod
    def create(cls, parsed):
        """Constructor.
        
        :param parsed: Parsed command line arguments.

        """
        return GeneratorContext.create(cls, metadata.TYPE, parsed)
