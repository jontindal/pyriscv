import itertools
import typing as t

import numpy as np


IntTypes = int | np.uint32 | np.int32


def to_uint32(val: IntTypes) -> np.uint32:
    int_val = int(val)
    if int_val < 0:
        int_val += 1 << 32
    return np.uint32(int_val)


def to_int32(val: IntTypes) -> np.int32:
    int_val = int(val)
    if int_val >= (1 << 31):
        int_val -= 1 << 32
    return np.int32(int_val)


def int_to_bits(val: IntTypes, width: int) -> str:
    """Get binary representation as a string.
    Uses two's complement for negative numbers"""
    return np.binary_repr(val, width)


def bits_to_uint(bits: str) -> int:
    """Convert binary string to unsigned int"""
    return int(bits, base=2)


def bits_to_int(bits: str) -> int:
    """Convert binary string to signed int using two's complement"""
    sign_bit = int(bits[0], base=2)
    return int(bits[1:], 2) - (sign_bit << (len(bits) - 1))


def bitfield_slice(bits: str, high: int, low: int) -> str:
    """Extract bitfields from a bit-array using Verilog bit-indexing order,
    so [0] is the right-most bit (which is opposite order than bitstring),
    and [1:0] are the 2 least significant bits, etc."""
    return bits[len(bits) - 1 - high: len(bits) - low]


def split_bitfield(bits: str, sizes: t.Iterable[int]) -> t.Iterable[str]:
    """Split bit-array into bitfields of specified sizes, starting from right-most bit"""
    assert sum(sizes) == len(bits), f"Expected sizes: {sizes} to sum to total length of bits: {len(bits)}"
    bit_iter = iter(bits)
    return reversed([''.join(itertools.islice(bit_iter, size)) for size in reversed(tuple(sizes))])
