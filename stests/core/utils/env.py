"""
.. module:: stests.core.utils.env.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: System test environment access utility functions.

.. moduleauthor:: Mark Conway-Greenslade <mark@casperlabs.io>

"""
import os
import typing



# Package env var prefix.
_PREFIX = 'STESTS_'


def get_var(
    name: str,
    default=None,
    convertor: typing.Callable = None
    ) -> str:
    """Returns an environment variable's current value.

    :param name: Environment variable name.
    :param default: Environment variable default value.
    :param convertor: Value conversion function to apply.

    :returns: An environment variable's current value.

    """
    name = get_var_name(name)
    value = os.getenv(name)
    value = value or default

    return value if convertor is None or value is None else convertor(value)


def get_var_name(name: str) -> str:
    """Returns an environment variable's name.

    :param name: Environment variable name.

    :returns: An environment variable's full name.

    """
    return f'{_PREFIX}{name.upper()}'


def get_network_id(default="LOC-01") -> str:
    """Returns identifier of network being tested.

    :param default: Network identifier default value.

    :returns: Network identifier.

    """
    return get_var("CONFIG_NETWORK_ID", default)
