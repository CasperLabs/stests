import stests.generators.wg_100.meta as wg_100
import stests.generators.wg_101.meta as wg_101
import stests.generators.wg_110.meta as wg_110
import stests.generators.wg_111.meta as wg_111
import stests.generators.wg_200.meta as wg_200
import stests.generators.wg_201.meta as wg_201
import stests.generators.wg_210.meta as wg_210
import stests.generators.wg_211.meta as wg_211



# Set of generators.
GENERATOR_SET = {
    wg_100,
    wg_101,
    wg_110,
    wg_111,
    wg_200,
    wg_201,
    wg_210,
    wg_211,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}
