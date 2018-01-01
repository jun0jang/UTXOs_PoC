from .crypto import Ecc
from .miner import createNewBlock
from .script import interpret, pay_to_public_key_hash, script_sig
from .tx import NormalTx
from .types import EMPTY_SCRIPT_SIG, OutPoint, ScriptSig, TxInput, TxOutput
from .validation import connectBlock


def sendTx(sending_ecc: Ecc, to_pub_key: str, value: int, outpoint: OutPoint) -> NormalTx:
    outputs = [
        TxOutput(value, pay_to_public_key_hash(to_pub_key))
    ]
    sig = NormalTx(
        [TxInput(outpoint, EMPTY_SCRIPT_SIG)],
        outputs
    ).sig(sending_ecc.priv_key)
    normal_tx = NormalTx(
        [TxInput(outpoint, ScriptSig(sig, sending_ecc.pub_key))],
        outputs
    )
    return normal_tx


def main():
    person1 = Ecc()
    person2 = Ecc()

    script1 = pay_to_public_key_hash(person1.pub_key)
    genesisBlock = createNewBlock(script1)
    connectBlock(genesisBlock)

    # Script verify
    prevTx = genesisBlock.txs[0]
    normal_tx1 = sendTx(person1, person2.pub_key, 50, OutPoint(prevTx.hash, 0))
    script = script_sig(normal_tx1.inputs[0].script_sig) + prevTx.outputs[0].script_pub_key
    env = interpret(script, normal_tx1)
    print(env.is_tx_valid)
