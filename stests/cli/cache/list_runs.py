import argparse

from beautifultable import BeautifulTable

from stests.cli.utils import get_table
from stests.core import cache
from stests.core.orchestration import ExecutionAspect
from stests.core.orchestration import ExecutionStatus
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for all runs.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network,
    )

# CLI argument: run type.
ARGS.add_argument(
    "--run-type",
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
    ("Start Time", BeautifulTable.ALIGN_LEFT),
    ("End Time", BeautifulTable.ALIGN_LEFT),
    ("Duration (s)", BeautifulTable.ALIGN_RIGHT),
    ("Status", BeautifulTable.ALIGN_RIGHT),
    ("Parent ID", BeautifulTable.ALIGN_RIGHT),
    ("Step", BeautifulTable.ALIGN_RIGHT),
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
        logger.log("No run information found.")
        return    

    # Filter by status.
    if args.status not in (None, "*"):
        for status in ExecutionStatus:
            if status.name.lower().startswith(args.status.lower()):
                data = [i for i in data if i.status == status]
                break
        #         print(status)
        # print(args.status)


    # Associate info with ctx.
    ctx_list = cache.orchestration.get_context_list(network_id, args.run_type)
    for i in data:
        i.ctx = _get_ctx(i, ctx_list)

    # Sort data.
    data = sorted(data, key=lambda i: f"{i.run_type}.{i.index_label}")

    # Set cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: _get_row(i), data)

    # Set table.
    t = get_table(cols, rows, max_width=1080)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent  

    # Render.
    print(t)
    print(f"Total runs = {len(data)}.  ")


def _get_ctx(i, ctx_list):
    for ctx in ctx_list:
        if i.run_type == ctx.run_type and i.run_index == ctx.run_index:
            return ctx


def _get_row(i):
    """Returns table row data.
    
    """
    return [
        i.run_type,
        i.index_label.strip(),
        i.ts_start,
        "--" if i.ts_end is None else i.ts_end,
        i.tp_elapsed_label,
        i.status_label.strip(),
        i.run_index_parent_label.strip(),
        "--" if (i.ctx is None or i.ctx.status == ExecutionStatus.COMPLETE) else \
        f"{i.ctx.step_label.strip()} > {i.ctx.label_step.strip()}",
    ]


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
