from .crypto import Ecc


def main():
    ecc1 = Ecc()
    signature = ecc1.sign("this is a Tx1")
    print(ecc1.verity(signature, "this is a Tx1"))