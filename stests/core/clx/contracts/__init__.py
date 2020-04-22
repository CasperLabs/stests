from stests.core.clx.contracts import counter_define_by_hash
from stests.core.clx.contracts import counter_define_by_name
from stests.core.clx.contracts import transfer_U512_by_hash
from stests.core.clx.contracts import transfer_U512_by_wasm
from stests.core.types.chain import ContractType



# Set of supported contracts.
CONTRACTS = {
    counter_define_by_hash,
    counter_define_by_name,
    transfer_U512_by_hash,
    transfer_U512_by_wasm,
}

# Map: Contract type -> contract moduel.
CONTRACTS_BY_TYPE = {i.TYPE: i for i in CONTRACTS}

# Set of supported singleton contracts (i.e. installed once and used from other accounts).
CONTRACTS_BY_HASH = {
    counter_define_by_hash,
    transfer_U512_by_hash,
}


def get_contract(contract_type: ContractType):
    """Returns pointer to a contract for subsequent use.
    
    :param contract_type: Type of contract to be installed.

    :returns: Pointer to a contract.

    """
    for contract in CONTRACTS:
        if contract.TYPE == contract_type or contract.TYPE.name == contract_type:
            return contract

    raise ValueError(f"Unsupported contract type: {contract_type}")
