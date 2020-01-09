from stests.generators.wg_100.phase_01.workflow.args import ARGS
from stests.generators.wg_100.phase_01.workflow.factory import get_workflow
from stests.core.mq.initialiser import init as init_broker
from stests.core.utils.execution import ExecutionContext
from stests.generators.wg_100 import metadata



# Set args.
args = ARGS.parse_args()

# Set context.
ctx = ExecutionContext.create(args.network_id, metadata.ID, args.simulator_run_id)

# Initialise broker.
init_broker(ctx)

# Set workflow (must be done AFTER broker is initialised).
workflow = get_workflow(ctx, args)

# Execute.
workflow.run()
