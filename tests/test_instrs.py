import pytest
import typing as t

import numpy as np

from pyriscv.assem import asm
from pyriscv.rv32i import Regs as R, RV32I
import pyriscv.utils as u

import alu_tests


INITIAL_PC = 0x1000


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
    alu_tests.ADD_TESTS
    + alu_tests.SUB_TESTS
    + alu_tests.XOR_TESTS
    + alu_tests.OR_TESTS
    + alu_tests.AND_TESTS
    + alu_tests.SLL_TESTS
    + alu_tests.SRL_TESTS
    + alu_tests.SRA_TESTS
    + alu_tests.SLT_TESTS
    + alu_tests.SLTU_TESTS,
)
def test_rr_op(
    instr: str, rd: R, rs1: R, rs2: R, correctval: int, val1: int, val2: int
):
    rv = RV32I()
    rv.set_reg(rs1, val1)
    rv.set_reg(rs2, val2)
    instr_bin = asm(instr, rd, rs1, rs2)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize(
    "instr,rd,rs1,correctval,val1,imm",
    alu_tests.ADDI_TESTS
    + alu_tests.XORI_TESTS
    + alu_tests.ORI_TESTS
    + alu_tests.ANDI_TESTS
    + alu_tests.SLLI_TESTS
    + alu_tests.SRLI_TESTS
    + alu_tests.SRAI_TESTS
    + alu_tests.SLTI_TESTS
    + alu_tests.SLTIU_TESTS,
)
def test_imm_op(instr: str, rd: R, rs1: R, correctval: int, val1: int, imm: int):
    rv = RV32I()
    rv.set_reg(rs1, val1)
    instr_bin = asm(instr, rd, rs1, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize(
    "instr,mem_addr,initial_mem,rd,rs1,correctval,val1,imm",
    [
        ("lw", 0x10, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x40302010, 0x0, 0x10),
        ("lw", 0x30, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x40302010, 0x20, 0x10),
        ("lw", 0xC, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x40302010, -0x4, 0x10),
        ("lw", 0xC, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x40302010, 0x10, -0x4),
        ("lw", 0x10, [0xAA, 0xAA, 0xAA, 0xAA], R.X1, R.X2, -0x55555556, 0x0, 0x10),
        ("lh", 0x10, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x2010, 0x0, 0x10),
        ("lh", 0x10, [0xAA, 0xAA, 0xAA, 0xAA], R.X1, R.X2, -0x5556, 0x0, 0x10),
        ("lb", 0x10, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x10, 0x0, 0x10),
        ("lb", 0x10, [0xAA, 0xAA, 0xAA, 0xAA], R.X1, R.X2, -0x56, 0x0, 0x10),
        ("lhu", 0x10, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x2010, 0x0, 0x10),
        ("lhu", 0x10, [0xAA, 0xAA, 0xAA, 0xAA], R.X1, R.X2, 0xAAAA, 0x0, 0x10),
        ("lbu", 0x10, [0x10, 0x20, 0x30, 0x40], R.X1, R.X2, 0x10, 0x0, 0x10),
        ("lbu", 0x10, [0xAA, 0xAA, 0xAA, 0xAA], R.X1, R.X2, 0xAA, 0x0, 0x10),
    ],
)
def test_load(
    instr: str,
    mem_addr: int,
    initial_mem: list[int],
    rd: R,
    rs1: R,
    correctval: int,
    val1: int,
    imm: int,
):
    rv = RV32I()
    rv.memory[mem_addr: mem_addr + 4] = initial_mem
    rv.set_reg(rs1, val1)
    instr_bin = asm(instr, rd, rs1, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize(
    "instr,rs1,rs2,val1,val2,imm,mem_addr,expected_mem",
    [
        ("sw", R.X2, R.X3, 0x0, 0x40302010, 0x10, 0x10, [0x10, 0x20, 0x30, 0x40]),
        ("sw", R.X2, R.X3, 0x20, 0x40302010, 0x10, 0x30, [0x10, 0x20, 0x30, 0x40]),
        ("sw", R.X2, R.X3, -0x4, 0x40302010, 0x10, 0xC, [0x10, 0x20, 0x30, 0x40]),
        ("sw", R.X2, R.X3, 0x10, 0x40302010, -0x4, 0xC, [0x10, 0x20, 0x30, 0x40]),
        ("sw", R.X2, R.X3, 0x0, 0xAAAAAAAA, 0x10, 0x10, [0xAA, 0xAA, 0xAA, 0xAA]),
        ("sh", R.X2, R.X3, 0x0, 0x40302010, 0x10, 0x10, [0x10, 0x20, 0x00, 0x00]),
        ("sh", R.X2, R.X3, 0x0, 0xAAAAAAAA, 0x10, 0x10, [0xAA, 0xAA, 0x00, 0x00]),
        ("sb", R.X2, R.X3, 0x0, 0x40302010, 0x10, 0x10, [0x10, 0x00, 0x00, 0x00]),
        ("sb", R.X2, R.X3, 0x0, 0xAAAAAAAA, 0x10, 0x10, [0xAA, 0x00, 0x00, 0x00]),
    ],
)
def test_store(
    instr: str,
    rs1: R,
    rs2: R,
    val1: int,
    val2: int,
    imm: int,
    mem_addr: int,
    expected_mem: list[int],
):
    rv = RV32I()
    rv.set_reg(rs1, val1)
    rv.set_reg(rs2, val2)
    instr_bin = asm(instr, rs1=rs1, rs2=rs2, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = np.array(expected_mem, dtype=np.uint8)
    np.testing.assert_array_equal(rv.memory[mem_addr: mem_addr + 4], expected)


@pytest.mark.parametrize(
    "instr,rs1,rs2,should_branch,val1,val2",
    [
        ("beq", R.X20, R.X21, True, 0x333334, 0x333334),
        ("beq", R.X20, R.X21, False, 0x333334, 0x333333),
        ("bne", R.X20, R.X21, False, 0x333334, 0x333334),
        ("bne", R.X20, R.X21, True, 0x333334, 0x333333),
        ("blt", R.X20, R.X21, False, 0x33333334, 0x33333334),
        ("blt", R.X20, R.X21, False, -0x4001, -0x4001),
        ("blt", R.X20, R.X21, True, -0x201, 0x5),
        ("blt", R.X20, R.X21, False, 0x33333334, -0x80000000),
        ("bge", R.X20, R.X21, True, 0x33333334, 0x33333334),
        ("bge", R.X20, R.X21, True, -0x4001, -0x4001),
        ("bge", R.X20, R.X21, False, -0x201, 0x5),
        ("bge", R.X20, R.X21, True, 0x33333334, -0x80000000),
        ("bltu", R.X20, R.X21, True, 0x0, 0xFFFFFFFE),
        ("bltu", R.X20, R.X21, True, 0xFFFFFFFE, 0xFFFFFFFF),
        ("bltu", R.X20, R.X21, False, 0x2000000, 0x20),
        ("bltu", R.X20, R.X21, False, 0xFFFFF7FF, 0x40),
        ("bgeu", R.X20, R.X21, False, 0x0, 0xFFFFFFFE),
        ("bgeu", R.X20, R.X21, False, 0xFFFFFFFE, 0xFFFFFFFF),
        ("bgeu", R.X20, R.X21, True, 0x2000000, 0x20),
        ("bgeu", R.X20, R.X21, True, 0xFFFFF7FF, 0x40),
    ],
)
def test_branch(instr: str, rs1: R, rs2: R, should_branch: bool, val1: int, val2: int):
    IMM = 0x10
    rv = RV32I()
    rv.set_pc(INITIAL_PC)
    rv.set_reg(rs1, val1)
    rv.set_reg(rs2, val2)
    instr_bin = asm(instr, rs1=rs1, rs2=rs2, imm=IMM)
    rv.execute(rv.decode(instr_bin))
    expected_pc = IMM + INITIAL_PC if should_branch else INITIAL_PC
    assert rv.pc == expected_pc, f"Found 0x{rv.pc:x}, expected 0x{expected_pc:x}"


@pytest.mark.parametrize(
    "instr,rd,imm",
    [
        ("jal", R.X1, 0x0),
        ("jal", R.X1, 0xAAAAA),
        ("jal", R.X1, -0x2000),
    ],
)
def test_jal(instr: str, rd: R, imm: int):
    rv = RV32I()
    rv.set_pc(INITIAL_PC)
    instr_bin = asm(instr, rd, imm=imm)
    rv.execute(rv.decode(instr_bin))
    assert (
        rv.regs[rd] == INITIAL_PC + 4
    ), f"Found 0x{rv.regs[rd]:x}, expected 0x{INITIAL_PC + 4:x}"
    expected_pc = u.to_int32(INITIAL_PC + imm)
    assert rv.pc == expected_pc, f"Found 0x{rv.pc:x}, expected 0x{expected_pc:x}"


@pytest.mark.parametrize(
    "instr,rd,rs1,val1,imm",
    [
        ("jalr", R.X1, R.X2, 0x66666666, 0x0),
        ("jalr", R.X1, R.X2, 0x66666666, 0x6AA),
        ("jalr", R.X1, R.X2, 0x66666666, -0x20),
    ],
)
def test_jalr(instr: str, rd: R, rs1: R, val1: int, imm: int):
    rv = RV32I()
    rv.set_pc(INITIAL_PC)
    rv.set_reg(rs1, val1)
    instr_bin = asm(instr, rd, rs1, imm=imm)
    rv.execute(rv.decode(instr_bin))
    assert (
        rv.regs[rd] == INITIAL_PC + 4
    ), f"Found 0x{rv.regs[rd]:x}, expected 0x{INITIAL_PC + 4:x}"
    expected_pc = u.to_int32(val1 + imm)
    assert rv.pc == expected_pc, f"Found 0x{rv.pc:x}, expected 0x{expected_pc:x}"


@pytest.mark.parametrize(
    "instr,rd,correctval,imm",
    [
        ("lui", R.X1, 0x1000, 0x1),
        ("lui", R.X1, 0x7FFFF000, 0x7FFFF),
        ("lui", R.X1, -0x1000, 0xFFFFF),
        ("lui", R.X0, 0x0, 0xFFFFF),
    ],
)
def test_lui(instr: str, rd: R, correctval: int, imm: int):
    rv = RV32I()
    instr_bin = asm(instr, rd, imm=imm)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"


@pytest.mark.parametrize(
    "instr,rd,correctval,imm,pc",
    [
        ("auipc", R.X1, 0x1000, 0x0, 0x1000),
        ("auipc", R.X1, 0x2000, 0x1, 0x1000),
        ("auipc", R.X1, 0x0, -0x1, 0x1000),
        ("auipc", R.X0, 0x0, 0xFFFFF, 0x1000),
    ],
)
def test_auipc(instr: str, rd: R, correctval: int, imm: int, pc: int):
    rv = RV32I()
    instr_bin = asm(instr, rd, imm=imm)
    rv.set_pc(pc)
    rv.execute(rv.decode(instr_bin))
    expected = u.to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"
