# Initialise logging.
from stests.core import logging
logging.initialise(logging.OutputMode.INTERACTIVE)

# Initialise broker.
from stests.core import mq
mq.initialise()

# Initialise encoder.
from stests.core.mq import encoder
encoder.initialise()

# Import actors: generators.
import stests.workflows.generators.wg_100.meta
import stests.workflows.generators.wg_110.meta
import stests.workflows.generators.wg_200.meta
import stests.workflows.generators.wg_210.meta

# Import actors: orchestration.
import stests.workflows.orchestration.actors
