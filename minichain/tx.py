from .crypto import sha256

import json


class Tx:

    def __init__(self, outputs):
        self.outputs = outputs

    def serialize(self):
        return self.toString()

    def toString(self):
        raise NotImplemented

    @property
    def hash(self):
        return sha256(sha256(self.serialize()))


class CoinBaseTx(Tx):

    def toString(self):
        return json.dumps(self.outputs)