from .block import Block
from .coins import outpoint_hash
from .helps import check_list_item_duplication
from .merkle import block_merkle_root
from .tx import isCoinBaseTx


def verify_block(block: Block) -> bool:

    # verify merkle hash
    if block_merkle_root(block.txs) != block.header.merkle_root:
        return False

    # block's first tx must be coinbase tx
    if (len(block.txs) == 0 or not isCoinBaseTx(block.txs[0])):
        return False

    # rest tx must be normal tx

    outpoint_hashs = []
    for tx in block.txs[1:]:
        if isCoinBaseTx(tx):
            return False

        outpoint_hashs + [outpoint_hash(*input.outpoint) for input in tx.inputs]

    # inputs duplication check
    if not check_list_item_duplication(outpoint_hashs):
        return False

    return True
