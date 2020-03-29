import typing

from stests.core.clx.contracts import utils_installer as installer
from stests.core.clx.contracts import counter_define
from stests.core.clx.contracts import counter_define_stored
from stests.core.clx.contracts import transfer_U512
from stests.core.clx.contracts import transfer_U512_stored
from stests.core.domain import Account
from stests.core.domain import ContractType
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext



# Set of supported contracts.
CONTRACTS = {
    counter_define,
    counter_define_stored,
    transfer_U512,
    transfer_U512_stored,
}

# Map: Contract type -> contract moduel.
CONTRACTS_BY_TYPE = {i.TYPE.name: i for i in CONTRACTS}

# Set of supported singleton contracts (i.e. installed once and used from other accounts).
CONTRACTS_SINGLETON = set([i for i in CONTRACTS if i.IS_SINGLETON])


def install_named(
    ctx: ExecutionContext,
    account,
    contract_type: ContractType,
    node_id: NodeIdentifier = None
    ) -> str:
    """Installs a singleton contract under an account & returns installed contract's hash.
    
    :param ctx: Execution context information.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param contract_type: Type of contract to be installed.
    :param node_id: Identifier of node to which deploy will be dispatched.

    :returns: Contract hash (in hex format).

    """
    if contract_type not in CONTRACTS_BY_TYPE:
        raise ValueError(f"Unsupported contract type: {contract_type}")

    contract = CONTRACTS_BY_TYPE[contract_type]

    return installer.install_named(ctx, account, contract, node_id)


def install_singleton(
    network_id: typing.Union[Network, NetworkIdentifier],
    account,
    contract,
    node_id: NodeIdentifier = None
    ) -> str:
    """Installs a singleton contract under an account & returns installed contract's hash.
    
    :param network_id: Network into which contract is being installed.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param contract: Module of contract to be deployed.
    :param node_id: Identifier of node to which deploy will be dispatched.

    :returns: Contract hash (in hex format).

    """
    if contract not in CONTRACTS_SINGLETON:
        raise ValueError("Unsupported contract.")

    return installer.install_singleton(network_id, account, contract, node_id)
