from .tx import CoinBaseTx
from .block import BlockHeader
from datetime import datetime
from .merkle import block_merkle_root


all_zero = "0000000000000000000000000000000000000000000000000000000000000000"

BLOCK_REWARD = 50


def createNewBlock(txOutScript, first_txs=list(), prevHash=all_zero):
    reward = CoinBaseTx([
        {
            'value': BLOCK_REWARD,
            txOutScript: txOutScript
        }
    ])
    txs = [reward]
    txs.extend(first_txs)

    block_header = BlockHeader(
        prev_hash=prevHash,
        timestamp=str(datetime.now()),
        merkle_root=block_merkle_root(txs),
        nounce=0,
    )

    while(not block_header.is_valid):
        block_header.nounce += 1

    print("Mined block %s" % (block_header.hash))
    return block_header, txs
