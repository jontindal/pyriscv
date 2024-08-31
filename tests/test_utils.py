import pytest

import numpy as np

import pyriscv.utils as u


@pytest.mark.parametrize(
    "val,expected",
    [
        (0x0000_0001, np.int32(0x0000_0001)),
        (0x7FFF_FFFF, np.int32(0x7FFF_FFFF)),
        (-0x0000_0001, np.int32(-0x0000_0001)),
        (-0x8000_0000, np.int32(-0x8000_0000)),
        (0x8000_0000, np.int32(-0x8000_0000)),
        (0xFFFF_FFFF, np.int32(-0x0000_0001)),
        (np.uint32(0x0000_0001), np.int32(0x0000_0001)),
        (np.uint32(0x7FFF_FFFF), np.int32(0x7FFF_FFFF)),
        (np.uint32(0x8000_0000), np.int32(-0x8000_0000)),
        (np.uint32(0xFFFF_FFFF), np.int32(-0x0000_0001)),
    ],
)
def test_to_int32(val: u.IntTypes, expected: np.int32):
    result = u.to_int32(val)
    assert (
        result == expected
    ), f"Got 0x{result:x}, expected 0x{expected:x} for input 0x{val:x}"


@pytest.mark.parametrize(
    "val,expected",
    [
        (0x0000_0001, np.uint32(0x0000_0001)),
        (0x7FFF_FFFF, np.uint32(0x7FFF_FFFF)),
        (-0x0000_0001, np.uint32(0xFFFF_FFFF)),
        (-0x8000_0000, np.uint32(0x8000_0000)),
        (0x8000_0000, np.uint32(0x8000_0000)),
        (0xFFFF_FFFF, np.uint32(0xFFFF_FFFF)),
        (np.int32(0x0000_0001), np.uint32(0x0000_0001)),
        (np.int32(0x7FFF_FFFF), np.uint32(0x7FFF_FFFF)),
        (np.int32(-0x0000_0001), np.uint32(0xFFFF_FFFF)),
        (np.int32(-0x8000_0000), np.uint32(0x8000_0000)),
    ],
)
def test_to_uint32(val: u.IntTypes, expected: np.uint32):
    result = u.to_uint32(val)
    assert (
        result == expected
    ), f"Got 0x{result:x}, expected 0x{expected:x} for input 0x{val:x}"


@pytest.mark.parametrize("val,width,expected", [(0x1, 3, "001"), (-0x1, 3, "111")])
def test_int_to_bits(val: u.IntTypes, width: int, expected: str):
    result = u.int_to_bits(val, width)
    assert result == expected, f"Got {result}, expected {expected}"


@pytest.mark.parametrize("val,expected", [("001", 1), ("111", 7)])
def test_bits_to_uint(val: str, expected: int):
    result = u.bits_to_uint(val)
    assert result == expected, f"Got {result}, expected {expected}"


@pytest.mark.parametrize("val,expected", [("001", 1), ("111", -1)])
def test_bits_to_int(val: str, expected: int):
    result = u.bits_to_int(val)
    assert result == expected, f"Got {result}, expected {expected}"
