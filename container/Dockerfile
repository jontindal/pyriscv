FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    git make cmake wget \
    build-essential device-tree-compiler libboost-regex-dev libboost-system-dev \
    m4 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RISCV-V toolchain download
ENV RV_TOOLCHAIN_URL=https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/download/v14.2.0-3/xpack-riscv-none-elf-gcc-14.2.0-3-linux-x64.tar.gz
ENV RV_FILE=xpack-riscv-none-elf-gcc-14.2.0-3-linux-x64.tar.gz
ENV RV_INSTALL_PATH=/opt/riscv
ENV PATH=$PATH:$RV_INSTALL_PATH/bin
RUN mkdir -p $RV_INSTALL_PATH && \
    chown root $RV_INSTALL_PATH && \
    wget -O "$RV_FILE" "$RV_TOOLCHAIN_URL" && \
    tar --strip-components 1 -xvzf "$RV_FILE" -C $RV_INSTALL_PATH && \
    rm "$RV_FILE"

# SPIKE
ENV SPIKE_INSTALL_PATH=/opt/spike
ENV PATH=$PATH:$SPIKE_INSTALL_PATH/bin
RUN mkdir -p $SPIKE_INSTALL_PATH && \
    chown root $SPIKE_INSTALL_PATH && \
    git clone --depth 1 https://github.com/riscv/riscv-isa-sim.git && \
    cd riscv-isa-sim && \
    mkdir build && \
    cd build && \
    ../configure --prefix=$SPIKE_INSTALL_PATH && \
    make -j $(nproc) 1>/dev/null && \
    make install && \
    cd ../../ && \
    rm -rf riscv-isa-sim

# SAIL
ENV SAIL_URL=https://github.com/rems-project/sail/releases/download/0.19-linux-binary/sail.tar.gz
ENV SAIL_FILE=sail-0.19-linux.tar.gz
ENV SAIL_INSTALL_PATH=/opt/sail
ENV PATH=$PATH:$SAIL_INSTALL_PATH/bin
RUN mkdir -p $SAIL_INSTALL_PATH && \
    chown root $SAIL_INSTALL_PATH && \
    wget -O "$SAIL_FILE" "$SAIL_URL" && \
    tar --strip-components 1 -xvzf "$SAIL_FILE" -C $SAIL_INSTALL_PATH && \
    rm "$SAIL_FILE"

# SAIL RISC-V
RUN git clone --depth 1 https://github.com/riscv/sail-riscv.git && \
    cd sail-riscv && \
    ./build_simulators.sh && \
    cp ./build/c_emulator/riscv_sim_rv* /usr/bin/ && \
    cd ../ && \
    rm -rf sail-riscv

# xpack toolchain uses riscv-none-elf prefix and is compatible with 32 and 64 bit
# Add symlink to riscv{32,64}-unknown-elf prefix that is commonly assumed
RUN cd $RV_INSTALL_PATH/bin && \
    for file in riscv-none-elf-*; do \
        ln -sf "$file" "riscv32-unknown-elf-${file#riscv-none-elf-}"; \
        ln -sf "$file" "riscv64-unknown-elf-${file#riscv-none-elf-}"; \
    done
