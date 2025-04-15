from enum import IntEnum
import sys
from typing import Protocol, TextIO

import numpy as np
import numpy.typing as npt

import pyriscv.utils as u


class DataSize(IntEnum):
    BYTE = 1
    HALF = 2
    WORD = 4


class MemRegion(Protocol):
    size: int
    start_offset: int

    def read(self, addr: int, size: DataSize) -> np.uint32:
        ...

    def write(self, addr: int, size: DataSize, value: np.uint32):
        ...


class ROMRegion(MemRegion):
    _bytes: npt.NDArray[np.uint8]

    def __init__(self, size: int, offset: int) -> None:
        self._bytes = np.zeros(size, dtype=np.uint8)
        self.start_offset = offset

    @property
    def size(self) -> int:
        return self._bytes.size

    def load(self, contents: bytes):
        for local_addr, byte in enumerate(contents):
            self._bytes[local_addr] = byte

    def read(self, local_addr: int, size: DataSize) -> np.uint32:
        match size:
            case DataSize.BYTE:
                bits = u.int_to_bits(self._bytes[local_addr], 8)
            case DataSize.HALF:
                bits = u.int_to_bits(self._bytes[local_addr + 1], 8) + u.int_to_bits(
                    self._bytes[local_addr], 8
                )
            case DataSize.WORD:
                bits = (
                    u.int_to_bits(self._bytes[local_addr + 3], 8)
                    + u.int_to_bits(self._bytes[local_addr + 2], 8)
                    + u.int_to_bits(self._bytes[local_addr + 1], 8)
                    + u.int_to_bits(self._bytes[local_addr], 8)
                )
        return u.to_uint32(u.bits_to_uint(bits))

    def write(self, addr: int, size: DataSize, value: np.uint32):
        raise RuntimeError(f"Invalid write to ROM at 0x{addr:x}")


class RAMRegion(ROMRegion):
    def write(self, local_addr: int, size: DataSize, value: np.uint32):
        reg_bits = u.int_to_bits(value, 32)
        match size:
            case DataSize.BYTE:
                self._bytes[local_addr] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 7, 0)
                )
            case DataSize.HALF:
                self._bytes[local_addr] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 7, 0)
                )
                self._bytes[local_addr + 1] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 15, 8)
                )
            case DataSize.WORD:
                self._bytes[local_addr] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 7, 0)
                )
                self._bytes[local_addr + 1] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 15, 8)
                )
                self._bytes[local_addr + 2] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 23, 16)
                )
                self._bytes[local_addr + 3] = u.bits_to_uint(
                    u.bitfield_slice(reg_bits, 31, 24)
                )


class SerialPort(MemRegion):
    """Single byte serial port"""
    read_file: TextIO
    write_file: TextIO

    def __init__(self, addr: int, read_file: TextIO = sys.stdin, write_file: TextIO = sys.stdout):
        self.start_offset = addr
        self.read_file = read_file
        self.write_file = write_file

    @property
    def size(self):
        return 1

    def read(self, local_addr: int, size: DataSize) -> np.uint32:
        if size is not DataSize.BYTE:
            raise RuntimeError("Can only read single bytes to serial port")
        return ord(self.read_file.read(1))

    def write(self, local_addr: int, size: DataSize, value: np.uint32):
        if size is not DataSize.BYTE:
            raise RuntimeError("Can only write single bytes to serial port")
        self.write_file.write(chr(value))


class RVMemory:
    mem_regions: list[MemRegion]
    program_mem: ROMRegion
    data_mem: RAMRegion

    def __init__(self) -> None:
        self.mem_regions = [
            ROMRegion(0x8000, 0x80000000),  # 32KB
            RAMRegion(0x2000, 0x90000000),  # 8KB
            SerialPort(0xa0000000)
        ]
        self.program_mem = self.mem_regions[0]
        self.data_mem = self.mem_regions[1]

    @staticmethod
    def addr_in_region(region: MemRegion, addr: int):
        return region.start_offset <= addr and addr <= region.start_offset + region.size

    def load_program(self, prog_bytes: bytes) -> int:
        """Load program and return program start address"""
        self.program_mem.load(prog_bytes)
        return self.program_mem.start_offset

    def write(self, addr: np.uint32, size: DataSize, value: np.uint32) -> None:
        for mem_region in self.mem_regions:
            if self.addr_in_region(mem_region, addr):
                mem_region.write(addr - mem_region.start_offset, size, value)
                return

        raise RuntimeError(f"Out of bounds write to addr: 0x{addr:x}")

    def read(self, addr: np.uint32, size: DataSize) -> np.uint32:
        for mem_region in self.mem_regions:
            if self.addr_in_region(mem_region, addr):
                return mem_region.read(addr - mem_region.start_offset, size)

        raise RuntimeError(f"Out of bounds read to addr: 0x{addr:x}")


class RiscofMemory(RVMemory):
    """
    Memory for RISCOF tests.
    All program memory goes into RAM.
    """

    def __init__(self) -> None:
        # Riscof requires 1.7MB for jal-01.S
        self.mem_regions = [
            RAMRegion(0x200000, 0x80000000),  # 2MB
        ]
        self.program_mem = self.mem_regions[0]
        self.data_mem = self.mem_regions[0]
