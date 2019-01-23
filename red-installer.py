#!/usr/bin/env python3
import argparse
import logging
import pathlib
import subprocess
import sys
import tarfile
import tempfile

logging.basicConfig(
    style="{",
    level=logging.INFO,
    stream=sys.stdout,
    format="{levelname:^10}: {message}",
)
log = logging.getLogger("red-installer")

argparser = argparse.ArgumentParser(
    prog="red-installer",
    description="Simple installer for Red-DiscordBot",
)
argparser.add_argument(
    "--url",
    "-u",
    metavar="URL",
    help=(
        "Install from a URL instead of from PyPI. Using this option will cause all "
        "other options to be ignored."
    )
)
argparser.add_argument(
    "--install-version",
    "-V",
    metavar="VERSION",
    help=(
        "Install a particular version from PyPI."
    )
)
argparser.add_argument(
    "--extra",
    "-e",
    action="append",
    metavar="EXTRA",
    dest="extras",
    help=(
        "Include an extra to be installed with Red. Extras are the words in square "
        "brackets when installing with pip. The voice extra is included by default. "
        "To include multiple extras, use this option multiple times."
    ),
    default=["voice"],
)
argparser.add_argument(
    "--dev",
    "-d",
    action="store_true",
    help=(
        "Install Red from the V3/develop branch on GitHub."
    )
)
argparser.add_argument(
    "--pre",
    action="store_true",
    help=(
        "Prefer newer pre-releases over stable releases. This option is ignored when "
        "used in conjunction with --install-version, --dev or --url."
    )
)

IS_VENV = hasattr(sys, "real_prefix") or (
    hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
)
PIP_INSTALL_ARGS = [sys.executable, "-m", "pip", "install", "--upgrade"]
if not IS_VENV:
    log.warning("Not in a virtual environment, will install to user site-packages")
    PIP_INSTALL_ARGS.append("--user")


def main(args=None):
    options = argparser.parse_args(args)

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
        ]
        if options.url is not None:
            args.append(options.url)
        else:
            if options.pre:
                args.append("--pre")
            if options.install_version:
                version_str = "==" + options.install_version
            else:
                version_str = ""
            if options.dev:
                package_str = (
                    "https://github.com/Cog-Creators/Red-DiscordBot/tarball/V3/develop"
                    "#egg=Red-DiscordBot"
                )
            else:
                package_str = "Red-DiscordBot"
            args.append(package_str + version_str)

        log.info("Downloading Red Archive with command: %s", " ".join(args))
        returncode = subprocess.call(args)
        if returncode:
            return returncode

        # The archive should be the only file in the temporary directory
        try:
            archive_path = next(pathlib.Path(tmpdir).iterdir())
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

        if options.extras:
            extras_str = "[" + ",".join(options.extras) + "]"
        else:
            extras_str = ""

        # Install Red itself and its PyPI-hosted dependencies
        args = PIP_INSTALL_ARGS + [str(archive_path) + extras_str]
        log.info("Installing Red package with command: %s", " ".join(args))
        return subprocess.call(args)


if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        log.fatal("Install failed, exiting...")
        sys.exit(exit_code)
    else:
        sys.exit(0)
