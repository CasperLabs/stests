import argparse
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import dramatiq

from stests.core import mq
from stests.core.types import AccountType
from stests.core.types import NetworkType
from stests.core.utils import args_validator
from stests.core.utils import encoder
from stests.core.utils import env
from stests.core.utils.generator import GeneratorContext
from stests.core.utils.generator import GeneratorScope
from stests.generators.wg_100 import defaults
from stests.generators.wg_100 import metadata



# Set command line arguments.
ARGS = argparse.ArgumentParser(f"Executes {metadata.DESCRIPTION} workflow.")

# CLI argument: scope -> network type.
ARGS.add_argument(
    "--network-type",
    dest="network_type",
    choices=[i.name.lower() for i in NetworkType],
    help="Type of network being tested.",
    type=str
    )

# CLI argument: scope -> network index.
ARGS.add_argument(
    "--network-idx",
    dest="network_idx",
    help="Network index - must be between 1 and 99.",
    type=args_validator.validate_network_idx,
    default=1
    )

# CLI argument: scope -> node index.
ARGS.add_argument(
    "--node-idx",
    dest="node_idx",
    help="Node index - must be between 1 and 999. If specified deploys are dispatched to this node only, otherwise deploys are dispatched to random nodes.",
    type=args_validator.validate_node_idx,
    default=1,
    required=False
    )

# CLI argument: scope -> run index.
ARGS.add_argument(
    "--run-idx",
    dest="run_idx",
    help="Generator run index - must be between 1 and 65536.",
    type=args_validator.validate_generator_run_idx,
    default=1
    )

# CLI argument: token name.
ARGS.add_argument(
    "--token-name",
    help=f"Name of ERC-20 token.  Default={defaults.TOKEN_NAME}",
    dest="token_name",
    type=str,
    default=defaults.TOKEN_NAME
    )

# CLI argument: token supply.
ARGS.add_argument(
    "--token-supply",
    help=f"Amount of ERC-20 token to be issued. Default={defaults.TOKEN_SUPPLY}",
    dest="token_supply",
    type=int,
    default=defaults.TOKEN_SUPPLY
    )

# CLI argument: user accounts.
ARGS.add_argument(
    "--user-accounts",
    help=f"Number of user accounts to generate. Default={defaults.USER_ACCOUNTS}",
    dest="user_accounts",
    type=int,
    default=defaults.USER_ACCOUNTS
    )

# CLI argument: bids / user.
ARGS.add_argument(
    "--user-bids",
    help=f"Number of bids per user to submit. Default={defaults.USER_BIDS}",
    dest="user_bids",
    type=int,
    default=defaults.USER_BIDS
    )

# CLI argument: initial CLX balance.
ARGS.add_argument(
    "--user-initial-clx-balance",
    help=f"Initial CLX balance of user accounts. Default={defaults.USER_INITIAL_CLX_BALANCE}",
    dest="user_initial_clx_balance",
    type=int,
    default=defaults.USER_INITIAL_CLX_BALANCE
    )


@dataclass_json
@dataclass
class Context(GeneratorContext):
    """WG-100 generator execution context information.
    
    """
    # Name of ERC20 token for which an auction is being simulated.
    token_name: str

    # Total amount of ERC20 token to be issued.
    token_supply: int

    # Number of user accounts to generate.
    user_accounts: int

    # Number of bids to submit per user.
    user_bids: int

    # Initial user account CLX balance.
    user_initial_clx_balance: int


    @staticmethod
    def create(args: argparse.Namespace):
        """Simple factory method.

        :param args: Parsed command line arguments.
        :returns: Generator context information.

        """
        return Context(
            scope = GeneratorScope.create(metadata.TYPE, args),
            token_name = 'token_name' in args and args.token_name,
            token_supply = 'token_supply' in args and args.token_supply,
            user_accounts = 'user_accounts' in args and args.user_accounts,
            user_bids = 'user_bids' in args and args.user_bids,
            user_initial_clx_balance = 'user_initial_clx_balance' in args and args.user_initial_clx_balance,
        )
        

# Framework requirement: register context.
encoder.register_type(Context)


def get_workflow(ctx: Context):
    """Returns a workflow group that performs various spinup tasks.
    
    """
    from stests.generators.wg_100.phase_01.actors import accounts
    from stests.generators.wg_100.phase_01.actors import contract

    def get_pipeline_for_faucet():
        """Returns a workflow pipeline to initialise a faucet account."""
        return \
            accounts.create.message(ctx, AccountType.FAUCET) | \
            accounts.fund_faucet.message()


    def get_pipeline_for_contract():
        """Returns a workflow pipeline to initialise a contract account."""
        return \
            accounts.create.message(ctx, AccountType.CONTRACT) | \
            accounts.fund_contract.message() | \
            contract.deploy.message()


    def get_pipeline_for_user(index):
        """Returns a workflow pipeline to initialise a user account."""
        return \
            accounts.create.message(ctx, AccountType.USER, index) | \
            accounts.fund_user.message() \


    def get_group_for_users():
        """Returns a workflow group to initialise a set of user accounts."""
        return dramatiq.group(map(
            lambda index: get_pipeline_for_user(index), 
            range(ctx.user_accounts)
        ))

    # return \
    #     get_pipeline_for_faucet() | \
    #     dramatiq.group([
    #         get_pipeline_for_contract(),
    #         get_group_for_users()
    #         ])
    #     ])

    return dramatiq.group([
        get_pipeline_for_faucet(),
        dramatiq.group([
            get_pipeline_for_contract(),
            get_group_for_users()
            ])
        ])



def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    ctx = Context.create(args)

    # Initialise broker.
    mq.init_broker(ctx.scope.network_id)

    workflow = get_workflow(ctx)
    workflow.run()

    


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())