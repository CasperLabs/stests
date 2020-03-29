import typing

from stests.core.clx.contracts.utils_installer import install as _install
from stests.core.clx.contracts import counter_define
from stests.core.clx.contracts import counter_define_stored
from stests.core.clx.contracts import transfer
from stests.core.clx.contracts import transfer_u512_stored
from stests.core.domain import Account
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier



# Set of support contracts.
CONTRACTS = {
    counter_define,
    # counter_define_stored,
    # transfer,
    transfer_u512_stored,
}


def install(
    network_id: typing.Union[Network, NetworkIdentifier],
    account,
    contract,
    node_id: NodeIdentifier = None
    ) -> str:
    """Installs a contract under an account & returns installed contract's hash.
    
    :param network: Network into which contract is being installed.
    :param contract: Module of contract to be deployed.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param node_id: Identifier of node to which deploys will be dispatched.

    :returns: Contract hash (in hex format).

    """
    if contract not in CONTRACTS:
        raise ValueError("Unsupported contract.")

    return _install(network_id, account, contract, node_id)
