import subprocess
import platform
from pathlib import Path
import sys

WIN = platform.system() == "Windows"
LINUX = platform.system() == "Linux"

COV_THRESHOLD = 57 if WIN else 58
PYTEST_SKIPS = [
    "decorator_skip",
    "pprint_heap_allocated",
]
UNLINK = [
    # https://github.com/conda-forge/ipython-feedstock/pull/231
    "test_zzz_autoreload.py",
]

if LINUX:
    PYTEST_SKIPS += ["system_interrupt"]

PYTEST_ARGS = ["pytest", "-vv", "--color=yes", "--tb=long"]

if len(PYTEST_SKIPS) == 1:
    PYTEST_ARGS += ["-k", f"not {PYTEST_SKIPS[0]}"]
elif PYTEST_SKIPS:
    PYTEST_ARGS += ["-k", f"""not ({" or ".join(PYTEST_SKIPS)})"""]

COV = [sys.executable, "-m", "coverage"]
COV_RUN = [*COV, "run", "--source", "IPython", "--branch", "-m", *PYTEST_ARGS]
COV_REPORT = [
    *COV,
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_THRESHOLD}",
]


def do(args: list[str]) -> int:
    print(">>>", *args, flush=True)
    return subprocess.call(args)


def main() -> int:
    print("Testing on Windows?      ", WIN)
    print("Testing on Linux?        ", LINUX)
    for stem in UNLINK:
        path = (Path("tests") / stem).unlink()
        print("... removing", path)

    return any(map(do, [COV_RUN, COV_REPORT]))


if __name__ == "__main__":
    sys.exit(main())
