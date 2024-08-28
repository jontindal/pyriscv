"""Class to manage dynamic memory for processor, for a little-endian system"""
import numpy as np
import numpy.typing as npt


class RAM:
    addr_offset: int
    memory: npt.NDArray[np.uint8]

    def __init__(self, no_bytes: int = 0x1000, addr_offset: int = 0x2000) -> None:
        self.addr_offset = addr_offset
        self.memory = np.zeros(no_bytes, dtype=np.uint8)

    def store_uint32(self, addr: int, value: int) -> None:
        assert value < (1 << 32)
        assert value >= 0

        index = addr - self.addr_offset
        self.memory[index] = value & 0xff
        self.memory[index + 1] = (value >> 8) & 0xff
        self.memory[index + 2] = (value >> 16) & 0xff
        self.memory[index + 3] = (value >> 24) & 0xff

    def load_uint32(self, addr: int) -> None:
        index = addr - self.addr_offset
        return (
            (self.memory[index])
            | (self.memory[index + 1] << 8)
            | (self.memory[index + 2] << 16)
            | (self.memory[index + 3] << 24)
        )
