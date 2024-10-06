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

The SAIL model can installed locally following these [instructions](https://riscof.readthedocs.io/en/stable/installation.html#install-plugin-models) or run from a Docker image. These instruction are for running from the Docker image. To use a local installation, you must change the `docker=true` line in **`riscof/config.ini`**.

The following command can be used to pull the SAIL docker image.

```bash
docker pull registry.gitlab.com/incoresemi/docker-images/compliance
```

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

There is a seperate entrypoint for RISCOF, `pyriscv-riscof`, which runs the emulator, writes the test signature to a file and has a modified memory map.

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

The **`firmware/`** directory provides a Makefile, linker script and startup code to compile binary programs. The two example programs, **`firmware/basic_asm.S`** and **`firmware/basic_c.c`**, can be compiled by changing the `TARGET` variable in the Makefile.
