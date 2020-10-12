import stests.orchestration.generators.wg_100.meta as wg_100
import stests.orchestration.generators.wg_110.meta as wg_110
import stests.orchestration.generators.wg_200.meta as wg_200



# Set of generators.
GENERATOR_SET = {
    wg_100,
    wg_110,
    wg_200,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}
