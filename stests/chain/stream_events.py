import json
import typing

import requests
import sseclient

from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import Node
from stests.events import EventType



def execute(node: Node, event_callback: typing.Callable):
    """Hooks upto a node's event stream invoking passed callback for each event.

    :param node: The node to which to bind.
    :param event_callback: Callback to invoke whenever an event of relevant type is received.

    """
    log_event(EventType.MONIT_STREAM_OPENING, node.address_event, node)

    # Iterate events.
    for event_type, event_id, payload, block_hash, deploy_hash in _yield_events(node):
        # Set event information for upstream.
        event_info = factory.create_node_event_info(
            node,
            event_id,
            event_type,
            block_hash,
            deploy_hash,
        )

        # Invoke callback.
        event_callback(node, event_info, payload)


def _yield_events(node: Node):
    """Yields events streaming from node.

    """
    # Set client.
    stream = requests.get(node.url_event, stream=True)
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


def _parse_event(node: Node, event_id: int, payload: dict) -> typing.Tuple[EventType, int, dict, typing.Optional[str], typing.Optional[str]]:
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
            None

    elif 'BlockFinalized' in payload:
        return \
            EventType.MONIT_BLOCK_FINALIZED, \
            event_id, \
            payload, \
            payload['BlockFinalized']['proto_block']['hash'], \
            None

    elif 'DeployProcessed' in payload:
        return \
            EventType.MONIT_DEPLOY_PROCESSED, \
            event_id, \
            payload, \
            payload['DeployProcessed']['block_hash'], \
            payload['DeployProcessed']['deploy_hash']

    log_event(
        EventType.MONIT_STREAM_EVENT_TYPE_UNKNOWN,
        f"event skipped as type is unsupported :: node={node.address_rpc}",
        node
        )
