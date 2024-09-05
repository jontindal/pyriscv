from dataclasses import dataclass
from enum import IntEnum

import numpy as np
import numpy.typing as npt

from pyriscv import mem
import pyriscv.utils as u


class Regs(IntEnum):
    X0 = 0
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X6 = 6
    X7 = 7
    X8 = 8
    X9 = 9
    X10 = 10
    X11 = 11
    X12 = 12
    X13 = 13
    X14 = 14
    X15 = 15
    X16 = 16
    X17 = 17
    X18 = 18
    X19 = 19
    X20 = 20
    X21 = 21
    X22 = 22
    X23 = 23
    X24 = 24
    X25 = 25
    X26 = 26
    X27 = 27
    X28 = 28
    X29 = 29
    X30 = 30
    X31 = 31


class Opcodes(IntEnum):
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
    rd: Regs | None = None
    rs1: Regs | None = None
    rs2: Regs | None = None
    funct3: int | None = None
    funct7: int | None = None
    imm: int | None = None


class RV32I:
    memory: mem.RVMemory
    regs: npt.NDArray[np.int32]
    pc: np.int32

    def __init__(self) -> None:
        self.memory = mem.RVMemory()
        self.regs = np.zeros(32, dtype=np.int32)
        self.pc = np.int32(0)

    def set_pc(self, val: u.IntTypes) -> None:
        self.pc = u.to_int32(val)

    def inc_pc(self) -> None:
        self.pc += mem.DataSize.WORD

    def set_reg(self, index: Regs, val: u.IntTypes) -> None:
        if index == 0:
            return
        self.regs[index] = u.to_int32(val)

    def fetch(self) -> np.uint32:
        instr_addr = u.to_uint32(self.pc)
        return self.memory.read(instr_addr, mem.DataSize.WORD)

    @staticmethod
    def decode(instr: np.uint32):
        bits = u.int_to_bits(instr, 32)

        opcode_bits, rd_bits, funct3_bits, rs1_bits, rs2_bits, funct7_bits = (
            u.split_bitfield(bits, (7, 5, 3, 5, 5, 7))
        )
        opcode = Opcodes(u.bits_to_uint(opcode_bits))
        rd = Regs(u.bits_to_uint(rd_bits))
        funct3 = u.bits_to_uint(funct3_bits)
        rs1 = Regs(u.bits_to_uint(rs1_bits))
        rs2 = Regs(u.bits_to_uint(rs2_bits))
        funct7 = u.bits_to_uint(funct7_bits)
        imm = None

        match opcode:
            case Opcodes.OP:
                pass
            case Opcodes.OP_IMM | Opcodes.LOAD | Opcodes.JALR:  # I-type
                imm = u.bits_to_int(u.bitfield_slice(bits, 31, 20))
            case Opcodes.STORE:  # S-Type
                imm = u.bits_to_int(
                    u.bitfield_slice(bits, 31, 25) + u.bitfield_slice(bits, 11, 7)
                )
            case Opcodes.BRANCH:  # B-Type
                imm = u.bits_to_int(
                    u.bitfield_slice(bits, 31, 31)
                    + u.bitfield_slice(bits, 7, 7)
                    + u.bitfield_slice(bits, 30, 25)
                    + u.bitfield_slice(bits, 11, 8)
                    + "0"
                )
            case Opcodes.JAL:  # J-Type
                imm = u.bits_to_int(
                    u.bitfield_slice(bits, 31, 31)
                    + u.bitfield_slice(bits, 19, 12)
                    + u.bitfield_slice(bits, 20, 20)
                    + u.bitfield_slice(bits, 30, 21)
                    + "0"
                )
            case Opcodes.LUI | Opcodes.AUIPC:  # U-type
                imm = u.bits_to_int(u.bitfield_slice(bits, 31, 12))
            case _:
                raise RuntimeError(f"Unknown opcode: {opcode}")

        return DecodedInstr(opcode, rd, rs1, rs2, funct3, funct7, imm)

    def execute(self, instr: DecodedInstr):
        match instr.opcode:
            case Opcodes.OP:
                return self.execute_op(instr)
            case Opcodes.OP_IMM:
                return self.execute_imm(instr)
            case Opcodes.LOAD:
                return self.execute_load(instr)
            case Opcodes.STORE:
                return self.execute_store(instr)
            case Opcodes.BRANCH:
                return self.execute_branch(instr)
            case Opcodes.JAL:
                return self.execute_jal(instr)
            case Opcodes.JALR:
                return self.execute_jalr(instr)
            case Opcodes.LUI:
                return self.execute_lui(instr)
            case Opcodes.AUIPC:
                return self.execute_auipc(instr)
            case _:
                raise RuntimeError(f"Unknown opcode: {instr.opcode}")

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
            result = (u.to_uint32(self.regs[instr.rs1]) << shift_num) % (1 << 32)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5 and instr.funct7 == 0x00:  # SRL
            shift_num = self.regs[instr.rs2] & 0x1F  # Only consider lower 5 bits
            result = u.to_uint32(self.regs[instr.rs1]) >> shift_num
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
                if u.to_uint32(self.regs[instr.rs1]) < u.to_uint32(self.regs[instr.rs2])
                else 0
            )
            self.set_reg(instr.rd, result)
        self.inc_pc()

    def execute_imm(self, instr: DecodedInstr):
        if instr.funct3 == 0x0:  # ADDI
            result = self.regs[instr.rs1] + u.to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x4:  # XORI
            result = self.regs[instr.rs1] ^ u.to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x6:  # ORI
            result = self.regs[instr.rs1] | u.to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x7:  # ANDI
            result = self.regs[instr.rs1] & u.to_int32(instr.imm)
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x1:
            if ((instr.imm >> 5) & 0x7F) == 0x00:  # SLLI
                shift_num = u.to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = (u.to_uint32(self.regs[instr.rs1]) << shift_num) % (1 << 32)
                self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x5:
            if ((instr.imm >> 5) & 0x7F) == 0x00:  # SRLI
                shift_num = u.to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = u.to_uint32(self.regs[instr.rs1]) >> shift_num
                self.set_reg(instr.rd, result)
            elif ((instr.imm >> 5) & 0x7F) == 0x20:  # SRAI
                shift_num = u.to_int32(instr.imm) & 0x1F  # Only consider lower 5 bits
                result = self.regs[instr.rs1] >> shift_num
                self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x2:  # SLTI
            result = 1 if self.regs[instr.rs1] < u.to_int32(instr.imm) else 0
            self.set_reg(instr.rd, result)
        elif instr.funct3 == 0x3:  # SLTIU
            result = (
                1 if u.to_uint32(self.regs[instr.rs1]) < u.to_uint32(instr.imm) else 0
            )
            self.set_reg(instr.rd, result)
        self.inc_pc()

    def execute_load(self, instr: DecodedInstr):
        addr = u.to_uint32(self.regs[instr.rs1] + instr.imm)
        match instr.funct3:
            case 0x0:  # LB
                read_val = self.memory.read(addr, mem.DataSize.BYTE)
                val = u.bits_to_int(u.int_to_bits(read_val, 8))
            case 0x1:  # LH
                read_val = self.memory.read(addr, mem.DataSize.HALF)
                val = u.bits_to_int(u.int_to_bits(read_val, 16))
            case 0x2:  # LW
                read_val = self.memory.read(addr, mem.DataSize.WORD)
                val = u.bits_to_int(u.int_to_bits(read_val, 32))
            case 0x4:  # LBU
                read_val = self.memory.read(addr, mem.DataSize.BYTE)
                val = u.bits_to_uint(u.int_to_bits(read_val, 8))
            case 0x5:  # LHU
                read_val = self.memory.read(addr, mem.DataSize.HALF)
                val = u.bits_to_uint(u.int_to_bits(read_val, 16))
        self.set_reg(instr.rd, val)
        self.inc_pc()

    def execute_store(self, instr: DecodedInstr):
        addr = u.to_uint32(self.regs[instr.rs1] + instr.imm)
        value = u.to_uint32(self.regs[instr.rs2])
        match instr.funct3:
            case 0x0:  # SB
                self.memory.write(addr=addr, size=mem.DataSize.BYTE, value=value)
            case 0x1:  # SH
                self.memory.write(addr, mem.DataSize.HALF, value)
            case 0x2:  # SW
                self.memory.write(addr=addr, size=mem.DataSize.WORD, value=value)
        self.inc_pc()

    def execute_branch(self, instr: DecodedInstr):
        match instr.funct3:
            case 0x0:  # BEQ
                branch = self.regs[instr.rs1] == self.regs[instr.rs2]
            case 0x1:  # BNE
                branch = self.regs[instr.rs1] != self.regs[instr.rs2]
            case 0x4:  # BLT
                branch = self.regs[instr.rs1] < self.regs[instr.rs2]
            case 0x5:  # BGT
                branch = self.regs[instr.rs1] >= self.regs[instr.rs2]
            case 0x6:  # BLTU
                branch = u.to_uint32(self.regs[instr.rs1]) < u.to_uint32(
                    self.regs[instr.rs2]
                )
            case 0x7:  # BGEU
                branch = u.to_uint32(self.regs[instr.rs1]) >= u.to_uint32(
                    self.regs[instr.rs2]
                )

        if branch:
            self.pc += instr.imm
        else:
            self.inc_pc()

    def execute_jal(self, instr: DecodedInstr):
        self.set_reg(instr.rd, self.pc + 4)
        self.pc += instr.imm

    def execute_jalr(self, instr: DecodedInstr):
        if instr.funct3 == 0x0:
            dest_addr = self.regs[instr.rs1] + instr.imm
            dest_addr &= ~1  # RISC-V spec defines that LSB should be set to 0

            self.set_reg(instr.rd, self.pc + 4)
            self.pc = dest_addr
        else:
            self.inc_pc()

    def execute_lui(self, instr: DecodedInstr):
        val = instr.imm << 12
        self.set_reg(instr.rd, val)
        self.inc_pc()

    def execute_auipc(self, instr: DecodedInstr):
        val = self.pc + (instr.imm << 12)
        self.set_reg(instr.rd, val)
        self.inc_pc()

    def run_bin(self, hex_filepath: str, max_instructions: int = 100):
        rom_bytes = open(hex_filepath, "rb").read()
        self.memory.load_rom(rom_bytes)
        self.pc = self.memory.rom.start_offset

        for i in range(max_instructions):
            bin_instr = self.fetch()
            decoded_instr = self.decode(bin_instr)

            print(f"addr: 0x{u.to_uint32(self.pc):x}\tbin instr: 0x{bin_instr:x}\t{decoded_instr = }")
            self.execute(decoded_instr)


if __name__ == "__main__":
    rv = RV32I()
    rv.run_bin("firmware/build/basic_c.bin")
