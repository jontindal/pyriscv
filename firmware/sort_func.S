.text
.global sort

sort:
    # Function to implement the following C code
    #
    # void sort(int *v, int n) {
    #     int i,j;
    #     for ( i=1; i<n; i++ ) {
    #         j = i-1;
    #         while ((j >= 0) && (v[j] > v[j+1]) ) {
    #             swap(v[j],v[j+1]);
    #             j = j-1;
    #         }
    #     }
    # }
    #
    # Arguments:
    # a0 = pointer to array v
    # a1 = integer n
    addi sp, sp, -28
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw ra, 24(sp)
    addi s0, a0, 0 # s0 = *v
    addi s1, a1, 0 # s1 = n
    addi s2, zero, 1                # i = 1
    ble s1, s2, i_loop_exit         # if n <= 1, exit
i_loop:
    addi s3, s2, -1                 # j = i - 1
while_loop:
    blt s3, zero, while_loop_exit   # if j < 0, exit
    slli t0, s3, 2                  # t0 = j * 4 (size of int)
    add  a0, s0, t0                 # a0 = &v[j]
    lw s4, 0(a0)                    # s4 = v[j]
    lw s5, 4(a0)                    # s5 = v[j+1]
    ble s4, s5, while_loop_exit     # if v[j] <= v[j+1], exit
    addi a1, a0, 4                  # a1 = &v[j+1]
    call swap
    addi s3, s3, -1                 # j = j - 1
    jal zero, while_loop
while_loop_exit:
    addi s2, s2, 1
    blt s2, s1, i_loop              # if i < n, repeat loop
i_loop_exit:
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 28
    ret
