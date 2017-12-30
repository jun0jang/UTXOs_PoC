from .crypto import Ecc
from .miner import createNewBlock
from .script import pay_to_public_key_hash


def main():
    ecc1 = Ecc()

    script1 = pay_to_public_key_hash(str(ecc1.pub_key))
    genesisBlock = createNewBlock(script1)
