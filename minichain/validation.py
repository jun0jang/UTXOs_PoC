from .block import Block
from .coins import CoinsView
from .merkle import block_merkle_root
from .tx import isCoinBaseTx


def connectBlock(block: Block):
    coin_view = CoinsView(temporary=True)

    if (not check_block(block)):
        return False

    for tx in block.txs:
        if not verify_tx(tx):
            return False

        coin_view.update_coin(tx)

    # if one of txs is not verify, CoinsView is not synchronization
    coin_view.flush()
    return True


def check_block(block: Block):

    # verify merkle hash
    if block_merkle_root(block.txs) != block.header.merkle_root:
        return False

    # block's first tx must be coinbase tx
    if (len(block.txs) == 0 or not isCoinBaseTx(block.txs[0])):
        return False

    # rest tx must be normal tx
    for tx in block.txs[1:]:
        if isCoinBaseTx(tx):
            return False

    return True


def verify_tx(tx):

    if isCoinBaseTx(tx):
        return True
