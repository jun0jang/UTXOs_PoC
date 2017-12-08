from fastecdsa import keys, curve, ecdsa
import hashlib


def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def ripemd160(msg):
    h = hashlib.new("ripemd160")
    h.update(msg.encode('utf-8'))
    return h.hexdigest()


class Ecc:

    def __init__(self):
        self.priv_key = self.generatePrivKey()
        self.pub_key = self.getPubKey(self.priv_key)

    def generatePrivKey(self):
        return keys.gen_private_key(curve.P256)

    def getPubKey(self, priv_key):
        return keys.get_public_key(priv_key, curve.P256)

    def sign(self, msg):
        return ecdsa.sign(sha256(msg), self.priv_key)

    def verity(self, signature, msg):
        return ecdsa.verify(signature, sha256(msg), self.pub_key)
