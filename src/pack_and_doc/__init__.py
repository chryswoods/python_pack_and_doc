"""
.. currentmodule:: pack_and_doc

Classes
=======

.. autosummary::
    :toctree: generated/

    ExampleClass

Functions
=========

.. autosummary::
    :toctree: generated/

    example_function

"""

from ._exampleclass import *
from ._examplefunction import *

from . import submodule

import sys as _sys

if _sys.version_info < (3, 7):
    print("pack_and_doc requires Python version 3.7 or above.")
    print("Your python is version")
    print(_sys.version)
    _sys.exit(-1)

from ._version import get_versions as _get_versions

_v = _get_versions()
__version__ = _v['version']
