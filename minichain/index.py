from .coins import CoinsView
from .crypto import Ecc
from .miner import createNewBlock
from .script import interpret, pay_to_public_key_hash, script_sig
from .tx import NormalTx
from .types import EMPTY_SCRIPT_SIG, OutPoint, ScriptSig, TxInput, TxOutput
from .validation import connectBlock


def main():
    person1 = Ecc()
    person2 = Ecc()

    script1 = pay_to_public_key_hash(person1.pub_key)
    genesisBlock = createNewBlock(script1)
    connectBlock(genesisBlock)

    # Script verify
    coin_view = CoinsView()

    prevTx = genesisBlock.txs[0]

    outputs = [TxOutput(50, pay_to_public_key_hash(person2.pub_key))]
    sig1 = NormalTx([TxInput(OutPoint(prevTx.hash, 0),
                             EMPTY_SCRIPT_SIG)],
                    outputs).sig(person1.priv_key)
    normal_tx1 = NormalTx([TxInput(OutPoint(prevTx.hash, 0), ScriptSig(sig1, person1.pub_key))],
                          outputs)
    prevOutput = coin_view.getCoin(normal_tx1.inputs[0].outpoint).output
    script = script_sig(normal_tx1.inputs[0].script_sig) + prevOutput.script_pub_key
    env = interpret(script, normal_tx1)
    print(env.is_tx_valid)
