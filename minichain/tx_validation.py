from .coins import CoinsView
from .script import interpret, script_sig
from .tx import NormalTx, isCoinBaseTx


def verify_tx(tx) -> bool:
    coins_view = CoinsView()

    if isCoinBaseTx(tx):
        return True

    if not check_inputs(tx):
        return False

    # UTXOs unlock and lock
    for input in tx.inputs:
        coin = coins_view.get_coin(input.outpoint)
        p2pkh_script = script_sig(input.script_sig) + coin.output.script_pub_key
        env = interpret(p2pkh_script, tx)

        if not env.is_tx_valid:
            return False

        coin.set_spent()

    return True


def check_inputs(tx: NormalTx) -> bool:
    coins_view = CoinsView()

    # it return false if inputs's outpoint is spend or not found
    if not coins_view.hasInputs(tx.inputs):
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
