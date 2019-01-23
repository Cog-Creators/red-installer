# red-installer

This is a simple installer for Red-DiscordBot, in use until the discord.py rewrite is
uploaded to the Python Package Index.

It is roughly equivalent to doing the following command on pip versions prior to 19.0:
```bash
pip install -U --process-dependency-links Red-DiscordBot[voice]
```

As such, installing pre-requirements and creating virtual environments is not handled by
this script.

Unlike the original `pip` command, this script will ensure that the correct version of
discord.py is installed when updating an existing installation, *without* bypassing the
cache and force reinstalling all dependencies.

## Usage
Please execute commands whilst activated in your virtual environment.

#### Linux and Mac
In bash/Terminal:
```bash
wget -O - "https://raw.githubusercontent.com/Cog-Creators/red-installer/master/red-installer.py" | python3 -
```

#### Windows
In PowerShell:
```powershell
(Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/Cog-Creators/red-installer/master/red-installer.py").Content | python -
```

Or, if you prefer, you can simply download red-installer.py with your web browser, open
Windows Command Prompt, activate your virtual environment and do `python
red-installer.py` in the directory where you downloaded the file.

### Options
To use any of these options, simply append them to the end of the commands above.
```
--url URL, -u URL   Install from a URL instead of from PyPI. Using this
                    option will cause all other options to be ignored.
--install-version VERSION, -V VERSION
                    Install a particular version from PyPI.
--extra EXTRA, -e EXTRA
                    Include an extra to be installed with Red. Extras are
                    the words in square brackets when installing with pip.
                    The voice extra is included by default. To include
                    multiple extras, use this option multiple times.
--dev, -d           Install Red from the V3/develop branch on GitHub.
--pre               Prefer newer pre-releases over stable releases. This
                    option is ignored when used in conjunction with
                    --install-version, --dev or --url.
```
