import pytest
import typing as t

import numpy as np

from assem import RegNames as R, asm
from ram import RAM
from rv32i import IntTypes, to_int32, to_uint32, RV32I

import arch_tests


@pytest.mark.parametrize(
    "val,expected",
    [
        (0x0000_0001, np.int32(0x0000_0001)),
        (0x7fff_ffff, np.int32(0x7fff_ffff)),
        (-0x0000_0001, np.int32(-0x0000_0001)),
        (-0x8000_0000, np.int32(-0x8000_0000)),
        (0x8000_0000, np.int32(-0x8000_0000)),
        (0xffff_ffff, np.int32(-0x0000_0001)),
        (np.uint32(0x0000_0001), np.int32(0x0000_0001)),
        (np.uint32(0x7fff_ffff), np.int32(0x7fff_ffff)),
        (np.uint32(0x8000_0000), np.int32(-0x8000_0000)),
        (np.uint32(0xffff_ffff), np.int32(-0x0000_0001)),
    ],
)
def test_to_int32(val: IntTypes, expected: np.int32):
    result = to_int32(val)
    assert result == expected, f"Got 0x{result:x}, expected 0x{expected:x} for input 0x{val:x}"


@pytest.mark.parametrize(
    "val,expected",
    [
        (0x0000_0001, np.uint32(0x0000_0001)),
        (0x7fff_ffff, np.uint32(0x7fff_ffff)),
        (-0x0000_0001, np.uint32(0xffff_ffff)),
        (-0x8000_0000, np.uint32(0x8000_0000)),
        (0x8000_0000, np.uint32(0x8000_0000)),
        (0xffff_ffff, np.uint32(0xffff_ffff)),
        (np.int32(0x0000_0001), np.uint32(0x0000_0001)),
        (np.int32(0x7fff_ffff), np.uint32(0x7fff_ffff)),
        (np.int32(-0x0000_0001), np.uint32(0xffff_ffff)),
        (np.int32(-0x8000_0000), np.uint32(0x8000_0000)),
    ],
)
def test_to_uint32(val: IntTypes, expected: np.uint32):
    result = to_uint32(val)
    assert result == expected, f"Got 0x{result:x}, expected 0x{expected:x} for input 0x{val:x}"


def test_ram():
    memory = RAM()
    memory.store_uint32(0x1000, 0x12345678)
    assert memory.load_uint32(0x1000)


@pytest.mark.parametrize(
    "asm_qwargs,expected",
    [
        ({"instr": "add", "rd": R.X1, "rs1": R.X2, "rs2": R.X3}, 0x003100B3),
        ({"instr": "srai", "rd": R.X1, "rs1": R.X2, "imm": 0x11}, 0x41115093),
        ({"instr": "lw", "rd": R.X1, "rs1": R.X2, "imm": 0x8}, 0x00812083),
        ({"instr": "sw", "rs2": R.X1, "rs1": R.X2, "imm": 0x8}, 0x00112423),
        ({"instr": "bne", "rs1": R.X10, "rs2": R.X11, "imm": 2000}, 0x7CB51863),
        ({"instr": "lui", "rd": R.X2, "imm": 0x12345}, 0x12345137),
    ],
)
def test_asm_single(asm_qwargs: dict[str, t.Any], expected: int):
    instr_bits = asm(**asm_qwargs)
    assert (
        instr_bits == expected
    ), f"Got 0x{instr_bits:x}, expected 0x{expected:x} for asm: {asm_qwargs}"


@pytest.mark.parametrize(
    "instr,rd,rs1,rs2,correctval,val1,val2",
    arch_tests.ADD_TESTS
    + arch_tests.SUB_TESTS
    + arch_tests.XOR_TESTS
    + arch_tests.OR_TESTS
    + arch_tests.AND_TESTS
    + arch_tests.SLL_TESTS
    + arch_tests.SRL_TESTS
    + arch_tests.SRA_TESTS
    + arch_tests.SLT_TESTS
    + arch_tests.SLTU_TESTS
)
def test_rr_op(
    instr: str, rd: R, rs1: R, rs2: R, correctval: int, val1: int, val2: int
):
    rv = RV32I(RAM())
    rv.set_reg(rs1, val1)
    rv.set_reg(rs2, val2)
    instr_bin = asm(instr, rd, rs1, rs2)
    rv.execute(rv.decode(instr_bin))
    expected = to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize(
    "instr,rd,rs1,correctval,val1,imm",
    arch_tests.ADDI_TESTS
    + arch_tests.XORI_TESTS
    + arch_tests.ORI_TESTS
    + arch_tests.ANDI_TESTS
    + arch_tests.SLLI_TESTS
    + arch_tests.SRLI_TESTS
    + arch_tests.SRAI_TESTS
    + arch_tests.SLTI_TESTS
    + arch_tests.SLTIU_TESTS
)
def test_imm_op(
    instr: str, rd: R, rs1: R, correctval: int, val1: int, imm: int
):
    rv = RV32I(RAM())
    rv.set_reg(rs1, val1)
    instr_bin = asm(instr, rd, rs1, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"
