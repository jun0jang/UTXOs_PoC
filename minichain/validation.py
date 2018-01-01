from .block import Block
from .coins import CoinsView, outpoint_hash
from .helps import check_list_item_duplication
from .merkle import block_merkle_root
from .tx import NormalTx, isCoinBaseTx


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

    if not check_inputs(tx):
        return False


def check_inputs(tx: NormalTx):
    coins_view = CoinsView()

    # it return false if inputs's outpoint is spend or not found
    if not coins_view.hasInputs(tx.inputs):
        return False

    # inputs duplication check
    outpoint_hashs = [outpoint_hash(*input.outpoint) for input in tx.inputs]
    if check_list_item_duplication(outpoint_hashs):
        return False

    # input's value must be greater then output's value
    value_in = 0
    for input in tx.inputs:
        prev_outpoint = input.outpoint
        coin = coins_view.get_coin(prev_outpoint)
        value_in += coin.output.satoshis

    value_out = 0
    for output in tx.outputs:
        value_out = output.satoshis

    if value_in < value_out:
        return False

    return True
