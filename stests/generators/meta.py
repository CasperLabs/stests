import stests.generators.wg_100.meta as wg_100
import stests.generators.wg_110.meta as wg_110



# Set of generators.
GENERATOR_SET = {
    wg_100,
    wg_110,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}
