from .tx import isCoinBaseTx
from .types import OutPoint, TxOutput


class Coin:
    def __init__(self, output: TxOutput, coin_base: bool):
        self.output = output
        self.coin_base = coin_base

    def __repr__(self):
        return "coinbase: %s, satoshis: %s" % (self.coin_base,
                                               self.output.satoshis)


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
            self.temporary_map = {}

    def update_coin(self, tx):
        coin_base = isCoinBaseTx(tx)
        tx_id = tx.hash
        for i, output in enumerate(tx.outputs):
            key = self.out_point(tx_id, i)
            coin = Coin(output, coin_base)
            self.temporary_map[key] = coin

    def out_point(self, tx_id, index):
        # txid + index = outpoint
        return tx_id + str(index)

    def flush(self):
        self.map.update(self.temporary_map)

    def getCoin(self, outpoint: OutPoint) -> Coin:
        return self.map[self.out_point(*outpoint)]
