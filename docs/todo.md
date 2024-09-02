# Todo

## General

- Setup pre-commit

## Emulator

- General fixes
  - Avoid overflow warnings
  - Add FENCE, FENCE.TSO, PAUSE, ECALL, EBREAK instructions
  - Cut down ALU tests and add to instruction tests
- Run executables
  - Run function to fetch, decode, execute
  - Add hex/ELF file loader to load sections into memory
    - Possibly use [pyelftools](https://github.com/eliben/pyelftools/wiki/User's-guide)
    - Could also parse `objdump` output file
    - Could use `--section only .text*` or `--section only .data*` args for `objcopy`
  - Add CLI to run ELF files
  - Add CLI to run RISCOF files and return test [signature](https://riscof.readthedocs.io/en/stable/testformat.html#the-risc-v-architectural-test-suite)

## VHDL core

- Define outer component
- Create testbench from this [example](https://github.com/themperek/cocotb-test/blob/master/tests/test_dff.py)
- Decide on pipeline structure
