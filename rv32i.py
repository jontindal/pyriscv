from dataclasses import dataclass
from enum import Enum
import typing as t

import numpy as np


IntTypes = int | np.uint32 | np.int32


def to_uint32(val: IntTypes) -> np.uint32:
    if val < 0:
        val += (1 << 32)
    return np.uint32(val)


def to_int32(val: IntTypes) -> np.int32:
    if val >= (1 << 31):
        val -= (1 << 32)
    return np.int32(val)


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
        return opcode

    def execute(self, instr: DecodedInstr):
        match instr.opcode:
            case Opcodes.OP:
                return self.execute_op(instr)

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
            result = self.regs[instr.rs1] >> self.regs[instr.rs2]
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5 and instr.funct7 == 0x00:  # SRL
            raise NotImplementedError
        elif instr.funct3 == 0x5 and instr.funct7 == 0x20:  # SRA
            raise NotImplementedError
        elif instr.funct3 == 0x2 and instr.funct7 == 0x00:  # SLT
            result = 1 if self.regs[instr.rs1] < self.regs[instr.rs2] else 0
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x3 and instr.funct7 == 0x00:  # SLTU
            raise NotImplementedError
