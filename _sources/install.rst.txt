=========================
Installation instructions
=========================

This is the installation guide. Because you are packaging using pip
then installation should be simple. Ideally potential new users
of your package should be able to get it installed and working
in less than 5 minutes without needing admin privileges of their computer.

Installation via Python
=======================

Pack and Doc is compiled and
`tested on Windows, Linux and OS X <https://github.com/chryswoods/python_pack_and_doc/actions>`__,
but should be able to compile and install on any operating system
with a working Python >= 3.7 and a C compiler.

To install Pack and Doc, you first need to install Python >= 3.7. To check
if you have Python 3.7 installed type;

.. code-block:: bash

    python -V

This should print out the version number of the Python you have available.
If the version number is ``2.???`` then you have a very old Python 2. If
this is the case, try;

.. code-block:: bash

    python3 -V

and see if you have a Python 3 that has a version number >= 3.7. If so,
please use ``python3`` instead of ``python``.

If you don't have Python >=3.7 installed, then you can install Python
either via your package manager, or more simply, by using
`anaconda <https://anaconda.org>`__.

Once you have a working Python >= 3.7, the easiest way to install
Pack and Doc is using
`pip <https://pip.pypa.io/en/stable/>`__.

.. code-block:: bash

    pip install pack_and_doc

(if this doesn't work, then you may need to use the command ``pip3``,
or you may have to `install pip <https://pip.pypa.io/en/stable/installing/>`__.
If you have trouble installing pip then we recommend that you download
and install `anaconda <https://anaconda.org>`__, which has pip included)

To install a specific version, e.g. 1.4.0, type

.. code-block:: bash

    pip install pack_and_doc==1.4.0

This will install a binary version of pack_and_doc if it is avaiable for your
operating system / processor / version of python. If not, then
the pack_and_doc pyx code that was compiled into C using
`cython <https://cython.org>`__,
will be compiled into an executable using your system C compiler
(e.g. `gcc <https://gcc.gnu.org>`__ or `clang <https://clang.llvm.org>`__).
You can control which C compiler to use by setting the ``CC`` environment
variable, e.g.

.. code-block:: bash

    CC=gcc pip install pack_and_doc

Pack and Doc is written in standard C, using
`OpenMP <https://www.openmp.org>`__ for parallelisation,
and it has no external dependencies, so
it should compile without issue. Note that the system C compiler on
OS X (Mac) does not support OpenMP. In this case you the code will
compile with OpenMP disabled. If you want to use all of the cores
of your computer than you will need to install
a different compiler, e.g. installing clang via
`homebrew <https://brew.sh>`__. If you have any problems then please
`post an issue on GitHub <https://github.com/chryswoods/python_pack_and_doc/issues>`__.

Source install
==============

You can download a source release of Pack and Doc from the
`project release page <https://github.com/chryswoods/python_pack_and_doc/releases>`__.

Once you have downloaded the file you can unpack it and change into
that directory using;

.. code-block:: bash

   tar -zxvf PythonPackAndDoc-X.Y.Z.tar.gz
   cd PythonPackAndDoc-X.Y.Z

where ``X.Y.Z`` is the version you downloaded. For the 1.4.0 release
this would be;

.. code-block:: bash

    tar -zxvf PythonPackAndDoc-1.4.0.tar.gz
    cd PythonPackAndDoc-1.4.0

Next you need to install the dependencies of Pack and Doc. Do this by typing;

.. code-block:: bash

    pip install -r requirements.txt
    pip install -r requirements-dev.txt

Now you are ready to compile and install Pack and Doc itself;

.. code-block:: bash

    make
    make install

You can choose the C compiler to use by setting the ``CC`` environment
variable, e.g.

.. code-block:: bash

    CC=clang make
    CC=clang make install

Pack and Doc is written in standard C, using
`OpenMP <https://www.openmp.org>`__ for parallelisation,
and it has no external dependencies, so
it should compile without issue. Note that the system C compiler on
OS X (Mac) does not support OpenMP. In this case you the code will
compile with OpenMP disabled. If you want to use all of the cores
of your computer than you will need to install
a different compiler, e.g. installing clang via
`homebrew <https://brew.sh>`__. If you have any problems then please
`post an issue on GitHub <https://github.com//chryswoods/python_pack_and_doc/issues>`__.

For developers
==============

You can clone the Pack and Doc repository to your computer and install from
there;

.. code-block:: bash

    git clone https://github.com/chryswoods/python_pack_and_doc
    cd python_pack_and_doc
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

From this point you can compile as if you have downloaded from source.
As a developer you may want to run the tests and create the website.
To do this type;

.. code-block:: bash

    pytest tests
    make doc

There are shortcuts for running the quick or slow tests, e.g.

.. code-block:: bash

   make test
   make quicktest
