.global main
.text

main:
    addi a1 , x0,   1000
    addi a1 , a1,   1000
    ret

.data
variable:
    .word 0xdeadbeef
