import subprocess
import platform
import os
import sys

WIN = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
PYPY = "__pypy__" in sys.builtin_module_names
PPC = "ppc" in platform.machine()

COV_THRESHOLD = "0"

# Environment variable should be set in the meta.yaml
MIGRATING = eval(os.environ.get("MIGRATING", "None"))

PYTEST_SKIPS = []

if WIN:
    pass
else:
    pass

if LINUX:
    COV_THRESHOLD = "73"
    PYTEST_SKIPS += ["system_interrupt"]

if PPC:
    pass

PYTEST_ARGS = [sys.executable, "-m", "pytest", "--pyargs", "IPython", "-vv"]

if PYPY:
    pass
else:
    PYTEST_ARGS += [
        "--cov", "IPython", "--no-cov-on-fail", "--cov-fail-under", COV_THRESHOLD,
        "--cov-report", "term-missing:skip-covered"
    ]

if len(PYTEST_SKIPS) == 1:
    PYTEST_ARGS += ["-k", f"not {PYTEST_SKIPS[0]}"]
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
        env = dict(os.environ)
        env["IPYTHON_TESTING_TIMEOUT_SCALE"] = "10"
        sys.exit(subprocess.call(PYTEST_ARGS, env=env))
