from utils import int_to_bits, bits_to_int, bitfield_slice

from rv32i import Regs


ASM_INSTR_FORMATS = {
    "lui": ("U", "???????_???_0110111"),
    "auipc": ("U", "???????_???_0010111"),
    "jal": ("J", "???????_???_1101111"),
    "jalr": ("I", "???????_000_1100111"),
    "beq": ("B", "???????_000_1100011"),
    "bne": ("B", "???????_001_1100011"),
    "blt": ("B", "???????_100_1100011"),
    "bge": ("B", "???????_101_1100011"),
    "bltu": ("B", "???????_110_1100011"),
    "bgeu": ("B", "???????_111_1100011"),
    "lb": ("I", "???????_000_0000011"),
    "lh": ("I", "???????_001_0000011"),
    "lw": ("I", "???????_010_0000011"),
    "lbu": ("I", "???????_100_0000011"),
    "lhu": ("I", "???????_101_0000011"),
    "sb": ("S", "???????_000_0100011"),
    "sh": ("S", "???????_001_0100011"),
    "sw": ("S", "???????_010_0100011"),
    "addi": ("I", "???????_000_0010011"),
    "slti": ("I", "???????_010_0010011"),
    "sltiu": ("I", "???????_011_0010011"),
    "xori": ("I", "???????_100_0010011"),
    "ori": ("I", "???????_110_0010011"),
    "andi": ("I", "???????_111_0010011"),
    "slli": ("I", "???????_001_0010011"),
    "srli": ("I", "???????_101_0010011"),
    "srai": ("I", "???????_101_0010011"),
    "add": ("R", "0000000_000_0110011"),
    "sub": ("R", "0100000_000_0110011"),
    "sll": ("R", "0000000_001_0110011"),
    "slt": ("R", "0000000_010_0110011"),
    "sltu": ("R", "0000000_011_0110011"),
    "xor": ("R", "0000000_100_0110011"),
    "srl": ("R", "0000000_101_0110011"),
    "sra": ("R", "0100000_101_0110011"),
    "or": ("R", "0000000_110_0110011"),
    "and": ("R", "0000000_111_0110011"),
}


def asm(instr: str, rd: Regs | None = None, rs1: Regs | None = None,
        rs2: Regs | None = None, imm: int | None = None,):
    typ, opcode_bits = ASM_INSTR_FORMATS[instr]
    funct7, funct3, opcode = opcode_bits.split("_")

    if rd is not None:
        rd = int_to_bits(rd, 5)
    if rs1 is not None:
        rs1 = int_to_bits(rs1, 5)
    if rs2 is not None:
        rs2 = int_to_bits(rs2, 5)

    match typ:
        case "R":
            bits = funct7 + rs2 + rs1 + funct3 + rd + opcode
        case "I":
            if instr in ("slli", "srli", "srai"):
                funct7 = 0x20 if instr == "srai" else 0x00
                imm_i = int_to_bits(funct7, 7) + int_to_bits(imm, 5)
            else:
                imm_i = int_to_bits(imm, 12)
            bits = imm_i + rs1 + funct3 + rd + opcode
        case "U":
            imm_u = int_to_bits(imm, 20)
            bits = imm_u + rd + opcode
        case "S":
            imm_s = int_to_bits(imm, 12)
            bits = (
                bitfield_slice(imm_s, 11, 5)
                + rs2
                + rs1
                + funct3
                + bitfield_slice(imm_s, 4, 0)
                + opcode
            )
        case "J":
            imm_j = int_to_bits(imm, 21)
            bits = (
                bitfield_slice(imm_j, 20, 20)
                + bitfield_slice(imm_j, 10, 1)
                + bitfield_slice(imm_j, 11, 11)
                + bitfield_slice(imm_j, 19, 12)
                + rd
                + opcode
            )
        case "B":
            imm_b = int_to_bits(imm, 13)
            bits = (
                bitfield_slice(imm_b, 12, 12)
                + bitfield_slice(imm_b, 10, 5)
                + rs2
                + rs1
                + funct3
                + bitfield_slice(imm_b, 4, 1)
                + bitfield_slice(imm_b, 11, 11)
                + opcode
            )

    return bits_to_int(bits)
