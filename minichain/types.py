from collections import namedtuple


OutPoint = namedtuple("OutPoint", ["txid", "index"])

TxOutput = namedtuple("TxOutput", ["value", "scriptPubKey"])

TxInput = namedtuple("TxInput", ["outpoint", "scriptSig"])
