import json
import typing

import requests
import sseclient

from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.events import EventType



def execute(node: Node, event_callback: typing.Callable, event_id: int = 0):
    """Hooks upto a node's event stream invoking passed callback for each event.

    :param node: The node to which to bind.
    :param event_callback: Callback to invoke whenever an event of relevant type is received.
    :param event_id: Identifer of event from which to start stream.

    """
    log_event(EventType.MONIT_STREAM_OPENING, node.address_event, node)
    for event_type, event_id, payload, block_hash, deploy_hash, account_key in _yield_events(node, event_id):
        event_info = factory.create_node_event_info(
            node,
            event_id,
            event_type,
            block_hash,
            deploy_hash,
            account_key,
        )
        event_callback(node, event_info, payload)


def _yield_events(node: Node, event_id: int):
    """Yields events streaming from node.

    """
    # Set url.
    url = node.url_event
    if event_id:
        url = f"{url}?start_from={event_id}"

    # Set client.
    stream = requests.get(url, stream=True)
    client = sseclient.SSEClient(stream)

    # Bind to stream & yield parsed events.
    try:
        for event in client.events():
            parsed = _parse_event(node, event.id, json.loads(event.data))
            if parsed:
                yield parsed

    # On stream error close & re-raise.
    except Exception as err:
        try:
            client.close()
        except:
            pass
        finally:
            raise err


def _parse_event(
    node: Node,
    event_id: int,
    payload: dict,
    ) -> typing.Tuple[
        EventType,
        int,                   # event id
        dict,                  # payload
        typing.Optional[str],  # block hash
        typing.Optional[str],  # deploy hash
        typing.Optional[str],  # account key
        ]:
    """Parses raw event data for upstream processing.

    """
    if 'ApiVersion' in payload:
        return

    elif 'BlockAdded' in payload:
        return \
            EventType.MONIT_BLOCK_ADDED, \
            event_id, \
            payload, \
            payload['BlockAdded']['block_hash'], \
            None, \
            None

    elif 'BlockFinalized' in payload:
        return \
            EventType.MONIT_BLOCK_FINALIZED, \
            event_id, \
            payload, \
            payload['BlockFinalized']['proto_block']['hash'], \
            None, \
            None

    elif 'FinalitySignature' in payload:
        return \
            EventType.MONIT_CONSENSUS_FINALITY_SIGNATURE, \
            event_id, \
            payload, \
            payload['FinalitySignature']['block_hash'], \
            None, \
            payload['FinalitySignature']['public_key']

    elif 'Fault' in payload:
        return \
            EventType.MONIT_CONSENSUS_FAULT, \
            event_id, \
            payload, \
            payload['Fault']['era_id'], \
            None, \
            None

    elif 'DeployProcessed' in payload:
        return \
            EventType.MONIT_DEPLOY_PROCESSED, \
            event_id, \
            payload, \
            payload['DeployProcessed']['block_hash'], \
            payload['DeployProcessed']['deploy_hash'], \
            None

    elif 'Step' in payload:
        return \
            EventType.MONIT_STEP, \
            event_id, \
            payload, \
            None, \
            None, \
            payload['Step']['era_id']

    log_event(
        EventType.MONIT_STREAM_EVENT_TYPE_UNKNOWN,
        f"event skipped as type is unsupported :: node={node.address_rpc} :: event type={list(payload.keys())[0]}",
        node
        )
