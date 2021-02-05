import random
import typing
from datetime import datetime

from stests.core import crypto
from stests.core.types.chain import Account
from stests.core.types.chain import AccountIdentifier
from stests.core.types.chain import AccountType
from stests.core.types.chain import Block
from stests.core.types.chain import BlockStatistics
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import ContractType
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.chain import DeployType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
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
    run_index=None,
    run_type=None,
    run_uid=None,
    ) -> Account:
    """Returns a domain object instance: Account.

    """
    if private_key is None:
        private_key, public_key = \
            _get_account_key_pair(
                network,
                typeof,
                index,
                key_algo,
                run_uid,
                )

    return Account(
        account_hash=crypto.get_account_hash_from_public_key(key_algo, public_key),
        account_key=crypto.get_account_key(key_algo, public_key),
        key_algo=key_algo.name,
        index=index if index is not None else 1,
        network=network,
        private_key=private_key,
        public_key=public_key,
        run_index=run_index,
        run_type=run_type,
        run_uid=run_uid,
        typeof=typeof
        )


def create_account_for_run(
    ctx: ExecutionContext,
    index: int = 1,
    run_type: str = None,
    ) -> Account:
    """Returns a domain object instance: Account.

    """
    try:
        key_algo = crypto.KeyAlgorithm[ctx.key_algorithm]
    except KeyError:
        key_algo = random.choice(list(crypto.KeyAlgorithm))

    return create_account(
        ctx.network,
        AccountType.GENERATOR_RUN,
        index=index,
        key_algo=key_algo,
        run_index=ctx.run_index,
        run_type=run_type or ctx.run_type,
        run_uid=ctx.uid,
        )


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


def create_account_key(
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


def create_block_on_addition(
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


def create_block_statistics_on_addition(
    block_hash: str,
    block_hash_parent: str,
    chain_name: str,
    deploy_cost_total: int,
    deploy_count: int,
    deploy_gas_price_avg: int,
    era_id: int,
    height: int,
    is_switch_block: bool,
    network: str,
    size_bytes: str,
    state_root_hash: str,
    status: int,
    timestamp: datetime,
    proposer: str,
    ) -> BlockStatistics:
    """Returns a domain object instance: BlockStatistics.

    """
    return BlockStatistics(
        block_hash = block_hash,
        block_hash_parent = block_hash_parent,
        chain_name = chain_name,
        deploy_cost_total = deploy_cost_total,
        deploy_count = deploy_count,
        deploy_gas_price_avg = deploy_gas_price_avg,
        era_id = era_id,
        height = height,
        is_switch_block = is_switch_block,
        network = network,
        size_bytes = size_bytes,
        state_root_hash = state_root_hash,
        status = status,
        timestamp = timestamp,
        proposer = proposer,
    )


def create_deploy_for_run(
    ctx: ExecutionContext,
    account: Account,
    node: Node,
    deploy_hash: str,
    dispatch_attempts: int,
    dispatch_duration: float,
    typeof: DeployType,
    associated_account: Account = None,
    ) -> Deploy:
    """Returns a domain object instance: Deploy.

    """
    return Deploy(
        account=account.account_key,
        account_index=account.index,
        associated_account=associated_account.account_key if associated_account else None,
        associated_account_index=associated_account.index if associated_account else None,
        block_hash=None,
        deploy_cost=None,
        deploy_hash=deploy_hash,
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        dispatch_node_index=node.index,
        dispatch_timestamp=datetime.utcnow(),
        era_id=None,
        finalization_duration=None,
        finalization_node_index=None,
        finalization_timestamp=None,
        network=ctx.network,
        phase_index=ctx.phase_index,
        round_id=None,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        state_root_hash=None,
        status=DeployStatus.DISPATCHED,
        step_index=ctx.step_index,
        step_label=ctx.step_label,
        typeof=typeof,
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
        account_key=account.account_key,
        account_index=account.index,
        contract_type=contract_type,
        hash=hash,
        name=name,
        network=account.network,
        run_index=account.run_index,
        run_type=account.run_type,
    )


def _get_account_key_pair(
    network: str,
    typeof: AccountType,
    index: int = 1,
    key_algo = crypto.KeyAlgorithm.ED25519,
    run_uid = None,
    ) -> typing.Tuple[str, str]:
    """Returns an ECC key pair to represent an on-chain account.

    """
    if typeof == AccountType.NETWORK_FAUCET:
        private_key, public_key = \
            crypto.get_key_pair(key_algo, crypto.KeyEncoding.HEX)

    elif typeof == AccountType.VALIDATOR_BOND:
        private_key, public_key = \
            crypto.get_key_pair(key_algo, crypto.KeyEncoding.HEX)

    elif typeof == AccountType.GENERATOR_RUN:
        # seed = f"{key_algo.name}-{network}-{run_uid}-{typeof.name}-{index}"
        # seed = seed.upper().encode("utf-8")
        # seed = crypto.get_hash(seed, encoding=crypto.HashEncoding.BYTES)
        # private_key, public_key = \
        #     crypto.get_key_pair_from_seed(seed, crypto.KeyAlgorithm.ED25519, crypto.KeyEncoding.HEX)
        private_key, public_key = \
            crypto.get_key_pair(key_algo, crypto.KeyEncoding.HEX)

    elif typeof == AccountType.OTHER:
        seed = f"{key_algo.name}-{network}-{typeof.name}-{index}"
        seed = seed.upper().encode("utf-8")
        seed = crypto.get_hash(seed, encoding=crypto.HashEncoding.BYTES)
        private_key, public_key = \
            crypto.get_key_pair_from_seed(seed, crypto.KeyAlgorithm.ED25519, crypto.KeyEncoding.HEX)

    return private_key, public_key
