from .tx import isCoinBaseTx


class Coin:
    def __init__(self, output, coin_base):
        self.value = output.satoshis
        self.scriptPubKey = output.scriptPubKey
        self.coin_base = coin_base


class CoinsView:
    map = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(CoinsView, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, base=None):
        # map <key, Coin> key: outpoint(Tx hash + index)
        if base is not None:
            self.map.update(base.map)

    def addCoins(self, tx):
        coin_base = isCoinBaseTx(tx)
        tx_id = tx.hash
        for i, output in enumerate(tx.outputs):
            key = self.out_point(tx_id, i)
            coin = Coin(output, coin_base)
            self.map[key] = coin

    def out_point(self, tx_id, index):
        # txid + index = outpoint
        return tx_id + index
