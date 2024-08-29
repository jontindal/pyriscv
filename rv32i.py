from dataclasses import dataclass
from enum import Enum
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


class Opcodes(Enum):
    OP = 0b0110011
    OP_IMM = 0b0010011
    LOAD = 0b0000011
    STORE = 0b0100011
    BRANCH = 0b1100011
    JAL = 0b1101111
    JALR = 0b1100111
    LUI = 0b0110111
    AUIPC = 0b0010111


@dataclass
class DecodedInstr:
    opcode: Opcodes
    rd: int | None = None
    rs1: int | None = None
    rs2: int | None = None
    funct3: int | None = None
    funct7: int | None = None
    imm: int | None = None


class RV32I:
    memory: np.ndarray[t.Any, np.uint8]
    regs: np.ndarray[32, np.int32]
    pc: int

    def __init__(self, memory: np.ndarray[t.Any, np.uint8]) -> None:
        self.memory = memory
        self.regs = np.zeros(32, dtype=np.int32)
        self.pc = 0

    def set_reg(self, index: int, val: IntTypes) -> None:
        if index == 0:
            return
        self.regs[index] = to_int32(val)

    @staticmethod
    def decode(instr: int):
        opcode = Opcodes(instr & 0x7F)
        if opcode == Opcodes.OP:
            rd = (instr >> 7) & 0x1F
            funct3 = (instr >> 12) & 0x7
            rs1 = (instr >> 15) & 0x1F
            rs2 = (instr >> 20) & 0x1F
            funct7 = (instr >> 25) & 0x7F
            return DecodedInstr(opcode, rd, rs1, rs2, funct3, funct7)
        elif opcode == Opcodes.OP_IMM:
            rd = (instr >> 7) & 0x1F
            funct3 = (instr >> 12) & 0x7
            rs1 = (instr >> 15) & 0x1F
            imm = (instr >> 20) & 0x7FF
            if (instr >> 31) & 0x1:
                imm -= 0x800
            return DecodedInstr(opcode, rd, rs1, funct3=funct3, imm=imm)
        raise NotImplementedError

    def execute(self, instr: DecodedInstr):
        match instr.opcode:
            case Opcodes.OP:
                return self.execute_op(instr)
            case Opcodes.OP_IMM:
                return self.execute_imm(instr)

    def execute_op(self, instr: DecodedInstr):
        if instr.funct3 == 0x0 and instr.funct7 == 0x00:  # ADD
            result = self.regs[instr.rs1] + self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x0 and instr.funct7 == 0x20:  # SUB
            result = self.regs[instr.rs1] - self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x4 and instr.funct7 == 0x00:  # XOR
            result = self.regs[instr.rs1] ^ self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x6 and instr.funct7 == 0x00:  # OR
            result = self.regs[instr.rs1] | self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x7 and instr.funct7 == 0x00:  # AND
            result = self.regs[instr.rs1] & self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x1 and instr.funct7 == 0x00:  # SLL
            shift_num = self.regs[instr.rs2] & 0x1F  # Only consider lower 5 bits
            result = (to_uint32(self.regs[instr.rs1]) << shift_num) % (1 << 32)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5 and instr.funct7 == 0x00:  # SRL
            shift_num = self.regs[instr.rs2] & 0x1F  # Only consider lower 5 bits
            result = to_uint32(self.regs[instr.rs1]) >> shift_num
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5 and instr.funct7 == 0x20:  # SRA
            shift_num = self.regs[instr.rs2] & 0x1F  # Only consider lower 5 bits
            result = self.regs[instr.rs1] >> shift_num
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x2 and instr.funct7 == 0x00:  # SLT
            result = 1 if self.regs[instr.rs1] < self.regs[instr.rs2] else 0
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x3 and instr.funct7 == 0x00:  # SLTU
            result = (
                1
                if to_uint32(self.regs[instr.rs1]) < to_uint32(self.regs[instr.rs2])
                else 0
            )
            self.set_reg(instr.rd, result)

    def execute_imm(self, instr: DecodedInstr):
        if instr.funct3 == 0x0:  # ADDI
            result = self.regs[instr.rs1] + to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x4:  # XORI
            result = self.regs[instr.rs1] ^ to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x6:  # ORI
            result = self.regs[instr.rs1] | to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x7:  # ANDI
            result = self.regs[instr.rs1] & to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x1:
            if ((instr.imm >> 5) & 0x7F) == 0x00:  # SLLI
                shift_num = to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = (to_uint32(self.regs[instr.rs1]) << shift_num) % (1 << 32)
                self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5:
            if ((instr.imm >> 5) & 0x7F) == 0x00:  # SRLI
                shift_num = to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = to_uint32(self.regs[instr.rs1]) >> shift_num
                self.set_reg(instr.rd, result)
            elif ((instr.imm >> 5) & 0x7F) == 0x20:  # SRAI
                shift_num = to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = self.regs[instr.rs1] >> shift_num
                self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x2:  # SLTI
            result = 1 if self.regs[instr.rs1] < to_int32(instr.imm) else 0
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x3:  # SLTIU
            result = 1 if to_uint32(self.regs[instr.rs1]) < to_uint32(instr.imm) else 0
            self.set_reg(instr.rd, result)
