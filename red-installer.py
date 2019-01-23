#!/usr/bin/env python3
import logging
import pathlib
import subprocess
import sys
import tarfile
import tempfile
from typing import List

logging.basicConfig(
    style="{",
    level=logging.INFO,
    stream=sys.stdout,
    format="{levelname:^10}: {message}",
)
log = logging.getLogger("red-installer")

IS_VENV: bool = hasattr(sys, "real_prefix") or (
    hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
)
PIP_INSTALL_ARGS: List[str] = [sys.executable, "-m", "pip", "install", "--upgrade"]
if not IS_VENV:
    log.warning("Not in a virtual environment, will install to user site-packages")
    PIP_INSTALL_ARGS.append("--user")


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download Red source distribution to a temporary directory
        args = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--no-deps",
            "--no-cache-dir",
            "--no-binary",
            "Red-DiscordBot",
            "--dest",
            str(tmpdir),
            "Red-DiscordBot",
        ]
        log.info("Downloading Red Archive with command: %s", " ".join(args))
        returncode = subprocess.call(args)
        if returncode:
            return returncode

        # The archive should be the only file in the temporary directory
        try:
            archive_path: pathlib.Path = next(pathlib.Path(tmpdir).iterdir())
        except StopIteration:
            log.fatal("`pip download` did not download a file")
            return 1

        # Rename archive to something universally recognisable
        # Pip doesn't like archive names that don't end with the usual suffixes
        rename_to = archive_path.parent / "Red-DiscordBot.tar.gz"
        archive_path.replace(rename_to)
        archive_path = rename_to

        # Extract dependency_links.txt to install discord.py
        with tarfile.open(archive_path) as archive:
            for member in archive:
                if member.name.endswith("dependency_links.txt"):
                    with archive.extractfile(member) as file:
                        dep_link = file.readline().decode()
                        break
            else:
                log.fatal("No dependency_links.txt found!")
                return 1

        # Remove trailing version number in egg link
        # For some reason it creates a bunch of weird shit in stdout
        end_str_idx = dep_link.rfind("#egg=discord.py") + len("#egg=discord.py")
        dep_link = dep_link[:end_str_idx]

        # Install discord.py
        args = PIP_INSTALL_ARGS + [dep_link]
        log.info("Installing discord.py with command: %s", " ".join(args))
        returncode = subprocess.call(args)
        if returncode:
            return returncode

        # Install Red itself and its PyPI-hosted dependencies
        args = PIP_INSTALL_ARGS + [str(archive_path) + "[voice]"]
        log.info("Installing Red package with command: %s", " ".join(args))
        return subprocess.call(args)


if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        log.fatal("Install failed, exiting...")
        sys.exit(exit_code)
    else:
        sys.exit(0)
