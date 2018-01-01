from datetime import datetime

from .block import Block, BlockHeader
from .merkle import block_merkle_root
from .tx import CoinBaseTx
from .types import Script, TxOutput

all_zero = "0" * 256

BLOCK_REWARD = 50


def createNewBlock(script_pub_key: Script, normal_txs: list=list(), prevHash: str=all_zero):
    reward = CoinBaseTx([
        TxOutput(satoshis=BLOCK_REWARD,
                 script_pub_key=script_pub_key)
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
