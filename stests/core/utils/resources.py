"""
.. module:: stests.core.utils.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: System test resources accessor.

.. moduleauthor:: Mark Conway-Greenslade <mark@casperlabs.io>

"""
import pathlib



# Name of resources directory.
_DIR_NAME = "resources"


def get_wasm(fname: str):
    """Instantiates, initialises & returns a term authority.

    :param str fname: Name of wasm file to load into memory.

    :returns: A loaded wasm file.
    :rtype: [byte]

    """
    with open(get_wasm_path(fname), "rb") as fstream:
        return fstream.read()


def get_wasm_path(fname: str):
    """Returns path to a test wasm file resource.

    :param str fname: Name of a wasm file.

    :returns: Path to a test wasm file.
    :rtype: str

    """
    if fname.split(".")[-1] != "wasm":
        fname = f"{fname}.wasm"

    return _get_dir("wasm").joinpath(fname)


def _get_dir(sub_dir=None):
    """Returns path to resources directory.

    """  
    # TODO: use env var
    root = pathlib.Path(__file__).parent.parent.parent.joinpath(_DIR_NAME)

    return root if sub_dir is None else root / sub_dir
