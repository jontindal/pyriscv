import pytest
import typing as t

from assem import RegNames as R, asm
from ram import RAM


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
