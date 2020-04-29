import datetime
import random
import typing
from datetime import datetime as dt

from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import crypto
from stests.core.utils import factory



def create_account(typeof: AccountType=None) -> Account:
    return factory.create_account(
        status=random.choice(list(AccountStatus)),
        typeof=typeof or random.choice(list(AccountType))
    )


def create_account_id() -> AccountIdentifier:
    return AccountIdentifier(
        index=1,
        run=create_run_id()
    )


def create_block() -> Block:
    return Block(
        block_hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        deploy_cost_total=int(1e7),
        deploy_count=1,
        deploy_gas_price_avg=1,
        network="lrt1",
        j_rank=1,
        m_rank=1,
        size_bytes=int(1e8),
        timestamp=dt.now().timestamp(),
        validator_id="dca0025bfb03f7be74c47371ca74883b47587f3630becb0e7b46b7c9ae6e8500",
        status=random.choice(list(BlockStatus))
    )


def create_contract() -> Contract:
    return Contract(
        account_index=1,
        hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        name="tests-contract",
        network="lrt1",
        run_type=None,
        run_index=None,
        typeof=ContractType.TRANSFER_U512_STORED
    )


def create_deploy() -> Deploy:
    return Deploy(
        account_index=1,
        block_hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        deploy_hash="02c74421666866809a2343f95229af960077a9bfed56b31bc9f231d108958eeb",
        dispatch_node=1,
        dispatch_ts=None,
        finalization_time=None,
        finalization_ts=None,
        network="lrt1",
        run_index=1,
        run_type="WG-XXX",
        status=random.choice(list(DeployStatus)),
        typeof=DeployType.NULL
    )


def create_network() -> Network:
    index=1
    typeof=NetworkType.LOC

    return Network(
        faucet=create_account(AccountType.FAUCET),
        index=index,
        name=f"{typeof.name}-{str(index).zfill(2)}",
        name_raw=f"{typeof.name.lower()}{index}",
        status=random.choice(list(NetworkStatus)),
        typeof=random.choice(list(NetworkType)),
    )


def create_network_id() -> NetworkIdentifier:
    return factory.create_network_id("lrt1")


def create_node() -> Node:
    return Node(
        account=create_account(AccountType.BOND),
        host="localhost",
        index=1,
        network="LOC-01",
        port=40400,
        status=random.choice(list(NodeStatus)),
        typeof=random.choice(list(NodeType)),
    )


def create_node_id() -> NodeIdentifier:
    return factory.create_node_id(create_network_id(), 1)


def create_transfer() -> Transfer:
    return Transfer(
        amount=int(1e7),
        asset="CLX",
        cp1_index=1,
        cp2_index=2,
        deploy_hash="02c74421666866809a2343f95229af960077a9bfed56b31bc9f231d108958eeb",
        deploy_hash_refund=None,
        is_refundable=False,
        network="lrt1",
        node=1,
        run_index=1,
        run_type="WG-XXX",
        status=TransferStatus.PENDING
        )


def create_execution_context() -> ExecutionContext:
    return ExecutionContext(        
        args=None,
        loop_count=0,
        loop_index=0,
        loop_interval=0,
        network="LOC-01",
        node_index=1,
        phase_index=1,
        run_index=1,
        run_type="WG-XXX",
        status=ExecutionStatus.IN_PROGRESS,
        step_index=1,
        step_label="a-test-step",        
        )


def create_execution_info() -> ExecutionInfo:
    return ExecutionInfo(
        aspect=ExecutionAspect.RUN,
        network="LOC-01",
        phase_index=1,
        run_index=1,
        run_type="WG-XXX",
        status=ExecutionStatus.IN_PROGRESS,
        step_index=1,
        step_label="a-test-step",        
        tp_duration=None,
        ts_start=dt.now().timestamp(),
        ts_end=None,
        _type_key="a-type-key"
        )


def create_execution_state() -> ExecutionState:
    return ExecutionState(
        aspect=ExecutionAspect.RUN,
        network="LOC-01",
        phase_index=1,
        run_index=1,
        run_type="WG-XXX",
        status=ExecutionStatus.IN_PROGRESS,
        step_index=1,
        step_label="a-test-step",  
        _type_key="a-type-key",      
        )

def create_lock_run() -> RunLock:
    return RunLock(
        network="lrt1",
        run_index=1,
        run_type="WG-XXX",
    )


def create_lock_phase() -> PhaseLock:
    return PhaseLock(
        network="lrt1",
        run_index=1,
        run_type="WG-XXX",
        phase_index=1,
    )


def create_lock_step() -> StepLock:
    return StepLock(
        network="lrt1",
        run_index=1,
        run_type="WG-XXX",
        phase_index=1,
        step_index=1
    )


def create_lock_stream() -> StreamLock:
    return StreamLock(
        network="lrt1",
        node_index=1,
        lock_index=1
    )


def create_run_id() -> RunIdentifier:
    return RunIdentifier(
        network=create_network_id(),
        index=1,
        type="WG-XXX"
    )



# Map: encodeable type to factory function.
FACTORIES: typing.Dict[typing.Type, typing.Callable] = {
    # Domain types.
    Account: create_account,
    AccountIdentifier: create_account_id,
    Block: create_block,
    Contract: create_contract,
    Deploy: create_deploy,
    Network: create_network,
    NetworkIdentifier: create_network_id,
    Node: create_node,
    NodeIdentifier: create_node_id,
    Transfer: create_transfer,
    # Orchestration types.
    ExecutionContext: create_execution_context,
    ExecutionInfo: create_execution_info,
    ExecutionState: create_execution_state,
    RunIdentifier: create_run_id,

    RunLock: create_lock_run,
    PhaseLock: create_lock_phase,
    StepLock: create_lock_step,
    StreamLock: create_lock_stream,
}


def get_instance(dcls: typing.Type) -> typing.Any:
    try:
        factory = FACTORIES[dcls]
    except KeyError:
        raise ValueError("Unsupported domain type: {}".format(dcls))
    else:
        return factory()
