import os

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

    # TEMPORARY: pull network info from cache - including nodes + validators
    validator_pvk_pem_fpath: str = None
    validator_pbk_hex: str = None


    @classmethod
    def create(cls, parsed):
        """Constructor.
        
        :param parsed: Parsed command line arguments.

        """
        args = WorkflowArguments.create(cls, metadata.TYPE, parsed)

        # TEMPORARY: inject validator pvk/pbk.
        args.validator_pvk_pem_fpath = get_validator_pvk_pem_fpath(args.network_id)
        args.validator_pbk_hex = get_validator_pbk_hex(args.network_id)

        return args


    @staticmethod
    def get_parser():
        """Returns the workflow's CLI argument parser.
        
        """
        return WorkflowArguments.get_parser(metadata.DESCRIPTION)



_OPS_DIR = os.getenv("CLABS_OPS")


def get_validator_pvk_pem_fpath(network_id, node_name="NODE-001"):
    return f"{_OPS_DIR}/chains/{network_id}/nodes/{node_name}/keys/validator-private.pem"

def get_validator_pbk_hex(network_id, node_name="NODE-001"):
    fpath = f"{_OPS_DIR}/chains/{network_id}/nodes/{node_name}/keys/validator-id-hex"
    with open(fpath, 'r') as fstream:
        return fstream.read()


# Framework requirement: register arguments type.
encoder.register_type(Arguments)
