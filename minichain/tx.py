import json
from typing import List

from .crypto import Ecc, sha256
from .types import EMPTY_SCRIPT_SIG, TxInput, TxOutput


class Tx:

    def __init__(self, outputs: List[TxOutput]):
        self.outputs = outputs

    def toString(self):
        raise NotImplemented

    def serialize(self):
        return self.toString()

    @property
    def hash(self):
        return sha256(sha256(self.serialize()))

    def sig(self, priv_key):
        return Ecc.sign(self.withEmptyInputsScriptSig().hash, priv_key)

    def withEmptyInputsScriptSig(self):
        raise NotImplemented


class CoinBaseTx(Tx):
    def __init__(self, outputs: List[TxOutput]):
        super(CoinBaseTx, self).__init__(outputs)

    def toString(self):
        return json.dumps({
            'outputs': self.outputs
        })


class NormalTx(Tx):
    def __init__(self, inputs: List[TxInput], outputs: List[TxOutput]):
        self.inputs = inputs
        super(NormalTx, self).__init__(outputs)

    def toString(self):
        return json.dumps({
            "inputs": self.inputs,
            "outputs": self.outputs
        })

    def withEmptyInputsScriptSig(self):
        new_inputs = [TxInput(outpoint=input.outpoint,
                              script_sig=EMPTY_SCRIPT_SIG)
                      for input in self.inputs]
        return NormalTx(new_inputs, self.outputs)


def isCoinBaseTx(tx):
    return isinstance(tx, CoinBaseTx)
