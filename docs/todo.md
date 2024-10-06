# Todo

## General

- Setup pre-commit

## Emulator

- General fixes
  - Avoid overflow warnings
  - Cut down ALU tests and add to instruction tests
  - Create tests FENCE, EBREAK and ECALL instructions
  - Add CI for pytests and riscof
  - Test across python versions
  - Add logging for CLI

## VHDL core

- Define outer component
- Create testbench from this [example](https://github.com/themperek/cocotb-test/blob/master/tests/test_dff.py)
- Decide on pipeline structure
