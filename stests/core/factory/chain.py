from datetime import datetime

from stests.core.types.chain import Account
from stests.core.types.chain import AccountIdentifier
from stests.core.types.chain import AccountType
from stests.core.types.chain import Block
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import ContractType
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.chain import DeploySummary
from stests.core.types.chain import DeployType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import Transfer
from stests.core.types.chain import TransferStatus
from stests.core.factory.infra import create_network_id
from stests.core.factory.orchestration import create_execution_id
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import crypto



def create_account(
    network: str,
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    if private_key is None:
        private_key, public_key = crypto.generate_key_pair(crypto.KeyEncoding.HEX)        

    return Account(
        index=index if index is not None else 1,
        network=network,
        private_key=private_key,
        public_key=public_key,
        run_index=None,
        run_type=None,
        typeof=typeof
        )


def create_account_for_run(
    ctx:ExecutionContext,
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    account = create_account(ctx.network, typeof, index, private_key, public_key)
    account.run_index = ctx.run_index
    account.run_type = ctx.run_type

    return account


def create_account_id(
    index: int,
    network: str,
    run_index: int,
    run_type: int,
    ) -> AccountIdentifier:
    """Returns a cache identifier: AccountIdentifier.
    
    """
    network_id = create_network_id(network)

    return AccountIdentifier(
        index=index,
        run=create_execution_id(network_id, run_index, run_type)
    )


def create_named_key(
    account: Account,
    contract_type: ContractType,
    name: str,
    hash: str,
    ) -> NamedKey:
    """Returns a domain object instance: NamedKey.
    
    """
    return NamedKey(
        account_index=account.index,
        contract_type=contract_type,
        hash=hash,
        name=name,
        network=account.network,
        run_index=account.run_index,
        run_type=account.run_type,
    )


def create_block_on_finalisation(
    node_id: NodeIdentifier,
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
        network=node_id.network.name,
        node_index=node_id.index,
        size_bytes=size_bytes,
        status=BlockStatus.FINALIZED,
        timestamp=timestamp,
        validator_id=validator_id
        )


def create_deploy_for_run(
    ctx: ExecutionContext,
    account: Account,
    node: Node,
    deploy_hash: str,
    typeof: DeployType
    ) -> Deploy:
    """Returns a domain object instance: Deploy.

    """
    return Deploy(
        account_index=account.index,
        block_hash=None,
        cost=None,
        deploy_hash=deploy_hash,
        dispatch_node=node.index,
        dispatch_ts=datetime.now(),
        finalization_node=None,
        finalization_time=None,
        finalization_time_is_acceptable=None,
        finalization_time_tolerance=None,
        finalization_ts=None,
        network=ctx.network,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,        
        status=DeployStatus.DISPATCHED,
        step_index=ctx.step_index,
        step_label=ctx.step_label,
        typeof=typeof,
    )


def create_transfer(
    ctx: ExecutionContext,
    amount: int,
    asset: str,
    cp1: Account,
    cp2: Account,
    deploy_hash: str,
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
        dispatch_ts=datetime.now(),
        network=ctx.network,
        node=ctx.node_index,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        step_index=ctx.step_index,
        step_label=ctx.step_label,
        status=status
    )
