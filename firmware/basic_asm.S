.global main
.text

main:
    addi x1 , x0,   1000
    addi x1 , x1,   1000

.data
variable:
    .word 0xdeadbeef
