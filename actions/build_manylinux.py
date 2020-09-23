
import sys
import os
import subprocess
import shlex
import glob


def run_command(cmd, dry=False):
    """Run the passed shell command"""
    if dry:
        print(f"[DRY-RUN] {cmd}")
        return

    print(f"[EXECUTE] {cmd}")

    try:
        args = shlex.split(cmd)
        subprocess.run(args).check_returncode()
    except Exception as e:
        print(f"[IGNORE ERROR] {e}")
        sys.exit(0)


def run_docker():
    PLAT = "manylinux1_x86_64"
    DOCKER_IMAGE = "quay.io/pypa/manylinux1_x86_64"
    pwd = os.getcwd()
    pyexe = "/opt/python/cp38-cp38/bin/python3.8"
    cmd = f"docker run --rm -e PLAT={PLAT} -v {pwd}:/io {DOCKER_IMAGE} " \
        f"{pyexe} /io/actions/build_manylinux.py build"

    run_command(cmd)


def build_wheels():
    pybins = ["/opt/python/cp37-cp37m/bin", "/opt/python/cp38-cp38/bin"]
    print(pybins)

    PLAT = os.getenv("PLAT")
    os.environ["CYTHONIZE"] = "1"
    print(PLAT)

    old_path = os.getenv("PATH")
    old_cwd = os.getcwd()

    for pybin in pybins:
        print(f"\nBUILDING WHEEL FOR {pybin}\n")
        print("Installing dependencies...")
        sys.stdout.flush()
        run_command(f"{pybin}/pip install -r /io/requirements.txt")
        run_command(f"{pybin}/pip install pytest")
        print("Building the wheel...")
        os.environ["PATH"] = f"{pybin}:{old_path}"
        sys.stdout.flush()
        os.chdir("/io/")
        run_command("mv build build_tmp")
        run_command("make")
        run_command(
            f"{pybin}/python setup.py bdist_wheel --dist-dir /wheelhouse")
        run_command("rm -rf build")
        run_command("mv build_tmp build")
        os.chdir(old_cwd)
        os.environ["PATH"] = old_path

    wheels = glob.glob("/wheelhouse/pack_and_doc*.whl")
    print(wheels)
    sys.stdout.flush()

    for wheel in wheels:
        print(f"\nREPAIRING WHEEL FOR {wheel}\n")
        sys.stdout.flush()
        run_command(
            f"auditwheel repair \"{wheel}\" --plat {PLAT} -w /io/dist/")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "build":
            build_wheels()
    except Exception:
        run_docker()
