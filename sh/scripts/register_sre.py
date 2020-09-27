import argparse
import os
import pathlib
import typing

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeType
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Register a network with stests.")


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    for network_id, accounts, nodes in _yield_network_artefacts():
        # Register network.
        network = _register_network(network_id)

        # Register network faucet.
        _register_faucet(network, accounts)

        # Register network nodes.
        for node_idx, node_info in enumerate([i.split(',') for i in nodes]):
            _register_node(network, node_idx, node_info)


def _yield_network_artefacts() -> typing.Tuple[str, typing.List, typing.List]:
    """Yields relevant artefacts from each sub-directory within $HOME/.casperlabs-stests/nets.
    
    """
    path = pathlib.Path(os.path.expanduser("~/.casperlabs-stests/nets"))
    if not path.exists:
        raise ValueError(f"Cannot find any network metadata in {path}")
    if not path.is_dir:
        raise ValueError(f"Invalid network metadata directory: {path}")

    for network_id in os.listdir(path):
        path_accounts = path / network_id / "accounts.csv"
        if not path_accounts.exists:
            raise ValueError(f"accounts.csv file not found: {path_accounts}")
        with open(path_accounts, 'r') as fstream:
            accounts = fstream.readlines()

        path_nodes = path / network_id / "nodes.csv"
        if not path_nodes.exists:
            raise ValueError(f"nodes.csv file not found: {path_nodes}")
        with open(path_nodes, 'r') as fstream:
            nodes = fstream.readlines()
        
        yield network_id, accounts, nodes


def _register_network(network_id: str):
    """Register a network.
    
    """
    network = factory.create_network(network_id)
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"registered {network.name_raw} - metadata")

    return network


def _register_faucet(
    network: Network,
    accounts: typing.List[typing.Union[str, int, str, int]]
    ):
    """Register a network's faucet account.
    
    """
    # Destructure faucet private key.
    pvk_b64, key_algo = _get_faucet_pvk(accounts)

    # Set key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_b64(pvk_b64, key_algo, crypto.KeyEncoding.HEX)

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.FAUCET,
        index=0,
        key_algo=key_algo,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"registered {network.name_raw} - faucet key")


def _register_node(
    network: Network,
    index: int,
    info: typing.Tuple[str, int, str, int]
    ):
    """Register a network node.
    
    """
    # Destructure node info.
    host, port, pvk_b64, weight = info

    # Set node.
    node = factory.create_node(
        host=host,
        index=index,  
        network_id=factory.create_network_id(network.name_raw),
        port=int(port),
        typeof=NodeType.FULL if int(weight) > 256 else NodeType.READ_ONLY,
        # weight=int(weight),
    )

    # Set bonding key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_b64(pvk_b64, crypto.KeyAlgorithm.ED25519, crypto.KeyEncoding.HEX)

    # Set bonding account.
    node.account = factory.create_account(
        network=network.name,
        typeof=AccountType.BOND,
        index=index,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=private_key,
        public_key=public_key,
    )    

    # Push.
    cache.infra.set_node(node)

    # Inform.
    utils.log(f"registered {network.name_raw} - {node.address} : {node.typeof.name}")


def _get_faucet_pvk(accounts: typing.List[typing.Union[str, int, str, int]]):
    """Returns faucet key derived from accounts.csv.
    
    """
    # Facuet is either first or last account and is distinguished by it's balance > 0.
    _, _, balance, _ = accounts[-1].split(',')
    account = accounts[-1] if int(balance) > 0 else accounts[0]

    # Destructure key info.
    pvk_b64, key_algo, _, _ = account.split(',')

    return pvk_b64, crypto.KeyAlgorithm[key_algo.upper()]


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
