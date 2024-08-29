import numpy as np


def int_to_bits(val: int, width: int) -> str:
    return np.binary_repr(val, width)


def bits_to_int(bits: str) -> int:
    return int(bits, 2)


def bitfield_slice(bits: str, high: int, low: int):
    """extract bitfields from a bit-array using Verilog bit-indexing order,
    so [0] is the right-most bit (which is opposite order than bitstring),
    and [1:0] are the 2 least significant bits, etc."""
    return bits[len(bits) - 1 - high: len(bits) - low]
