from .block import Block
from .coins import CoinsView
from .merkle import block_merkle_root
from .tx import isCoinBaseTx


def connectBlock(block: Block):
    coin_view = CoinsView()

    if (not checkBlock(block)):
        return False


def checkBlock(block: Block):

    # verify merkle hash
    if block_merkle_root(block.txs) != block.header["merkle_root"]:
        return False

    # block's first tx must be coinbase tx
    if (len(block.txs) == 0 or not isCoinBaseTx(block.txs[0])):
        return False

    # rest tx must be normal tx
    for tx in block.txs[1:]:
        if isCoinBaseTx(tx):
            return False
