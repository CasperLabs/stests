import argparse
import random

from stests import chain
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import AccountType
from stests.core.types.infra import Network
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from stests.core.utils.misc import Timer
from arg_utils import get_network_nodeset_by_node



# CLI argument parser.
ARGS = argparse.ArgumentParser("Dispatches set of native transfers to target chain.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    default=0,
    dest="node",
    help="Node index, e.g. 1.  If 0, then each deploy is dispatched to a node chosen at random.  If -1, then dispatched to a single node chosen at random.",
    type=args_validator.validate_node_index_optional
    )

# CLI argument: transfer count.
ARGS.add_argument(
    "--transfers",
    default=100,
    dest="transfers",
    help="Number of transfers to dispatch.",
    type=int,
    )

# CLI argument: CSPR per transfer.
ARGS.add_argument(
    "--amount",
    help="Motes per transfer. Default=25e8",
    dest="amount",
    type=int,
    default=int(25e8)
    )

# CLI argument: # transfers to dispatch.
ARGS.add_argument(
    "--accounts",
    help="Number of target accounts to create on the fly. If set to 0 then each target account is unique, otherwise a single target account is created.",
    dest="accounts",
    type=int,
    default=1
    )

# Map: account index <-> account.
_ACCOUNTS = dict()


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    utils.log(f"Dispatching {args.transfers} native transfers:")

    network, nodeset = get_network_nodeset_by_node(args)    
    cp1 = network.faucet

    utils.log(f"... node              : {nodeset[0].address if len(nodeset) == 1 else 'any'}")
    utils.log(f"... amount / transfer : {args.amount}")
    utils.log(f"... counter-party 1   : {cp1.account_key}")

    with Timer() as timer:
        for deploy_idx in range(1, args.transfers + 1):
            chain.set_transfer_native(
                chain.DeployDispatchInfo(cp1, network, random.choice(nodeset)),
                _get_account_for_cp2(network, args.accounts, deploy_idx),
                args.amount,
                verbose=False,
                )

    utils.log(f"Dispatch complete")
    utils.log(f"... total transfers   : {args.transfers}")
    utils.log(f"... total accounts    : {min(args.accounts if args.accounts != 0 else args.transfers, args.transfers)}")
    utils.log(f"... total amount      : {args.amount * args.transfers}")
    utils.log(f"... total time        : {timer.elapsed:.2f} seconds")
    utils.log(f"... dispatch rate     : {(args.transfers / timer.elapsed):.2f} / second")


def _get_account_for_cp2(network: Network, accounts: int, deploy_idx: int) -> Account:
    """Returns counter-party 2 account.
    
    """
    if accounts != 0:
        account_idx = _get_account_idx_for_deploy(accounts, deploy_idx)
        if not account_idx in _ACCOUNTS:
            _ACCOUNTS[account_idx] = factory.create_account(network.name, AccountType.OTHER, index=account_idx)
        return _ACCOUNTS[account_idx]
    return factory.create_account(network.name, AccountType.OTHER, index=deploy_idx)


def _get_account_idx_for_deploy(accounts: int, deploy_idx: int) -> int:
    """Returns account index to use for a particular transfer.
    
    :param accounts: Number of accounts within batch.
    :param deploy_idx: Index of deploy within batch.
    :returns: Ordinal index of account used to dispatch deploy.

    """
    return deploy_idx if accounts == 0 else \
           deploy_idx % accounts or accounts


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
