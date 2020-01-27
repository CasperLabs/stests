from dataclasses import dataclass
from dataclasses_json import dataclass_json

from stests.core.utils import encoder
from stests.core.utils.workflow import WorkflowArguments
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata



@dataclass_json
@dataclass
class Arguments(WorkflowArguments):
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

    # Name of smart contract .wasm file..
    wasm_contract_filename: str = defaults.WASM_CONTRACT_FILENAME

    # TODO: pull network info from cache - including nodes + validators
    validator_pvk_pem_fpath: str = "/Users/a-0/ops/clabs/chain-000/nodes/node-000/keys/validator-private.pem"
    validator_pbk_hex = "d09cad126cbecff01b7231c6565ba483735e00f5cd93aa1ef011844c881ec1e8"


    @classmethod
    def create(cls, parsed):
        """Constructor.
        
        :param parsed: Parsed command line arguments.

        """
        return WorkflowArguments.create(cls, metadata.TYPE, parsed)


    @staticmethod
    def get_parser():
        """Returns the workflow's CLI argument parser.
        
        """
        return WorkflowArguments.get_parser(metadata.DESCRIPTION)


# Framework requirement: register arguments type.
encoder.register_type(Arguments)
