from .crypto import Ecc
from .miner import createNewBlock
from .script import pay_to_public_key_hash
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
    person3 = Ecc()

    script1 = pay_to_public_key_hash(person1.pub_key)
    genesisBlock = createNewBlock(script1)
    connectBlock(genesisBlock)

    prevTx = genesisBlock.txs[0]

    tx1 = sendTx(person1, person2.pub_key, 50, OutPoint(prevTx.hash, 0))
    tx2 = sendTx(person2, person3.pub_key, 49, OutPoint(tx1.hash, 0))
    tx3 = sendTx(person3, person1.pub_key, 48, OutPoint(tx2.hash, 0))

    script2 = pay_to_public_key_hash(person2.pub_key)
    block1 = createNewBlock(script2, [tx1, tx2, tx3], genesisBlock.header.hash)
