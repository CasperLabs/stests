from stests.generators import launcher
from stests.generators.wg_100 import meta


# Will start off 1 or N runs depending on parallel-count cli arg.
launcher.start_generator(meta)
