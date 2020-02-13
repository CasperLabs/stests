import casperlabs_client as pyclx


client = pyclx.CasperLabsClient()


def on_block_added(block_info):
    print(666, type(new_block_info), new_block_info)


def on_block_finalized(new_finalized_block):
    print(777, type(new_finalized_block), new_finalized_block)


for event in client.stream_events():
    if event.HasField("block_added"):
        on_block_added(event.block_added.block)
    elif event.HasField("new_finalized_block"):
        on_block_finalized(event.new_finalized_block)
    else:
        print(dir(event))

# for block in client.showBlocks(100):
#     print(type(block))
