import pathlib

from stests.core.utils.env import get_var



def get_contract_path(wasm_filename: str) -> pathlib.Path:
    """Returns a path to a smart contract.

    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a wasm blob.
    
    """
    # Return wasm at path specified by env var.
    path = pathlib.Path(get_var("PATH_WASM")) / wasm_filename    
    if path.exists():
        return path

    # Return wasm at python client root.
    path = pathlib.Path(os.path.dirname(casperlabs_client.__file__)) / wasm_filename
    if path.exists():
        return path

    raise ValueError("WASM file could not be found. Verify the STESTS_PATH_WASM env var setting.")