import typing

from casperlabs_client.abi import ABI

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.clx.query import get_balance
from stests.core.domain import *
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger



@utils.clx_op
def do_refund(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int = None,
    contract: Contract = None,
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a refund between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be refunded.

    :returns: Dispatched deploy.

    """
    # Set amount - escape if cp1 has insufficient funds.
    amount = amount or (get_balance(ctx, cp1) - defaults.CLX_TX_FEE)
    if amount <= 0:
        logger.log_warning("Counter party 1 does not have enough CLX to pay refund transaction fee.")
        return

    (node, dhash) = do_transfer(ctx, cp1, cp2, amount, contract, is_refundable=False, deploy_type=DeployType.TRANSFER_REFUND)

    return (node, dhash, amount)


@utils.clx_op
def do_transfer(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    contract: Contract = None,
    is_refundable: bool = True,
    deploy_type: DeployType = DeployType.TRANSFER
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param contract: The transfer contract to call (if any).
    :param is_refundable: Flag indicating whether a refund is required.
    :param deploy_type: The type of deploy to dispatch.

    :returns: Dispatched deploy & transfer.

    """
    # Set client.
    node, client  = utils.get_client(ctx)

    # Transfer using on-chain contract hash - does not dispatch wasm.
    if contract:
        # Set args.
        session_args = ABI.args([
            ABI.account("address", cp2.public_key),
            ABI.big_int("amount", amount)
            ])
        # Dispatch.
        dhash = client.deploy(
            session_hash=contract.hash_as_bytes,
            session_args=session_args,
            from_addr=cp1.public_key,
            private_key=cp1.private_key_as_pem_filepath,
            # TODO: allow these to be passed in via standard arguments
            payment_amount=defaults.CLX_TX_FEE,
            gas_price=defaults.CLX_TX_GAS_PRICE
        )

    # Transfer using local contract - dispatches wasm.
    else:
        # Dispatch.
        dhash = client.transfer(
            amount=amount,
            target_account_hex=cp2.public_key,
            from_addr=cp1.public_key,
            private_key=cp1.private_key_as_pem_filepath,
            # TODO: allow these to be passed in via standard arguments
            payment_amount=defaults.CLX_TX_FEE,
            gas_price=defaults.CLX_TX_GAS_PRICE
        )

    logger.log(f"PYCLX :: transfer :: {dhash} :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key[:8]}")

    return (node, dhash)


@utils.clx_op
def do_deploy_network_contract(
    network: Network,
    contract_type: ContractType,
    contract_name: str
    ) -> str:
    """Deploys a client side smart contract to chain for future reference.

    :param network: Network to which a client contract is being deployed.
    :param contract_type: Type of contract to be deployed.
    :param contract_name: Name of contract as specified in wasm blob.

    :returns: Contract hash (in hex format).

    """
    # Set client.
    _, client = utils.get_client(network)

    # Set args.
    session=utils.get_contract_path(contract_type)
    session_args = ABI.args([
        ABI.string_value("target", "hash")
        ])

    # Dispatch.
    dhash = client.deploy(
        session=session,
        session_args=session_args,
        from_addr=network.faucet.public_key,
        private_key=network.faucet.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: deploy-contract :: {contract_type.value} :: dhash={dhash} -> awaiting processing")

    # Get block hash.
    dinfo = client.showDeploy(dhash, wait_for_processed=True)
    bhash = dinfo.processing_results[0].block_info.summary.block_hash.hex()
    logger.log(f"PYCLX :: deploy-contract :: {contract_type.value} :: dhash={dhash} -> processing complete")

    # Get contract hash.
    chash = utils.get_contract_hash(client, network.faucet, bhash, contract_name)
    logger.log(f"PYCLX :: deploy-contract :: {contract_type.value} :: chash={chash}")

    return chash


@utils.clx_op
def do_deploy_contract(
    ctx: ExecutionContext,
    account: Account,
    contract_type: ContractType
    ) -> typing.Tuple[Node, str]:
    """Deploys a smart contract to chain for future use.

    :param ctx: Execution context information.
    :param account: Account under which contract will be deployed.
    :param contract_type: Type of contract to be deployed.

    :returns: 2 member tuple -> (node, deploy hash)

    """
    # Set client.
    node, client = utils.get_client(ctx)

    # Set args.
    session=utils.get_contract_path(ContractType[contract_type])
    session_args = ABI.args([
        ABI.string_value("target", "hash"),
        ])
    
    # Dispatch.
    dhash = client.deploy(
        session=session,
        session_args=session_args,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: deploy-contract :: {contract_type} :: dhash={dhash}")

    return (node, dhash)


@utils.clx_op
def do_deploy_contract_to_name(
    ctx: ExecutionContext,
    account: Account,
    contract_type: ContractType
    ) -> typing.Tuple[Node, str]:
    """Deploys a smart contract to a known name for future use.

    :param ctx: Execution context information.
    :param account: Account under which contract will be deployed.
    :param contract_type: Type of contract to be deployed.

    :returns: 2 member tuple -> (node, deploy hash)

    """
    # Set client.
    node, client = utils.get_client(ctx)

    # Set args.
    session=utils.get_contract_path(ContractType[contract_type])
    
    # Dispatch.
    dhash = client.deploy(
        session=session,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: deploy-contract :: {contract_type} :: dhash={dhash}")

    return (node, dhash)


@utils.clx_op
def do_deploy_contract_to_hash(
    ctx: ExecutionContext,
    account: Account,
    contract_type: ContractType
    ) -> typing.Tuple[Node, str]:
    """Deploys a smart contract to a hash for future use.

    :param ctx: Execution context information.
    :param account: Account under which contract will be deployed.
    :param contract_type: Type of contract to be deployed.

    :returns: 2 member tuple -> (node, deploy hash)

    """
    # Set client.
    node, client = utils.get_client(ctx)

    # Set args.
    session=utils.get_contract_path(ContractType[contract_type])
    session_args = ABI.args([
        ABI.string_value("target", "hash")
        ])
    
    # Dispatch.
    dhash = client.deploy(
        session=session,
        session_args=session_args,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: deploy-contract :: {contract_type} :: dhash={dhash}")

    return (node, dhash)