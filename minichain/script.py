from hashlib import new, sha256


def pay_to_public_key_hash(recipient_public_key):
    recipient_public_key_hash = new('ripemd160', sha256(recipient_public_key)).hexdigest()
    # todo : 제네시스 블록에선 script 반환 안해도된다. input과 output 검증에서 script와 interpret가 사용되기 때문에 CoinBaseTx에선 구현 X
    return recipient_public_key
