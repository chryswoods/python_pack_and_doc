# Package setup copied from
# https://github.com/FedericoStra/cython-package-example
# Thanks - this was really helpful :-)

import os
import versioneer
from setuptools import setup, Extension
import distutils.sysconfig
import distutils.ccompiler
import multiprocessing
from glob import glob
import platform
import tempfile
import shutil
import sys

try:
    from Cython.Build import cythonize
    have_cython = True
except Exception:
    have_cython = False

_system_input = input

# has the user asked for a build?
is_build = False

for arg in sys.argv[1:]:
    lower = arg.lower()
    if arg in ["build", "bdist_wheel", "build_py"]:
        is_build = True
        break


def setup_package():
    # First, set some flags regarding the distribution
    IS_MAC = False
    IS_LINUX = False
    IS_WINDOWS = False
    MACHINE = platform.machine()

    openmp_flags = ["-fopenmp", "-openmp"]

    if platform.system() == "Darwin":
        IS_MAC = True
        if is_build:
            print(f"\nCompiling on a Mac ({MACHINE})")

    elif platform.system() == "Windows":
        IS_WINDOWS = True
        openmp_flags.insert(0, "/openmp")   # MSVC flag
        if is_build:
            print(f"\nCompiling on Windows ({MACHINE})")

    elif platform.system() == "Linux":
        IS_LINUX = True
        if is_build:
            print(f"\nCompiling on Linux ({MACHINE})")

    else:
        if is_build:
            print(f"Unrecognised platform {platform.system()}. Assuming Linux")
        IS_LINUX = True

    # Get the compiler that (I think) distutils will use
    # - I will need this to add options etc.
    compiler = distutils.ccompiler.new_compiler()
    distutils.sysconfig.customize_compiler(compiler)

    user_openmp_flag = os.getenv("OPENMP_FLAG", None)

    if user_openmp_flag is not None:
        openmp_flags.insert(user_openmp_flag, 0)

    # override 'input' so that defaults can be used when this is run in batch
    # or CI/CD
    def input(prompt: str, default="y"):
        """Wrapper for 'input' that returns 'default' if it detected
        that this is being run from within a batch job or other
        service that doesn't have access to a tty
        """
        import sys

        try:
            if sys.stdin.isatty():
                return _system_input(prompt)
            else:
                print(f"Not connected to a console, so having to use "
                      f"the default ({default})")
                return default
        except Exception as e:
            print(f"Unable to get the input: {e.__class__} {e}")
            print(f"Using the default ({default}) instead")
            return default

    # Check if compiler support openmp (and find the correct openmp flag)
    def get_openmp_flag():
        openmp_test = \
            r"""
            #include <omp.h>
            #include <stdio.h>

            int main(int argc, char **argv)
            {
                int nthreads, thread_id;

                #pragma omp parallel private(nthreads, thread_id)
                {
                    thread_id = omp_get_thread_num();
                    nthreads = omp_get_num_threads();
                    printf("I am thread %d of %d\n", thread_id, nthreads);
                }

                return 0;
            }
            """

        tmpdir = tempfile.mkdtemp()
        curdir = os.getcwd()
        os.chdir(tmpdir)
        filename = r'openmp_test.c'

        with open(filename, 'w') as file:
            file.write(openmp_test)
            file.flush()

        openmp_flag = None

        if user_openmp_flag:
            openmp_flags.insert(0, user_openmp_flag)

        for flag in openmp_flags:
            try:
                # Compiler and then link using each openmp flag...
                compiler.compile(sources=["openmp_test.c"],
                                 extra_preargs=[flag])
                openmp_flag = flag
                break
            except Exception as e:
                print(f"Cannot compile: {e.__class__} {e}")
                pass

        # clean up
        os.chdir(curdir)
        shutil.rmtree(tmpdir)

        return openmp_flag

    if is_build:
        openmp_flag = get_openmp_flag()
    else:
        openmp_flag = None

    include_dirs = []

    if is_build and (openmp_flag is None):
        print(f"\nYour compiler {compiler.compiler_so[0]} does not support "
              f"OpenMP with any of the known OpenMP flags {openmp_flags}. "
              f"If you know which flag to use can you specify it using "
              f"the environent variable OPENMP_FLAG. Otherwise, we will "
              f"have to compile the serial version of the code.")

        if IS_MAC:
            print(f"\nThis is common on Mac, as the default compiler does not "
                  f"support OpenMP. If you want to compile with OpenMP then "
                  f"install llvm via homebrew, e.g. 'brew install llvm', see "
                  f"https://embeddedartistry.com/blog/2017/02/24/installing-llvm-clang-on-osx/")

            print(f"\nRemember then to choose that compiler by setting the "
                  f"CC environment variable, or passing it on the 'make' line, "
                  f"e.g. 'CC=/usr/local/opt/llvm/bin/clang make'")

        result = input("\nDo you want compile without OpenMP? (y/n) ",
                       default="y")

        if result is None or result.strip().lower()[0] != "y":
            sys.exit(-1)

        include_dirs.append("src/pack_and_doc/disable_openmp")

    cflags = "-O3"
    lflags = []

    if openmp_flag:
        cflags = f"{cflags} {openmp_flag}"
        lflags.append(openmp_flag)

    nbuilders = int(os.getenv("CYTHON_NBUILDERS", 2))

    if nbuilders < 1:
        nbuilders = 1

    if is_build:
        print(f"Number of builders equals {nbuilders}\n")

    compiler_directives = {"language_level": 3, "embedsignature": True,
                           "boundscheck": False, "cdivision": True,
                           "initializedcheck": False,
                           "cdivision_warnings": False,
                           "wraparound": False, "binding": False,
                           "nonecheck": False, "overflowcheck": False}

    if os.getenv("CYTHON_LINETRACE", 0):
        if is_build:
            print("Compiling with Cython line-tracing support - will be SLOW")
        define_macros = [("CYTHON_TRACE", "1")]
        compiler_directives["linetrace"] = True
    else:
        define_macros = []

    # Thank you Priyaj for pointing out this little documented feature - finally
    # I can build the C code into a library!
    # https://www.edureka.co/community/21524/setuptools-shared-libary-cython-wrapper-linked-shared-libary
    ext_lib_path = "src/pack_and_doc/example_library"
    sources = ["library.c"]

    ext_libraries = [['example_library', {
        'sources': [os.path.join(ext_lib_path, src)
                    for src in sources],
        'include_dirs': [],
        'macros': [],
    }]]

    def no_cythonize(extensions, **_ignore):
        # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
        for extension in extensions:
            sources = []
            for sfile in extension.sources:
                path, ext = os.path.splitext(sfile)
                if ext in (".pyx", ".py"):
                    if extension.language == "c++":
                        ext = ".cpp"
                    else:
                        ext = ".c"
                    sfile = path + ext
                sources.append(sfile)
            extension.sources[:] = sources
        return extensions

    main_pyx_files = glob("src/pack_and_doc/*.pyx")
    submodule_pyx_files = glob("src/pack_and_doc/submodule/*.pyx")

    libraries = ["example_library"]

    extensions = []

    for pyx in submodule_pyx_files:
        _, name = os.path.split(pyx)
        name = name[0:-4]
        module = f"pack_and_doc.submodule.{name}"

        extensions.append(Extension(module, [pyx], define_macros=define_macros,
                                    libraries=libraries,
                                    extra_compile_args=lflags,
                                    include_dirs=include_dirs))

    for pyx in main_pyx_files:
        _, name = os.path.split(pyx)
        name = name[0:-4]
        module = f"pack_and_doc.{name}"

        extensions.append(Extension(module, [pyx], define_macros=define_macros,
                                    libraries=libraries,
                                    extra_compile_args=lflags,
                                    include_dirs=include_dirs))

    CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0)))

    if not have_cython:
        CYTHONIZE = False

    os.environ['CFLAGS'] = cflags

    if CYTHONIZE:
        extensions = cythonize(extensions,
                               compiler_directives=compiler_directives,
                               nthreads=nbuilders)
    else:
        extensions = no_cythonize(extensions)

    with open("requirements.txt") as fp:
        install_requires = fp.read().strip().split("\n")

    with open("requirements-dev.txt") as fp:
        dev_requires = fp.read().strip().split("\n")

    setup(
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        ext_modules=extensions,
        install_requires=install_requires,
        libraries=ext_libraries,
        extras_require={
            "dev": dev_requires,
            "docs": ["sphinx", "sphinx-rtd-theme"]
        },
        entry_points={
            "console_scripts": [
                "pack_and_doc = pack_and_doc.scripts.main:cli"
            ]
        },
        data_files=[("share/pack_and_doc/requirements",
                     ["requirements.txt"])]
    )


if __name__ == "__main__":
    # Freeze to support parallel compilation when using spawn instead of fork
    # (thanks to pandas for showing how to do this in their setup.py)
    multiprocessing.freeze_support()
    setup_package()
