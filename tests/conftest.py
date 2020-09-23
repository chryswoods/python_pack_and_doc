
import pytest

# ensure that the cython build directory is first in the path.
# This makes sure that we test against the local code and not
# the installed pack_and_doc code

import glob
import sys
import os

script_dir = os.path.dirname(__file__)
build_dir = os.path.join(script_dir, "..", "build")

build_paths = glob.glob(f"{build_dir}/*/pack_and_doc")

for path in build_paths:
    dir, name = os.path.split(path)
    sys.path.insert(0, dir)

print(f"PYTHONPATH = {sys.path}")


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )

    parser.addoption(
        "--runveryslow", action="store_true", default=False,
        help="run very slow (integration) tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers",
                            "veryslow: mark test as very slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runveryslow"):
        # --runveryslow given in cli: do not skip any slow or veryslow test
        return
    elif config.getoption("--runslow"):
        # --runslow given in cli: skip veryslow tests
        skip_veryslow = pytest.mark.skip(
            reason="need --runveryslow option to run")

        for item in items:
            if "veryslow" in item.keywords:
                item.add_marker(skip_veryslow)
    else:
        # skip slow and veryslow tests
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        skip_veryslow = pytest.mark.skip(
            reason="need --runveryslow option to run")

        for item in items:
            if "veryslow" in item.keywords:
                item.add_marker(skip_veryslow)
            elif "slow" in item.keywords:
                item.add_marker(skip_slow)
