from .crypto import Ecc
from .script import pay_to_public_key_hash
from .miner import createNewBlock


def main():
    ecc1 = Ecc()

    script1 = pay_to_public_key_hash(str(ecc1.pub_key))
    block1 = createNewBlock(script1)
