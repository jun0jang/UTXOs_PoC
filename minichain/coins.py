from typing import List

from .tx import isCoinBaseTx
from .types import OutPoint, TxInput, TxOutput


class Coin:
    def __init__(self, output: TxOutput, coin_base: bool):
        self.output = output
        self.coin_base = coin_base
        self.is_spent = False

    def __repr__(self):
        return "coinbase: %s, satoshis: %s" % (self.coin_base,
                                               self.output.satoshis)

    def set_spent(self):
        self.is_spent = True


class CoinsView:
    map = {}
    temporary_map = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(CoinsView, cls).__new__(cls)
        return cls.instance

    def __init__(self, temporary=False):
        # map <key, Coin> key: outpoint(Tx hash + index)
        if temporary is not None:
            self.temporary_map = self.map

    def update_coin(self, tx):
        coin_base = isCoinBaseTx(tx)
        tx_id = tx.hash
        for i, output in enumerate(tx.outputs):
            key = outpoint_hash(tx_id, i)
            coin = Coin(output, coin_base)
            self.temporary_map[key] = coin

    def flush(self):
        self.map.update(self.temporary_map)

    def get_coin(self, outpoint: OutPoint) -> Coin:
        return self.map[outpoint_hash(*outpoint)]

    def hasInputs(self, inputs: List[TxInput]):
        for input in inputs:
            if not self.hasCoin(input.outpoint):
                return False
        return True

    def hasCoin(self, outpoint: OutPoint):
        key = outpoint_hash(*outpoint)
        coin = self.temporary_map.get(key, None)
        if coin or not coin.is_spent:
            return True

        return False


def outpoint_hash(tx_id, index):
    # txid + index = outpoint
    return tx_id + str(index)
