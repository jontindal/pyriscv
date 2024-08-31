# RISCOF setup

Setup instructions to be able to run the RISC-V arch using [RISCOF](https://riscof.readthedocs.io/en/stable/index.html). Includes installation of the toolchain, two emulators and the RISCOF package.

Based on RISCOF [Quickstart](https://riscof.readthedocs.io/en/stable/installation.html) guide.

## Install RISC-V toolchain

The 32-bit RISC-V [toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) should be built and installed.

### Create install directory and add to PATH

```bash
export RV_INSTALL_PATH=/opt/riscv
sudo mkdir $RV_INSTALL_PATH
sudo chown $USER $RV_INSTALL_PATH
printf 'export PATH="%s/bin:$PATH"\n' $RV_INSTALL_PATH >> ~/.profile
. ~/.profile
```

### Install dependencies

```bash
sudo apt-get install autoconf automake autotools-dev curl python3 python3-pip libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build git cmake libglib2.0-dev libslirp-dev
```

### Build toolchain

```bash
git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git
cd riscv-gnu-toolchain
./configure --prefix=$RV_INSTALL_PATH --with-arch=rv32gc --with-abi=ilp32d # for 32-bit toolchain
make
```

## Get SAIL emulator docker image

```bash
docker pull registry.gitlab.com/incoresemi/docker-images/compliance
```

## Install Spike emulator

### Create install directory and add to PATH temporarily

```bash
export SPIKE_INSTALL_PATH="$(pwd)/spike_install"
mkdir $RV_INSTALL_PATH
export PATH="$SPIKE_INSTALL_PATH/bin:$PATH"
```

### Build emulator

```bash
sudo apt-get install device-tree-compiler
git clone https://github.com/riscv-software-src/riscv-isa-sim.git
cd riscv-isa-sim
mkdir build
cd build
../configure --prefix=$SPIKE_INSTALL_PATH
make
make install
```

## Test with `riscof`

### Installation

```bash
pip install riscof
```

### Create Env files

```bash
riscof setup --dutname=spike

# Configure to use docker container
echo 'docker=true' >> config.ini
echo 'image=registry.gitlab.com/incoresemi/docker-images/compliance' >> config.ini

# Patch SAIL plugin to include docker support
curl https://gitlab.com/incoresemi/riscof-plugins/-/raw/master/sail_cSim/riscof_sail_cSim.py -o sail_cSim/riscof_sail_cSim.py
```

Note: plugin patch needed to fix this [issue](https://github.com/riscv-software-src/riscof/issues/99).

### Run tests

```bash
riscof --verbose info arch-test --clone
riscof validateyaml --config=config.ini
riscof testlist --config=config.ini --suite=riscv-arch-test/riscv-test-suite/ --env=riscv-arch-test/riscv-test-suite/env
riscof run --config=config.ini --suite=riscv-arch-test/riscv-test-suite/ --env=riscv-arch-test/riscv-test-suite/env --no-browser
```

## Appendix

### Test install instructions

#### Create docker container

```bash
docker run --rm -it ubuntu:22.04 /bin/bash
```

#### Create user with sudo

```bash
apt-get update && apt-get -y install sudo
useradd --create-home --shell /bin/bash --gid root --groups sudo testuser
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
su - testuser
```
