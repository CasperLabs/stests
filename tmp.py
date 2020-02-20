import casperlabs_client as pyclx
client = pyclx.CasperLabsClient()


deploys = [
    ("1d46c241eded38dff0b9fed5d08c787f5b3c9e35a2ac91575d51288d9479b563", "0ac15b8757f6ecf005d83a75c4304afec20d2e098c2c110acd6ea56011dbaac1"),
    ("ecc110979e11849afa8f15d0b5d7607b6c22af31f39c35a4b8b031e45211b3b6", "c90198c68f4a0ad55178c608fa4ac9ca1522e90c7a6308c9ee6d6542b01b0047"),
    ("9b8ef99a898f8eac8a75b162d1f51dc70ed259094aef5aff42940dd94062607b", "e21d0a07709709a5e3b6beca4ca036a195b0522de2022473db23c232504c7267"),
    ("a0dd9e419627be993a330e405d14d8e98ffa8422a02a831eba399f84cb74cfad", "e21d0a07709709a5e3b6beca4ca036a195b0522de2022473db23c232504c7267"),
    ("cce49305a543d12ee85110f883c28180aaf939f90061d995b8a5f0faf8e2cb3d", "d9c7cad273a1d23359bafa0753a641958d9c29ee55717033f7f3a0ee480f2dbd"),
]

# for dhash, _ in deploys:
#     for entity in cache.get_run_deploys(dhash):
#         print(entity)

# bhash = "f4a121bef3949827f2ef2406c1c873109203dec5e4b3b9521d2958f020c0d1d1"
# cache.get_networks()

from stests.core import cache
from test.core.utils_factory import create_block, create_network_id

network_id = create_network_id()
block = create_block()

key, was_cached = cache.set_network_block(network_id, block) 

print(key, was_cached)

