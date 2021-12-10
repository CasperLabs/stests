import json
import typing

import pycspr
import requests
from pycspr.factory.accounts import parse_public_key
import sseclient

from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.events import EventType



def execute(node: Node, event_callback: typing.Callable, event_id: int = 0, stream_type="sigs"):
    """Hooks upto a node's event stream invoking passed callback for each event.

    :param node: The node to which to bind.
    :param event_callback: Callback to invoke whenever an event of relevant type is received.
    :param event_id: Identifer of event from which to start stream.

    """
    log_event(EventType.MONIT_STREAM_OPENING, node.address_event, node)

    for event_type, event_id, payload, block_hash, deploy_hash, account_key in _yield_events(node, event_id, stream_type):
        event_info = factory.create_node_event_info(
            node,
            event_id,
            event_type,
            block_hash,
            deploy_hash,
            account_key,
        )
        event_callback(node, event_info, payload)


def _yield_events(node: Node, event_id: int, event_channel: str):
    """Yields events streaming from node.

    """
    event_channel = pycspr.NodeEventChannel[event_channel]
    for event in node.client.yield_events(event_channel, None, event_id):
        parsed = _parse_event(node, event)
        if parsed:
            yield parsed


def _parse_event(node: Node, info: pycspr.NodeEventInfo):
    """Parses event information for upstream processing.
    
    """
    if info.typeof == pycspr.NodeEventType.ApiVersion:
        return
    
    if info.typeof == pycspr.NodeEventType.BlockAdded:
        return \
            EventType.MONIT_BLOCK_ADDED, \
            info.idx, \
            info.payload, \
            info.payload['BlockAdded']['block_hash'], \
            None, \
            None

    if info.typeof == pycspr.NodeEventType.DeployAccepted:
        return \
            EventType.MONIT_DEPLOY_ACCEPTED, \
            info.idx, \
            info.payload, \
            None, \
            info.payload['DeployAccepted']['deploy'], \
            None

    if info.typeof == pycspr.NodeEventType.DeployExpired:
        return \
            EventType.MONIT_DEPLOY_EXPIRED, \
            info.idx, \
            info.payload, \
            None, \
            info.payload['DeployExpired']['deploy_hash'], \
            None

    if info.typeof == pycspr.NodeEventType.DeployProcessed:
        return \
            EventType.MONIT_DEPLOY_PROCESSED, \
            info.idx, \
            info.payload, \
            info.payload['DeployProcessed']['block_hash'], \
            info.payload['DeployProcessed']['deploy_hash'], \
            None

    if info.typeof == pycspr.NodeEventType.Fault:
        return \
            EventType.MONIT_CONSENSUS_FAULT, \
            info.idx, \
            info.payload, \
            info.payload['Fault']['era_id'], \
            None, \
            None

    if info.typeof == pycspr.NodeEventType.FinalitySignature:
        return \
            EventType.MONIT_CONSENSUS_FINALITY_SIGNATURE, \
            info.idx, \
            info.payload, \
            info.payload['FinalitySignature']['block_hash'], \
            None, \
            info.payload['FinalitySignature']['public_key']

    if info.typeof == pycspr.NodeEventType.Step:
        return \
            EventType.MONIT_STEP, \
            info.idx, \
            info.payload, \
            None, \
            None, \
            info.payload['Step']['era_id']

    log_event(
        EventType.MONIT_STREAM_EVENT_TYPE_UNKNOWN,
        f"event skipped as type is unsupported :: node={node.address_rpc} :: event type={info.typeof.name}",
        node
        )
