from .crypto import sha256, ripemd160


def pay_to_public_key_hash(recipient_public_key):
    recipient_public_key_hash = ripemd160(sha256(recipient_public_key))
    # todo : 현재 단계는 sciprt 구현 안해도됨.
    return recipient_public_key_hash
