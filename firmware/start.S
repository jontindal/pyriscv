.section    ._start

_start:
    # Set stack pointer
    la sp, _estack

    # Copy data section from ROM to RAM
    la a0, _sidata
    la a1, _sdata
    la a2, _edata

    bge a1, a2, end_init_data
loop_init_data:
    lw a3, 0(a0)
    sw a3, 0(a1)
    addi a0, a0, 4
    addi a1, a1, 4
    blt a1, a2, loop_init_data
end_init_data:

    # Initialise BSS section with zeros
    la a0, _sbss
    la a1, _ebss
    bge a0, a1, end_init_bss
loop_init_bss:
    sw zero, 0(a0)
    addi a0, a0, 4
    blt a0, a1, loop_init_bss
end_init_bss:

    # Call main function
    call main

    # Stop execution
    ebreak
