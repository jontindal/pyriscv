from enum import IntEnum
import itertools

import numpy as np
import numpy.typing as npt

import pyriscv.utils as u


class DataSize(IntEnum):
    BYTE = 1
    HALF = 2
    WORD = 4


class MemoryRegion:
    bytes: npt.NDArray[np.uint8]
    start_offset: int

    def __init__(self, size: int, offset: int) -> None:
        self.bytes = np.zeros(size, dtype=np.uint8)
        self.start_offset = offset

    def local_addr(self, addr: int) -> int:
        return addr - self.start_offset

    def addr_in_region(self, addr: np.uint32) -> bool:
        return self.start_offset <= addr and addr <= self.start_offset + self.bytes.size

    def read(self, addr: int, size: DataSize) -> np.uint32:
        local_addr = self.local_addr(addr)
        match size:
            case DataSize.BYTE:
                bits = u.int_to_bits(self.bytes[local_addr], 8)
            case DataSize.HALF:
                bits = (
                    u.int_to_bits(self.bytes[local_addr + 1], 8)
                    + u.int_to_bits(self.bytes[local_addr], 8)
                )
            case DataSize.WORD:
                bits = (
                    u.int_to_bits(self.bytes[local_addr + 3], 8)
                    + u.int_to_bits(self.bytes[local_addr + 2], 8)
                    + u.int_to_bits(self.bytes[local_addr + 1], 8)
                    + u.int_to_bits(self.bytes[local_addr], 8)
                )
        return u.to_uint32(u.bits_to_uint(bits))

    def write(self, addr: int, size: DataSize, value: np.uint32):
        local_addr = self.local_addr(addr)
        reg_bits = u.int_to_bits(value, 32)
        match size:
            case DataSize.BYTE:
                self.bytes[local_addr] = u.bits_to_uint(u.bitfield_slice(reg_bits, 7, 0))
            case DataSize.HALF:
                self.bytes[local_addr] = u.bits_to_uint(u.bitfield_slice(reg_bits, 7, 0))
                self.bytes[local_addr + 1] = u.bits_to_uint(u.bitfield_slice(reg_bits, 15, 8))
            case DataSize.WORD:
                self.bytes[local_addr] = u.bits_to_uint(u.bitfield_slice(reg_bits, 7, 0))
                self.bytes[local_addr + 1] = u.bits_to_uint(u.bitfield_slice(reg_bits, 15, 8))
                self.bytes[local_addr + 2] = u.bits_to_uint(u.bitfield_slice(reg_bits, 23, 16))
                self.bytes[local_addr + 3] = u.bits_to_uint(u.bitfield_slice(reg_bits, 31, 24))


class RVMemory:
    rom: MemoryRegion
    ram: MemoryRegion

    def __init__(self) -> None:
        self.rom = MemoryRegion(0x8000, 0x80000000)  # 32KB
        self.ram = MemoryRegion(0x1000, 0x90000000)  # 4KB

    def load_rom(self, rom_bytes: bytes) -> None:
        start_addr = self.rom.start_offset
        for addr, byte in zip(itertools.count(start_addr), rom_bytes):
            self.rom.write(addr, DataSize.BYTE, byte)

    def write(self, addr: np.uint32, size: DataSize, value: np.uint32) -> None:
        if self.ram.addr_in_region(addr):
            self.ram.write(addr, size, value)
        else:
            raise RuntimeError(f"Out of bounds write to addr: {addr}")

    def read(self, addr: np.uint32, size: DataSize) -> np.uint32:
        if self.rom.addr_in_region(addr):
            return self.rom.read(addr, size)
        elif self.ram.addr_in_region(addr):
            return self.ram.read(addr, size)
        else:
            raise RuntimeError(f"Out of bounds read to addr: {addr}")
