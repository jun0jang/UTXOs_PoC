from .block import Block
from .block_validation import verify_block
from .coins import CoinsView
from .tx_validation import verify_tx


def connectBlock(block: Block):
    coin_view = CoinsView(temporary=True)

    if (not verify_block(block)):
        return False

    for tx in block.txs:
        if not verify_tx(tx):
            return False

        coin_view.update_coin(tx)

    coin_view.flush()
    return True
