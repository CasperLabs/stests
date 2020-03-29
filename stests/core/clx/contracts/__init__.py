import typing

from stests.core.clx.contracts.utils_installer import install as _install
from stests.core.clx.contracts import counter_define
from stests.core.clx.contracts import counter_define_stored
from stests.core.clx.contracts import transfer_U512
from stests.core.clx.contracts import transfer_U512_stored
from stests.core.domain import Account
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier



# Set of supported singleton contracts (i.e. installed once and used from other accounts).
CONTRACTS_SINGLETON = {
    counter_define,
    transfer_U512_stored,
}


def install(
    network_id: typing.Union[Network, NetworkIdentifier],
    account,
    contract,
    node_id: NodeIdentifier = None
    ) -> str:
    """Installs a singleton contract under an account & returns installed contract's hash.
    
    :param network: Network into which contract is being installed.
    :param contract: Module of contract to be deployed.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param node_id: Identifier of node to which deploys will be dispatched.

    :returns: Contract hash (in hex format).

    """
    if contract not in CONTRACTS_SINGLETON:
        raise ValueError("Unsupported contract.")

    return _install(network_id, account, contract, node_id)
