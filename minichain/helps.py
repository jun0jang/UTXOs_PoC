from fastecdsa.point import Point


def strToPoint(pub_key: str):
    x, y = pub_key.split(",")
    return Point(int(x), int(y))
