import argparse

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.types.orchestration import ExecutionAspect
from stests.core.types.orchestration import ExecutionInfo
from stests.core.types.orchestration import ExecutionStatus
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for all runs.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: run type.
ARGS.add_argument(
    "--type",
    help=f"Run type - e.g. wg-100.",
    dest="run_type",
    type=args_validator.validate_run_type,
    )

# CLI argument: status.
ARGS.add_argument(
    "--status",
    help=f"Run status - e.g. complete.",
    dest="status",
    default="all",
    )


# Table columns.
COLS = [
    ("Generator", BeautifulTable.ALIGN_LEFT),
    ("ID", BeautifulTable.ALIGN_LEFT),
    ("Execution Start Time", BeautifulTable.ALIGN_LEFT),
    ("Execution End Time", BeautifulTable.ALIGN_LEFT),
    ("Duration (s)", BeautifulTable.ALIGN_RIGHT),
    ("Deploys", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
    ("Current Step", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.orchestration.get_info_list(network_id, args.run_type)
    data = [i for i in data if i.aspect == ExecutionAspect.RUN]
    if not data:
        utils.log("No run information found.")
        return    

    # Filter by status.
    if args.status not in (None, "*"):
        for status in ExecutionStatus:
            if status.name.lower().startswith(args.status.lower()):
                data = [i for i in data if i.status == status]
                break

    # Associate info with execution context.
    ctx_list = cache.orchestration.get_context_list(network_id, args.run_type)
    for i in data:
        i.ctx = _get_ctx(i, ctx_list)

    # Associate info with deploy count.
    keys, counts = cache.orchestration.get_deploy_count_list(network_id, args.run_type)
    counts = dict(zip(keys, counts))
    for i in data:
        i.deploy_count = _get_deploy_count(i, counts)

    # Sort data.
    data = sorted(data, key=lambda i: f"{i.run_type}.{i.label_index}")

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: _get_row(i, counts), data)

    # Set table.
    t = utils.get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent  

    # Render.
    print(t)
    print("----------------------------------------------------------------------------------------------------------------------------")
    print(f"{network_id.name} - total runs = {len(data)}.")
    print("----------------------------------------------------------------------------------------------------------------------------")


def _get_ctx(i, ctx_list):
    """Returns execution context associated with a run.
    
    """
    for ctx in ctx_list:
        if i.run_type == ctx.run_type and i.run_index == ctx.run_index:
            return ctx


def _get_deploy_count(i: ExecutionInfo, counts):
    """Returns count of deploys dispatched during course of a run.
    
    """
    key = f"{i.network}:{i.run_type}:{i.label_run_index}:deploy-count:-"
    for count in counts:
        if count.endswith(key):
            return counts[count]

    return "--"


def _get_row(i, counts):
    """Returns table row data.
    
    """
    deploy_count = _get_deploy_count(i, counts)

    return [
        i.run_type,
        i.label_index.strip(),
        i.ts_start.isoformat()[:-3],
        i.ts_end.isoformat()[:-3] if i.ts_end else "--",
        i.label_tp_elapsed,
        i.deploy_count,
        i.label_status.strip(),
        "--".rjust(20) if (i.ctx is None or i.ctx.status == ExecutionStatus.COMPLETE) else f"{i.ctx.step_label.rjust(20)}",
    ]


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
