"""
Sample of the ffficial RISC-V tests from
https://github.com/riscv-non-isa/riscv-arch-test/blob/main/riscv-test-suite
"""
from assem import RegNames as R

ADD_TESTS = [
    ("add", R.X24, R.X4,  R.X24, 0x80000000, 0x7fffffff, 0x1),
    ("add", R.X28, R.X10, R.X10, 0x40000, 0x20000, 0x20000),
    ("add", R.X21, R.X21, R.X21, 0xfdfffffe, -0x1000001, -0x1000001),
    ("add", R.X22, R.X22, R.X31, 0x3fffe, -0x2, 0x40000),
    ("add", R.X11, R.X12, R.X6,  0xaaaaaaac, 0x55555556, 0x55555556),
    ("add", R.X10, R.X29, R.X13, 0x80000002, 0x2, -0x80000000),
    ("add", R.X26, R.X31, R.X5,  0xffffffef, -0x11, 0x0),
    ("add", R.X7,  R.X2,  R.X1,  0xe6666665, 0x66666666, 0x7fffffff),
    ("add", R.X14, R.X8,  R.X25, 0x2aaaaaaa, -0x80000000, -0x55555556),
    ("add", R.X1,  R.X13, R.X8,  0xfdffffff, 0x0, -0x2000001),
    ("add", R.X0,  R.X28, R.X9,  0, 0x1, 0x800000),
    ("add", R.X20, R.X14, R.X4,  0x9, 0x7, 0x2),
    ("add", R.X16, R.X7,  R.X19, 0xc, 0x8, 0x4),
    ("add", R.X8,  R.X23, R.X29, 0x808, 0x800, 0x8),
    ("add", R.X13, R.X5,  R.X27, 0x10, 0x0, 0x10),
    ("add", R.X27, R.X25, R.X20, 0x55555576, 0x55555556, 0x20),
    ("add", R.X17, R.X15, R.X26, 0x2f, -0x11, 0x40),
    ("add", R.X29, R.X17, R.X2,  0x7b, -0x5, 0x80),
    ("add", R.X4,  R.X24, R.X17, 0x120, 0x20, 0x100),
    ("add", R.X2,  R.X16, R.X11, 0x40000200, 0x40000000, 0x200),
]

SUB_TESTS = [
    ("sub", R.X26, R.X24, R.X26, 0x5555554e, 0x55555554, 0x6),
    ("sub", R.X23, R.X17, R.X17, 0x0, 0x2000000, 0x2000000),
    ("sub", R.X16, R.X16, R.X16, 0x0, -0x7, -0x7),
    ("sub", R.X31, R.X31, R.X19, 0x99999998, -0x3, 0x66666665),
    ("sub", R.X8,  R.X23, R.X14, 0x0, 0x80000, 0x80000),
    ("sub", R.X18, R.X13, R.X24, 0x7bffffff, -0x4000001, -0x80000000),
    ("sub", R.X0,  R.X12, R.X4,  0, 0x20, 0x0),
    ("sub", R.X10, R.X22, R.X9,  0x60000000, -0x20000001, 0x7fffffff),
    ("sub", R.X25, R.X10, R.X27, 0xffff, 0x10000, 0x1),
    ("sub", R.X14, R.X8,  R.X3,  0xc0000000, -0x80000000, -0x40000000),
    ("sub", R.X29, R.X25, R.X30, 0xffe00000, 0x0, 0x200000),
    ("sub", R.X15, R.X18, R.X8,  0x7fffdfff, 0x7fffffff, 0x2000),
    ("sub", R.X3,  R.X14, R.X15, 0xfffffff1, 0x1, 0x10),
    ("sub", R.X13, R.X26, R.X29, 0xfffffff7, -0x7, 0x2),
    ("sub", R.X19, R.X21, R.X31, 0xfffffffe, 0x2, 0x4),
    ("sub", R.X11, R.X30, R.X5,  0xfefffff7, -0x1000001, 0x8),
    ("sub", R.X30, R.X28, R.X7,  0xaaaaaa8a, -0x55555556, 0x20),
    ("sub", R.X7,  R.X9,  R.X10, 0xffffff7f, -0x41, 0x40),
    ("sub", R.X17, R.X0,  R.X18, 0xffffff80, 0x0, 0x80),
    ("sub", R.X27, R.X2,  R.X12, 0xbfffff00, -0x40000000, 0x100),
]

SLL_TESTS = [
    ("sll", R.X28, R.X16, R.X28, 0xfffdfc00, -0x81, 0xa),
    ("sll", R.X0,  R.X21, R.X21, 0, 0x5, 0x5),
    ("sll", R.X18, R.X18, R.X18, 0x80000000, -0x8001, -0x8001),
    ("sll", R.X5,  R.X5,  R.X13, 0x7, 0x7, 0x0),
    ("sll", R.X23, R.X22, R.X12, 0x180, 0x6, 0x6),
    ("sll", R.X6,  R.X19, R.X0,  0x80000000, -0x80000000, 0x0),
    ("sll", R.X13, R.X25, R.X24, 0x0, 0x0, 0x4),
    ("sll", R.X16, R.X12, R.X26, 0xffe00000, 0x7fffffff, 0x15),
    ("sll", R.X20, R.X6,  R.X14, 0x10, 0x1, 0x4),
    ("sll", R.X22, R.X14, R.X1,  0x0, 0x2, 0x1f),
    ("sll", R.X21, R.X29, R.X7,  0x10, 0x4, 0x2),
    ("sll", R.X4,  R.X31, R.X10, 0x0, 0x8, 0x1f),
    ("sll", R.X7,  R.X17, R.X20, 0x0, 0x10, 0x1f),
    ("sll", R.X12, R.X20, R.X11, 0x10000000, 0x20, 0x17),
    ("sll", R.X3,  R.X11, R.X22, 0x800000, 0x40, 0x11),
    ("sll", R.X24, R.X0,  R.X30, 0x0, 0x0, 0x10),
    ("sll", R.X8,  R.X3,  R.X31, 0x0, 0x100, 0x1b),
    ("sll", R.X10, R.X27, R.X17, 0x200, 0x200, 0x0),
    ("sll", R.X11, R.X10, R.X19, 0x0, 0x400, 0x1b),
    ("sll", R.X1,  R.X8,  R.X27, 0x20000, 0x800, 0x6),
]

SLT_TESTS = [
    ("slt", R.X26, R.X18, R.X26, 0x0, 0x66666667, 0x66666667),
    ("slt", R.X1,  R.X20, R.X20, 0x0, 0x33333334, 0x33333334),
    ("slt", R.X21, R.X21, R.X21, 0x0, -0x4001, -0x4001),
    ("slt", R.X15, R.X15, R.X27, 0x1, -0x201, 0x5),
    ("slt", R.X7,  R.X5,  R.X18, 0x0, 0x33333334, -0x80000000),
    ("slt", R.X17, R.X25, R.X19, 0x0, 0x8000000, 0x0),
    ("slt", R.X23, R.X9,  R.X31, 0x1, 0x20000, 0x7fffffff),
    ("slt", R.X11, R.X2,  R.X15, 0x1, -0x20001, 0x1),
    ("slt", R.X22, R.X28, R.X13, 0x1, -0x80000000, 0x400),
    ("slt", R.X30, R.X10, R.X7,  0x1, 0x0, 0x8),
    ("slt", R.X5,  R.X24, R.X22, 0x0, 0x7fffffff, -0x101),
    ("slt", R.X24, R.X8,  R.X3,  0x0, 0x1, -0x201),
    ("slt", R.X2,  R.X26, R.X9,  0x0, 0x10000000, 0x2),
    ("slt", R.X8,  R.X4,  R.X14, 0x0, 0x8000, 0x4),
    ("slt", R.X25, R.X6,  R.X4,  0x1, -0x1001, 0x10),
    ("slt", R.X14, R.X31, R.X25, 0x0, 0x1000000, 0x20),
    ("slt", R.X20, R.X14, R.X8,  0x1, 0x5, 0x40),
    ("slt", R.X19, R.X7,  R.X11, 0x1, 0x0, 0x80),
    ("slt", R.X9,  R.X19, R.X29, 0x1, 0x5, 0x100),
    ("slt", R.X6,  R.X3,  R.X23, 0x0, 0x400000, 0x200),
]

SLTU_TESTS = [
    ("sltu", R.X31, R.X0,  R.X31, 0x1, 0x0, 0xfffffffe),
    ("sltu", R.X5,  R.X19, R.X19, 0x0, 0x100000, 0x100000),
    ("sltu", R.X25, R.X25, R.X25, 0x0, 0x40000000, 0x40000000),
    ("sltu", R.X14, R.X14, R.X24, 0x1, 0xfffffffe, 0xffffffff),
    ("sltu", R.X12, R.X17, R.X13, 0x0, 0x1, 0x1),
    ("sltu", R.X24, R.X26, R.X18, 0x1, 0x0, 0xb),
    ("sltu", R.X19, R.X5,  R.X14, 0x0, 0xffffffff, 0x0),
    ("sltu", R.X0,  R.X3,  R.X22, 0, 0x4, 0x2),
    ("sltu", R.X20, R.X23, R.X29, 0x0, 0xf7ffffff, 0x4),
    ("sltu", R.X10, R.X4,  R.X6,  0x0, 0x11, 0x8),
    ("sltu", R.X1,  R.X12, R.X17, 0x0, 0x7fffffff, 0x10),
    ("sltu", R.X6,  R.X30, R.X8,  0x0, 0x2000000, 0x20),
    ("sltu", R.X3,  R.X21, R.X16, 0x0, 0xfffff7ff, 0x40),
    ("sltu", R.X17, R.X29, R.X26, 0x0, 0x400, 0x80),
    ("sltu", R.X28, R.X18, R.X10, 0x1, 0xd, 0x100),
    ("sltu", R.X11, R.X2,  R.X28, 0x1, 0x4, 0x200),
    ("sltu", R.X29, R.X8,  R.X30, 0x0, 0xffffffbf, 0x400),
    ("sltu", R.X7,  R.X22, R.X11, 0x1, 0x80, 0x800),
    ("sltu", R.X9,  R.X15, R.X4,  0x0, 0x200000, 0x1000),
    ("sltu", R.X13, R.X28, R.X12, 0x1, 0x80, 0x2000),
]

XOR_TESTS = [
    ("xor", R.X24, R.X27, R.X24, 0x66666666, 0x66666665, 0x3),
    ("xor", R.X10, R.X13, R.X13, 0x0, 0x5, 0x5),
    ("xor", R.X23, R.X23, R.X23, 0x0, -0x4001, -0x4001),
    ("xor", R.X28, R.X28, R.X14, 0xffffffb7, -0x41, 0x8),
    ("xor", R.X18, R.X1,  R.X2,  0x0, -0x1, -0x1),
    ("xor", R.X19, R.X5,  R.X22, 0x80400000, 0x400000, -0x80000000),
    ("xor", R.X13, R.X26, R.X12, 0xffffffef, -0x11, 0x0),
    ("xor", R.X4,  R.X12, R.X11, 0xd5555555, -0x55555556, 0x7fffffff),
    ("xor", R.X17, R.X19, R.X30, 0x0, 0x1, 0x1),
    ("xor", R.X3,  R.X11, R.X1,  0x6fffffff, -0x80000000, -0x10000001),
    ("xor", R.X8,  R.X24, R.X29, 0xffff4afc, 0x0, -0xb504),
    ("xor", R.X9,  R.X0,  R.X18, 0x1000, 0x0, 0x1000),
    ("xor", R.X26, R.X10, R.X6,  0x80002, 0x80000, 0x2),
    ("xor", R.X30, R.X22, R.X31, 0xffffffdb, -0x21, 0x4),
    ("xor", R.X16, R.X8,  R.X0,  0x6, 0x6, 0x0),
    ("xor", R.X15, R.X16, R.X27, 0x25, 0x5, 0x20),
    ("xor", R.X31, R.X3,  R.X26, 0xffdfffbf, -0x200001, 0x40),
    ("xor", R.X14, R.X9,  R.X25, 0xffff7f7f, -0x8001, 0x80),
    ("xor", R.X6,  R.X30, R.X10, 0x55555456, 0x55555556, 0x100),
    ("xor", R.X7,  R.X2,  R.X9,  0xffffbdff, -0x4001, 0x200),
]

SRL_TESTS = [
    ("srl", R.X11, R.X26, R.X11, 0x1ff7f, -0x400001, 0xf),
    ("srl", R.X12, R.X31, R.X31, 0x155, 0x55555556, 0x55555556),
    ("srl", R.X7,  R.X7,  R.X7,  0x1, -0x1, -0x1),
    ("srl", R.X18, R.X18, R.X12, 0x100, 0x100, 0x0),
    ("srl", R.X8,  R.X14, R.X3,  0x0, 0x9, 0x9),
    ("srl", R.X20, R.X21, R.X22, 0x80000, -0x80000000, 0xc),
    ("srl", R.X30, R.X4,  R.X17, 0x0, 0x0, 0xf),
    ("srl", R.X6,  R.X1,  R.X4,  0x1, 0x7fffffff, 0x1e),
    ("srl", R.X15, R.X0,  R.X21, 0x0, 0x0, 0x1d),
    ("srl", R.X5,  R.X28, R.X23, 0x0, 0x2, 0x6),
    ("srl", R.X4,  R.X9,  R.X30, 0x0, 0x4, 0xa),
    ("srl", R.X10, R.X13, R.X29, 0x2, 0x8, 0x2),
    ("srl", R.X25, R.X2,  R.X16, 0x0, 0x10, 0x7),
    ("srl", R.X19, R.X11, R.X28, 0x0, 0x20, 0x8),
    ("srl", R.X23, R.X10, R.X6,  0x0, 0x40, 0xb),
    ("srl", R.X0,  R.X3,  R.X1,  0, 0x80, 0x6),
    ("srl", R.X14, R.X6,  R.X8,  0x0, 0x200, 0xe),
    ("srl", R.X9,  R.X20, R.X27, 0x0, 0x400, 0x1d),
    ("srl", R.X16, R.X30, R.X18, 0x0, 0x800, 0xd),
    ("srl", R.X24, R.X22, R.X10, 0x10, 0x1000, 0x8),
]

SRA_TESTS = [
    ("sra", R.X27, R.X16, R.X27, -0x800000, -0x80000000, 0x8),
    ("sra", R.X16, R.X12, R.X12, 0x2000000, 0x2000000, 0x2000000),
    ("sra", R.X1,  R.X1,  R.X1,  -0x1, -0x801, -0x801),
    ("sra", R.X13, R.X13, R.X19, 0x33333333, 0x33333333, 0x0),
    ("sra", R.X8,  R.X28, R.X2,  0x0, 0x6, 0x6),
    ("sra", R.X19, R.X26, R.X31, 0x0, 0x0, 0x3),
    ("sra", R.X29, R.X14, R.X28, 0x1fff, 0x7fffffff, 0x12),
    ("sra", R.X12, R.X10, R.X26, 0x0, 0x1, 0x2),
    ("sra", R.X15, R.X30, R.X16, 0x0, 0x2, 0x4),
    ("sra", R.X6,  R.X24, R.X0,  0x4, 0x4, 0x0),
    ("sra", R.X3,  R.X21, R.X15, 0x0, 0x8, 0xa),
    ("sra", R.X10, R.X15, R.X30, 0x10, 0x10, 0x0),
    ("sra", R.X22, R.X18, R.X4,  0x4, 0x20, 0x3),
    ("sra", R.X11, R.X19, R.X17, 0x0, 0x40, 0x17),
    ("sra", R.X0,  R.X5,  R.X14, 0, 0x80, 0x8),
    ("sra", R.X5,  R.X6,  R.X24, 0x10, 0x100, 0x4),
    ("sra", R.X31, R.X7,  R.X18, 0x0, 0x200, 0x1f),
    ("sra", R.X30, R.X31, R.X21, 0x0, 0x400, 0x10),
    ("sra", R.X2,  R.X4,  R.X11, 0x0, 0x800, 0x13),
    ("sra", R.X9,  R.X22, R.X25, 0x400, 0x1000, 0x2),
]

OR_TESTS = [
    ("or", R.X26, R.X8,  R.X26, 0x100010, 0x100000, 0x10),
    ("or", R.X17, R.X6,  R.X6,  0x2, 0x2, 0x2),
    ("or", R.X31, R.X31, R.X31, 0xefffffff, -0x10000001, -0x10000001),
    ("or", R.X27, R.X27, R.X29, 0xfffff7ff, -0x801, 0x400000),
    ("or", R.X18, R.X30, R.X19, 0xffefffff, -0x100001, -0x100001),
    ("or", R.X9,  R.X21, R.X14, 0x80020000, 0x20000, -0x80000000),
    ("or", R.X4,  R.X26, R.X24, 0xffffdfff, -0x2001, 0x0),
    ("or", R.X30, R.X9,  R.X8,  0x7fffffff, 0x0, 0x7fffffff),
    ("or", R.X8,  R.X23, R.X7,  0xff7fffff, -0x800001, 0x1),
    ("or", R.X22, R.X12, R.X0,  0x80000000, -0x80000000, 0x0),
    ("or", R.X28, R.X10, R.X30, 0x7fffffff, 0x7fffffff, 0x40),
    ("or", R.X16, R.X18, R.X21, 0x55555555, 0x1, 0x55555554),
    ("or", R.X12, R.X14, R.X17, 0x1002, 0x1000, 0x2),
    ("or", R.X15, R.X19, R.X16, 0xff7fffff, -0x800001, 0x4),
    ("or", R.X7,  R.X4,  R.X2,  0xfffffbff, -0x401, 0x8),
    ("or", R.X11, R.X2,  R.X22, 0x7fffffff, 0x7fffffff, 0x20),
    ("or", R.X25, R.X28, R.X15, 0xfffffdff, -0x201, 0x80),
    ("or", R.X6,  R.X25, R.X1,  0xb504, 0xb504, 0x100),
    ("or", R.X20, R.X17, R.X10, 0x204, 0x4, 0x200),
    ("or", R.X5,  R.X20, R.X23, 0xffefffff, -0x100001, 0x400),
]

AND_TESTS = [
    ("and", R.X25, R.X24, R.X25, 0x0, 0x4000, 0x7),
    ("and", R.X18, R.X3,  R.X3,  0x800, 0x800, 0x800),
    ("and", R.X19, R.X19, R.X19, 0xfffffffd, -0x3, -0x3),
    ("and", R.X5,  R.X5,  R.X14, 0x7fffffff, -0x1, 0x7fffffff),
    ("and", R.X20, R.X23, R.X16, 0x5, 0x5, 0x5),
    ("and", R.X30, R.X20, R.X2,  0x0, 0x2, -0x80000000),
    ("and", R.X13, R.X7,  R.X24, 0x0, 0x33333333, 0x0),
    ("and", R.X10, R.X30, R.X27, 0x1, -0x40000001, 0x1),
    ("and", R.X22, R.X28, R.X18, 0x0, -0x80000000, 0x800),
    ("and", R.X0,  R.X2,  R.X15, 0, 0x0, 0x200),
    ("and", R.X12, R.X25, R.X26, 0x55555555, 0x7fffffff, 0x55555555),
    ("and", R.X2,  R.X1,  R.X31, 0x0, 0x1, 0x55555554),
    ("and", R.X14, R.X27, R.X11, 0x0, 0x40000, 0x2),
    ("and", R.X4,  R.X31, R.X23, 0x4, -0x20001, 0x4),
    ("and", R.X27, R.X21, R.X9,  0x8, -0x55555555, 0x8),
    ("and", R.X23, R.X26, R.X7,  0x0, 0x400, 0x10),
    ("and", R.X24, R.X9,  R.X20, 0x20, -0x8, 0x20),
    ("and", R.X26, R.X15, R.X13, 0x40, -0x101, 0x40),
    ("and", R.X17, R.X12, R.X4,  0x80, -0x2000001, 0x80),
    ("and", R.X8,  R.X4,  R.X17, 0x0, 0x66666665, 0x100),
]

# # addi
# err += test_imm(m, 'addi', x7,  x20, 0x1ffff800, 0x20000000, -0x800)
# err += test_imm(m, 'addi', x3,  x3,  0x400, 0x400, 0x0)
# err += test_imm(m, 'addi', x22, x4,  0x5fe, -0x201, 0x7ff)
# err += test_imm(m, 'addi', x11, x30, 0x1, 0x0, 0x1)
# err += test_imm(m, 'addi', x31, x27, 0x80000010, -0x80000000, 0x10)
# err += test_imm(m, 'addi', x30, x17, 0x80000005, 0x7fffffff, 0x6)
# err += test_imm(m, 'addi', x28, x18, 0x5, 0x1, 0x4)
# err += test_imm(m, 'addi', x6,  x13, 0xa, 0x5, 0x5)
# err += test_imm(m, 'addi', x16, x10, 0xaaaaaa8a, -0x55555555, -0x21)
# err += test_imm(m, 'addi', x21, x9,  0xfffffff1, -0x11, 0x2)
# err += test_imm(m, 'addi', x2,  x7,  0xb50d, 0xb505, 0x8)
# err += test_imm(m, 'addi', x18, x22, 0xffff4b1c, -0xb504, 0x20)
# err += test_imm(m, 'addi', x0,  x29, 0, -0x200001, 0x40)
# err += test_imm(m, 'addi', x13, x25, 0x85, 0x5, 0x80)
# err += test_imm(m, 'addi', x29, x11, 0xfe0000ff, -0x2000001, 0x100)
# err += test_imm(m, 'addi', x8,  x6,  0x210, 0x10, 0x200)
# err += test_imm(m, 'addi', x4,  x19, 0x402, 0x2, 0x400)
# err += test_imm(m, 'addi', x10, x12, 0x55555552, 0x55555554, -0x2)
# err += test_imm(m, 'addi', x26, x31, 0x55555552, 0x55555555, -0x3)
# err += test_imm(m, 'addi', x15, x26, 0x5555554f, 0x55555554, -0x5]

# # slti
# err += test_imm(m, 'slti', x12, x25, 0x0, -0x81, -0x800)
# err += test_imm(m, 'slti', x5,  x5,  0x1, -0x1001, 0x0)
# err += test_imm(m, 'slti', x28, x4,  0x1, -0x40000000, 0x7ff)
# err += test_imm(m, 'slti', x15, x31, 0x1, -0x11, 0x1)
# err += test_imm(m, 'slti', x13, x1,  0x1, -0x80000000, 0x3)
# err += test_imm(m, 'slti', x1,  x15, 0x1, 0x0, 0x2)
# err += test_imm(m, 'slti', x9,  x16, 0x0, 0x7fffffff, -0x8)
# err += test_imm(m, 'slti', x31, x11, 0x0, 0x1, -0x400)
# err += test_imm(m, 'slti', x27, x14, 0x0, 0x10, 0x10)
# err += test_imm(m, 'slti', x26, x12, 0x0, 0x33333334, 0x4)
# err += test_imm(m, 'slti', x4,  x17, 0x0, 0x3fffffff, 0x8)
# err += test_imm(m, 'slti', x10, x18, 0x1, -0x2001, 0x20)
# err += test_imm(m, 'slti', x21, x27, 0x1, 0x3, 0x40)
# err += test_imm(m, 'slti', x8,  x3,  0x0, 0x55555554, 0x80)
# err += test_imm(m, 'slti', x0,  x7,  0, 0x55555554, 0x100)
# err += test_imm(m, 'slti', x24, x22, 0x1, -0x55555556, 0x200)
# err += test_imm(m, 'slti', x18, x24, 0x0, 0x4000, 0x400)
# err += test_imm(m, 'slti', x25, x6,  0x1, -0x401, -0x2)
# err += test_imm(m, 'slti', x23, x21, 0x0, 0x66666667, -0x3)
# err += test_imm(m, 'slti', x7,  x0,  0x0, 0x0, -0x5]

# # sltiu
# err += test_imm(m, 'sltiu', x28, x23, 0x0, 0x400, 0x0)
# err += test_imm(m, 'sltiu', x2,  x2,  0x1, 0x800, 0xfff)
# err += test_imm(m, 'sltiu', x25, x3,  0x0, 0x4, 0x1)
# err += test_imm(m, 'sltiu', x11, x19, 0x1, 0x0, 0x6)
# err += test_imm(m, 'sltiu', x15, x14, 0x0, 0xffffffff, 0x2c)
# err += test_imm(m, 'sltiu', x4,  x13, 0x0, 0x1, 0x0)
# err += test_imm(m, 'sltiu', x3,  x26, 0x0, 0xd, 0xd)
# err += test_imm(m, 'sltiu', x29, x20, 0x0, 0xaaaaaaaa, 0x2)
# err += test_imm(m, 'sltiu', x16, x27, 0x0, 0x7fffffff, 0x4)
# err += test_imm(m, 'sltiu', x20, x17, 0x0, 0xfeffffff, 0x8)
# err += test_imm(m, 'sltiu', x8,  x31, 0x0, 0x800, 0x10)
# err += test_imm(m, 'sltiu', x23, x24, 0x1, 0xc, 0x20)
# err += test_imm(m, 'sltiu', x26, x25, 0x0, 0x55555555, 0x40)
# err += test_imm(m, 'sltiu', x6,  x22, 0x0, 0x80000, 0x80)
# err += test_imm(m, 'sltiu', x5,  x12, 0x0, 0xfffffff7, 0x100)
# err += test_imm(m, 'sltiu', x1,  x9,  0x0, 0x80000000, 0x200)
# err += test_imm(m, 'sltiu', x10, x28, 0x0, 0xfffbffff, 0x400)
# err += test_imm(m, 'sltiu', x31, x21, 0x1, 0x0, 0x800)
# err += test_imm(m, 'sltiu', x21, x0,  0x1, 0x0, 0xffe)
# err += test_imm(m, 'sltiu', x14, x11, 0x1, 0x12, 0xffd]

# # xori
# err += test_imm(m, 'xori', x10, x24, 0xcccccb34, 0x33333334, -0x800)
# err += test_imm(m, 'xori', x18, x18, 0x4, 0x4, 0x0)
# err += test_imm(m, 'xori', x24, x15, 0xfffff803, -0x4, 0x7ff)
# err += test_imm(m, 'xori', x20, x11, 0x3, 0x2, 0x1)
# err += test_imm(m, 'xori', x21, x7,  0x80000554, -0x80000000, 0x554)
# err += test_imm(m, 'xori', x27, x17, 0xfffffbff, 0x0, -0x401)
# err += test_imm(m, 'xori', x1,  x22, 0x80000009, 0x7fffffff, -0xa)
# err += test_imm(m, 'xori', x22, x20, 0x5, 0x1, 0x4)
# err += test_imm(m, 'xori', x31, x19, 0x0, -0x201, -0x201)
# err += test_imm(m, 'xori', x5,  x9,  0xffffffdd, -0x21, 0x2)
# err += test_imm(m, 'xori', x29, x28, 0x80000008, -0x80000000, 0x8)
# err += test_imm(m, 'xori', x4,  x30, 0xbfffffef, -0x40000001, 0x10)
# err += test_imm(m, 'xori', x8,  x27, 0x7fffffdf, 0x7fffffff, 0x20)
# err += test_imm(m, 'xori', x25, x3,  0x66666626, 0x66666666, 0x40)
# err += test_imm(m, 'xori', x17, x31, 0xfff7ff7f, -0x80001, 0x80)
# err += test_imm(m, 'xori', x16, x29, 0xffff4bfc, -0xb504, 0x100)
# err += test_imm(m, 'xori', x6,  x4,  0x200, 0x0, 0x200)
# err += test_imm(m, 'xori', x3,  x14, 0xffeffbff, -0x100001, 0x400)
# err += test_imm(m, 'xori', x15, x12, 0x7, -0x7, -0x2)
# err += test_imm(m, 'xori', x9,  x21, 0xfffffff8, 0x5, -0x3]

# # ori
# err += test_imm(m, 'ori', x22, x5,  0xfffffdff, -0x201, -0x800)
# err += test_imm(m, 'ori', x27, x27, 0x0, 0x0, 0x0)
# err += test_imm(m, 'ori', x8,  x17, 0x333337ff, 0x33333334, 0x7ff)
# err += test_imm(m, 'ori', x1,  x20, 0xffff4afd, -0xb504, 0x1)
# err += test_imm(m, 'ori', x19, x12, 0x8000002d, -0x80000000, 0x2d)
# err += test_imm(m, 'ori', x3,  x8,  0x7fffffff, 0x7fffffff, 0x555)
# err += test_imm(m, 'ori', x26, x28, 0x667, 0x1, 0x667)
# err += test_imm(m, 'ori', x23, x16, 0xffffffff, 0x7, -0x7)
# err += test_imm(m, 'ori', x31, x25, 0x40002, 0x40000, 0x2)
# err += test_imm(m, 'ori', x11, x23, 0x20000004, 0x20000000, 0x4)
# err += test_imm(m, 'ori', x17, x14, 0xfffffdff, -0x201, 0x8)
# err += test_imm(m, 'ori', x7,  x31, 0x12, 0x2, 0x10)
# err += test_imm(m, 'ori', x4,  x21, 0x8020, 0x8000, 0x20)
# err += test_imm(m, 'ori', x5,  x15, 0x840, 0x800, 0x40)
# err += test_imm(m, 'ori', x25, x30, 0xfffbffff, -0x40001, 0x80)
# err += test_imm(m, 'ori', x30, x11, 0xfffffffb, -0x5, 0x100)
# err += test_imm(m, 'ori', x10, x4,  0xfff7ffff, -0x80001, 0x200)
# err += test_imm(m, 'ori', x0,  x13, 0, -0x40000001, 0x400)
# err += test_imm(m, 'ori', x6,  x26, 0xffffffff, -0x21, -0x2)
# err += test_imm(m, 'ori', x18, x19, 0xffffffff, 0xb503, -0x3]

# # andi
# err += test_imm(m, 'andi', x10, x22, 0xfffff800, -0x2, -0x800)
# err += test_imm(m, 'andi', x25, x25, 0x0, -0x1001, 0x0)
# err += test_imm(m, 'andi', x17, x16, 0x7ff, -0x2000001, 0x7ff)
# err += test_imm(m, 'andi', x8,  x2,  0x1, -0x20001, 0x1)
# err += test_imm(m, 'andi', x30, x28, 0x0, -0x80000000, 0x4)
# err += test_imm(m, 'andi', x19, x4,  0x0, 0x0, -0x800)
# err += test_imm(m, 'andi', x2,  x10, 0x6, 0x7fffffff, 0x6)
# err += test_imm(m, 'andi', x13, x7,  0x0, 0x1, 0x554)
# err += test_imm(m, 'andi', x9,  x27, 0x80, 0x80, 0x80)
# err += test_imm(m, 'andi', x3,  x17, 0x7fffffd4, 0x7fffffff, -0x2c)
# err += test_imm(m, 'andi', x26, x0,  0x0, 0x0, 0x2)
# err += test_imm(m, 'andi', x21, x23, 0x0, 0x66666666, 0x8)
# err += test_imm(m, 'andi', x14, x6,  0x0, 0x0, 0x10)
# err += test_imm(m, 'andi', x22, x5,  0x0, 0x100, 0x20)
# err += test_imm(m, 'andi', x29, x8,  0x40, -0x5, 0x40)
# err += test_imm(m, 'andi', x23, x12, 0x0, 0x1, 0x100)
# err += test_imm(m, 'andi', x6,  x15, 0x200, -0x55555555, 0x200)
# err += test_imm(m, 'andi', x11, x29, 0x0, 0x0, 0x400)
# err += test_imm(m, 'andi', x1,  x20, 0x66666666, 0x66666667, -0x2)
# err += test_imm(m, 'andi', x5,  x31, 0xffeffffd, -0x100001, -0x3]

# # slli
# err += test_imm(m, 'slli', x27, x17, 0xe0000000, -0x40000001, 0x1d)
# err += test_imm(m, 'slli', x26, x26, 0x33330000, 0x66666666, 0xf)
# err += test_imm(m, 'slli', x11, x22, 0xfffeffff, -0x10001, 0x0)
# err += test_imm(m, 'slli', x6,  x15, 0x4, 0x4, 0x0)
# err += test_imm(m, 'slli', x16, x9,  0x80000000, -0x400001, 0x1f)
# err += test_imm(m, 'slli', x20, x11, 0x0, 0x4, 0x1f)
# err += test_imm(m, 'slli', x19, x1,  0x800, 0x8, 0x8)
# err += test_imm(m, 'slli', x25, x19, 0x0, -0x80000000, 0x10)
# err += test_imm(m, 'slli', x12, x8,  0x0, 0x0, 0xc)
# err += test_imm(m, 'slli', x30, x27, 0xffffff00, 0x7fffffff, 0x8)
# err += test_imm(m, 'slli', x4,  x2,  0x2, 0x1, 0x1)
# err += test_imm(m, 'slli', x14, x31, 0x80, 0x2, 0x6)
# err += test_imm(m, 'slli', x17, x24, 0x40000, 0x10, 0xe)
# err += test_imm(m, 'slli', x10, x4,  0x100, 0x20, 0x3)
# err += test_imm(m, 'slli', x2,  x18, 0x8000000, 0x40, 0x15)
# err += test_imm(m, 'slli', x23, x5,  0x10000000, 0x80, 0x15)
# err += test_imm(m, 'slli', x8,  x13, 0x200, 0x100, 0x1)
# err += test_imm(m, 'slli', x0,  x20, 0, 0x200, 0x0)
# err += test_imm(m, 'slli', x9,  x16, 0x1000, 0x400, 0x2)
# err += test_imm(m, 'slli', x5,  x21, 0x40000000, 0x800, 0x13]

# # srli
# err += test_imm(m, 'srli', x8,  x30, 0x3fffd2bf, -0xb504, 0x2)
# err += test_imm(m, 'srli', x17, x17, 0x0, 0x7, 0x13)
# err += test_imm(m, 'srli', x19, x27, 0xffff4afc, -0xb504, 0x0)
# err += test_imm(m, 'srli', x9,  x29, 0x3fffffff, 0x3fffffff, 0x0)
# err += test_imm(m, 'srli', x22, x25, 0x1, -0xa, 0x1f)
# err += test_imm(m, 'srli', x13, x1,  0x0, 0x200, 0x1f)
# err += test_imm(m, 'srli', x0,  x21, 0, 0x3, 0x3)
# err += test_imm(m, 'srli', x29, x0,  0x0, 0x0, 0x9)
# err += test_imm(m, 'srli', x18, x16, 0x0, 0x0, 0x1)
# err += test_imm(m, 'srli', x27, x20, 0x3fff, 0x7fffffff, 0x11)
# err += test_imm(m, 'srli', x2,  x31, 0x0, 0x1, 0x12)
# err += test_imm(m, 'srli', x31, x7,  0x0, 0x2, 0x1d)
# err += test_imm(m, 'srli', x16, x14, 0x0, 0x4, 0xf)
# err += test_imm(m, 'srli', x25, x12, 0x0, 0x8, 0x1b)
# err += test_imm(m, 'srli', x11, x4,  0x0, 0x10, 0xf)
# err += test_imm(m, 'srli', x23, x24, 0x0, 0x20, 0x17)
# err += test_imm(m, 'srli', x28, x8,  0x0, 0x40, 0xd)
# err += test_imm(m, 'srli', x30, x15, 0x0, 0x80, 0x1e)
# err += test_imm(m, 'srli', x20, x18, 0x0, 0x100, 0x1f)
# err += test_imm(m, 'srli', x14, x13, 0x0, 0x400, 0x12]

# # srai
# err += test_imm(m, 'srai', x25, x31, -0x1, -0x9, 0x9)
# err += test_imm(m, 'srai', x10, x10, 0x2, 0x5, 0x1)
# err += test_imm(m, 'srai', x28, x8,  -0x1000001, -0x1000001, 0x0)
# err += test_imm(m, 'srai', x5,  x17, 0x100000, 0x100000, 0x0)
# err += test_imm(m, 'srai', x27, x23, -0x1, -0x20001, 0x1f)
# err += test_imm(m, 'srai', x20, x13, 0x0, 0x1, 0x1f)
# err += test_imm(m, 'srai', x11, x22, 0x0, 0x4, 0x4)
# err += test_imm(m, 'srai', x30, x7,  -0x80000000, -0x80000000, 0x0)
# err += test_imm(m, 'srai', x14, x18, 0x0, 0x0, 0xe)
# err += test_imm(m, 'srai', x19, x3,  0x0, 0x7fffffff, 0x1f)
# err += test_imm(m, 'srai', x29, x25, 0x0, 0x2, 0x11)
# err += test_imm(m, 'srai', x3,  x30, 0x0, 0x8, 0x11)
# err += test_imm(m, 'srai', x22, x2,  0x0, 0x10, 0x12)
# err += test_imm(m, 'srai', x2,  x12, 0x0, 0x20, 0xd)
# err += test_imm(m, 'srai', x12, x1,  0x0, 0x40, 0x17)
# err += test_imm(m, 'srai', x24, x20, 0x0, 0x80, 0x9)
# err += test_imm(m, 'srai', x0,  x11, 0, 0x100, 0x10)
# err += test_imm(m, 'srai', x8,  x26, 0x1, 0x200, 0x9)
# err += test_imm(m, 'srai', x17, x9,  0x0, 0x400, 0x11)
# err += test_imm(m, 'srai', x23, x16, 0x0, 0x800, 0x1b)
