import logging
import pathlib

import riscof.utils as utils
from riscof.pluginTemplate import pluginTemplate

logger = logging.getLogger()


class pyriscv(pluginTemplate):
    __model__ = "pyriscv"

    __version__ = "0.1.0"

    def __init__(self, *args, config: dict, **kwargs):
        super().__init__(*args, **kwargs)

        self.dut_exe = pathlib.Path(config.get("PATH", "")) / "pyriscv-riscof"
        self.num_jobs = str(config.get("jobs", 1))  # Number of jobs for make
        self.pluginpath = pathlib.Path(config["pluginpath"]).resolve()
        self.isa_spec = pathlib.Path(config["ispec"]).resolve()
        self.platform_spec = pathlib.Path(config["pspec"]).resolve()

        if "target_run" in config and config["target_run"] == "0":
            # To only compile tests, not run on target
            self.target_run = False
        else:
            self.target_run = True

    def initialise(self, suite: str, workdir: str, env: str):
        # Working directory to store artifacts from DUT, framework and reference plugin
        self.work_dir = workdir

        # Architectural test-suite directory
        self.suite_dir = suite

        linker_path = self.pluginpath / "env" / "link.ld"
        include_path = self.pluginpath / "env"

        self.compile_args = [
            "-static",
            "-mcmodel=medany",
            "-fvisibility=hidden",
            "-nostdlib",
            "-nostartfiles",
            "-g",
            f"-T {linker_path}",
            f"-I {include_path}",
            f"-I {env}",
        ]

    def build(self, isa_yaml: str, platform_yaml: str):
        ispec = utils.load_yaml(isa_yaml)["hart0"]

        # Capture the XLEN value by picking the max value in 'supported_xlen' field of isa yaml
        self.xlen = "64" if 64 in ispec["supported_xlen"] else "32"

        self.compile_cmd = f"riscv{self.xlen}-unknown-elf-gcc"

        abi = "lp64" if 64 in ispec["supported_xlen"] else "ilp32"
        self.compile_args.append(f"-mabi={abi}")

    def runTests(self, testlist: dict):
        makefile_path = pathlib.Path(self.work_dir) / f"Makefile.{self.name[:-1]}"
        if makefile_path.exists():
            makefile_path.unlink()

        make = utils.makeUtil(
            makeCommand=f"make -k -j{self.num_jobs}",
            makefilePath=str(makefile_path),
        )

        for testname, testentry in testlist.items():
            test = testentry["test_path"]

            test_dir = pathlib.Path(testentry["work_dir"])

            elf_file = "test.elf"
            bin_file = "test.bin"

            # RISCOF expects the signature to be named as DUT-<dut-name>.signature
            sig_file = test_dir / f"{self.name[:-1]}.signature"

            compile_args = self.compile_args.copy()
            compile_args.extend(
                [
                    *[f"-D{macro}" for macro in testentry["macros"]],
                    f"-march={testentry['isa'].lower()}",
                    f"-o {elf_file}",
                    test,
                ]
            )

            compile_cmd = " ".join([self.compile_cmd] + compile_args)
            copy_cmd = f"riscv{self.xlen}-unknown-elf-objcopy --strip-all -O binary {elf_file} {bin_file}"

            if self.target_run:
                simcmd = f"{self.dut_exe} {bin_file} --test-signature={sig_file}"
            else:
                simcmd = 'echo "NO RUN"'

            execute = (
                f"@cd {testentry['work_dir']}; {compile_cmd}; {copy_cmd}; {simcmd};"
            )
            make.add_target(execute)

        make.execute_all(self.work_dir)

        # if target runs are not required then we simply exit as this point after running all
        # the makefile targets.
        if not self.target_run:
            raise SystemExit(0)
