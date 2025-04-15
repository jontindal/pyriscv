.global main
.text

.equ SERIAL_BASE, 0xa0000000

main:
    la t0, msg                # Load address of message string into t0
    li t1, SERIAL_BASE        # Load address of the I/O output register

print_loop:
    lbu t2, 0(t0)             # Load byte from string (unsigned)
    beqz t2, done             # If null terminator, we're done
    sb t2, 0(t1)              # Store byte to output address
    addi t0, t0, 1            # Move to next character
    j print_loop              # Repeat

done:
    ret

.data
variable:
    .word 0xdeadbeef
msg:
    .asciz "Hello, World!\n"    # Null-terminated string
