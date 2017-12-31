from .coins import CoinsView
from .crypto import Ecc
from .miner import createNewBlock
from .script import pay_to_public_key_hash
from .validation import connectBlock


def main():
    ecc1 = Ecc()

    script1 = pay_to_public_key_hash(str(ecc1.pub_key))
    genesisBlock = createNewBlock(script1)
    connectBlock(genesisBlock)

    coin_view = CoinsView()
    print(coin_view.map)
