import argparse
import os
import pathlib
import typing

import toml

from stests.core import cache
from stests.core import crypto
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeGroup
from stests.core.types.infra import NodeType
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Register an nctl network with stests.")

# Map: key prefix to algo.
KEY_ALGO = {
    "01": "ed25519",
    "02": "secp256k1",
}


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    for artefacts in _yield_artefacts():
        _register(artefacts)


def _get_account(accounts, public_key, key_algo):
    """Returns matching entry in accounts.toml.

    """
    for account in [i for i in accounts['accounts'] if i.get("validator", False)]:
        pbk =  account["public_key"]
        if pbk.startswith(f"0{key_algo.value}") and pbk.endswith(public_key):
            return pbk, \
                KEY_ALGO[pbk[0:2]], \
                account["balance"], \
                int(account["validator"]["bonded_amount"])


def _yield_artefacts():
    """Yields aretefacts for mapping to stests types.

    """
    # Set path to nctl network artefacts.
    path = pathlib.Path(os.getenv("NCTL")) / "assets"
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid nctl network - network path not found: {path}")

    # Set paths to each network.
    paths = [i for i in path.rglob("net-*") if i.is_dir()]
    if not paths:
        raise ValueError(f"Invalid nctl network - networks undefined")

    # For each nctl network, yield relevant artefacts.
    for path in paths:
        yield int(str(path).split("-")[-1]), \
              _get_artefacts_count_of_bootstrap_nodes(path), \
              _get_artefacts_count_of_genesis_nodes(path), \
              _get_artefacts_accounts(path), \
              _get_artefacts_faucet(path), \
              _get_artefacts_nodeset(path)


def _get_artefacts_accounts(path: pathlib.Path) -> typing.List[dict]:
    """Returns accounts artefacts to be mapped.

    """
    # Set path to accounts.toml.
    path = path / "chainspec" / "accounts.toml"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - accounts.toml file not found: {path}")

    # Open accounts.toml.
    data = toml.load(path)

    return data


def _get_artefacts_faucet(path: pathlib.Path):
    """Returns faucet artefacts to be mapped.

    """
    # Set path to private key.
    path = path / "faucet" / "secret_key.pem"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - private key file not found: {path}")

    return path


def _get_artefacts_count_of_bootstrap_nodes(_: pathlib.Path) -> int:
    """Returns number of network bootstrap nodes.

    """
    return 3


def _get_artefacts_count_of_genesis_nodes(path: pathlib.Path) -> int:
    """Returns number of network genesis nodes.

    """
    path = path / "nodes"

    return int(len(os.listdir(path)) / 2)


def _get_artefacts_nodeset(path: pathlib.Path):
    """Returns nodeset artefacts to be mapped.

    """
    # Set path to nodeset.
    path = path / "nodes"
    if not path.exists():
        raise ValueError(f"Invalid nctl network - nodes undefined")

    # Set paths to each node.
    paths = [i for i in path.rglob("node-*") if i.is_dir()]
    if not paths:
        raise ValueError(f"Invalid nctl network - nodes undefined")
    paths = sorted(paths, key=lambda p: str(p).split("-")[-1].rjust(3, '0'))

    return [_get_artefacts_node(i) for i in paths]


def _get_artefacts_node(path: pathlib.Path) -> typing.Tuple[int, dict, pathlib.Path]:
    """Returns node artefacts to be mapped.

    """
    # Set path to config.
    path_cfg = path / "config" / "1_0_0" / "config.toml"
    if not path_cfg.exists():
        raise ValueError(f"Invalid nctl node - node config toml file not found: {path}")

    # Set path to private key.
    path_pvk = path / "keys" / "secret_key.pem"
    if not path_pvk.exists():
        raise ValueError(f"Invalid nctl node - private key file not found: {path}")

    return \
        int(str(path).split("-")[-1]), \
        toml.load(path_cfg), \
        path_pvk


def _register(artefacts):
    """Register a network.

    """
    network_idx, count_of_bootstrap_nodes, count_of_genesis_nodes, accounts, faucet_pvk_as_pem, nodeset = artefacts
    network = _register_network(network_idx, count_of_bootstrap_nodes, count_of_genesis_nodes)
    _register_faucet(network, faucet_pvk_as_pem)
    for node in nodeset:
        _register_node(network, accounts, node)


def _register_faucet(network: Network, path_pvk_pem: str):
    """Register a network's faucet account.

    """
    # Set key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_pvk_pem,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.NETWORK_FAUCET,
        index=0,
        key_algo=crypto.DEFAULT_KEY_ALGO,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Registered {network.name} - faucet key")


def _register_network(network_idx: int, count_of_bootstrap_nodes: int, count_of_genesis_nodes: int):
    """Register a network.

    """
    # Set network.
    network = factory.create_network(
        f"nctl{network_idx}",
        f"casper-net-{network_idx}",
        count_of_bootstrap_nodes,
        count_of_genesis_nodes,
        )

    # Push to cache.
    cache.infra.set_network(network)

    # Inform.
    utils.log(f"Registered {network.name} - metadata")

    return network


def _register_node(network: Network, accounts: dict, info: typing.Tuple[int, dict, pathlib.Path]):
    """Register a network node.

    """
    # Destructure node info.
    index, cfg, path_pvk_pem = info

    # Set bonding key pair.
    private_key, public_key = crypto.get_key_pair_from_pvk_pem_file(
        path_pvk_pem,
        crypto.DEFAULT_KEY_ALGO,
        crypto.KeyEncoding.HEX
        )

    # Set entry in accounts.toml.
    account_info = _get_account(accounts, public_key, crypto.DEFAULT_KEY_ALGO)
    if account_info is None:
        return

    # Set staking weight.
    _, _, _, stake_weight = account_info

    # Set node addrress.
    node_address_event = cfg['event_stream_server']['address']
    node_address_rest = cfg['rest_server']['address']
    node_address_rpc = cfg['rpc_server']['address']

    # Set node host.
    node_host_event = node_address_event.split(":")[0]
    node_host_rest = node_address_rest.split(":")[0]
    node_host_rpc = node_address_rpc.split(":")[0]
    assert node_host_event == node_host_rest == node_host_rpc, "hostname mismatch"
    node_host = node_host_event

    # Set node ports - derived.
    node_port_event = _get_node_port("event", network.index, index)
    node_port_rpc = _get_node_port("rpc", network.index, index)
    node_port_rest = _get_node_port("rest", network.index, index)

    # Set node group.
    if index <= network.count_of_bootstrap_nodes:
        group = NodeGroup.BOOTSTRAP
    elif index <= network.count_of_genesis_nodes:
        group = NodeGroup.GENESIS
    else:
        group = NodeGroup.OTHER

    # Set function flags - initially only interact with genesis nodes.
    use_to_dispatch = group in (NodeGroup.BOOTSTRAP, NodeGroup.GENESIS)
    use_to_monitor = group in (NodeGroup.BOOTSTRAP, NodeGroup.GENESIS)
    use_to_query = group in (NodeGroup.BOOTSTRAP, NodeGroup.GENESIS)

    # Set node.
    node = factory.create_node(
        group=group,
        host=node_host,
        index=index,
        network_id=factory.create_network_id(network.name_raw),
        port_rest=node_port_rest,
        port_rpc=node_port_rpc,
        port_event=node_port_event,
        typeof=NodeType.VALIDATOR,
        use_to_dispatch=use_to_dispatch,
        use_to_monitor=use_to_monitor,
        use_to_query=use_to_query,
        weight=stake_weight,
    )

    # Set bonding account.
    node.account = factory.create_account(
        network=network.name,
        typeof=AccountType.VALIDATOR_BOND,
        index=index,
        key_algo=crypto.KeyAlgorithm.ED25519,
        private_key=private_key,
        public_key=public_key,
    )

    # Push.
    cache.infra.set_node(node)

    # Inform.
    utils.log(f"Registered {node.label}")


def _get_node_port(port_type:str, net_index: int, node_index: int) -> int:
    """Returns a node port.

    """
    if port_type == "rpc":
        return 40000 + (net_index * 100) + node_index
    if port_type == "rest":
        return 50000 + (net_index * 100) + node_index
    if port_type == "event":
        return 60000 + (net_index * 100) + node_index


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
