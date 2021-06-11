import random
import typing
from datetime import datetime as dt

from stests import events
from stests.core import crypto
from stests.core import factory
from stests.core import types
from stests.core.types.logging import LogMessage



def create_account() -> types.chain.Account:
    return factory.create_account(
        network="lrt1",
        typeof=random.choice(list(types.chain.AccountType)),
    )


def create_account_key() -> types.chain.AccountIdentifier:
    return factory.create_account_key(
        index=1,
        network="lrt1",
        run_index=1,
        run_type="WG-100",
    )


def create_block() -> types.chain.Block:
    return factory.create_block_on_addition(
        node_id=create_node_id(),
        block_hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        deploy_cost_total=int(1e7),
        deploy_count=1,
        deploy_gas_price_avg=10,
        j_rank=1,
        m_rank=1,
        size_bytes=int(1e8),
        timestamp=dt.utcnow().timestamp(),
        validator_id="dca0025bfb03f7be74c47371ca74883b47587f3630becb0e7b46b7c9ae6e8500",
    )


def create_block_statistics() -> types.chain.BlockStatistics:
    return factory.create_block_statistics_on_addition(
        block_hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        chain_name="main",
        deploy_cost_total=int(1e7),
        deploy_count=1,
        deploy_gas_price_avg=10,
        era_id=42,
        j_rank=1,
        m_rank=1,
        magic_bit=1,
        message_role="a-role",
        network="lrt1",
        round_id=12,
        size_bytes=int(1e8),
        timestamp=dt.utcnow().timestamp(),
        validator_id="dca0025bfb03f7be74c47371ca74883b47587f3630becb0e7b46b7c9ae6e8500",
    )


def create_deploy() -> types.chain.Deploy:
    return factory.create_deploy_for_run(
        ctx=create_execution_context(),
        account=create_account(),
        associated_account=create_account(),
        node=create_node(),
        deploy_hash="02c74421666866809a2343f95229af960077a9bfed56b31bc9f231d108958eeb",
        dispatch_attempts=1,
        dispatch_duration=float(2),
        typeof=random.choice(list(types.chain.DeployType)),
    )


def create_named_key() -> types.chain.NamedKey:
    return factory.create_named_key(
        account=create_account(),
        contract_type=random.choice(list(types.chain.ContractType)),
        name="a-named-key",
        hash="02c74421666866809a2343f95229af960077a9bfed56b31bc9f231d108958eeb",
    )


def create_network() -> types.infra.Network:
    return factory.create_network(
        f"{types.infra.NetworkType.LOC.name}-{str(1).zfill(2)}",
        types.infra.NetworkType.LOC.name
    )


def create_network_id() -> types.infra.NetworkIdentifier:
    return factory.create_network_id("lrt1")


def create_node() -> types.infra.Node:
    return factory.create_node(
        host="localhost",
        index=1,
        network_id=create_network_id(),
        port_rest=14101,
        port_rpc=11101,
        port_event=18101,
        typeof=random.choice(list(types.infra.NodeType)),
        status=random.choice(list(types.infra.NodeStatus)),
    )


def create_node_event_info() -> types.infra.NodeEventInfo:
    return factory.create_node_event_info(
        node=create_node(),
        event_id=1001,
        event_type=random.choice(list(events.EventType)),
        block_hash="9dbc064574aafcba8cadbd20aa6ef5b396e64ba970d829c188734ac09ae34f64",
        deploy_hash="02c74421666866809a2343f95229af960077a9bfed56b31bc9f231d108958eeb",
    )


def create_node_id() -> types.infra.NodeIdentifier:
    return factory.create_node_id(create_network_id(), 1)


def create_node_monitoring_lock() -> types.infra.NodeMonitoringLock:
    return factory.create_node_monitoring_lock(
        node_id=create_node_id(),
        lock_index=1
    )


def create_execution_context() -> types.orchestration.ExecutionContext:
    return factory.create_execution_context(
        args=None,
        prune_on_completion=False,
        deploys_per_second=100,
        key_algorithm="ED25519",
        loop_count=10,
        loop_interval_ms=1000,
        execution_mode="periodic",
        network_id=create_network_id(),
        node_id=create_node_id(),
        run_index=1,
        run_type="WG-100",
    )


def create_execution_identifier() -> types.orchestration.ExecutionIdentifier:
    return factory.create_execution_id(
        network_id=create_network_id(),
        run_index=1,
        run_type="WG-100",
    )


def create_execution_info() -> types.orchestration.ExecutionInfo:
    return factory.create_execution_info(
        aspect=random.choice(list(types.orchestration.ExecutionAspect)),
        ctx=create_execution_context(),
    )


def create_execution_lock() -> types.orchestration.ExecutionLock:
    return factory.create_execution_lock(
        aspect=random.choice(list(types.orchestration.ExecutionAspect)),
        network="lrt1",
        run_index=1,
        run_type="WG-100",
        phase_index=1,
        step_index=1,
    )


def create_log_application_info() -> types.logging.ApplicationInfo:
    return types.logging.ApplicationInfo(
        system="stests",
        sub_system="unit tests",
        version="1.0.0",
    )


def create_log_event_info() -> types.logging.EventInfo:
    return types.logging.EventInfo(
        id="1234",
        level=types.logging.Level.DEBUG,
        priority=1,
        timestamp=dt.utcnow().timestamp(),
        type="UNIT_TEST",
    )

def create_log_message() -> types.logging.LogMessage:
    return types.logging.LogMessage(
        app=create_log_application_info(),
        event=create_log_event_info(),
        process=create_log_process_info(),
        message="Hello Dolly",
        data={
            "a-field": 1234,
        },
    )


def create_log_process_info() -> types.logging.ProcessInfo:
    return types.logging.ProcessInfo(
        os_user="a-0",
        pid="12345"
    )


# Map: encodeable type to factory function.
FACTORIES: typing.Dict[typing.Type, typing.Callable] = {
    # Chain types.
    types.chain.Account: create_account,
    types.chain.AccountIdentifier: create_account_key,
    types.chain.Block: create_block,
    types.chain.BlockStatistics: create_block_statistics,
    types.chain.Deploy: create_deploy,
    types.chain.NamedKey: create_named_key,

    # Infra types.
    types.infra.Network: create_network,
    types.infra.NetworkIdentifier: create_network_id,
    types.infra.Node: create_node,
    types.infra.NodeEventInfo: create_node_event_info,
    types.infra.NodeIdentifier: create_node_id,
    types.infra.NodeMonitoringLock: create_node_monitoring_lock,

    # Orchestration types.
    types.orchestration.ExecutionContext: create_execution_context,
    types.orchestration.ExecutionIdentifier: create_execution_identifier,
    types.orchestration.ExecutionInfo: create_execution_info,
    types.orchestration.ExecutionLock: create_execution_lock,

    # Logging types.
    types.logging.LogMessage: create_log_message,
    types.logging.ApplicationInfo: create_log_application_info,
    types.logging.EventInfo: create_log_event_info,
    types.logging.ProcessInfo: create_log_process_info,
}


def get_instance(dcls: typing.Type) -> typing.Any:
    try:
        factory = FACTORIES[dcls]
    except KeyError:
        raise ValueError("Unsupported domain type: {}".format(dcls))
    else:
        return factory()
