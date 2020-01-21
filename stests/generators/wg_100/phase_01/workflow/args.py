import argparse
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from stests.core.utils import env
from stests.generators.wg_100 import metadata
from stests.generators.wg_100.phase_01.workflow import defaults



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes the {metadata.DESCRIPTION} workload generator.")

# ... execution context arguments
# TODO: specify
ARGS.add_argument(
    "--simulator-id",
    help="Simulator run identifier.",
    dest="simulator_id",
    type=int,
    default=0
    )

ARGS.add_argument(
    "--network-id",
    help="Network identifier.",
    dest="network_id",
    type=str,
    default=env.get_network_id()
    )

# ... generator specific arguments
ARGS.add_argument(
    "--bids-per-account",
    help="Number of bids per account to submit.",
    dest="bids_per_accounts",
    type=int,
    default=defaults.DEFAULT_BIDS_PER_ACCOUNT
    )

ARGS.add_argument(
    "--contract-name",
    help="Name of smart contract to be loaded from resources directory.",
    dest="contract_name",
    type=str,
    default=defaults.DEFAULT_CONTRACT_WASM_FILENAME
    )

# TODO: specify
ARGS.add_argument(
    "--faucet-account",
    help="Address of a faucet smart contract.",
    dest="faucet_account",
    type=str
    )

ARGS.add_argument(
    "--user-initial-clx-balance",
    help="Initial CLX balance of user accounts.",
    dest="user_initial_clx_balance",
    type=int,
    default=defaults.DEFAULT_USER_CLX_BALANCE
    )

ARGS.add_argument(
    "--max-user-accounts",
    help="Maximum number of user accounts to generate.",
    dest="max_user_accounts",
    type=int,
    default=defaults.DEFAULT_USER_ACCOUNTS
    )

ARGS.add_argument(
    "--token-name",
    help="Name of ERC20 token for which an auction is being simulated.",
    dest="token_name",
    type=str,
    default=defaults.DEFAULT_TOKEN_NAME
    )

ARGS.add_argument(
    "--token-supply",
    help="Total amount of ERC20 token to be issued.",
    dest="token_supply",
    type=int,
    default=defaults.DEFAULT_TOKEN_SUPPLY
    )


# @dataclass_json
# @dataclass
# class Arguments():
#     simulator_type: str = metadata.ID

