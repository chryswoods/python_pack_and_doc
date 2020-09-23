
import pack_and_doc
import sys
import os
import subprocess
import shlex

branch = pack_and_doc.__branch__
release = pack_and_doc.__version__
version = pack_and_doc.__version__.split("+")[0]

print(f"Build docs for branch {branch} version {version}")

# we will only build docs for the main and devel branches
# (as these are moved into special locations)

if branch not in ["main", "devel"]:
    if branch.find(version) != -1:
        print(f"Building the docs for tag {version}")
        is_tagged_release = True
    else:
        print(f"We don't build the docs for branch {branch}")
        sys.exit(0)

os.environ["PACK_AND_DOC_VERSION"] = version
os.environ["PACK_AND_DOC_BRANCH"] = branch
os.environ["PACK_AND_DOC_RELEASE"] = release
os.environ["PACK_AND_DOC_REPOSITORY"] = pack_and_doc.__repository__
os.environ["PACK_AND_DOC_REVISIONID"] = pack_and_doc.__revisionid__


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
        print(f"[ERROR] {e}")
        sys.exit(-1)


# install doc dependencies
run_command("pip install sphinx sphinx_issues sphinx_rtd_theme "
            "sphinxcontrib-programoutput")

# make the documentation
run_command("make doc")
