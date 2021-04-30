import os
import pathlib

from stests.core.types.infra import Network



# Name of casper client binary.
_BINARY_CLIENT = "casper-client"


def get_path_to_client(network: Network):
    """Returns a path to node rust client.

    :param network: Target network being tested.
    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a smart contract wasm blob.
    
    """
    return _get_path_to_binary(network, _BINARY_CLIENT)


def get_path_to_contract(network: Network, wasm_filename: str):
    """Returns a path to a smart contract.

    :param network: Target network being tested.
    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a smart contract wasm blob.
    
    """
    return _get_path_to_binary(network, wasm_filename)


def _get_path_to_binary(network: Network, fname: str):
    """Returns a path to a binary executable.

    :param network: Target network being tested.
    :param fname: Name of binary file to be loaded into memory.

    :returns: Path to a binary file.
    
    """
    # LRT paths.
    if network.name_raw.startswith('lrt'):
        path = pathlib.Path(os.path.expanduser("~/.casperlabs-stests/nets")) / f"{network.name_raw}" / "bin" / fname
        if path.exists():
            return path

    # NCTL paths.
    if network.name_raw.startswith('nctl'):
        path_nctl = pathlib.Path(os.getenv("NCTL")) / "assets" / f"net-{network.index}" / "bin"

        path = path_nctl / fname
        if path.exists():
            return path

        path = path_nctl / "auction" / fname
        if path.exists():
            return path

        path = path_nctl / "eco" / fname
        if path.exists():
            return path

        path = path_nctl / "transfers" / fname
        if path.exists():
            return path

    # Custom.
    if os.getenv("CSPR_BIN"):
        path = pathlib.Path(os.getenv("CSPR_BIN")) / fname
        if path.exists():
            return path

    raise ValueError(f"Binary file could not be found: {network.name_raw} :: {fname}")
