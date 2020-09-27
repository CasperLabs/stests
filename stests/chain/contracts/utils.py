import os
import pathlib

from stests.core.types.infra import Network
from stests.core.utils.env import get_var



def get_contract_path(wasm_filename: str, network: Network=None) -> pathlib.Path:
    """Returns a path to a smart contract.

    :param wasm_filename: Name of wasm file to be loaded into memory.
    :param network: Target network being tested.

    :returns: Path to a wasm blob.
    
    """
    # Return wasm at path specified by env var.
    path = pathlib.Path(get_var("PATH_WASM")) / wasm_filename    
    if path.exists():
        return path

    # Return wasm at NCTL path.
    path = pathlib.Path(os.getenv("NCTL")) / "assets" / f"net-{network.index}" / "bin" / wasm_filename
    if path.exists():
        return path

    raise ValueError("WASM file could not be found.")
