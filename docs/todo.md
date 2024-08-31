# Todo

## General

- Create python project for emulator
- Setup pre-commit
- Include cocotb-test from this [example](https://github.com/themperek/cocotb-test/blob/master/tests/test_dff.py)

## Emulator

- Avoid overflow warnings
- Add overall function to run instruction
- Add memory manager with memory map
- Create linker file and have it execute compiled hex files
- Add FENCE, FENCE.TSO, PAUSE, ECALL, EBREAK instructions
- Cut down ALU tests and add to instruction tests

## VHDL core

- Define outer component
- Create testbench
- Decide on pipeline structure
