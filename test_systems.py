import pytest
import typing as t

from assem import asm
from ram import RAM
from rv32i import Regs as R, RV32I
import utils as u

import arch_tests


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
    expected = u.to_int32(correctval)
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
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize("instr,rd,correctval,imm", [
    ("lui", R.X1, 0x1000, 0x1),
    ("lui", R.X1, 0x7ffff000, 0x7ffff),
    ("lui", R.X1, -0x1000, 0xfffff),
    ("lui", R.X0, 0x0, 0xfffff),
])
def test_lui(instr: str, rd: R, correctval: int, imm: int):
    rv = RV32I(RAM())
    instr_bin = asm(instr, rd, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize("instr,rd,correctval,imm,pc", [
    ("auipc", R.X1, 0x1000, 0x0, 0x1000),
    ("auipc", R.X1, 0x2000, 0x1, 0x1000),
    ("auipc", R.X1, 0x0, -0x1, 0x1000),
    ("auipc", R.X0, 0x0, 0xfffff, 0x1000),
])
def test_auipc(instr: str, rd: R, correctval: int, imm: int, pc: int):
    rv = RV32I(RAM())
    instr_bin = asm(instr, rd, imm=imm)
    rv.set_pc(pc)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"
