cmake_minimum_required(VERSION 3.16)
project(rv32i C ASM)

set(LINKER_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/sections.lds")
add_link_options(-T${LINKER_SCRIPT})

function(add_riscv_executable target_name)
    set(options USE_STDLIB)
    set(multiValueArgs SOURCES)
    cmake_parse_arguments(ARG "${options}" "" "${multiValueArgs}" ${ARGN})

    add_executable(${target_name} ${ARG_SOURCES} start.S)
    
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
                ${target_name}.bin
        COMMAND ${CMAKE_OBJDUMP} -D $<TARGET_FILE:${target_name}> > 
                ${target_name}-dump.txt
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating binary and disassembly for ${target_name}"
    )
endfunction()

add_riscv_executable(basic_asm SOURCES basic_asm.S)
add_riscv_executable(basic_c SOURCES basic_c.c USE_STDLIB)
add_riscv_executable(sort SOURCES sort.c sort_func.S USE_STDLIB)