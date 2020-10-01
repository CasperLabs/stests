import random
from datetime import datetime

from stests.core import crypto
from stests.core.types.chain import Account
from stests.core.types.chain import AccountIdentifier
from stests.core.types.chain import AccountType
from stests.core.types.chain import Block
from stests.core.types.chain import BlockStatistics
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import BlockSummary
from stests.core.types.chain import ContractType
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.chain import DeploySummary
from stests.core.types.chain import DeployType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import Transfer
from stests.core.types.chain import TransferStatus
from stests.core.factory.infra import create_network_id
from stests.core.factory.orchestration import create_execution_id
from stests.core.types.orchestration import ExecutionContext



def create_account(
    network: str,
    typeof: AccountType,
    index: int = 1,
    key_algo = crypto.KeyAlgorithm.ED25519,
    private_key: str = None,
    public_key: str = None,
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    if private_key is None:
        private_key, public_key = \
            crypto.get_key_pair(key_algo, crypto.KeyEncoding.HEX)

    return Account(
        account_hash=crypto.get_account_hash(key_algo, public_key),
        account_id=crypto.get_account_id(key_algo, public_key),
        key_algo=key_algo.name,
        index=index if index is not None else 1,
        network=network,
        private_key=private_key,
        public_key=public_key,
        run_index=None,
        run_type=None,
        typeof=typeof
        )


def create_account_for_run(
    ctx: ExecutionContext,
    typeof: AccountType,
    index: int = 1,
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    try:
        key_algo = crypto.KeyAlgorithm[ctx.key_algorithm]
    except KeyError:
        key_algo = random.choice(list(crypto.KeyAlgorithm))

    account = create_account(
        ctx.network,
        typeof,
        index=index,
        key_algo=key_algo,
        )
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


def create_block_statistics_on_finalization(
    block_hash: str,
    chain_name: str,
    deploy_cost_total: int,
    deploy_count: int,
    deploy_gas_price_avg: int,
    j_rank: int,
    m_rank: int,
    magic_bit: int,
    message_role: str,
    network: str,
    round_id: int,
    size_bytes: int,
    timestamp: datetime,
    validator_id: str,
    ) -> BlockStatistics:
    """Returns a domain object instance: BlockStatistics.
    
    """
    return BlockStatistics(
        block_hash=block_hash,
        chain_name=chain_name,
        deploy_cost_total=deploy_cost_total,
        deploy_count=deploy_count,
        deploy_gas_price_avg=deploy_gas_price_avg,
        j_rank=j_rank,
        m_rank=m_rank,
        magic_bit=magic_bit,
        message_role=message_role,
        network=network,
        round_id=round_id,
        size_bytes=size_bytes,
        status=BlockStatus.FINALIZED,
        timestamp=timestamp,
        validator_id=validator_id,
    )


def create_block_summary_on_finalisation(info: NodeEventInfo) -> BlockSummary:
    """Returns a domain object instance: BlockSummary.
    
    """
    return BlockSummary(
        block_hash=info.block_hash,
        network=info.network,
        status=BlockStatus.FINALIZED,
    )


def create_deploy_for_run(
    ctx: ExecutionContext,
    account: Account,
    node: Node,
    deploy_hash: str,
    dispatch_attempts: int,
    dispatch_duration: float,
    typeof: DeployType
    ) -> Deploy:
    """Returns a domain object instance: Deploy.

    """
    return Deploy(
        account=account.account_id,
        account_index=account.index,
        block_hash=None,
        deploy_cost=None,
        deploy_hash=deploy_hash,
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        dispatch_node=node.address,
        dispatch_timestamp=datetime.now(),
        finalization_duration=None,
        finalization_node=None,
        finalization_timestamp=None,
        network=ctx.network,
        phase_index=ctx.phase_index,
        round_id=None,
        run_index=ctx.run_index,
        run_type=ctx.run_type,        
        status=DeployStatus.DISPATCHED,
        step_index=ctx.step_index,
        step_label=ctx.step_label,
        typeof=typeof,
    )


def create_deploy_summary_on_finalisation(info: NodeEventInfo) -> DeploySummary:
    """Returns a domain object instance: DeploySummary.
    
    """
    return DeploySummary(
        block_hash=info.block_hash,
        deploy_hash=info.deploy_hash,
        network=info.network,
        status=DeployStatus.FINALIZED,
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
        account_id=account.account_id,
        account_index=account.index,
        contract_type=contract_type,
        hash=hash,
        name=name,
        network=account.network,
        run_index=account.run_index,
        run_type=account.run_type,
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
        asset=asset or "CSPR",
        cp1_index=cp1.index,
        cp2_index=cp2.index,
        deploy_hash=deploy_hash,
        dispatch_timestamp=datetime.now(),
        network=ctx.network,
        node=ctx.node_index,
        phase_index=ctx.phase_index,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        step_index=ctx.step_index,
        step_label=ctx.step_label,
        status=status
    )
