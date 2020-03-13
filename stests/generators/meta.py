import stests.generators.wg_100.meta as wg_100
import stests.generators.wg_200.meta as wg_200



# Set of generators.
GENERATOR_SET = {
    wg_100,
    wg_200,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}
