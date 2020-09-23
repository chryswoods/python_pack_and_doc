import sys
import subprocess
import shlex


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
        print(f"[IGNORE_ERROR] {e}")
        sys.exit(0)


run_command("git fetch --tags")
