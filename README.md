# pyriscv

This project is a python emulator for the RV32I instruction set.

The emulator was developed by testing against a range of unit tests in pytest.

The emulator has been verified with the [RISC-V Architectural Test Suite](https://github.com/riscv-non-isa/riscv-arch-test) using the [RISCOF](https://riscof.readthedocs.io/en/stable/) framework.

## Installation

This has been built for and tested on **Python 3.10** on Ubuntu 20.04 and Windows.

```bash
pip install -e .
```

### Installation of RISCOF

This has been tested on Ubuntu 20.04.

#### Prerequisites

- [RISCV-GNU toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain)
- [Docker](https://docs.docker.com/engine/install/)
- [GNU Make](https://www.gnu.org/software/make/)

#### SAIL reference model

The RISCOF framework compares the results of the DUT (`pyriscv`) against a reference model ([SAIL](https://github.com/riscv/sail-riscv)).

##### Local installation

The SAIL model can installed locally following these [instructions](https://riscof.readthedocs.io/en/stable/installation.html#install-plugin-models).
To use a local installation, you must set `docker=false` in **`riscof/config.ini`**.

##### Using Docker

The SAIL model can also be run from a Docker image.

The following command can be used to pull the SAIL docker image.

```bash
docker pull jontindal/riscv-arch-test
```

Alternatively, the docker image from InCore Semiconductors can also be used for running RISCOF. The image is available at `registry.gitlab.com/incoresemi/docker-images/compliance`. However, the standard library installed with the RISC-V toolchain in this image is not compatible `pyriscv`, meaning it cannot be used for the testcases in `firmware/`.

#### Install `pyriscv` with RISCOF dependency

```bash
pip install -e .[dev]
```

## Usage

### CLI

Use the following command to run the emulator:

```bash
pyriscv <Path to program binary>
```

There is a separate entrypoint for RISCOF, `pyriscv-riscof`, which runs the emulator, writes the test signature to a file and has a modified memory map.

### Running pytest unit tests

```bash
pytest
```

### Running RISCOF architecture tests

```bash
cd riscof/
riscof --verbose info arch-test --clone
riscof run --config=config.ini --suite=riscv-arch-test/riscv-test-suite/ --env=riscv-arch-test/riscv-test-suite/env --no-browser
```

A summary of the test results is written to **`riscof_work/report.html`**.

### Firmware

The **`firmware/`** directory provides CMake build configuration, linker script, and startup code to compile binary programs.

**Building:**
```bash
cmake -S . -B build
cmake --build build
```

**Available targets:**
- `basic_asm` - Assembly-only program (no stdlib)
- `basic_c` - C program with minimal stdlib support
- `sort` - Bubble sort implementation in C and assembly

Each target generates a `.bin` binary and `-dump.txt` disassembly in the `build/` directory.
