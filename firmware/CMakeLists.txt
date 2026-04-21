cmake_minimum_required(VERSION 3.24)
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/toolchain-riscv-none-elf.cmake)

project(rv32i C ASM)

set(LINKER_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/sections.lds")
set(RISCV_STARTUP_FILE "${CMAKE_CURRENT_SOURCE_DIR}/start.S")

function(add_riscv_executable target_name)
    set(options USE_STDLIB)
    set(multiValueArgs SOURCES)
    cmake_parse_arguments(ARG "${options}" "" "${multiValueArgs}" ${ARGN})

    add_executable(${target_name} ${ARG_SOURCES})

    # Set RV32I target
    target_compile_options(${target_name} PRIVATE -march=rv32i -mabi=ilp32 -mcmodel=medany)
    target_link_options(${target_name} PRIVATE -march=rv32i -mabi=ilp32 -mcmodel=medany -static)

    # Replace default startup file with custom startup file
    target_link_options(${target_name} PRIVATE -nostartfiles)
    target_sources(${target_name} PRIVATE ${RISCV_STARTUP_FILE})

    # Add custom linker script
    target_link_options(${target_name} PRIVATE "-T${LINKER_SCRIPT}")
    set_target_properties(${target_name} PROPERTIES
        LINK_DEPENDS ${LINKER_SCRIPT}
    )

    # Print memory usage
    target_link_options(${target_name} PRIVATE -Wl,--gc-sections -Wl,--print-memory-usage)
    
    if(ARG_USE_STDLIB)
        target_compile_options(${target_name} PRIVATE --specs=nosys.specs)
        target_link_options(${target_name} PRIVATE --specs=nosys.specs)
        target_sources(${target_name} PRIVATE syscalls.c)
    else()
        target_compile_options(${target_name} PRIVATE -nostdlib)
        target_link_options(${target_name} PRIVATE -nostdlib)
    endif()

    add_custom_command(
        TARGET ${target_name} POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -O binary -S $<TARGET_FILE:${target_name}> 
                $<TARGET_FILE_DIR:${target_name}>/${target_name}.bin
        COMMAND ${CMAKE_OBJDUMP} -D $<TARGET_FILE:${target_name}> > 
                $<TARGET_FILE_DIR:${target_name}>/${target_name}-dump.txt
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating binary and disassembly for ${target_name}"
    )
endfunction()

add_riscv_executable(basic_asm SOURCES basic_asm.S)
add_riscv_executable(basic_c SOURCES basic_c.c USE_STDLIB)
add_riscv_executable(sort SOURCES sort.c sort_func.S USE_STDLIB)
