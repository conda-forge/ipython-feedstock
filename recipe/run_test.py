import subprocess
import platform
import os
import sys

WIN = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
PYPY = "__pypy__" in sys.builtin_module_names

# TODO: remove when all test dependencies are available on pypy37 for Windows
MIGRATING = WIN and PYPY

# this is generally failing, for whatever reason
NOSE_EXCLUDE = ["recursion"]

if WIN:
    NOSE_EXCLUDE += ["home_dir_3", "home_dir_5", "store_restore", "storemagic"]
else:
    NOSE_EXCLUDE += ["history"]

if LINUX:
    # https://github.com/ipython/ipython/issues/12164
    NOSE_EXCLUDE += ["system_interrupt"]

IPTEST_ARGS = []

if PYPY:
    # TODO: figure out a better way to skip doctests, so the 500+ `core` tests
    #       that _do_ work are executed
    IPTEST_ARGS = [
        "autoreload",
        "extensions",
        "lib",
        "terminal",
        "testing",
        "utils",
    ]
    NOSE_EXCLUDE += [
        "audio",
        "check_complete",
        "memory_error",
        "obj_del",
        "reset_del",
        "tclass",
        "ultratb",
        "xdel",
        "longer"
    ]

if __name__ == "__main__":
    print("Building on Windows?", WIN)
    print("Building on Linux?", LINUX)
    print("Building for PyPy?", PYPY)
    print("Is this a migration?", MIGRATING)

    if MIGRATING:
        print("This is a migration, skipping test suite! Put it back later!", flush=True)
    else:
        env = dict(os.environ)
        env["NOSE_EXCLUDE"] = "|".join(sorted(NOSE_EXCLUDE))
        print("NOSE_EXCLUDE is {NOSE_EXCLUDE}".format(**env), flush=True)
        print("ipytest3 args", *IPTEST_ARGS, flush=True)
        sys.exit(subprocess.call(["iptest3", *IPTEST_ARGS], env=env))
