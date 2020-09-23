
import pytest

from pack_and_doc.submodule import FastClass


def test_fast_class():
    c = FastClass()
    c.func()


if __name__ == "__main__":
    test_fast_class()
