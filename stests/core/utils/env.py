"""
.. module:: stests.core.utils.env.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: System test environment access utility functions.

.. moduleauthor:: Mark Conway-Greenslade <mark@casperlabs.io>

"""
import os


# Package env var prefix.
_PREFIX = 'CL_STESTS_'


def get_env_var(name: str, default=None) -> str:
    """Returns an environment variable's current value.

    :param name: Environment variable name.
    :param default: Environment variable default value.

    :returns: An environment variable's current value.

    """
    # Apply prefix.
    key = f'{_PREFIX}{name.upper()}'

    return os.getenv(key) or default


def get_network_id(default="LOC-DEV-01") -> str:
    """Returns identifier of network being tested.

    :param default: Network identifier default value.

    :returns: Network identifier.

    """
    # Apply prefix.
    key = f'{_PREFIX}CONFIG_NETWORK_ID'

    return os.getenv(key) or default
