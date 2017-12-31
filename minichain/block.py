import json
from collections import namedtuple

from .crypto import sha256

Block = namedtuple("Block", ["header", "txs"])


class BlockHeader:

    def __init__(self, prev_hash, merkle_root, timestamp, nounce):
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nounce = nounce

    @property
    def hash(self):
        return sha256(json.dumps(self.represent_dict))

    @property
    def represent_dict(self):
        return {
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "nounce": self.nounce
        }

    @property
    def is_valid(self):
        return self.hash.startswith("0000")
