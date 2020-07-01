import stests.workflows.generators.wg_100.meta as wg_100
import stests.workflows.generators.wg_110.meta as wg_110
import stests.workflows.generators.wg_120.meta as wg_120
import stests.workflows.generators.wg_200.meta as wg_200
import stests.workflows.generators.wg_210.meta as wg_210
import stests.workflows.generators.wg_1000.meta as wg_1000



# Set of generators.
GENERATOR_SET = {
    wg_100,
    wg_110,
    wg_120,
    wg_200,
    wg_210,
    wg_1000,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}
