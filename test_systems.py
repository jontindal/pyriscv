import pytest
import typing as t

from assem import RegNames as R, asm
from ram import RAM
from rv32i import to_int32, RV32I


def test_ram():
    memory = RAM()
    memory.store_uint32(0x1000, 0x12345678)
    assert memory.load_uint32(0x1000)


@pytest.mark.parametrize("asm_qwargs,expected", [
    ({"instr": "add", "rd": R.X1, "rs1": R.X2, "rs2": R.X3}, 0x003100b3),
    ({"instr": "srai", "rd": R.X1, "rs1": R.X2, "imm": 0x11}, 0x41115093),
    ({"instr": "lw", "rd": R.X1, "rs1": R.X2, "imm": 0x8}, 0x00812083),
    ({"instr": "sw", "rs2": R.X1, "rs1": R.X2, "imm": 0x8}, 0x00112423),
    ({"instr": "bne", "rs1": R.X10, "rs2": R.X11, "imm": 2000}, 0x7cb51863),
    ({"instr": "lui", "rd": R.X2, "imm": 0x12345}, 0x12345137),
])
def test_asm_single(asm_qwargs: dict[str, t.Any], expected: int):
    instr_bits = asm(**asm_qwargs)
    assert instr_bits == expected, f"Got 0x{instr_bits:x}, expected 0x{expected:x} for asm: {asm_qwargs}"


ADD_TESTS = [
    ("add", R.X24, R.X4,  R.X24, 0x80000000, 0x7fffffff, 0x1),
    ("add", R.X28, R.X10, R.X10, 0x40000, 0x20000, 0x20000),
    ("add", R.X21, R.X21, R.X21, 0xfdfffffe, -0x1000001, -0x1000001),
    ("add", R.X22, R.X22, R.X31, 0x3fffe, -0x2, 0x40000),
    ("add", R.X11, R.X12, R.X6,  0xaaaaaaac, 0x55555556, 0x55555556),
    ("add", R.X10, R.X29, R.X13, 0x80000002, 0x2, -0x80000000),
    ("add", R.X26, R.X31, R.X5,  0xffffffef, -0x11, 0x0),
    ("add", R.X7,  R.X2,  R.X1,  0xe6666665, 0x66666666, 0x7fffffff),
    ("add", R.X14, R.X8,  R.X25, 0x2aaaaaaa, -0x80000000, -0x55555556),
    ("add", R.X1,  R.X13, R.X8,  0xfdffffff, 0x0, -0x2000001),
    ("add", R.X0,  R.X28, R.X9,  0, 0x1, 0x800000),
    ("add", R.X20, R.X14, R.X4,  0x9, 0x7, 0x2),
    ("add", R.X16, R.X7,  R.X19, 0xc, 0x8, 0x4),
    ("add", R.X8,  R.X23, R.X29, 0x808, 0x800, 0x8),
    ("add", R.X13, R.X5,  R.X27, 0x10, 0x0, 0x10),
    ("add", R.X27, R.X25, R.X20, 0x55555576, 0x55555556, 0x20),
    ("add", R.X17, R.X15, R.X26, 0x2f, -0x11, 0x40),
    ("add", R.X29, R.X17, R.X2,  0x7b, -0x5, 0x80),
    ("add", R.X4,  R.X24, R.X17, 0x120, 0x20, 0x100),
    ("add", R.X2,  R.X16, R.X11, 0x40000200, 0x40000000, 0x200),
]

@pytest.mark.parametrize("instr,rd,rs1,rs2,correctval,val1,val2", ADD_TESTS)
def test_rr_op(instr: str, rd: R, rs1: R, rs2: R, correctval: int, val1: int, val2: int):
    rv = RV32I(RAM())
    rv.set_reg(rs1, val1)
    rv.set_reg(rs2, val2)
    instr_bin = asm(instr, rd, rs1, rs2)
    rv.execute(rv.decode(instr_bin))
    expected = to_int32(correctval)
    assert rv.regs[rd] == expected, f"Found 0x{rv.regs[rd]:x}, expected 0x{expected:x}"
