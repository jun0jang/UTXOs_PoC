from collections import Counter

from fastecdsa.point import Point


def strToPoint(pub_key: str) -> Point:
    x, y = pub_key.split(",")
    return Point(int(x), int(y))


def check_list_item_duplication(target: list) -> bool:
    # list is empty if block only contain coinbase tx
    if not target:
        return True

    counting = Counter(target).values()
    return not max(counting) > 1
