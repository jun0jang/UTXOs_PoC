from typing import List, NamedTuple, Union


class OpPush(NamedTuple):
    literal: str
    opcode: str = "push"


class OpDup(NamedTuple):
    opcode: str = "dup"


class OpHash160(NamedTuple):
    opcode: str = "hash160"


class OpEq(NamedTuple):
    opcode: str = "eq"


class OpVerify(NamedTuple):
    opcode: str = "verify"


class OpChecking(NamedTuple):
    opcode: str = "checking"


Op = Union[OpPush, OpHash160, OpEq, OpVerify, OpChecking]

Script = List[Op]


class OutPoint(NamedTuple):
    tx_id: str
    index: int


class ScriptSig(NamedTuple):
    signature: str
    pub_key: str


class TxOutput(NamedTuple):
    satoshis: int
    script_pub_key: Script


class TxInput(NamedTuple):
    outpoint: OutPoint
    script_sig: ScriptSig


EMPTY_SCRIPT_SIG = ScriptSig(str(), str())
