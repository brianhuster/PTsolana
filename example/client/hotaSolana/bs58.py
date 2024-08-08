import math
from typing import Union


class BaseX:
    def __init__(self, alphabet: str):
        if len(alphabet) >= 255:
            raise TypeError("Alphabet too long")
        self.base_map = [255] * 256
        for i, char in enumerate(alphabet):
            x = ord(char)
            if self.base_map[x] != 255:
                raise TypeError(f"{char} is ambiguous")
            self.base_map[x] = i
        self.base = len(alphabet)
        self.leader = alphabet[0]
        # log(base) / log(256), rounded up
        self.factor = math.log(self.base) / math.log(256)
        # log(256) / log(base), rounded up
        self.ifactor = math.log(256) / math.log(self.base)
        self.alphabet = alphabet

    def encode(self, source: Union[bytearray, bytes, list]) -> str:
        if not isinstance(source, (bytearray, bytes)):
            raise TypeError("Expected bytearray or bytes")
        if len(source) == 0:
            return ""
        zeroes = 0
        length = 0
        pbegin = 0
        pend = len(source)
        while pbegin != pend and source[pbegin] == 0:
            pbegin += 1
            zeroes += 1
        size = int(((pend - pbegin) * self.ifactor + 1))
        b58 = bytearray(size)
        while pbegin != pend:
            carry = source[pbegin]
            i = 0
            for it1 in range(size - 1, -1, -1):
                carry += (256 * b58[it1])
                b58[it1] = carry % self.base
                carry //= self.base
                i += 1
                if carry == 0 and i >= length:
                    break
            if carry != 0:
                raise ValueError("Non-zero carry")
            length = i
            pbegin += 1
        it2 = size - length
        while it2 != size and b58[it2] == 0:
            it2 += 1
        str_res = self.leader * zeroes
        for it2 in range(it2, size):
            str_res += self.alphabet[b58[it2]]
        return str_res

    def decode_unsafe(self, source: str) -> Union[bytearray, None]:
        if not isinstance(source, str):
            raise TypeError("Expected string")
        if len(source) == 0:
            return bytearray()
        psz = 0
        zeroes = 0
        length = 0
        while source[psz] == self.leader:
            zeroes += 1
            psz += 1
        size = int(((len(source) - psz) * self.factor + 1))
        b256 = bytearray(size)
        while psz < len(source):
            carry = self.base_map[ord(source[psz])]
            if carry == 255:
                return None
            i = 0
            for it3 in range(size - 1, -1, -1):
                carry += (self.base * b256[it3])
                b256[it3] = carry % 256
                carry //= 256
                i += 1
                if carry == 0 and i >= length:
                    break
            if carry != 0:
                raise ValueError("Non-zero carry")
            length = i
            psz += 1
        it4 = size - length
        while it4 != size and b256[it4] == 0:
            it4 += 1
        return bytearray(zeroes) + b256[it4:]

    def decode(self, string: str) -> bytearray:
        buffer = self.decode_unsafe(string)
        if buffer is not None:
            return buffer
        raise ValueError(f"Non-base{self.base} character")


# Base58 encoding/decoding
bs58 = BaseX("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
