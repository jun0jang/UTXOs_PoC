from .crypto import ripemd160, sha256


def opPush(literal):
    return {"opcode": "push", "literal": literal}


def opDup():
    return {"opcode": "dup"}


def opHash160():
    return {"opcode": "hash160"}


def opEq():
    return {"opcode": "eq"}


def opVerify():
    return {"opcode": "verify"}


def opChecksig():
    return {"opcode": "checksig"}

# lock script
def pay_to_public_key_hash(recipient_public_key):
    recipient_public_key_hash = ripemd160(sha256(recipient_public_key))
    return [opDup(),
            opHash160(),
            opPush(recipient_public_key_hash),
            opEq(),
            opVerify(),
            opChecksig()]
