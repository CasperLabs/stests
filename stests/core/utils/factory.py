from datetime import datetime
import typing

from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import crypto



def create_account(
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    status: AccountStatus = AccountStatus.NEW
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    if private_key is None:
        private_key, public_key = crypto.generate_key_pair(crypto.KeyEncoding.HEX)        

    return Account(
        index=index if index is not None else 1,
        network=None,
        node=None,
        private_key=private_key,
        public_key=public_key,
        run_index=None,
        run_type=None,
        status=status or AccountStatus.NEW,
        typeof=typeof
        )


def create_account_for_run(
    ctx:ExecutionRunInfo,
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    status: AccountStatus = AccountStatus.NEW
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    account = create_account(typeof, index, private_key, public_key, status)
    account.network = ctx.network
    account.node = ctx.node_index
    account.run_index = ctx.run_index
    account.run_type = ctx.run_type

    return account


def create_account_id(
    index: int,
    network: str,
    run_index: int,
    run_type: int,
    ) -> Account:
    """Returns a cache identifier: Account.
    
    """
    network_id = create_network_id(network)

    return AccountIdentifier(
        index=index,
        run=create_run_id(network_id, run_index, run_type)
    )


def create_block(
    network_id: NetworkIdentifier,
    block_hash: str,
    deploy_cost_total: int,
    deploy_count: int, 
    deploy_gas_price_avg: int,
    j_rank: int,
    m_rank: int,
    size_bytes: int,
    timestamp: datetime,
    validator_id: str
    ) -> Block:
    """Returns a domain object instance: Block.
    
    """
    return Block(
        block_hash=block_hash,
        deploy_cost_total=deploy_cost_total,
        deploy_count=deploy_count, 
        deploy_gas_price_avg=deploy_gas_price_avg,
        j_rank=j_rank,
        m_rank=m_rank,
        network=network_id.name,
        size_bytes=size_bytes,
        status=BlockStatus.NULL,
        timestamp=timestamp,
        validator_id=validator_id
        )


def create_deploy(
    network_id: NetworkIdentifier,
    block_hash: str,
    deploy_hash: str,
    status: DeployStatus
    ) -> Deploy:
    """Returns a domain object instance: Deploy.
    
    """
    return Deploy(
        block_hash=block_hash,
        deploy_hash=deploy_hash,
        dispatch_node=None,
        dispatch_ts=datetime.now() if status == DeployStatus.DISPATCHED else None,
        finalization_time=None,
        finalization_time_is_acceptable=None,
        finalization_time_tolerance=None,
        finalization_ts=datetime.now() if status == DeployStatus.FINALIZED else None,
        network=network_id.name,
        run_index=None,
        run_type=None,
        status=status,
        typeof=DeployType.NULL,    
    )


def create_deploy_for_run(
    ctx: ExecutionRunInfo,
    node: Node,
    deploy_hash: str,
    typeof: DeployType
    ) -> Deploy:
    """Returns a domain object instance: Deploy.

    """
    return Deploy(
        block_hash=None,
        deploy_hash=deploy_hash,
        dispatch_node=node.index,
        dispatch_ts=datetime.now(),
        finalization_time=None,
        finalization_time_is_acceptable=None,
        finalization_time_tolerance=None,
        finalization_ts=None,
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,        
        status=DeployStatus.DISPATCHED,
        typeof=typeof
    )


def create_network(name_raw: str) -> Network:
    """Returns a domain object instance: Network.
    
    """
    identifier = create_network_id(name_raw)

    return Network(
        faucet=None,
        index=identifier.index,
        name=identifier.name,
        name_raw=name_raw,
        status=NetworkStatus.HEALTHY,
        typeof=identifier.type
    )


def create_network_id(name_raw: str) -> NetworkIdentifier:
    """Returns a cache identifier: NetworkIdentifier.
    
    """
    # If name has already been parsed.
    if name_raw.upper() == name_raw:
        return NetworkIdentifier(name_raw)

    # Parse raw name.
    name_raw = name_raw.lower()
    for network_type in [i.name.lower() for i in NetworkType]:
        if name_raw.startswith(network_type):
            index=int(name_raw[len(network_type):])
            typeof=name_raw[:len(network_type)].upper()
            name = f"{typeof}-{str(index).zfill(2)}"
            return NetworkIdentifier(name=name)

    raise ValueError("Network identifier is unsupported")


def create_node(
    host: str,
    index: int,
    network_id: NetworkIdentifier,
    port: int,
    typeof: NodeType,
    status=NodeStatus.HEALTHY
    ) -> Node:
    """Returns a domain object instance: Node.
    
    """
    return Node(
        account=None,
        host=host,
        index=index,
        network=network_id.name,
        port=port,
        status=status,
        typeof=typeof
    )


def create_node_id(
    network_id: NetworkIdentifier,
    index: int
    ) -> NodeIdentifier:
    """Returns a cache identifier: NodeIdentifier.
    
    """
    return NodeIdentifier(network_id, index)


def create_run_context(
    args: typing.Any,
    loop_count: int,
    loop_interval: int,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier,
    run_index: int,
    run_type: str
    ) -> ExecutionRunInfo:
    """Returns a domain object instance: ExecutionRunInfo.
    
    """
    return ExecutionRunInfo(
        args=args,
        loop_count=loop_count,
        loop_interval=loop_interval,
        network=network_id.name,
        node_index=node_id.index,
        run_index=run_index,
        run_type=run_type,
        phase_index=0,
        step_index=0,
        step_label=None,
        # TODO: remove
        run_step=None
    )


def create_run_phase(
    network_id: NetworkIdentifier,
    run_index: int,
    run_type: str,
    phase_index: int
    ) -> ExecutionPhaseInfo:
    """Returns a domain object instance: ExecutionPhaseInfo.
    
    """
    return ExecutionPhaseInfo(
        network=network_id.name,
        phase_index=phase_index,
        run_index=run_index,
        run_type=run_type,
        status=ExecutionStatus.IN_PROGRESS,
        ts_duration=None,
        ts_start=datetime.now(),
        ts_end=None
    )


def create_run_id(
    network_id: NetworkIdentifier,
    run_index: int,
    run_type: str
    ) -> ExecutionRunIdentifier:
    """Returns a cache identifier: ExecutionRunIdentifier.
    
    """
    return ExecutionRunIdentifier(network_id, run_index, run_type)


def create_transfer(
    ctx: ExecutionRunInfo,
    amount: int,
    asset: str,
    cp1: Account,
    cp2: Account,
    deploy_hash: str,
    is_refundable: bool,
    status=TransferStatus.PENDING
    ) -> Transfer:
    """Returns a domain object instance: Transfer.
    
    """
    return Transfer(
        amount=amount,
        asset=asset or "CLX",
        cp1_index=cp1.index,
        cp2_index=cp2.index,
        deploy_hash=deploy_hash,
        deploy_hash_refund=None,
        is_refundable=is_refundable,
        network=ctx.network,
        node=ctx.node_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        status=status
    )
