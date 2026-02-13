set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR riscv)

set(TOOLCHAIN_PREFIX riscv-none-elf)

set(CMAKE_C_COMPILER "${TOOLCHAIN_PREFIX}-gcc")
set(CMAKE_CXX_COMPILER "${TOOLCHAIN_PREFIX}-g++")
set(CMAKE_ASM_COMPILER "${TOOLCHAIN_PREFIX}-gcc")
set(CMAKE_OBJCOPY "${TOOLCHAIN_PREFIX}-objcopy")
set(CMAKE_OBJDUMP "${TOOLCHAIN_PREFIX}-objdump")
set(CMAKE_SIZE "${TOOLCHAIN_PREFIX}-size")

# Prevent CMake from testing the compiler (requires full linking)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

add_compile_options(-march=rv32i -mabi=ilp32 -static -mcmodel=medany)
add_link_options(-march=rv32i -mabi=ilp32 -static -mcmodel=medany -nostartfiles)
add_link_options(-Wl,--gc-sections -Wl,--print-memory-usage)