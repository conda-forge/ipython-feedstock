import subprocess
import platform
import os
import sys

WIN = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
PYPY = "__pypy__" in sys.builtin_module_names
PPC = "ppc" in platform.machine()

COV_THRESHOLD = "100"

# Environment variable should be set in the meta.yaml
MIGRATING = eval(os.environ.get("MIGRATING", "None"))

PYTEST_SKIPS = []

if WIN:
    pass
else:
    pass

if LINUX:
    pass

if PPC:
    pass

PYTEST_ARGS = [sys.executable, "pytest", "--pyargs", "ipython", "-vv"]

if PYPY:
    pass
else:
    PYTEST_ARGS += [
        "--cov", "ipython", "--no-cov-on-fail", "--cov-fail-under", COV_THRESHOLD,
        "--cov-report", "term-missing:skip-covered"
    ]

if len(PYTEST_SKIPS) == 1:
    PYTEST_ARGS += ["-k", f"not {PYTEST_SKIPS}"]
elif PYTEST_SKIPS:
    PYTEST_ARGS += ["-k", f"""not ({" or ".join(PYTEST_SKIPS) })"""]

if __name__ == "__main__":
    print("Building on Windows?", WIN)
    print("Building on Linux?", LINUX)
    print("Building for PyPy?", PYPY)
    print("Is this a migration?", MIGRATING)

    if MIGRATING:
        print("This is a migration, skipping test suite! Put it back later!", flush=True)
    else:
        sys.exit(subprocess.call(PYTEST_ARGS))
