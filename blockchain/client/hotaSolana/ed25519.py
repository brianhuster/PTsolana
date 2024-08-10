from typing import Tuple, Union

P = 57896044618658097711785492504343953926634992332820282019728792003956564819949  # ed25519 is twisted edwards curve
N = 7237005577332262213973186563042994240857116359379907606001950938285454250989  # curve's (group) order
Gx = 15112221349535400772501151409588531511454012693041857206046113283949847762202  # base point x
Gy = 46316835694926478169428394003475163141307993866256225615783033603165251855960  # base point y
CURVE = {
    "a": -1,  # where a=-1, d = -(121665/121666) == -(121665 * inv(121666)) mod P
    "d": 37095705934669439343138083508754565189542113879843219016388785533085940283555,
    "p": P,
    "n": N,
    "h": 8,
    "Gx": Gx,
    "Gy": Gy,  # field prime, curve (group) order, cofactor
}

def err(m=""):
    raise Exception(m)
def strCheck(s):
    return isinstance(s, str)
def isu8(a):
    return isinstance(a, bytes)
def au8(a, l=None):
    if not isu8(a) or (isinstance(l, int) and l > 0 and len(a) != l):
        err("bytes of valid length expected")
    return a
def u8n(data):
    return bytes(data)
def toU8(a, len):
    if strCheck(a):
        a = bytes.fromhex(a)
    return au8(a, len)
def mod(a, b=P):
    r = a % b
    return r if r >= 0 else b + r
def isPoint(p):
    if isinstance(p, Point):
        return p
    err("Point expected")

class Point:
    def __init__(self, ex, ey, ez, et):
        self.ex = ex
        self.ey = ey
        self.ez = ez
        self.et = et

    @staticmethod
    def fromHex(hex, zip215=False):
        d = CURVE["d"]
        hex = toU8(hex, 32)
        normed = bytearray(hex) 
        lastByte = normed[-1]
        normed[-1] = lastByte & ~0x80  # adjust first LE byte = last BE byte
        y = int.from_bytes(normed, "little")  # decode as little-endian, convert to num

        if zip215 and not (1 <= y < 2**256):
            err("bad y coord 1")  # zip215=true [1..2^256-1]
        if not zip215 and not (1 <= y < P):
            err("bad y coord 2")  # zip215=false [1..P-1]

        y2 = mod(y * y)  # y²
        u = mod(y2 - 1)  # u=y²-1
        v = mod(d * y2 + 1)  # v=dy²+1
        isValid, x = uvRatio(u, v)  # (uv³)(uv⁷)^(p-5)/8; square root
        if not isValid:
            err("bad y coordinate 3")  # not square root: bad point
        isXOdd = (x & 1) == 1  # adjust sign of x coordinate
        isLastByteOdd = (lastByte & 0x80) != 0  # x_0, last bit
        if not zip215 and x == 0 and isLastByteOdd:
            err("bad y coord 3")  # x=0 and x_0 = 1
        if isLastByteOdd != isXOdd:
            x = mod(-x)

        in0MaskRange = lambda x: 0 <= x < 2**256

        if not in0MaskRange(x) or not in0MaskRange(y):
            err("bad y coord 4")
        return Point(x, y, 1, mod(x * y))  # Z=1, T=xy

def pow2(x: int, power: int) -> int:
    """Computes x raised to the power of 2."""
    r = x
    while power > 0:
        r *= r
        r %= P
        power -= 1
    return r

def pow_2_252_3(x: int) -> Tuple[int, int]:
    """Computes x^(2^252-1) and x^3 modulo P."""
    x2 = (x * x) % P  # x^2,       bits 1
    b2 = (x2 * x) % P  # x^3,       bits 11
    b4 = (pow2(b2, 2) * b2) % P  # x^(2^4-1), bits 1111
    b5 = (pow2(b4, 1) * x) % P  # x^(2^5-1), bits 11111
    b10 = (pow2(b5, 5) * b5) % P  # x^(2^10)
    b20 = (pow2(b10, 10) * b10) % P  # x^(2^20)
    b40 = (pow2(b20, 20) * b20) % P  # x^(2^40)
    b80 = (pow2(b40, 40) * b40) % P  # x^(2^80)
    b160 = (pow2(b80, 80) * b80) % P  # x^(2^160)
    b240 = (pow2(b160, 80) * b80) % P  # x^(2^240)
    b250 = (pow2(b240, 10) * b10) % P  # x^(2^250)
    pow_p_5_8 = (pow2(b250, 2) * x) % P  # < To pow to (p+3)/8, multiply it by x.
    return pow_p_5_8, b2

RM1 = 19681161376707505956807079304988542015446066515923890162744021073123829784752  # √-1
def uvRatio(u: int, v: int) -> Tuple[bool, int]:
    """Computes the square root of (u/v) modulo P."""
    v3 = mod(v * v * v)  # v³
    v7 = mod(v3 * v3 * v)  # v⁷
    pow = pow_2_252_3(u * v7)[0]  # (uv⁷)^(p-5)/8
    x = mod(u * v3 * pow)  # (uv³)(uv⁷)^(p-5)/8
    vx2 = mod(v * x * x)  # vx²
    root1 = x  # First root candidate
    root2 = mod(x * RM1)  # Second root candidate; RM1 is √-1
    useRoot1 = vx2 == u  # If vx² = u (mod p), x is a square root
    useRoot2 = vx2 == mod(-u)  # If vx² = -u, set x <-- x * 2^((p-1)/4)
    noRoot = vx2 == mod(-u * RM1)  # There is no valid root, vx² = -u√-1
    if useRoot1:
        x = root1
    if useRoot2 or noRoot:
        x = root2  # We return root2 anyway, for const-time
    if (mod(x) & 1) == 1:
        x = mod(-x)  # edIsNegative
    return (useRoot1 or useRoot2), x

def isOnCurve(hex: str) -> bool:
    """Checks if a point is on the curve."""
    try:
        Point.fromHex(hex)
        return True
    except Exception:
        return False