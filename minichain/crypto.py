import hashlib

from fastecdsa import curve, ecdsa, keys


def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def ripemd160(msg):
    h = hashlib.new("ripemd160")
    h.update(msg.encode('utf-8'))
    return h.hexdigest()


class Ecc:

    def __init__(self):
        self.priv_key = self.generatePrivKey()
        self._pub_key = self.getPubKey(self.priv_key)

    @property
    def pub_key(self) -> str:
        return "%s,%s" % (self._pub_key.x,
                          self._pub_key.y)

    def generatePrivKey(self):
        return keys.gen_private_key(curve.P256)

    def getPubKey(self, priv_key):
        return keys.get_public_key(priv_key, curve.P256)

    @classmethod
    def sign(cls, msg, priv_key):
        return ecdsa.sign(msg, priv_key)

    @classmethod
    def verity(cls, msg, signature, pub_key) -> bool:
        return ecdsa.verify(signature, msg, pub_key)

# Todo script check
