from collections import namedtuple

OutPoint = namedtuple("OutPoint", ["txid", "index"])

TxOutput = namedtuple("TxOutput", ["satoshis", "scriptPubKey"])

TxInput = namedtuple("TxInput", ["outpoint", "scriptSig"])
