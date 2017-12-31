from typing import List

from .crypto import Ecc, ripemd160, sha256
from .helps import strToPoint
from .tx import Tx
from .types import (OpChecking, OpDup, OpEq, OpHash160, OpPush, OpVerify,
                    Script, ScriptSig)


# lock script(P2PKH)
def pay_to_public_key_hash(recipient_public_key) -> Script:
    recipient_public_key_hash = ripemd160(sha256(recipient_public_key))
    return [OpDup(),
            OpHash160(),
            OpPush(recipient_public_key_hash),
            OpEq(),
            OpVerify(),
            OpChecking()]


# un-lock script
def script_sig(ss: ScriptSig):
    return [OpPush(ss.signature), OpPush(ss.pub_key)]


def interpret(script, tx: Tx):
    env = Env([])
    for op in script:
        if op.opcode == "push":
            literal = op.literal
            env.push(literal)
        elif op.opcode == "checking":
            if len(env.stack) != 2:
                raise Exception("StackError")
            sig, pub_key = env.stack[:2]
            pub_key = strToPoint(pub_key)
            env.replace2(str(Ecc.verity(tx.withEmptyInputsScriptSig().hash,
                                        sig,
                                        pub_key)))
        elif op.opcode == "hash160":
            env.replace(ripemd160(sha256(env.top)))
        elif op.opcode == "dup":
            env.push(env.top)
        elif op.opcode == "eq":
            x, y = env.stack[-2:]
            env.replace2(str(x == y))
        elif op.opcode == "verify":
            if env.top is False:
                env.stack.pop()
                env.invalidate()
            else:
                env.stack.pop()
    return env


class Env:
    tx_valid = True

    def __init__(self, stack: List[str]):
        self.stack = stack

    def invalidate(self):
        self.tx_valid = False

    @property
    def is_tx_valid(self):
        if len(self.stack) != 1:
            return False
        return self.tx_valid and self.top == "True"

    @property
    def top(self):
        return self.stack[-1]

    def push(self, literal):
        self.stack.append(literal)

    def replace(self, item: str):
        self.stack[-1] = item

    def replace2(self, item: str):
        self.stack.pop()
        self.stack[-1] = item

    def __repr__(self):
        return "%s" % (self.stack)
