import argparse

from pyriscv import mem, rv32i, utils


def pyriscv():
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_filepath", type=str, help="Path to program binary")

    args = parser.parse_args()
    bin_filepath = args.bin_filepath

    rv = rv32i.RV32I(mem.RiscofMemory())
    rv.load_bin(bin_filepath)

    rv.run_program()


def riscof() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_filepath", type=str, help="Path to program binary")

    parser.add_argument("--test-signature", type=str, help="Path to output test signature")

    args = parser.parse_args()
    bin_filepath, test_signature_path = args.bin_filepath, args.test_signature

    rv = rv32i.RV32I(mem.RiscofMemory())
    rv.load_bin(bin_filepath)

    rv.run_program()

    test_sig_start = utils.to_uint32(rv.regs[rv32i.Regs.X10])
    test_sig_end = utils.to_uint32(rv.regs[rv32i.Regs.X11])

    test_sig_words = [rv.memory.ram.read(addr, mem.DataSize.WORD) for addr in range(test_sig_start, test_sig_end, 4)]

    file_lines = [f"{word:08x}\n" for word in test_sig_words]
    with open(test_signature_path, "w") as f:
        f.writelines(file_lines)
