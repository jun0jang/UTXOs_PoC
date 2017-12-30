import json

from .crypto import sha256


def block_merkle_root(txs):
    def merkle_root(hashes):
        hashes_len = len(hashes)

        if hashes_len == 1:
            return hashes[0]

        if hashes_len % 2 != 0:
            hashes.append(hashes[-1])

        next_hashes = []
        for i in range(0, hashes_len, 2):
            two_tx_hash = sha256(json.dumps([hashes[i], hashes[i + 1]]))
            next_hashes.append(two_tx_hash)

        return merkle_root(next_hashes)

    hashes = [tx.hash for tx in txs]
    return merkle_root(hashes)
