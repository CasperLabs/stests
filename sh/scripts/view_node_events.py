import argparse
import json

from stests import chain
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from arg_utils import get_network_nodeset



# CLI argument parser.
ARGS = argparse.ArgumentParser("Renders node event stream information.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    default=1,
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )

# CLI argument: event type filter.
ARGS.add_argument(
    "--type",
    default="*",
    dest="event_type",
    help="Event type, if specified then one of: block-added | block-finalized | deploy-processed).",
    type=str
    )

# CLI argument: event id offset.
ARGS.add_argument(
    "--from",
    default=0,
    dest="event_id",
    help="The event ID from which the stream should start for this client.",
    type=int
    )


def main(args):
    """Entry point.

    :param args: Parsed CLI arguments.

    """
    def _filter(node: Node, info: NodeEventInfo, payload: dict):
        """Applies a filter to incoming events.
        
        """
        if args.event_type == "*" or \
           info.event_type.name == f"MONIT_{args.event_type.upper().replace('-', '_')}":
            _on_event_callback(node, info, payload)

    _, node = get_network_node(args)
    chain.stream_events(node, _filter, args.event_id)


def _on_event_callback(node: Node, info: NodeEventInfo, payload: dict):
    """Event callback.
    
    """
    utils.log_line()

    for label, data in (
        ("Event Emitter", info.node_address),
        ("Event ID", info.event_id),
        ("Event Type", info.event_type.name[6:]),
        ("Event Timestamp", info.event_timestamp.isoformat()),
    ):
        print(f"{label.ljust(20)}: {data}")

    print(json.dumps(payload, indent=4))        


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())