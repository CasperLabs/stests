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
    for payload, event_type, block_hash, deploy_hash in _yield_events(node):
        event_callback(node, factory.create_node_event_info(
            node,
            0,    # TODO: get event identifier from payload
            event_type,
            block_hash,
            deploy_hash,
        ), payload)


def _yield_events(node: Node):
    """Yields events streaming from node.

    """
    stream = requests.get(node.url_event, stream=True)
    client = sseclient.SSEClient(stream)
    try:
        for event in client.events():
            parsed = _parse_event_payload(node, json.loads(event.data))
            if parsed:
                yield parsed
    except Exception as err:
        try:
            client.close()
        except:
            pass
        finally:
            raise err


def _parse_event_payload(node: Node, obj: dict) -> typing.Tuple[dict, EventType, typing.Optional[str], typing.Optional[str]]:
    """Parses raw event data for upstream processing.

    """
    if 'ApiVersion' in obj:
        return

    if 'BlockAdded' in obj:
        return \
            obj, \
            EventType.MONIT_BLOCK_ADD, \
            obj['BlockAdded']['block_hash'], \
            None

    if 'BlockFinalized' in obj:
        return \
            obj, \
            EventType.MONIT_BLOCK_FINALIZED, \
            obj['BlockFinalized']['proto_block']['hash'], \
            None

    if 'DeployProcessed' in obj:
        return \
            obj, \
            EventType.MONIT_DEPLOY_PROCESSED, \
            None, \
            None

    log_event(
        EventType.MONIT_STREAM_EVENT_TYPE_UNKNOWN,
        f"event skipped as type is unsupported :: node={node.address_rpc}",
        node
        )
    print(obj)
