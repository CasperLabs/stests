from stests.workflows.generators import launcher
from stests.workflows.generators.wg_200 import meta


# Will start off 1 or N runs depending on parallel-count cli arg.
launcher.start_generator(meta)
