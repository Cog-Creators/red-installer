# red-installer

This is a simple installer for Red-DiscordBot, in use until discord.py is uploaded to
the Python Package Index.

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
Please execute the following command whilst activated in your virtual environment.

### Linux and Mac
In bash/Terminal:
```bash
wget "https://raw.githubusercontent.com/Tobotimus/red-installer/master/red-installer.py" | python3 -
```

### Windows
In PowerShell:
```powershell
(Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/Tobotimus/red-installer/master/red-installer.py").Content | python -
```

Or, if you prefer, you can simply download red-installer.py with your web browser, open
Windows Command Prompt, activate your virtual environment and do `python
red-installer.py` in the directory where you downloaded the file.
