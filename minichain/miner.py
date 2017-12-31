from datetime import datetime

from .block import Block, BlockHeader
from .merkle import block_merkle_root
from .tx import CoinBaseTx
from .types import TxOutput

all_zero = "0000000000000000000000000000000000000000000000000000000000000000"

BLOCK_REWARD = 50


def createNewBlock(scriptPubKey, normal_txs=list(), prevHash=all_zero):
    reward = CoinBaseTx([
        TxOutput(satoshis=BLOCK_REWARD,
                 scriptPubKey=scriptPubKey)
    ])
    txs = [reward]
    txs.extend(normal_txs)

    block_header = BlockHeader(
        prev_hash=prevHash,
        timestamp=str(datetime.now()),
        merkle_root=block_merkle_root(txs),
        nounce=0,
    )

    while(not block_header.is_valid):
        block_header.nounce += 1

    print("Mined block %s" % (block_header.hash))
    return Block(block_header, txs)
